/**
 * @brief The numbers L04 quotes, pinned. Needs no toolkit and is never guarded.
 *
 * The two facts this lecture rests on are that the gain error is one part in one plus the loop
 * gain, and that a decade of diode current costs sixty millivolts. Both are cheap to state and
 * both are easy to get subtly wrong in prose.
 */
#include "qacademy/test/test.hpp"

#include <cmath>

namespace
{
constexpr double ThermalVoltage{0.026};
constexpr double Saturation{1.0e-14};

struct Test
{
    static constexpr double Tolerance{1.0e-9};
};

[[nodiscard]] double gainError(const double openLoop, const double feedbackFraction)
{
    return 1.0 / (1.0 + (openLoop * feedbackFraction));
}

[[nodiscard]] double diodeCurrent(const double voltage)
{
    return Saturation * (std::exp(voltage / ThermalVoltage) - 1.0);
}
} // namespace

/**
 * @brief The gain error is one part in one plus the loop gain, and that is the whole of feedback.
 */
TEST(ReferenceFeedback, ErrorIsOnePartInOnePlusLoopGain)
{
    // A gain of 10 from an amplifier with 1e5: loop gain 1e4, error 0.01 per cent.
    EXPECT_NEAR(gainError(1.0e5, 0.1) * 100.0, 0.01, 1.0e-5);

    // The same amplifier at a gain of 1000: loop gain 100, error 1 per cent.
    EXPECT_NEAR(gainError(1.0e5, 1.0e-3) * 100.0, 0.9901, 1.0e-4);
}

/**
 * @brief Each decade of accuracy costs a decade of loop gain, so accuracy is expensive.
 */
TEST(ReferenceFeedback, AccuracyCostsLoopGainDecadeForDecade)
{
    for (const double decades : {1.0, 2.0, 3.0, 4.0})
    {
        const double wanted{std::pow(10.0, -decades)};
        const double needed{(1.0 / wanted) - 1.0};

        EXPECT_NEAR(gainError(needed, 1.0), wanted, wanted * 1.0e-9);
    }
}

/**
 * @brief Gain and bandwidth trade one for one, which is why the product is what is sold.
 */
TEST(ReferenceFeedback, GainBandwidthIsAProduct)
{
    constexpr double product{1.0e6};

    EXPECT_NEAR(product / 10.0, 100.0e3, Test::Tolerance);
    EXPECT_NEAR(product / 100.0, 10.0e3, Test::Tolerance);

    // Two stages of ten have ten times the bandwidth of one stage of a hundred.
    EXPECT_NEAR((product / 10.0) / (product / 100.0), 10.0, Test::Tolerance);
}

/**
 * @brief A decade of diode current costs sixty millivolts.
 */
TEST(ReferenceDiode, ADecadeCostsSixtyMillivolts)
{
    EXPECT_NEAR(ThermalVoltage * std::log(10.0), 0.05987, 1.0e-5);

    const double atOneMilliamp{ThermalVoltage * std::log(1.0e-3 / Saturation)};
    const double atTenMilliamps{ThermalVoltage * std::log(1.0e-2 / Saturation)};

    EXPECT_NEAR(atTenMilliamps - atOneMilliamp, ThermalVoltage * std::log(10.0), 1.0e-9);
}

/**
 * @brief The diode's incremental resistance is the thermal voltage over the current.
 *
 * Twenty-six ohms at one milliamp, and it is the same quantity as the r_e that the whole of
 * Part 2 is built on, because a base-emitter junction is a diode.
 */
TEST(ReferenceDiode, IncrementalResistanceIsThermalVoltageOverCurrent)
{
    const double voltage{ThermalVoltage * std::log(1.0e-3 / Saturation)};
    const double conductance{(diodeCurrent(voltage) + Saturation) / ThermalVoltage};

    EXPECT_NEAR(1.0 / conductance, 26.0, 1.0e-3);
}

/**
 * @brief The constant-drop model is exact at exactly one current, and errs both ways around it.
 *
 * Above it the real drop exceeds 0.65 V so the model overestimates the current; below it the
 * reverse. Pinned because the sign reversal is the Cross-check's result.
 */
TEST(ReferenceDiode, ConstantDropModelErrsBothWays)
{
    const double exact{ThermalVoltage * std::log(1.0e-3 / Saturation)};

    // At ten times that current the real drop is higher than 0.65 V.
    EXPECT_TRUE(exact + (ThermalVoltage * std::log(10.0)) > 0.65);

    // At a hundredth of it, lower.
    EXPECT_TRUE(exact - (2.0 * ThermalVoltage * std::log(10.0)) < 0.65);
}
