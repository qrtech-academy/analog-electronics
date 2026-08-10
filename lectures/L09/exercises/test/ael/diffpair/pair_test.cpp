/**
 * @brief Tests for ael::diffpair.
 *
 * Dormant until `ael/diffpair/pair.hpp` exists.
 *
 * `RejectionIsTheRatioOfTheTwoGains` and `LinearRangeTakesNoTailCurrent` are the two structural
 * ones. Together they require the code to demonstrate the lecture's two claims rather than to
 * restate them.
 */
#if __has_include("ael/diffpair/pair.hpp")

#include "ael/diffpair/pair.hpp"

#include "qacademy/test/test.hpp"

#include <cmath>

namespace
{
constexpr double Tail{2.0e-3};
constexpr double Load{10.0e3};
constexpr double TailResistance{10.0e3};
} // namespace

/** @brief Half the tail per side, so 26 ohm and not 13. */
TEST(DiffPair, IntrinsicEmitterResistance)
{
    EXPECT_NEAR(ael::diffpair::intrinsicEmitterResistance(Tail), 26.0, 0.01);
    EXPECT_NEAR(ael::diffpair::intrinsicEmitterResistance(20.0e-3), 2.6, 0.001);

    // Twice what the tail current alone would give. This is the lecture's commonest slip.
    EXPECT_NEAR(ael::diffpair::intrinsicEmitterResistance(Tail) / (0.026 / Tail), 2.0, 1.0e-12);
}

/** @brief The differential gain to one collector, inverting, with the factor of two in it. */
TEST(DiffPair, DifferentialGain)
{
    const double gain{ael::diffpair::differentialGain(Load, Tail)};

    EXPECT_TRUE(std::isfinite(gain));
    EXPECT_TRUE(gain < 0.0);
    EXPECT_NEAR(gain, -192.31, 0.02);

    // Degeneration divides it by the emitter factor, exactly as in L07.
    EXPECT_NEAR(ael::diffpair::differentialGain(Load, Tail) /
                    ael::diffpair::differentialGain(Load, Tail, 234.0),
                (26.0 + 234.0) / 26.0, 0.01);
}

/** @brief The common-mode gain, with the tail appearing doubled. */
TEST(DiffPair, CommonModeGain)
{
    EXPECT_NEAR(ael::diffpair::commonModeGain(Load, Tail, TailResistance), -0.4994, 0.001);

    // Doubling the tail resistance halves it, which is what "2 R_tail" means.
    EXPECT_NEAR(ael::diffpair::commonModeGain(Load, Tail, 1.0e6) /
                    ael::diffpair::commonModeGain(Load, Tail, 2.0e6),
                2.0, 0.01);
}

/**
 * @brief The rejection is the ratio of the two gains, so the collector resistor cancels.
 *
 * Asked for at two loads four decades apart and required to agree to machine precision, which it
 * can only do if `commonModeRejection` divides one of your gain functions by the other. A
 * separately derived formula agrees to three or four digits and fails here, and then the lecture's
 * central claim is an assertion rather than something the code shows.
 */
TEST(DiffPair, RejectionIsTheRatioOfTheTwoGains)
{
    for (const double tailResistance : {1.0e3, 10.0e3, 1.0e6})
    {
        const double reference{ael::diffpair::commonModeRejection(100.0, Tail, tailResistance)};

        EXPECT_TRUE(std::isfinite(reference));

        for (const double load : {10.0e3, 1.0e6})
        {
            EXPECT_NEAR(ael::diffpair::commonModeRejection(load, Tail, tailResistance) / reference,
                        1.0, 1.0e-12);
        }
    }
}

/** @brief And its value: 385, which is 52 decibels. */
TEST(DiffPair, RejectionOfTheWorkedPair)
{
    const double rejection{ael::diffpair::commonModeRejection(Load, Tail, TailResistance)};

    EXPECT_NEAR(rejection, 385.1, 0.5);
    EXPECT_NEAR(ael::diffpair::decibels(rejection), 51.71, 0.05);
}

/** @brief Eighty decibels from a resistor tail needs 260 kilohm, which is 520 V at 2 mA. */
TEST(DiffPair, TheTailIsASupplyVoltageQuestion)
{
    double low{1.0e3};
    double high{1.0e7};

    for (int iteration{0}; iteration < 200; ++iteration)
    {
        const double middle{std::sqrt(low * high)};
        if (ael::diffpair::decibels(ael::diffpair::commonModeRejection(Load, Tail, middle)) < 80.0)
        {
            low = middle;
        }
        else { high = middle; }
    }

    const double required{std::sqrt(low * high)};

    EXPECT_NEAR(required, 260.0e3, 2.0e3);
    EXPECT_NEAR(required * Tail, 520.0, 8.0);
}

