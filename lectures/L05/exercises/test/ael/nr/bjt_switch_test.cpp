/**
 * @brief The Cross-check circuit: a saturated switch, solved.
 *
 * Dormant until the nonlinear solver, the netlist and the BJT model all exist.
 *
 * Two transistor junctions rather than L04's one, so this is the circuit that does not converge
 * at all without the step limiting applied to both of them.
 */
#if __has_include("ael/nr/solve.hpp") && __has_include("ael/net/netlist.hpp") && \
                                                       __has_include("ael/device/bjt.hpp")

#include "ael/device/bjt.hpp"
#include "ael/net/netlist.hpp"
#include "ael/nr/solve.hpp"

#include "qacademy/test/test.hpp"

#include <cmath>

namespace
{
using ael::net::Netlist;
using ael::net::Node;

constexpr Node Rail{1U};
constexpr Node Base{2U};
constexpr Node Collector{3U};

/** The switch of Appendix A.4: 5 V logic through 470 ohm, 50 ohm collector load. */
[[nodiscard]] Netlist switchCircuit(const double forwardBeta)
{
    ael::device::bjt::Parameters parameters{};
    parameters.forwardBeta = forwardBeta;

    Netlist netlist{};
    netlist.addVoltageSource(Rail, ael::net::Ground, 5.0);
    netlist.addResistor(Rail, Base, 470.0);
    netlist.addResistor(Rail, Collector, 50.0);
    netlist.addBjt(Collector, Base, ael::net::Ground, parameters);
    return netlist;
}
} // namespace

/**
 * @brief The switch saturates: 98.9 mA and 57 millivolts across the transistor.
 *
 * Both numbers are the model's, and both are optimistic against a real device, which has bulk
 * resistance the transport model does not. See Appendix C.8.
 */
TEST(BjtSwitch, SaturatesHard)
{
    const auto solution{ael::nr::solve(switchCircuit(50.0))};

    EXPECT_TRUE(solution.converged);
    EXPECT_TRUE(std::isfinite(solution.nodeVoltages[Collector]));
    EXPECT_NEAR(solution.nodeVoltages[Collector], 0.0571, 2.0e-3);

    const double collectorCurrent{(5.0 - solution.nodeVoltages[Collector]) / 50.0};
    EXPECT_NEAR(collectorCurrent, 98.86e-3, 0.5e-3);
}

/**
 * @brief It converges in single figures, which is what the limiting on both junctions buys.
 *
 * Without limiting on both, this circuit does not converge at all: each junction drives the other
 * and the iteration oscillates rather than merely crawling as L04's did.
 */
TEST(BjtSwitch, ConvergesQuickly)
{
    const auto solution{ael::nr::solve(switchCircuit(50.0))};

    EXPECT_TRUE(solution.converged);
    EXPECT_TRUE(solution.iterations < std::size_t{20U});
}

/**
 * @brief The design does not depend on beta, and that is the whole claim of forced-beta sizing.
 *
 * Seven and a half times the parameter, a fifth of a per cent of the answer.
 */
TEST(BjtSwitch, InsensitiveToBeta)
{
    const auto low{ael::nr::solve(switchCircuit(40.0))};
    const auto high{ael::nr::solve(switchCircuit(300.0))};

    EXPECT_TRUE(low.converged);
    EXPECT_TRUE(high.converged);

    const double lowCurrent{(5.0 - low.nodeVoltages[Collector]) / 50.0};
    const double highCurrent{(5.0 - high.nodeVoltages[Collector]) / 50.0};

    EXPECT_TRUE(std::fabs(highCurrent - lowCurrent) / lowCurrent < 0.005);
}

/**
 * @brief Below the forced beta it collapses, which is the cliff the method buys margin against.
 *
 * At a beta of eight the transistor cannot deliver what the base drive assumed, leaves saturation,
 * and sits at over a volt. No silicon transistor is anywhere near this.
 */
TEST(BjtSwitch, CollapsesBelowTheForcedBeta)
{
    const auto solution{ael::nr::solve(switchCircuit(8.0))};

    EXPECT_TRUE(solution.converged);
    EXPECT_TRUE(solution.nodeVoltages[Collector] > 1.0);

    const double collectorCurrent{(5.0 - solution.nodeVoltages[Collector]) / 50.0};
    EXPECT_TRUE(collectorCurrent < 80.0e-3);
}

#endif
