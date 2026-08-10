/**
 * @brief Tests for ael::ac, the complex solve and the sweep.
 *
 * Dormant until both `ael/ac/sweep.hpp` and `ael/net/netlist.hpp` exist.
 *
 * The expectations are closed forms computed in the test. The solver does not know what a filter
 * is; it stamps admittances and eliminates. That it lands on 1/(1 + jwRC) is the evidence.
 */
#if __has_include("ael/ac/sweep.hpp") && __has_include("ael/net/netlist.hpp")

#include "ael/ac/sweep.hpp"
#include "ael/net/netlist.hpp"

#include "qacademy/test/test.hpp"

#include <cmath>
#include <complex>

namespace
{
using ael::net::Netlist;
using ael::net::Node;

constexpr Node Out{1U};
constexpr Node Top{2U};

constexpr double Resistance{1.0e3};
constexpr double Capacitance{159.0e-9};

struct Test
{
    static constexpr double MagnitudeTolerance{1.0e-9};
    static constexpr double DegreeTolerance{1.0e-6};
    static constexpr double FrequencyTolerance{1.0e-6};
};

[[nodiscard]] double corner(const double resistance, const double capacitance)
{
    return 1.0 / (2.0 * M_PI * resistance * capacitance);
}

[[nodiscard]] double degrees(const std::complex<double> value)
{
    return std::arg(value) * 180.0 / M_PI;
}

/** A 1 V source, a series resistor, and a shunt capacitor. */
[[nodiscard]] Netlist lowpass()
{
    Netlist netlist{};
    netlist.addVoltageSource(Top, ael::net::Ground, 1.0);
    netlist.addResistor(Top, Out, Resistance);
    netlist.addCapacitor(Out, ael::net::Ground, Capacitance);
    return netlist;
}
} // namespace

/**
 * @brief Well below the corner a capacitor is an open circuit and the filter does nothing.
 */
TEST(Ac, PassesAtLowFrequency)
{
    const auto point{ael::ac::solveAt(lowpass(), corner(Resistance, Capacitance) / 1.0e4)};

    EXPECT_TRUE(point.solved);
    EXPECT_NEAR(std::abs(point.nodeVoltages[Out]), 1.0, 1.0e-7);
}

/**
 * @brief At the corner: three decibels down and forty-five degrees of lag.
 *
 * The sign of the phase is the point. A low-pass lags, so this number is negative. A solver that
 * stamps the capacitor's impedance where its admittance belongs produces the right magnitude and
 * the wrong sign, and a magnitude plot will never show it.
 */
TEST(Ac, CornerMagnitudeAndPhase)
{
    const double cornerHz{corner(Resistance, Capacitance)};
    const auto point{ael::ac::solveAt(lowpass(), cornerHz)};

    EXPECT_TRUE(point.solved);
    EXPECT_NEAR(std::abs(point.nodeVoltages[Out]), 1.0 / std::sqrt(2.0), Test::MagnitudeTolerance);
    EXPECT_NEAR(degrees(point.nodeVoltages[Out]), -45.0, Test::DegreeTolerance);
}

/**
 * @brief The whole response, against the closed form, at four frequencies across three decades.
 */
TEST(Ac, MatchesTheClosedForm)
{
    const double cornerHz{corner(Resistance, Capacitance)};

    for (const double ratio : {0.01, 0.1, 1.0, 10.0})
    {
        const auto point{ael::ac::solveAt(lowpass(), ratio * cornerHz)};
        const std::complex<double> expected{1.0 / std::complex<double>{1.0, ratio}};

        EXPECT_TRUE(point.solved);
        EXPECT_NEAR(std::abs(point.nodeVoltages[Out]), std::abs(expected),
                    Test::MagnitudeTolerance);
        EXPECT_NEAR(degrees(point.nodeVoltages[Out]), degrees(expected), Test::DegreeTolerance);
    }
}

/**
 * @brief A high-pass is the same two components with the output taken across the resistor.
 *
 * At the corner it is also three decibels down, and it leads by forty-five degrees rather than
 * lagging. Included because a solver with an inverted phase passes the low-pass test if its
 * author has also inverted the expectation, and cannot pass both.
 */
TEST(Ac, HighPassLeads)
{
    const double cornerHz{corner(Resistance, Capacitance)};

    Netlist netlist{};
    netlist.addVoltageSource(Top, ael::net::Ground, 1.0);
    netlist.addCapacitor(Top, Out, Capacitance);
    netlist.addResistor(Out, ael::net::Ground, Resistance);

    const auto point{ael::ac::solveAt(netlist, cornerHz)};

    EXPECT_TRUE(point.solved);
    EXPECT_NEAR(std::abs(point.nodeVoltages[Out]), 1.0 / std::sqrt(2.0), Test::MagnitudeTolerance);
    EXPECT_NEAR(degrees(point.nodeVoltages[Out]), 45.0, Test::DegreeTolerance);
}

