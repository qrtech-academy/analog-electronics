/**
 * @brief The numbers L06 quotes, pinned. Needs no toolkit and is never guarded.
 *
 * The most important one is not a value but a contradiction: the tempting argument this lecture
 * corrects cannot be completed, and the test says so in arithmetic.
 */
#include "qacademy/test/test.hpp"

#include <cmath>

namespace
{
constexpr double ThermalVoltage{0.026};

[[nodiscard]] constexpr double parallel(const double a, const double b)
{
    return (a * b) / (a + b);
}
} // namespace

/**
 * @brief The tempting argument contradicts itself, and by a factor of forty-seven.
 *
 * It begins by saying the collector current rose 10 per cent and ends by describing a
 * base-emitter voltage of 0.55 V. Those cannot both be true of one circuit: 100 mV below 0.65 V
 * is a current forty-seven times smaller, not a tenth larger.
 */
TEST(ReferenceDrift, TheTemptingArgumentIsSelfContradictory)
{
    const double ratio{std::exp(-0.100 / ThermalVoltage)};

    EXPECT_NEAR(1.0 / ratio, 46.8, 0.1);
    EXPECT_TRUE(ratio < 0.03);

    // And the premise it started from.
    EXPECT_TRUE(1.10 > ratio * 40.0);
}

/**
 * @brief At a held base, the collector current rises about 8 per cent per degree.
 *
 * From 2 mV of base-emitter drift inside an exponential whose scale is 26 mV. The full physics,
 * whose tempco is nearer -1.77 mV per degree, gives 7; the round figure is the one to calculate
 * with, and Appendix B.1 says so.
 */
TEST(ReferenceDrift, UndegeneratedDriftIsEightPerCentPerDegree)
{
    const double perDegree{std::exp(0.002 / ThermalVoltage) - 1.0};

    EXPECT_TRUE(perDegree > 0.06);
    EXPECT_TRUE(perDegree < 0.09);

    // Ten degrees is more than a doubling.
    EXPECT_TRUE(std::pow(1.0 + perDegree, 10.0) > 2.0);
}

/**
 * @brief The emitter resistor divides the drift by the same factor it divides the gain.
 *
 * That equality is the lecture's whole argument, and it is why the stability is not free.
 */
TEST(ReferenceDrift, SuppressionEqualsTheEmitterFactor)
{
    constexpr double current{1.0e-3};
    constexpr double emitter{1.0e3};

    const double re{ThermalVoltage / current};
    const double emitterFactor{(re + emitter) / re};

    const double without{std::exp(0.002 / ThermalVoltage) - 1.0};
    const double with{(0.002 / emitter) / current};

    EXPECT_NEAR(emitterFactor, 39.5, 0.1);
    EXPECT_NEAR(without / with, emitterFactor, emitterFactor * 0.05);
}

/**
 * @brief The base current droops the divider by its Thevenin resistance: 120 mV, then 105.
 *
 * L01's loading arithmetic, for the fourth time in this course, now costing 12 per cent of a bias
 * current.
 */
TEST(ReferenceBias, BaseCurrentDroopsTheDivider)
{
    constexpr double supply{10.0};
    constexpr double upper{33.0e3};
    constexpr double lower{6.8e3};

    const double thevenin{parallel(upper, lower)};
    const double unloaded{(supply * lower) / (upper + lower)};

    EXPECT_NEAR(thevenin, 5638.2, 0.1);
    EXPECT_NEAR(unloaded, 1.7085, 1.0e-4);

    // The first pass, from the unloaded current: twenty-one microamps of base current through
    // 5.6 kilohm is over a hundred millivolts. Converged it settles at 18.7 microamps and 105 mV.
    EXPECT_NEAR(21.2e-6 * thevenin, 0.1195, 1.0e-3);
    EXPECT_NEAR(18.69e-6 * thevenin, 0.1054, 1.0e-3);
}

/**
 * @brief The 220 mV rule lands on an E12 value and gives an emitter factor near ten.
 */
TEST(ReferenceBias, TheTwoHundredAndTwentyMillivoltRule)
{
    constexpr double current{1.0e-3};
    const double resistor{0.220 / current};
    const double re{ThermalVoltage / current};

    EXPECT_NEAR(resistor, 220.0, 1.0e-9);
    EXPECT_NEAR((re + resistor) / re, 9.46, 0.01);

    // At ten times the current it is ten times smaller, and still E12.
    EXPECT_NEAR(0.220 / 1.0e-2, 22.0, 1.0e-9);
}
