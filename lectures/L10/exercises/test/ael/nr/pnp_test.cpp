/**
 * @brief Tests for the PNP L10 adds to the netlist and the solver.
 *
 * Dormant until the solver, the netlist and the BJT model all exist.
 *
 * A PNP is an NPN with every voltage and every current negated, and these tests assert exactly
 * that: the same circuit built both ways, mirrored about ground, must give mirrored answers to
 * machine precision. A separately written PNP model agrees to a few digits and fails here.
 */
// clang-format off
#if __has_include("ael/nr/solve.hpp") && __has_include("ael/net/netlist.hpp") && \
    __has_include("ael/device/bjt.hpp")
// clang-format on

#include "ael/device/bjt.hpp"
#include "ael/net/netlist.hpp"
#include "ael/nr/solve.hpp"

#include "qacademy/test/test.hpp"

#include <cmath>
#include <cstddef>

namespace
{
using ael::net::Ground;
using ael::net::Netlist;
using ael::net::Node;
using ael::net::Polarity;

constexpr Node Rail{1U};
constexpr Node Collector{2U};
constexpr Node Base{3U};

/** A common-emitter stage, built either way up. */
[[nodiscard]] Netlist stage(const Polarity polarity)
{
    const double sign{polarity == Polarity::Npn ? 1.0 : -1.0};

    Netlist netlist{};
    netlist.addVoltageSource(Rail, Ground, sign * 10.0);
    netlist.addVoltageSource(Base, Ground, sign * 0.65);
    netlist.addResistor(Rail, Collector, 4.7e3);
    netlist.addBjt(Collector, Base, Ground, ael::device::bjt::Parameters{}, polarity);
    return netlist;
}
} // namespace

/**
 * @brief The same stage, both polarities, mirrored about ground.
 *
 * Every node voltage must be the exact negative of its counterpart. This is the whole
 * specification of a PNP and it is checkable in four lines.
 */
TEST(Pnp, IsAnNpnWithEverythingNegated)
{
    const auto npn{ael::nr::solve(stage(Polarity::Npn))};
    const auto pnp{ael::nr::solve(stage(Polarity::Pnp))};

    EXPECT_TRUE(npn.converged);
    EXPECT_TRUE(pnp.converged);

    for (std::size_t node{1U}; node < npn.nodeVoltages.size(); ++node)
    {
        EXPECT_TRUE(std::isfinite(pnp.nodeVoltages[node]));
        EXPECT_NEAR(pnp.nodeVoltages[node], -npn.nodeVoltages[node], 1.0e-9);
    }
}

/** @brief And the currents mirror too, which the node voltages alone would not catch. */
TEST(Pnp, TheSourceCurrentsMirror)
{
    const auto npn{ael::nr::solve(stage(Polarity::Npn))};
    const auto pnp{ael::nr::solve(stage(Polarity::Pnp))};

    for (std::size_t source{0U}; source < npn.sourceCurrents.size(); ++source)
    {
        EXPECT_NEAR(pnp.sourceCurrents[source], -npn.sourceCurrents[source], 1.0e-12);
    }
}

/** @brief A PNP stage is a real amplifier, not a device that sits cut off. */
TEST(Pnp, TheStageActuallyConducts)
{
    const auto pnp{ael::nr::solve(stage(Polarity::Pnp))};
    const double current{(-10.0 - pnp.nodeVoltages[Collector]) / 4.7e3};

    EXPECT_TRUE(std::fabs(current) > 0.1e-3);
    EXPECT_TRUE(std::fabs(current) < 10.0e-3);
}

#endif
