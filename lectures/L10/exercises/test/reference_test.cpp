/**
 * @brief The numbers L10 quotes, pinned. Needs no toolkit and is never guarded.
 *
 * Two of these are the course's conclusions rather than its arithmetic: that a stage loaded by a
 * current source has a gain which does not depend on its current, and that closing a loop makes
 * a forward path that varies by a factor of fourteen into a closed-loop gain that varies by nine
 * parts in a hundred thousand.
 */
#include "qacademy/test/test.hpp"

#include <cmath>

namespace
{
constexpr double ThermalVoltage{0.026};
constexpr double EarlyVoltage{100.0};
constexpr double Beta{50.0};

constexpr double Tail{2.0e-3};
constexpr double BufferCurrent{1.0e-3};
constexpr double StageCurrent{1.0e-3};
constexpr double Idle{0.120};
constexpr double Speaker{8.0};
constexpr double ClosedLoop{20.0};
constexpr double Supply{15.0};

[[nodiscard]] constexpr double parallel(const double a, const double b)
{
    return (a * b) / (a + b);
}

[[nodiscard]] constexpr double intrinsicEmitterResistance(const double current)
{
    return ThermalVoltage / current;
}

[[nodiscard]] constexpr double outputResistance(const double current)
{
    return EarlyVoltage / current;
}

[[nodiscard]] constexpr double darlingtonInput(const double current, const double load)
{
    return Beta * Beta * ((2.0 * intrinsicEmitterResistance(current)) + load);
}

[[nodiscard]] constexpr double darlingtonGain(const double current, const double load)
{
    return load / ((2.0 * intrinsicEmitterResistance(current)) + load);
}

[[nodiscard]] constexpr double loaded(const double gain, const double source, const double load)
{
    return (gain * load) / (source + load);
}

[[nodiscard]] double decibels(const double ratio) { return 20.0 * std::log10(ratio); }

/** The open-loop gain, with the output stage's beta as the parameter the last test varies. */
[[nodiscard]] double openLoop(const double outputBeta)
{
    const double pairLoad{parallel(outputResistance(Tail / 2.0), outputResistance(Tail / 2.0))};
    const double stageLoad{
        parallel(outputResistance(StageCurrent), outputResistance(StageCurrent))};

    const double stage3Input{Beta * intrinsicEmitterResistance(StageCurrent)};
    const double bufferInput{darlingtonInput(BufferCurrent, stage3Input)};
    const double outputInput{outputBeta * outputBeta *
                             ((2.0 * intrinsicEmitterResistance(Idle)) + Speaker)};

    const double stage1{
        loaded(pairLoad / intrinsicEmitterResistance(Tail / 2.0), pairLoad, bufferInput)};
    const double buffer{darlingtonGain(BufferCurrent, stage3Input)};
    const double stage3{
        loaded(stageLoad / intrinsicEmitterResistance(StageCurrent), stageLoad, outputInput)};
    const double output{darlingtonGain(Idle, Speaker)};

    return stage1 * buffer * stage3 * output;
}
} // namespace

/**
 * @brief A stage loaded by a current source has a gain that does not depend on its current.
 *
 * The load is r_o against r_o, which falls as one over the current; the transconductance rises as
 * the current; they cancel exactly and the answer is V_A over twice V_T. Written as a sweep,
 * because a single point would look like a coincidence.
 */
TEST(ReferenceGain, IntrinsicGainDoesNotDependOnCurrent)
{
    const auto gainAt{
        [](const double current)
        {
            const double load{parallel(outputResistance(current), outputResistance(current))};
            return load / intrinsicEmitterResistance(current);
        }};

    for (const double current : {1.0e-6, 1.0e-4, 1.0e-3, 1.0e-2, 1.0})
    {
        EXPECT_NEAR(gainAt(current), EarlyVoltage / (2.0 * ThermalVoltage), 1.0e-9);
    }

    EXPECT_NEAR(gainAt(1.0e-3), 1923.1, 0.1);
    EXPECT_NEAR(decibels(gainAt(1.0e-3)), 65.68, 0.02);
}

/** @brief The only lever is r_o, and the only way to raise that is a cascode. */
TEST(ReferenceGain, ACascodeIsTheOnlyWayToMoreGain)
{
    const double bare{outputResistance(StageCurrent)};
    const double cascoded{Beta * bare};

    const double plain{parallel(bare, bare) / intrinsicEmitterResistance(StageCurrent)};
    const double boosted{parallel(cascoded, cascoded) / intrinsicEmitterResistance(StageCurrent)};

    EXPECT_NEAR(decibels(plain), 65.7, 0.1);
    EXPECT_NEAR(decibels(boosted), 99.7, 0.2);
    EXPECT_NEAR(boosted / plain, Beta, 1.0e-9);
}

