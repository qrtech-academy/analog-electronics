/**
 * @brief The numbers L07 quotes, pinned. Needs no toolkit and is never guarded.
 *
 * The load-bearing one is not a value. It is that the tempting output-resistance rule can be
 * refuted from the shape of the expression alone, without knowing any of the numbers in it: a
 * parallel combination is smaller than either of its parts, and R_C * EF is ten times larger than
 * R_C. That test is written so that it would still pass if every constant in this course changed.
 */
#include "qacademy/test/test.hpp"

#include <cmath>

namespace
{
constexpr double ThermalVoltage{0.026};
constexpr double EarlyVoltage{100.0};
constexpr double Beta{50.0};

constexpr double Current{1.0e-3};
constexpr double CollectorResistor{10.0e3};
constexpr double EmitterResistor{234.0};

[[nodiscard]] constexpr double parallel(const double a, const double b)
{
    return (a * b) / (a + b);
}

[[nodiscard]] constexpr double intrinsicEmitterResistance(const double current)
{
    return ThermalVoltage / current;
}

[[nodiscard]] constexpr double emitterFactor(const double current, const double emitter)
{
    return (intrinsicEmitterResistance(current) + emitter) / intrinsicEmitterResistance(current);
}

/** The expression of Appendix B.3, which is what the emitter factor actually multiplies. */
[[nodiscard]] constexpr double resistanceIntoCollector(const double current, const double emitter)
{
    const double output{EarlyVoltage / current};
    const double degenerated{parallel(emitter, Beta * intrinsicEmitterResistance(current))};

    return (output * (1.0 + (degenerated / intrinsicEmitterResistance(current)))) + degenerated;
}
} // namespace

/**
 * @brief The tempting rule cannot be right, and the refutation needs no numbers.
 *
 * A stage's output resistance is the collector resistor in parallel with whatever the transistor
 * presents. A parallel combination is smaller than either part. So no arrangement of anything
 * inside the transistor can push the answer above R_C, and R_C * EF is ten times above it.
 *
 * This test asserts that reasoning rather than the arithmetic, which is why it uses a sweep: the
 * conclusion holds for every current, every load and every degeneration resistor, and would still
 * hold if every constant in this course were different.
 */
TEST(ReferenceEmitterFactor, OutputResistanceCanNeverExceedTheCollectorResistor)
{
    for (const double current : {0.1e-3, 1.0e-3, 10.0e-3})
    {
        for (const double load : {1.0e3, 10.0e3, 100.0e3})
        {
            for (const double emitter : {0.0, 26.0, 234.0, 2340.0})
            {
                const double actual{parallel(load, resistanceIntoCollector(current, emitter))};

                EXPECT_TRUE(std::isfinite(actual));
                EXPECT_TRUE(actual < load);

                // And the tempting rule breaks that bound wherever there is any degeneration.
                if (emitter > 0.0) { EXPECT_TRUE((load * emitterFactor(current, emitter)) > load); }
            }
        }
    }
}

/**
 * @brief The size of the disagreement, at the worked operating point: a factor of ten.
 */
TEST(ReferenceEmitterFactor, TheWorkedStageDisagreesByTen)
{
    const double tempting{CollectorResistor * emitterFactor(Current, EmitterResistor)};
    const double corrected{
        parallel(CollectorResistor, resistanceIntoCollector(Current, EmitterResistor))};

    EXPECT_NEAR(tempting, 100.0e3, 1.0);
    EXPECT_NEAR(corrected, 9885.0, 5.0);
    EXPECT_NEAR(tempting / corrected, 10.1, 0.1);
}

/**
 * @brief The factor is real. It belongs to the collector node, not to the stage.
 *
 * 100 kilohm becomes 863, which is the emitter factor of ten arriving very nearly intact at the
 * node it describes. It falls short of a clean 1000 kilohm because the base resistance shunts
 * part of the degeneration, and that shunt is the same ceiling the cascode runs into.
 */
TEST(ReferenceEmitterFactor, TheFactorBelongsToTheCollectorNode)
{
    const double bare{resistanceIntoCollector(Current, 0.0)};
    const double degenerated{resistanceIntoCollector(Current, EmitterResistor)};

    EXPECT_NEAR(bare, 100.0e3, 1.0);
    EXPECT_NEAR(degenerated, 863.0e3, 1.0e3);

    const double achieved{degenerated / bare};
    const double nominal{emitterFactor(Current, EmitterResistor)};

    // Most of the nominal factor arrives, and it arrives short rather than over.
    EXPECT_TRUE(achieved > (0.8 * nominal));
    EXPECT_TRUE(achieved < nominal);
}

/**
 * @brief With a resistive load the boost buys 9 per cent; with a mirror it nearly doubles.
 *
 * This pair is the argument for the current-mirror load, and it is why the correction is worth
 * more than the error costs.
 */
