/**
 * @brief Tests for ael::device::diode.
 *
 * Dormant until `ael/device/diode.hpp` exists.
 */
#if __has_include("ael/device/diode.hpp")

#include "ael/device/diode.hpp"

#include "qacademy/test/test.hpp"

#include <cmath>

namespace
{
constexpr double Saturation{1.0e-14};
constexpr double ThermalVoltage{0.026};
} // namespace

/** @brief The equation, and the minus one that only matters in reverse. */
TEST(Diode, TheEquation)
{
    EXPECT_NEAR(ael::device::diode::current(0.0, Saturation), 0.0, 1.0e-18);

    // Reverse biased, it settles at minus the saturation current.
    EXPECT_NEAR(ael::device::diode::current(-1.0, Saturation), -Saturation, 1.0e-18);

    // A decade of current costs sixty millivolts.
    const double low{ael::device::diode::current(0.60, Saturation)};
    const double high{
        ael::device::diode::current(0.60 + (ThermalVoltage * std::log(10.0)), Saturation)};
    EXPECT_NEAR(high / low, 10.0, 1.0e-6);
}

/** @brief The conductance is the current over the thermal voltage: 26 ohm at 1 mA. */
TEST(Diode, ConductanceIsCurrentOverThermalVoltage)
{
    const double voltage{ThermalVoltage * std::log(1.0e-3 / Saturation)};

    EXPECT_NEAR(ael::device::diode::current(voltage, Saturation), 1.0e-3, 1.0e-9);
    EXPECT_NEAR(1.0 / ael::device::diode::conductance(voltage, Saturation), 26.0, 1.0e-3);
}

/**
 * @brief The limiter damps large increasing steps and leaves everything else alone.
 *
 * Damping a decreasing step makes convergence worse rather than better, and a limiter that damps
 * everything looks like it works while taking twice as many iterations as it should.
 */
TEST(Diode, LimitDampsOnlyLargeIncreasingSteps)
{
    // A large increase is damped hard: five volts becomes a fraction of a volt.
    const double damped{ael::device::diode::limit(5.0, 0.0)};
    EXPECT_TRUE(damped > 0.0);
    EXPECT_TRUE(damped < 0.5);

    // A small increase passes through untouched.
    EXPECT_NEAR(ael::device::diode::limit(0.660, 0.650), 0.660, 1.0e-12);

    // A decrease passes through untouched, however large.
    //
    // The finiteness check is not decoration. A limiter that damps decreasing steps as well takes
    // the logarithm of a negative number here and returns NaN, and EXPECT_NEAR does not catch
    // that: it tests `difference > tolerance`, which is false when the difference is NaN, so the
    // assertion passes. Anywhere a defect could plausibly produce NaN, assert finiteness first.
    const double decreasing{ael::device::diode::limit(0.100, 5.000)};
    EXPECT_TRUE(std::isfinite(decreasing));
    EXPECT_NEAR(decreasing, 0.100, 1.0e-12);
}

#endif
