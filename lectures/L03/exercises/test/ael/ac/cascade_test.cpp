/**
 * @brief The Cross-check circuit, through the solver: a cascade, and the buffer that fixes it.
 *
 * Dormant until the AC solver and the netlist both exist.
 *
 * Two identical RC sections connected directly do not give the response of one section squared,
 * because the second loads the first. Putting a follower between them makes the premise true.
 * Both halves are here, because the second is what turns a fault into a design rule.
 */
#if __has_include("ael/ac/sweep.hpp") && __has_include("ael/net/netlist.hpp")

#include "ael/ac/sweep.hpp"
#include "ael/net/netlist.hpp"

#include "qacademy/test/test.hpp"

#include <cmath>

namespace
{
using ael::net::Netlist;
using ael::net::Node;

constexpr double Resistance{1.0e3};
constexpr double Capacitance{159.0e-9};

constexpr Node Source{1U};
constexpr Node Middle{2U};
constexpr Node Output{3U};
constexpr Node Buffered{4U};

[[nodiscard]] double corner() { return 1.0 / (2.0 * M_PI * Resistance * Capacitance); }

/**
 * @brief The frequency at which a swept response falls to 1/sqrt(2) of its low-frequency value.
 *
 * Found by bisection on a logarithmic axis rather than by scanning a sweep, so the test's own
 * resolution never limits what it can assert about the solver.
 */
[[nodiscard]] double halfPower(const Netlist& netlist, const Node output)
{
    const auto magnitude{[&](const double frequency) {
        return std::abs(ael::ac::solveAt(netlist, frequency).nodeVoltages[output]);
    }};

    const double reference{magnitude(corner() / 1.0e4)};
    double low{corner() / 1.0e3};
    double high{corner() * 10.0};

    for (int i{0}; i < 60; ++i)
    {
        const double middle{std::sqrt(low * high)};
        if (magnitude(middle) > reference / std::sqrt(2.0)) { low = middle; }
        else { high = middle; }
    }
    return std::sqrt(low * high);
}
} // namespace

/**
 * @brief Cascaded directly, the pair is 3 dB down at 0.374 of one section's corner.
 *
 * Not 0.644, which is what squaring one section's response predicts. The difference is the
 * loading, and it is a factor of 1.72.
 */
TEST(Cascade, DirectlyCascadedSectionsLoadEachOther)
{
    Netlist netlist{};
    netlist.addVoltageSource(Source, ael::net::Ground, 1.0);
    netlist.addResistor(Source, Middle, Resistance);
    netlist.addCapacitor(Middle, ael::net::Ground, Capacitance);
    netlist.addResistor(Middle, Output, Resistance);
    netlist.addCapacitor(Output, ael::net::Ground, Capacitance);

    EXPECT_NEAR(halfPower(netlist, Output) / corner(), 0.37417, 1.0e-3);
}

/**
 * @brief With a unity-gain buffer between them, the pair is 3 dB down at 0.644 instead.
 *
 * Which is exactly what squaring one section's response predicts. The buffer does not improve the
 * filter; it makes the circuit match the description.
 */
TEST(Cascade, ABufferRestoresIndependence)
{
    Netlist netlist{};
    netlist.addVoltageSource(Source, ael::net::Ground, 1.0);
    netlist.addResistor(Source, Middle, Resistance);
    netlist.addCapacitor(Middle, ael::net::Ground, Capacitance);
    netlist.addVcvs(Buffered, ael::net::Ground, Middle, ael::net::Ground, 1.0);
    netlist.addResistor(Buffered, Output, Resistance);
    netlist.addCapacitor(Output, ael::net::Ground, Capacitance);

    const double expected{std::sqrt(std::sqrt(2.0) - 1.0)};

    EXPECT_NEAR(halfPower(netlist, Output) / corner(), expected, 1.0e-3);
    EXPECT_NEAR(expected, 0.64359, 1.0e-4);
}

/**
 * @brief An inverting amplifier built from a VCVS matches the ideal closed form, nearly.
 *
 * The residual is the finite-gain error, 1/(1 + T), and predicting it rather than noticing it is
 * L04's first result. Here it is only required to be small.
 */
TEST(Cascade, InvertingAmplifierMatchesTheIdealGain)
{
    constexpr double input{10.0e3};
    constexpr double feedback{100.0e3};
    constexpr Node inverting{2U};

    Netlist netlist{};
    netlist.addVoltageSource(Source, ael::net::Ground, 1.0);
    netlist.addResistor(Source, inverting, input);
    netlist.addResistor(inverting, Output, feedback);
    netlist.addVcvs(Output, ael::net::Ground, ael::net::Ground, inverting, 1.0e5);

    const auto point{ael::ac::solveAt(netlist, 1000.0)};

    constexpr double openLoop{1.0e5};
    const double ideal{feedback / input};

    // The exact finite-gain result, rather than a tolerance wide enough to hide it. An inverting
    // amplifier with open-loop gain A delivers -Rf/Rin scaled by A/(A + 1 + Rf/Rin), which here
    // is 9.9989 rather than 10. Asserting the formula turns the shortfall from a nuisance the
    // tolerance has to absorb into the thing being tested, and it is L04's first result.
    const double expected{ideal * openLoop / (openLoop + 1.0 + ideal)};

    EXPECT_TRUE(point.solved);
    EXPECT_NEAR(std::abs(point.nodeVoltages[Output]), expected, 1.0e-9);
    EXPECT_NEAR(expected, 9.99890, 1.0e-5);

    // The shortfall is one part in the loop gain, and the loop gain is A times the feedback
    // fraction. Small, real, and predictable.
    EXPECT_TRUE((ideal - expected) / ideal < 2.0e-4);

    // And the inverting input is a virtual ground: microvolts, not volts.
    EXPECT_TRUE(std::abs(point.nodeVoltages[inverting]) < 1.0e-3);
}

#endif