/**
 * @brief A series LC is a short circuit at resonance, and an inductor's phase is the opposite one.
 */
TEST(Ac, SeriesResonanceIsAShort)
{
    constexpr double inductance{10.0e-3};
    constexpr double capacitance{1.0e-6};
    const double resonance{1.0 / (2.0 * M_PI * std::sqrt(inductance * capacitance))};

    Netlist netlist{};
    netlist.addVoltageSource(Top, ael::net::Ground, 1.0);
    netlist.addResistor(Top, Out, 10.0);
    netlist.addInductor(Out, Node{3U}, inductance);
    netlist.addCapacitor(Node{3U}, ael::net::Ground, capacitance);

    const auto point{ael::ac::solveAt(netlist, resonance)};

    EXPECT_TRUE(point.solved);

    // The LC pair cancels, so the whole source appears across the 10 ohm resistor and the node
    // between resistor and inductor sits at zero.
    EXPECT_NEAR(std::abs(point.nodeVoltages[Out]), 0.0, 1.0e-9);
}

/**
 * @brief The sweep is logarithmic and inclusive at both ends.
 */
TEST(Sweep, LogarithmicAndInclusive)
{
    const auto points{ael::ac::sweep(lowpass(), 10.0, 100000.0, 5U)};

    EXPECT_EQ(points.size(), std::size_t{5U});
    EXPECT_NEAR(points.front().frequency, 10.0, Test::FrequencyTolerance);
    EXPECT_NEAR(points.back().frequency, 100000.0, 1.0e-3);

    // Four decades over five points is one decade per step.
    for (std::size_t i{1U}; i < points.size(); ++i)
    {
        EXPECT_NEAR(points[i].frequency / points[i - 1U].frequency, 10.0, 1.0e-6);
    }
}

/**
 * @brief One point is a legal sweep, and it is the one that divides by zero if unguarded.
 */
TEST(Sweep, SinglePoint)
{
    const auto points{ael::ac::sweep(lowpass(), 1000.0, 100000.0, 1U)};

    EXPECT_EQ(points.size(), std::size_t{1U});
    EXPECT_NEAR(points.front().frequency, 1000.0, Test::FrequencyTolerance);
    EXPECT_TRUE(points.front().solved);
}

/**
 * @brief Zero and negative frequencies are refused rather than stamped.
 *
 * An inductor's admittance at zero frequency is infinite. A sweep that starts at DC produces
 * either a NaN or a silently wrong answer, and neither is acceptable from something whose whole
 * purpose is to be the leg you trust.
 */
TEST(Sweep, RefusesNonPositiveFrequencies)
{
    EXPECT_TRUE(ael::ac::sweep(lowpass(), 0.0, 1000.0, 10U).empty());
}

/**
 * @brief The Cross-check circuit: a divider feeding an RC section.
 *
 * The corner is set by everything the capacitor sees looking back, which is the series resistor
 * plus the divider's Thevenin resistance, so it lands at 151 Hz rather than the 1001 Hz the
 * series resistor alone would suggest. See Appendix C.8.
 */
TEST(Ac, CornerIsSetByEverythingTheCapacitorSees)
{
    constexpr double upper{33.0e3};
    constexpr double lower{6.8e3};

    Netlist netlist{};
    const Node supply{3U};
    netlist.addVoltageSource(supply, ael::net::Ground, 10.0);
    netlist.addResistor(supply, Top, upper);
    netlist.addResistor(Top, ael::net::Ground, lower);
    netlist.addResistor(Top, Out, Resistance);
    netlist.addCapacitor(Out, ael::net::Ground, Capacitance);

    const double thevenin{(upper * lower) / (upper + lower)};
    const double expected{corner(thevenin + Resistance, Capacitance)};

    // At low frequency the output is the unloaded divider: no current flows through the series
    // resistor once the capacitor has charged.
    const auto low{ael::ac::solveAt(netlist, expected / 1.0e4)};
    EXPECT_TRUE(low.solved);
    EXPECT_NEAR(std::abs(low.nodeVoltages[Out]), (10.0 * lower) / (upper + lower), 1.0e-6);

    // And at the true corner it is three decibels below that.
    const auto atCorner{ael::ac::solveAt(netlist, expected)};
    EXPECT_TRUE(atCorner.solved);
    EXPECT_NEAR(std::abs(atCorner.nodeVoltages[Out]),
                std::abs(low.nodeVoltages[Out]) / std::sqrt(2.0), 1.0e-6);
    EXPECT_NEAR(degrees(atCorner.nodeVoltages[Out]), -45.0, 1.0e-4);
}

#endif