/** @brief The budget: 131 dB of stage gain, 120 dB of amplifier. */
TEST(ReferenceBudget, LoadingCostsElevenDecibels)
{
    const double unloaded{1923.0769 * 1923.0769};
    const double actual{openLoop(Beta)};

    EXPECT_NEAR(decibels(unloaded), 131.4, 0.1);
    EXPECT_NEAR(decibels(actual), 119.9, 0.2);
    EXPECT_NEAR(decibels(unloaded) - decibels(actual), 11.5, 0.2);
}

/**
 * @brief The two stages with no voltage gain are worth about 31 decibels each.
 *
 * More than either gain stage could add, from circuits that amplify nothing. This is the course's
 * conclusion and it is asserted rather than left as prose.
 */
TEST(ReferenceBudget, TheStagesWithNoGainAreWorthThirtyOneDecibelsEach)
{
    const double pairLoad{parallel(outputResistance(Tail / 2.0), outputResistance(Tail / 2.0))};
    const double stageLoad{
        parallel(outputResistance(StageCurrent), outputResistance(StageCurrent))};
    const double stage3Input{Beta * intrinsicEmitterResistance(StageCurrent)};

    const double withEverything{openLoop(Beta)};

    // Stage 1 driving stage 3 with no buffer between them.
    const double noBuffer{
        loaded(pairLoad / intrinsicEmitterResistance(Tail / 2.0), pairLoad, stage3Input) *
        loaded(stageLoad / intrinsicEmitterResistance(StageCurrent), stageLoad,
               darlingtonInput(Idle, Speaker)) *
        darlingtonGain(Idle, Speaker)};

    // A single follower on the output instead of a Darlington.
    const double singleInput{Beta * (intrinsicEmitterResistance(Idle) + Speaker)};
    const double noDarlington{
        loaded(pairLoad / intrinsicEmitterResistance(Tail / 2.0), pairLoad,
               darlingtonInput(BufferCurrent, stage3Input)) *
        darlingtonGain(BufferCurrent, stage3Input) *
        loaded(stageLoad / intrinsicEmitterResistance(StageCurrent), stageLoad, singleInput) *
        (Speaker / (intrinsicEmitterResistance(Idle) + Speaker))};

    EXPECT_NEAR(decibels(withEverything / noBuffer), 31.5, 0.5);
    EXPECT_NEAR(decibels(withEverything / noDarlington), 31.0, 0.5);

    // Both cost signal, and by far less than they buy.
    EXPECT_TRUE(darlingtonGain(BufferCurrent, stage3Input) < 1.0);
    EXPECT_TRUE(decibels(1.0 / darlingtonGain(BufferCurrent, stage3Input)) < 1.0);
}

/**
 * @brief The amplifier has no open-loop operating point, and the arithmetic says why.
 *
 * Fifteen volts of rail over a million of gain is fifteen microvolts, and no pair of transistors
 * matches to that. A solver that reports the output at a rail is right.
 */
TEST(ReferenceBudget, FifteenMicrovoltsSaturatesTheOutput)
{
    const double offset{Supply / openLoop(Beta)};

    EXPECT_NEAR(offset * 1.0e6, 15.2, 0.5);

    // An ordinary pair of transistors is two orders of magnitude away from that.
    EXPECT_TRUE((1.0e-3 / offset) > 50.0);
}

/**
 * @brief Closing the loop: a forward path that varies by fourteen times, a gain that does not.
 *
 * The last assertion in the course, and the one everything else was for.
 */
TEST(ReferenceLoop, TheClosedLoopDoesNotCareWhatBetaIs)
{
    const auto closed{[](const double outputBeta)
                      {
                          const double open{openLoop(outputBeta)};
                          return open / (1.0 + (open / ClosedLoop));
                      }};

    const double weak{openLoop(20.0)};
    const double strong{openLoop(200.0)};

    // The forward path moves by more than a factor of ten.
    EXPECT_TRUE((strong / weak) > 10.0);
    EXPECT_NEAR(decibels(weak), 106.4, 0.5);
    EXPECT_NEAR(decibels(strong), 129.2, 0.5);

    // The closed loop moves by under a hundredth of a per cent.
    EXPECT_NEAR(closed(20.0), 20.0, 0.01);
    EXPECT_NEAR(closed(200.0), 20.0, 0.01);
    EXPECT_TRUE(std::fabs(closed(200.0) - closed(20.0)) < 0.01);
    EXPECT_TRUE(std::fabs((closed(200.0) / closed(20.0)) - 1.0) < 1.0e-4);
}

/** @brief And the error at the nominal design, which is what L03 promised in Part I. */
TEST(ReferenceLoop, TheErrorIsTwoThousandthsOfAPerCent)
{
    const double open{openLoop(Beta)};
    const double closed{open / (1.0 + (open / ClosedLoop))};

    EXPECT_NEAR(open / ClosedLoop, 49300.0, 500.0);
    EXPECT_NEAR(100.0 * (ClosedLoop - closed) / ClosedLoop, 0.00203, 0.0002);
}
