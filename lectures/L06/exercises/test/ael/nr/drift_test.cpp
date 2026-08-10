/**
 * @brief The Cross-check: the drift of the worked stage, through the solver.
 *
 * Dormant until the solver, the netlist and the BJT model all exist.
 *
 * The ratio between the degenerated and undegenerated drift is the assertion that matters. It
 * should be about the emitter factor, and if it is not, the suppression is coming from somewhere
 * other than where the theory says.
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
constexpr Node EmitterNode{4U};

constexpr double Supply{10.0};
constexpr double Upper{33.0e3};
constexpr double Lower{6.8e3};
constexpr double CollectorResistor{4.7e3};

/** The worked stage, with an emitter resistor of the given value. */
[[nodiscard]] Netlist stage(const double emitterResistor, const double temperature)
{
    ael::device::bjt::Parameters parameters{};
    parameters.temperature = temperature;

    Netlist netlist{};
    netlist.addVoltageSource(Rail, ael::net::Ground, Supply);
    netlist.addResistor(Rail, Base, Upper);
    netlist.addResistor(Base, ael::net::Ground, Lower);
    netlist.addResistor(Rail, Collector, CollectorResistor);
    netlist.addResistor(EmitterNode, ael::net::Ground, emitterResistor);
    netlist.addBjt(Collector, Base, EmitterNode, parameters);
    return netlist;
}

[[nodiscard]] double collectorCurrent(const Netlist& netlist)
{
    const auto solution{ael::nr::solve(netlist)};
    return (Supply - solution.nodeVoltages[Collector]) / CollectorResistor;
}

/**
 * @brief The drift of a stage whose base is held by an ideal source and whose emitter is grounded.
 *
 * This is what "no degeneration" actually means: nothing anywhere in the circuit responds to the
 * collector current. It is the effect Appendix B.1 puts at 8 per cent per degree from a round
 * -2 mV per degree; measured here against the full physics, whose tempco is nearer -1.77 mV per
 * degree, it comes out at 7.
 */
[[nodiscard]] double fixedBaseDriftPerDegree()
{
    const auto currentAt{[](const double temperature)
                         {
                             ael::device::bjt::Parameters parameters{};
                             parameters.temperature = temperature;

                             Netlist netlist{};
                             netlist.addVoltageSource(Rail, ael::net::Ground, Supply);
                             netlist.addVoltageSource(Base, ael::net::Ground, 0.6533);
                             netlist.addResistor(Rail, Collector, CollectorResistor);
                             netlist.addBjt(Collector, Base, ael::net::Ground, parameters);

                             const auto solution{ael::nr::solve(netlist)};
                             return (Supply - solution.nodeVoltages[Collector]) / CollectorResistor;
                         }};

    return ((currentAt(310.15) / currentAt(300.15)) - 1.0) / 10.0;
}
} // namespace

/**
 * @brief The quiescent current is 0.93 mA, not the 1.06 the unloaded divider predicts.
 */
TEST(Drift, QuiescentPointIncludesTheDroop)
{
    const double current{collectorCurrent(stage(1.0e3, 300.15))};

    EXPECT_TRUE(std::isfinite(current));
    EXPECT_NEAR(current, 0.93e-3, 0.06e-3);
}

/**
 * @brief With a one kilohm emitter resistor the drift is a fifth of a per cent per degree.
 */
TEST(Drift, DegeneratedStageIsStable)
{
    const double cold{collectorCurrent(stage(1.0e3, 300.15))};
    const double warm{collectorCurrent(stage(1.0e3, 310.15))};

    const double perDegree{((warm / cold) - 1.0) / 10.0};

    EXPECT_TRUE(std::isfinite(perDegree));
    EXPECT_TRUE(perDegree > 0.0);
    EXPECT_TRUE(perDegree < 0.005);
}

/**
 * @brief Without it the drift is percent-per-degree, which is what the lecture exists to prevent.
 *
 * The comparison has to be a stage driven from a *fixed base voltage*, not the same stage with a
 * tiny emitter resistor. Shrinking the emitter resistor does not remove the degeneration: the
 * divider's own Thevenin resistance still carries the base current, so the base voltage still
 * falls as the current rises, and that is a feedback path of its own. It also drives the
 * transistor into saturation, where drift means nothing.
 */
TEST(Drift, UndegeneratedStageIsNot)
{
    const double perDegree{fixedBaseDriftPerDegree()};

    EXPECT_TRUE(std::isfinite(perDegree));
    EXPECT_TRUE(perDegree > 0.04);
    EXPECT_TRUE(perDegree < 0.12);
}

/**
 * @brief And the ratio between the two is about the emitter factor.
 *
 * This is the Cross-check's real assertion: not that degeneration helps, but that it helps by the
 * factor the theory names, which is the same factor it costs in gain.
 */
TEST(Drift, SuppressionRatioIsAboutTheEmitterFactor)
{
    const auto driftOf{[](const double emitterResistor)
                       {
                           const double cold{collectorCurrent(stage(emitterResistor, 300.15))};
                           const double warm{collectorCurrent(stage(emitterResistor, 310.15))};
                           return ((warm / cold) - 1.0) / 10.0;
                       }};

    const double degenerated{driftOf(1.0e3)};
    const double undegenerated{fixedBaseDriftPerDegree()};
    const double ratio{undegenerated / degenerated};

    // The emitter factor at about 0.93 mA with a kilohm is roughly 37.
    EXPECT_TRUE(std::isfinite(ratio));
    EXPECT_TRUE(ratio > 15.0);
    EXPECT_TRUE(ratio < 90.0);
}

#endif