/** @brief The differential output is limited by matching instead, and by 46 decibels more. */
TEST(DiffPair, TheDifferentialOutputIsADifferentQuestion)
{
    const double singleEnded{ael::diffpair::commonModeRejection(Load, Tail, TailResistance)};
    const double differential{
        ael::diffpair::commonModeRejectionDifferential(Tail, TailResistance, 0.01)};

    EXPECT_NEAR(ael::diffpair::decibels(differential), 97.7, 0.2);
    EXPECT_NEAR(ael::diffpair::decibels(differential) - ael::diffpair::decibels(singleEnded), 46.0,
                0.3);

    // It improves with matching, which the single-ended figure does not do at all.
    EXPECT_NEAR(ael::diffpair::commonModeRejectionDifferential(Tail, TailResistance, 0.001) /
                    differential,
                10.0, 1.0e-9);
}

/** @brief A mirror load has no factor of two in it, which is half of what it buys. */
TEST(DiffPair, MirrorGainHasNoFactorOfTwo)
{
    EXPECT_NEAR(ael::diffpair::mirrorGain(Tail, 50.0e3), -1923.1, 1.0);

    // At the same load it is exactly twice the resistively loaded single-ended answer.
    EXPECT_NEAR(ael::diffpair::mirrorGain(Tail, Load) / ael::diffpair::differentialGain(Load, Tail),
                2.0, 1.0e-12);
}

/** @brief The large-signal transfer: a tanh, saturating at the tail current. */
TEST(DiffPair, Transfer)
{
    EXPECT_NEAR(ael::diffpair::transfer(0.0, Tail), 0.0, 1.0e-15);
    EXPECT_NEAR(ael::diffpair::transfer(5.0e-3, Tail) * 1.0e3, 0.1918, 0.002);
    EXPECT_NEAR(ael::diffpair::transfer(0.100, Tail) * 1.0e3, 1.9160, 0.002);

    // Odd, and bounded by the tail however hard it is driven.
    EXPECT_NEAR(ael::diffpair::transfer(-0.030, Tail), -ael::diffpair::transfer(0.030, Tail),
                1.0e-15);
    EXPECT_TRUE(std::fabs(ael::diffpair::transfer(10.0, Tail)) <= Tail);

    // The slope at the origin is 1/r_e, not 1/(2 r_e). The two in the *gain* to one collector
    // comes from taking one collector; the difference current has no two in it, because both
    // sides move. Getting this backwards is easy and this assertion is where it shows.
    constexpr double step{1.0e-7};
    EXPECT_NEAR((ael::diffpair::transfer(step, Tail) / step) *
                    ael::diffpair::intrinsicEmitterResistance(Tail),
                1.0, 1.0e-6);
}

/**
 * @brief The linear range takes no tail current, because the tail cancels.
 *
 * A signature with one in it is a derivation that stopped early, and the physical claim it would
 * hide is that biasing the pair harder improves its linearity. It does not.
 */
TEST(DiffPair, LinearRangeTakesNoTailCurrent)
{
    EXPECT_NEAR(ael::diffpair::linearRange(0.01) * 1.0e3, 9.06, 0.05);
    EXPECT_NEAR(ael::diffpair::linearRange(0.05) * 1.0e3, 20.8, 0.2);

    // And it does what it says: at that input the tanh is one per cent below its tangent.
    const double range{ael::diffpair::linearRange(0.01)};
    const double actual{ael::diffpair::transfer(range, Tail)};
    const double tangent{range * Tail / (2.0 * 0.026)};

    EXPECT_NEAR(actual / tangent, 0.99, 0.001);
}

/** @brief Offset: a millivolt of device mismatch costs twice what one per cent of load does. */
TEST(DiffPair, InputOffset)
{
    EXPECT_NEAR(ael::diffpair::inputOffset(0.01, 0.0, Load, Tail) * 1.0e3, 0.52, 0.01);
    EXPECT_NEAR(ael::diffpair::inputOffset(0.0, 1.0e-3, Load, Tail) * 1.0e3, 1.00, 0.001);
    EXPECT_NEAR(ael::diffpair::inputOffset(0.01, 1.0e-3, Load, Tail) * 1.0e3, 1.52, 0.01);

    // The load mismatch is referred through the gain, so it does not depend on the load itself.
    EXPECT_NEAR(ael::diffpair::inputOffset(0.01, 0.0, 100.0e3, Tail) /
                    ael::diffpair::inputOffset(0.01, 0.0, Load, Tail),
                1.0, 1.0e-9);
}

#endif
