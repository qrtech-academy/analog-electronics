/**
 * @brief The Cross-check: the output resistance of a degenerated stage, through the solver.
 *
 * Dormant until the solver, the netlist, the BJT model and the small-signal model all exist.
 *
 * The measurement is a derivative rather than a value. Force the collector node to two voltages a
 * few millivolts apart with the input held, and divide the change in the forcing source's voltage
 * by the change in its current. That gives the load resistor and the transistor in parallel,
 * which is what a stage's output resistance is, and it does so without assuming any formula.
 *
 * **Every comparison here is made at the same collector current**, found by bisecting on the base
 * voltage before each measurement. That matters more than it looks: r_o is V_A/I_C, so a
 * comparison between two stages at different currents is a comparison of two different
 * transistors and says nothing about degeneration.
 */
// clang-format off
#if __has_include("ael/nr/solve.hpp") && __has_include("ael/net/netlist.hpp") && \
    __has_include("ael/device/bjt.hpp") && __has_include("ael/ssm/model.hpp")
// clang-format on

#include "ael/device/bjt.hpp"
#include "ael/net/netlist.hpp"
#include "ael/nr/solve.hpp"
#include "ael/ssm/model.hpp"

#include "qacademy/test/test.hpp"

#include <cmath>
#include <cstddef>

namespace
{
using ael::net::Ground;
using ael::net::Netlist;
using ael::net::Node;

constexpr Node Rail{1U};
constexpr Node Base{2U};
constexpr Node Collector{3U};
constexpr Node EmitterNode{4U};

constexpr double Supply{10.0};
constexpr double CollectorResistor{10.0e3};
constexpr double EmitterResistor{234.0};
constexpr double MirrorResistance{100.0e3};

constexpr double Operating{5.0};
constexpr double Step{5.0e-3};
constexpr double Target{1.0e-3};

/** The forcing source is the third voltage source added, and `sourceCurrents` is in that order. */
constexpr std::size_t Probe{2U};

/**
 * @brief The stage, with its collector forced to a stated voltage by a source we can measure.
 *
 * The base is held by an ideal source rather than by a divider, because an output resistance is
 * measured with the input held still, and a divider would let the base move as the operating
 * point shifted.
 *
 * A zero emitter resistor is the emitter tied straight to ground rather than a very small
 * resistance, which keeps a conductance of a million siemens out of a matrix whose other entries
 * are ten-thousandths.
 */
[[nodiscard]] Netlist stage(const double baseVoltage, const double load,
                            const double emitterResistor, const double forced)
{
    const Node emitter{emitterResistor > 0.0 ? EmitterNode : Ground};

    Netlist netlist{};
    netlist.addVoltageSource(Rail, Ground, Supply);
    netlist.addVoltageSource(Base, Ground, baseVoltage);
    netlist.addResistor(Rail, Collector, load);
    if (emitterResistor > 0.0) { netlist.addResistor(EmitterNode, Ground, emitterResistor); }
    netlist.addBjt(Collector, Base, emitter, ael::device::bjt::Parameters{});
    netlist.addVoltageSource(Collector, Ground, forced);
    return netlist;
}

/** @brief The collector current: everything the forcing source does not supply comes via the load.
 */
[[nodiscard]] double currentAt(const double baseVoltage, const double load,
                               const double emitterResistor)
{
    const auto solution{ael::nr::solve(stage(baseVoltage, load, emitterResistor, Operating))};

    return solution.sourceCurrents[Probe] + ((Supply - Operating) / load);
}

/**
 * @brief The base voltage that puts the target current through the stage, by bisection.
 *
 * The bracket is the emitter's own drop plus a range around a junction, rather than something
 * generous like nought to two volts. A generous bracket puts the first few trials at a
 * base-emitter voltage of a volt and more, where the exponential asks the solver for hundreds of
 * amps, and a solver that does not converge there returns something this function cannot detect.
 */
[[nodiscard]] double baseVoltageFor(const double load, const double emitterResistor)
{
    double low{0.40 + (Target * emitterResistor)};
    double high{0.75 + (Target * emitterResistor)};

    for (int iteration{0}; iteration < 50; ++iteration)
    {
        const double middle{0.5 * (low + high)};

        if (currentAt(middle, load, emitterResistor) < Target) { low = middle; }
        else { high = middle; }
    }

    return 0.5 * (low + high);
}

/**
 * @brief The output resistance at the collector node, by central difference, at the target
 * current.
 *
 * `sourceCurrents[k]` is the current leaving the positive terminal into the circuit, so raising
 * the forced voltage raises that current by one over the parallel combination of everything
 * attached to the node.
 */
[[nodiscard]] double measuredOutputResistance(const double load, const double emitterResistor)
{
    const double baseVoltage{baseVoltageFor(load, emitterResistor)};

    const auto below{ael::nr::solve(stage(baseVoltage, load, emitterResistor, Operating - Step))};
    const auto above{ael::nr::solve(stage(baseVoltage, load, emitterResistor, Operating + Step))};

    return (2.0 * Step) / (above.sourceCurrents[Probe] - below.sourceCurrents[Probe]);
}
} // namespace