TEST(ReferenceEmitterFactor, TheBoostIsOnlyVisibleWithAMirrorLoad)
{
    const double output{EarlyVoltage / Current};

    const double resistiveBare{parallel(CollectorResistor, resistanceIntoCollector(Current, 0.0))};
    const double resistiveDegenerated{
        parallel(CollectorResistor, resistanceIntoCollector(Current, EmitterResistor))};

    const double mirrorBare{parallel(output, resistanceIntoCollector(Current, 0.0))};
    const double mirrorDegenerated{
        parallel(output, resistanceIntoCollector(Current, EmitterResistor))};

    EXPECT_NEAR(resistiveBare, 9090.9, 1.0);
    EXPECT_NEAR(resistiveDegenerated, 9885.4, 1.0);
    EXPECT_NEAR(mirrorBare, 50.0e3, 1.0);
    EXPECT_NEAR(mirrorDegenerated, 89.6e3, 200.0);

    // Nine per cent against eighty.
    EXPECT_TRUE((resistiveDegenerated / resistiveBare) < 1.15);
    EXPECT_TRUE((mirrorDegenerated / mirrorBare) > 1.5);
}

/**
 * @brief A cascode is the same expression with R_E set to r_o, and it caps at beta.
 *
 * The emitter factor that would apply is 3847. The answer is a factor of fifty, because the base
 * resistance shunts the degeneration. Teaching the cascode therefore needs no new machinery,
 * which is this course's best argument for teaching the emitter factor as an idea at all.
 */
TEST(ReferenceEmitterFactor, TheCascodeIsDegenerationByTheOutputResistance)
{
    const double output{EarlyVoltage / Current};
    const double cascode{resistanceIntoCollector(Current, output)};

    EXPECT_NEAR(emitterFactor(Current, output), 3847.0, 1.0);
    EXPECT_NEAR(cascode, 5.04e6, 0.02e6);

    // The ceiling, which the nominal factor of 3847 says nothing about.
    EXPECT_TRUE(cascode > (Beta * output));
    EXPECT_TRUE(cascode < (1.1 * Beta * output));
}

/**
 * @brief Miller: four picofarads becomes one and a half nanofarads, and the stage rolls off.
 */
TEST(ReferenceMiller, TheCapacitanceIsMultipliedByTheGain)
{
    constexpr double feedback{4.0e-12};

    const double gain{CollectorResistor / intrinsicEmitterResistance(Current)};
    const double input{feedback * (1.0 + gain)};

    EXPECT_NEAR(gain, 384.6, 0.1);
    EXPECT_NEAR(input, 1.542e-9, 0.005e-9);

    const double corner{1.0 / (2.0 * M_PI * 1.0e3 * input)};

    EXPECT_NEAR(corner, 103.0e3, 1.0e3);

    // Without the multiplication the same source would reach tens of megahertz.
    EXPECT_TRUE((1.0 / (2.0 * M_PI * 1.0e3 * feedback)) > 30.0e6);
}

/**
 * @brief Degeneration buys bandwidth at exactly the rate it costs gain.
 *
 * The Miller capacitance is proportional to the gain, so the input corner is inversely
 * proportional to it, and the product is a constant. That is the whole reason the cascode is
 * interesting: it moves the corner without paying.
 */
TEST(ReferenceMiller, GainTimesBandwidthIsConstantWithoutACascode)
{
    const auto cornerAt{
        [](const double emitter)
        {
            const double gain{CollectorResistor / (intrinsicEmitterResistance(Current) + emitter)};
            return std::make_pair(gain, 1.0 / (2.0 * M_PI * 600.0 * 4.0e-12 * (1.0 + gain)));
        }};

    const auto bare{cornerAt(0.0)};
    const auto degenerated{cornerAt(EmitterResistor)};

    EXPECT_TRUE(degenerated.second > (9.0 * bare.second));

    // The exact statement, which is what the Miller expression says: the corner times one plus
    // the gain is the corner the bare capacitance would have given, whatever the gain is.
    const double unmultiplied{1.0 / (2.0 * M_PI * 600.0 * 4.0e-12)};

    EXPECT_NEAR(bare.second * (1.0 + bare.first), unmultiplied, 1.0);
    EXPECT_NEAR(degenerated.second * (1.0 + degenerated.first), unmultiplied, 1.0);

    // And therefore the gain-bandwidth product is constant to within the one in the sum, which is
    // 2.3 per cent between these two gains and vanishes as the gain rises.
    EXPECT_NEAR((bare.first * bare.second) / (degenerated.first * degenerated.second), 1.0, 0.03);
}

/**
 * @brief r_s is 250 ohm where r_e is 26, and that is why SF is 2 where EF is 10.
 *
 * Both from the same 220 mV across the degeneration resistor. This test pins the
 * correspondence and never derives it; this is the derivation, in four lines.
 */
TEST(ReferenceSourceFactor, TheSameDropGivesTwoRatherThanTen)
{
    constexpr double mosfetTransconductance{4.0e-3};

    const double emitter{intrinsicEmitterResistance(Current)};
    const double source{1.0 / mosfetTransconductance};

    EXPECT_NEAR(emitter, 26.0, 0.01);
    EXPECT_NEAR(source, 250.0, 0.01);

    const double drop{0.220};

    EXPECT_NEAR(1.0 + ((drop / Current) / emitter), 9.46, 0.01);
    EXPECT_NEAR(1.0 + ((drop / Current) / source), 1.88, 0.01);

    // The ratio between the two factors is the ratio between the two transconductances.
    EXPECT_NEAR(source / emitter, (1.0 / mosfetTransconductance) / (ThermalVoltage / Current),
                1.0e-9);
}
