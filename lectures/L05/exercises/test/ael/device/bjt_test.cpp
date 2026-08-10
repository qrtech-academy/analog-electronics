/**
 * @brief Tests for ael::device::bjt, the transport model.
 *
 * Dormant until `ael/device/bjt.hpp` exists.
 *
 * The point of the transport form is that saturation is not a case it handles; it is what the
 * equation does. Several of these tests exist to check that no branching crept in.
 */
#if __has_include("ael/device/bjt.hpp")

#include "ael/device/bjt.hpp"

#include "qacademy/test/test.hpp"

#include <cmath>

namespace
{
using ael::device::bjt::Parameters;
using ael::device::bjt::Region;

constexpr double ThermalVoltage{0.026};

[[nodiscard]] Parameters defaults() { return Parameters{}; }
} // namespace

/**
 * @brief With the collector reverse biased the model collapses to Ic = beta * Ib.
 *
 * Beta is a constant of the device and not a function of the current, so the assertion is that
 * the ratio is the *same* at three currents three decades apart, and separately that it is
 * beta_F. The three points are taken at a **fixed collector-emitter voltage**, because from L07
 * the collector current carries an Early factor and beta rises a few per cent with it. The
 * loose absolute tolerance is that few per cent; the tight one, between the three points, is the
 * statement that actually matters here.
 */
TEST(Bjt, ForwardActiveGivesBeta)
{
    const auto parameters{defaults()};
    const auto ratioAt{
        [&parameters](const double vbe)
        {
            const auto currents{ael::device::bjt::currents(vbe, vbe - 5.0, parameters)};
            return currents.collector / currents.base;
        }};

    const double reference{ratioAt(0.65)};

    EXPECT_TRUE(std::isfinite(reference));
    EXPECT_NEAR(ratioAt(0.55) / reference, 1.0, 1.0e-6);
    EXPECT_NEAR(ratioAt(0.75) / reference, 1.0, 1.0e-6);
    EXPECT_NEAR(reference, parameters.forwardBeta, 0.06 * parameters.forwardBeta);
}

/** @brief The emitter carries the sum of the other two. */
TEST(Bjt, EmitterIsTheSum)
{
    const auto currents{ael::device::bjt::currents(0.65, -5.0, defaults())};

    EXPECT_NEAR(currents.emitter, currents.base + currents.collector, 1.0e-15);
}

/**
 * @brief Sixty millivolts of base-emitter voltage is a decade of collector current.
 *
 * Two things are asserted, and they are asserted to different tolerances on purpose.
 *
 * The tight one is that **equal steps give equal ratios**, which is what "exponential" means and
 * is exactly true whatever the thermal voltage turns out to be. The loose one is that the step is
 * 60 mV, which is only true to about a per cent: 60 mV is a decade at 26.06 mV, and kT/q at the
 * 300.15 K L06 makes the default is 25.87. The round figure is the one to calculate with and the
 * model is not obliged to reproduce it.
 *
 * All three points sit at a **fixed collector-emitter voltage**, so the base-collector voltage
 * moves with the base-emitter one. Holding it still instead would change V_CE by 60 mV between
 * the points, and from L07 the Early effect makes the collector current depend on that.
 */
TEST(Bjt, ADecadePerSixtyMillivolts)
{
    constexpr double decade{ThermalVoltage * 2.302585092994046};

    const auto at{[](const double vbe)
                  { return ael::device::bjt::currents(vbe, vbe - 5.0, defaults()).collector; }};

    const double first{at(0.60 + decade) / at(0.60)};
    const double second{at(0.60 + (2.0 * decade)) / at(0.60 + decade)};

    EXPECT_TRUE(std::isfinite(first));
    EXPECT_NEAR(second / first, 1.0, 1.0e-9);
    EXPECT_NEAR(first, 10.0, 0.2);
}

/**
 * @brief Forward biasing the collector junction stops the collector current rising.
 *
 * This is saturation, and it must fall out of the same expression rather than out of a branch.
 */
TEST(Bjt, SaturationFallsOutOfTheEquation)
{
    const auto active{ael::device::bjt::currents(0.78, -1.0, defaults())};
    const auto saturated{ael::device::bjt::currents(0.78, 0.72, defaults())};

    EXPECT_TRUE(saturated.collector < active.collector);

    // And the ratio of collector to base current is well below beta once saturated.
    EXPECT_TRUE(saturated.collector / saturated.base < defaults().forwardBeta / 2.0);
}

/** @brief The four regions, from the two junction voltages and nothing else. */
TEST(Bjt, RegionClassification)
{
    EXPECT_TRUE(ael::device::bjt::region(0.0, -5.0) == Region::Cutoff);
    EXPECT_TRUE(ael::device::bjt::region(0.7, -2.3) == Region::Active);
    EXPECT_TRUE(ael::device::bjt::region(0.8, 0.7) == Region::Saturation);
    EXPECT_TRUE(ael::device::bjt::region(-1.0, 0.7) == Region::ReverseActive);
}

/**
 * @brief The switch design: forced beta, and no h_FE anywhere in it.
 */
TEST(Bjt, BaseResistorFromForcedBeta)
{
    EXPECT_NEAR(ael::device::bjt::baseResistor(5.0, 0.1, 10.0), 430.0, 1.0e-9);
    EXPECT_NEAR(ael::device::bjt::baseResistor(3.3, 0.15, 10.0), 173.33, 1.0e-2);

    // Twice the load current needs half the resistor.
    EXPECT_NEAR(ael::device::bjt::baseResistor(5.0, 0.2, 10.0),
                ael::device::bjt::baseResistor(5.0, 0.1, 10.0) / 2.0, 1.0e-9);
}

#endif