/**
 * @brief The bisection lands on the operating point the lecture quotes.
 *
 * If this fails, nothing below it means anything, because every comparison is made at this
 * current and every closed form is evaluated at it.
 */
TEST(OutputResistance, TheStageIsWhereTheLectureSaysItIs)
{
    const double baseVoltage{baseVoltageFor(CollectorResistor, EmitterResistor)};
    const double current{currentAt(baseVoltage, CollectorResistor, EmitterResistor)};

    EXPECT_TRUE(std::isfinite(current));
    EXPECT_NEAR(current, Target, 0.01e-3);

    // A milliamp through 234 ohm, plus a drop, is where the base has to be.
    EXPECT_NEAR(baseVoltage, 0.89, 0.03);
}

/**
 * @brief Leg 3 against leg 2: the solver and the corrected closed form agree.
 *
 * They should, to a per cent or two, and the residue is worth knowing rather than tuning away.
 * The closed form uses 26 mV where the device uses kT/q, and takes r_o as V_A/I_C where
 * differentiating the model gives (V_A + V_CE)/I_C. Neither difference reaches the stage's output
 * resistance in any size, because the ten kilohm load swamps both.
 */
TEST(OutputResistance, TheSolverAgreesWithTheCorrectedClosedForm)
{
    const double measured{measuredOutputResistance(CollectorResistor, EmitterResistor)};
    const double predicted{
        ael::ssm::outputResistance(CollectorResistor, Target, EmitterResistor, 50.0, 100.0)};

    EXPECT_TRUE(std::isfinite(measured));
    EXPECT_NEAR(measured / predicted, 1.0, 0.03);
}

/**
 * @brief Leg 3 against leg 1: the tempting rule is out by ten, in the impossible direction.
 *
 * This is the assertion the whole lecture is built around. The measurement is about 9.9 kilohm
 * and the tempting rule gives 100. The second check is the one that needs no numbers: whatever
 * the measurement turns out to be, it lies below the load resistor, because everything at that
 * node is in parallel with it.
 */
TEST(OutputResistance, TheTemptingRuleIsOutByTen)
{
    const double measured{measuredOutputResistance(CollectorResistor, EmitterResistor)};
    const double tempting{CollectorResistor * ael::ssm::emitterFactor(Target, EmitterResistor)};

    EXPECT_TRUE(std::isfinite(measured));
    EXPECT_NEAR(measured, 9.9e3, 0.4e3);
    EXPECT_TRUE(measured < CollectorResistor);
    EXPECT_TRUE((tempting / measured) > 9.0);
}

/**
 * @brief Nine per cent, measured. That is what the degeneration bought at this node.
 *
 * A factor of ten in gain was given up for it. The comparison is against the same stage with the
 * emitter grounded and rebiased to the same current, so the only thing that differs between the
 * two solves is the degeneration itself.
 */
TEST(OutputResistance, DegenerationBarelyMovesItWithAResistiveLoad)
{
    const double degenerated{measuredOutputResistance(CollectorResistor, EmitterResistor)};
    const double bare{measuredOutputResistance(CollectorResistor, 0.0)};

    EXPECT_TRUE(std::isfinite(bare));
    EXPECT_TRUE(degenerated > bare);
    EXPECT_TRUE((degenerated / bare) < 1.15);
}

/**
 * @brief Leg 4: with a mirror load the same degeneration nearly doubles it.
 *
 * A current mirror is, at this node and for this measurement, a resistance of r_o with a current
 * through it that does not depend on the node voltage. A current that does not depend on the node
 * voltage contributes nothing to a derivative, so the measurement needs only the resistance, and
 * that is why the load here is a hundred kilohm rather than a second transistor.
 */
TEST(OutputResistance, AMirrorLoadIsWhereTheBoostAppears)
{
    const double degenerated{measuredOutputResistance(MirrorResistance, EmitterResistor)};
    const double bare{measuredOutputResistance(MirrorResistance, 0.0)};

    EXPECT_TRUE(std::isfinite(degenerated));
    EXPECT_TRUE(std::isfinite(bare));

    // Against 1.09 with the resistive load. Same transistor, same emitter resistor, same boost.
    EXPECT_TRUE((degenerated / bare) > 1.5);
    EXPECT_TRUE(degenerated < MirrorResistance);
}

/**
 * @brief And the boost is at the collector node, where it has been all along.
 *
 * With the load effectively removed, the resistance looking into the collector is hundreds of
 * kilohm against a hundred without degeneration. Nothing about the transistor changed between
 * this test and the one above it; only the resistor that was hiding the result.
 */
TEST(OutputResistance, TheBoostIsAtTheCollectorNode)
{
    constexpr double huge{1.0e9};

    const double degenerated{measuredOutputResistance(huge, EmitterResistor)};
    const double bare{measuredOutputResistance(huge, 0.0)};

    EXPECT_TRUE(std::isfinite(degenerated));
    EXPECT_TRUE(degenerated > 300.0e3);
    EXPECT_TRUE((degenerated / bare) > 5.0);

    // And it is short of a clean factor of ten, because the base resistance shunts part of it.
    EXPECT_TRUE((degenerated / bare) < ael::ssm::emitterFactor(Target, EmitterResistor));
}

#endif
