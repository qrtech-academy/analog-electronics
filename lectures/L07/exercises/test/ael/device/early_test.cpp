/**
 * @brief Tests for the Early effect L07 adds to ael::device::bjt.
 *
 * Dormant until `ael/device/bjt.hpp` exists.
 *
 * `earlyVoltage` has been in `Parameters` since L05 and did nothing. These tests exist to check
 * that it now does, because a model in which it is still ignored gives an infinite r_o, and then
 * the Cross-check returns exactly R_C and proves nothing at all.
 */
#if __has_include("ael/device/bjt.hpp")

#include "ael/device/bjt.hpp"

#include "qacademy/test/test.hpp"

#include <cmath>

namespace
{
using ael::device::bjt::Parameters;

/** @brief Collector current at a stated base-emitter and collector-emitter voltage. */
[[nodiscard]] double collectorCurrent(const double vbe, const double vce, const Parameters& p)
{
    return ael::device::bjt::currents(vbe, vbe - vce, p).collector;
}
} // namespace

/**
 * @brief The collector current is no longer independent of the collector voltage.
 *
 * One part in a hundred per volt, which is 1/V_A. If this test says the current did not move, the
 * Early term is absent and everything downstream of it in this lecture is untestable.
 */
TEST(Early, CollectorCurrentRisesWithCollectorVoltage)
{
    const Parameters parameters{};

    const double low{collectorCurrent(0.65, 5.0, parameters)};
    const double high{collectorCurrent(0.65, 6.0, parameters)};

    EXPECT_TRUE(std::isfinite(low));
    EXPECT_TRUE(high > low);
    EXPECT_NEAR((high / low) - 1.0, 0.0095, 0.002);
}

/**
 * @brief And it rises by exactly the factor the model names, not approximately.
 *
 * The whole term is one multiplication by (1 + V_CE/V_A), so the ratio between two collector
 * voltages is a ratio of two such factors and nothing else. A model that has approximated this,
 * or that applies the factor to only part of the expression, fails here rather than at the third
 * decimal of some downstream result.
 */
TEST(Early, TheFactorIsExact)
{
    Parameters parameters{};

    for (const double first : {1.0, 5.0, 20.0})
    {
        for (const double second : {2.0, 8.0, 30.0})
        {
            const double measured{collectorCurrent(0.65, second, parameters) /
                                  collectorCurrent(0.65, first, parameters)};
            const double predicted{(1.0 + (second / parameters.earlyVoltage)) /
                                   (1.0 + (first / parameters.earlyVoltage))};

            EXPECT_TRUE(std::isfinite(measured));
            EXPECT_NEAR(measured, predicted, 1.0e-9);
        }
    }
}

/**
 * @brief The parameter is read rather than hard-coded.
 *
 * A model with 100 written into it passes every test above and fails this one.
 */
TEST(Early, TheParameterIsUsed)
{
    Parameters standard{};
    Parameters flat{};
    flat.earlyVoltage = 1000.0;

    const double standardSlope{
        (collectorCurrent(0.65, 6.0, standard) / collectorCurrent(0.65, 5.0, standard)) - 1.0};
    const double flatSlope{(collectorCurrent(0.65, 6.0, flat) / collectorCurrent(0.65, 5.0, flat)) -
                           1.0};

    EXPECT_TRUE(std::isfinite(flatSlope));

    // Ten times the Early voltage is 9.57 times the slope, not ten: the factor is
    // (1 + V/V_A), so the one in the denominator moves too.
    EXPECT_NEAR(standardSlope / flatSlope, 9.571, 0.02);
}

/**
 * @brief r_o comes out of the model at about V_A over I_C, which is where the number in the
 * lecture comes from.
 *
 * It is not exactly V_A/I_C. Differentiating the factor gives (V_A + V_CE)/I_C, so at 5 V it is
 * 105 kilohm rather than 100. The lecture quotes the round figure and this is the difference.
 */
TEST(Early, OutputResistanceIsAboutTheEarlyVoltageOverTheCurrent)
{
    const Parameters parameters{};

    // A base-emitter voltage near 1 mA, found from the exponential rather than assumed.
    const double vbe{0.026 * std::log(1.0e-3 / parameters.saturationCurrent)};

    const double low{collectorCurrent(vbe, 4.9, parameters)};
    const double middle{collectorCurrent(vbe, 5.0, parameters)};
    const double high{collectorCurrent(vbe, 5.1, parameters)};
    const double resistance{0.2 / (high - low)};

    EXPECT_TRUE(std::isfinite(resistance));

    // Exactly (V_A + V_CE)/I_C, which is what differentiating the factor gives. The difference
    // between this and the lecture's V_A/I_C is the five volts the collector is sitting at.
    EXPECT_NEAR(resistance, (parameters.earlyVoltage + 5.0) / middle, 1.0e-3 * resistance);

    // And the round figure the lecture quotes is within a twentieth of it.
    EXPECT_NEAR(resistance / (parameters.earlyVoltage / middle), 1.05, 0.01);
}

/**
 * @brief With a very large Early voltage the L05 device comes back exactly.
 *
 * This is the regression guard for the four lectures already written against the old model. If
 * the addition has changed anything other than the collector voltage dependence, the limit does
 * not close and this fails.
 */
TEST(Early, ALargeEarlyVoltageRecoversThePerfectCurrentSource)
{
    Parameters ideal{};
    ideal.earlyVoltage = 1.0e12;

    const double low{collectorCurrent(0.65, 1.0, ideal)};
    const double high{collectorCurrent(0.65, 20.0, ideal)};

    EXPECT_NEAR(high / low, 1.0, 1.0e-9);
}

/**
 * @brief Beta rises with the collector voltage, which is why a datasheet's beta curve slopes.
 *
 * The factor multiplies the collector current and not the base current, so h_FE comes out as
 * beta_F times the same (1 + V_CE/V_A). That is the physical behaviour and it is not an optional
 * detail: putting the factor on the whole transport current instead leaves beta flat and makes
 * the resistance looking into the collector come out **18 per cent high**, above the emitter
 * factor rather than below it, which contradicts the shunting argument the lecture makes. This
 * test is what stops that version being written.
 */
TEST(Early, BetaRisesWithTheCollectorVoltage)
{
    const Parameters parameters{};

    for (const double vce : {1.0, 5.0, 20.0})
    {
        const auto currents{ael::device::bjt::currents(0.65, 0.65 - vce, parameters)};
        const double predicted{parameters.forwardBeta * (1.0 + (vce / parameters.earlyVoltage))};

        EXPECT_TRUE(std::isfinite(currents.base));
        EXPECT_NEAR(currents.collector / currents.base, predicted, 1.0e-4);
    }
}

#endif
