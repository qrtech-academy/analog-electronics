/**
 * @brief The Cross-check: the bias a class-AB stage needs, through the solver.
 *
 * Dormant until the solver, the netlist, the BJT model and the output-stage model all exist.
 *
 * **Only one half of the stage is simulated**, and that is not a shortcut. At idle the two halves
 * are symmetric and no current flows in the load, so the output node sits at zero and each device
 * carries the same current from half the bias voltage. One NPN with its base held at V_bias/2 and
 * its emitter resistor returned to ground is therefore an exact model of the idle condition, and
 * it needs no PNP in the netlist.
 */
// clang-format off
#if __has_include("ael/nr/solve.hpp") && __has_include("ael/net/netlist.hpp") && \
    __has_include("ael/device/bjt.hpp") && __has_include("ael/output/classab.hpp")
// clang-format on

#include "ael/device/bjt.hpp"
#include "ael/net/netlist.hpp"
#include "ael/nr/solve.hpp"
#include "ael/output/classab.hpp"

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
constexpr Node EmitterNode{3U};

constexpr double Supply{15.0};
constexpr double Degeneration{0.22};
constexpr double Idle{0.120};
constexpr double VbeOn{0.65};

/** One half of the stage: the rail source carries the collector current and nothing else. */
[[nodiscard]] Netlist half(const double baseVoltage)
{
    Netlist netlist{};
    netlist.addVoltageSource(Rail, Ground, Supply);
    netlist.addVoltageSource(Base, Ground, baseVoltage);
    netlist.addResistor(EmitterNode, Ground, Degeneration);
    netlist.addBjt(Rail, Base, EmitterNode, ael::device::bjt::Parameters{});
    return netlist;
}

[[nodiscard]] double collectorCurrentAt(const double baseVoltage)
{
    return ael::nr::solve(half(baseVoltage)).sourceCurrents[std::size_t{0U}];
}

/** The bias voltage that produces a stated idle current, by bisection on half of it. */
[[nodiscard]] double biasFor(const double idle)
{
    double low{0.40};
    double high{0.95};

    for (int iteration{0}; iteration < 50; ++iteration)
    {
        const double middle{0.5 * (low + high)};

        if (collectorCurrentAt(middle) < idle) { low = middle; }
        else { high = middle; }
    }

    return low + high;
}
} // namespace

/**
 * @brief The half-stage model is the stage: half the bias gives the idle current.
 */
TEST(IdleCurrent, TheHalfStageCarriesTheIdleCurrent)
{
    const double bias{biasFor(Idle)};
    const double current{collectorCurrentAt(bias / 2.0)};

    EXPECT_TRUE(std::isfinite(current));
    EXPECT_NEAR(current, Idle, 0.002);
}

/**
 * @brief Leg 3 against leg 2: the solver and the exponential agree on the bias.
 *
 * To about half a per cent, and the residue has two named causes rather than being slop. The
 * closed form takes V_T as 26 mV where the device computes kT/q, which is 25.87 at 300 K; and the
 * device has an Early effect that the closed form does not, so it needs slightly less drive at a
 * collector sitting 15 V up.
 */
TEST(IdleCurrent, TheSolverAgreesWithTheExponential)
{
    const double measured{biasFor(Idle)};
    const double predicted{ael::output::biasVoltage(Idle, Degeneration)};

    EXPECT_TRUE(std::isfinite(measured));
    EXPECT_NEAR(measured / predicted, 1.0, 0.02);
    EXPECT_TRUE(std::fabs(measured - predicted) < 0.04);
}

/**
 * @brief Leg 3 against leg 1: the constant-drop model is out by a quarter of a volt.
 *
 * The comparison the lecture is built on. Legs 2 and 3 sit within 40 mV of each other; leg 1 is
 * 250 mV away from both, and in a calculation where 26 mV is a factor of e.
 */
TEST(IdleCurrent, TheConstantDropModelIsOutByAQuarterOfAVolt)
{
    const double measured{biasFor(Idle)};
    const double naive{2.0 * (VbeOn + (Idle * Degeneration))};

    EXPECT_TRUE((measured - naive) > 0.2);
    EXPECT_NEAR(measured - naive, 0.26, 0.04);
}

/**
 * @brief And backwards: the constant-drop bias leaves the stage in class B.
 *
 * A couple of milliamps rather than 120. The solver's answer is somewhat larger than the closed
 * form's 1.96 mA for the same two reasons as above, and this is the lesson in miniature: a half
 * per cent disagreement in a bias voltage is a twenty per cent disagreement in the current it
 * produces, because the exponential is still an exponential down here.
 */
TEST(IdleCurrent, TheConstantDropBiasGivesMilliampsNotAHundredAndTwenty)
{
    const double naive{2.0 * (VbeOn + (Idle * Degeneration))};
    const double resulting{collectorCurrentAt(naive / 2.0)};

    EXPECT_TRUE(std::isfinite(resulting));
    EXPECT_TRUE(resulting > 0.5e-3);
    EXPECT_TRUE(resulting < 6.0e-3);
    EXPECT_TRUE((Idle / resulting) > 20.0);

    // And it is the same shape of answer the closed form gave, within the exponential's leverage.
    const double predicted{ael::output::idleCurrent(naive, Degeneration)};

    EXPECT_NEAR(resulting / predicted, 1.0, 0.5);
}

/**
 * @brief A decade of idle current is 120 mV of junction, plus what the resistors add.
 *
 * Two junctions in series at 60 mV each, and then the emitter resistors contribute 2 x 0.22 x the
 * change in current, which is another 40 mV between 10 and 100 mA. A bias generator set a few tens
 * of millivolts high delivers several times the idle current it was asked for, which is why the
 * multiplier in a real amplifier is adjustable and why it is set with a meter in the supply rail
 * rather than with a calculator.
 */
TEST(IdleCurrent, ADecadeOfIdleCurrentIsAHundredAndTwentyMillivoltsOfJunction)
{
    const double low{biasFor(10.0e-3)};
    const double high{biasFor(100.0e-3)};

    EXPECT_TRUE(std::isfinite(low));

    // The junction part alone, recovered by taking the resistors' contribution back out.
    const double resistive{2.0 * Degeneration * (100.0e-3 - 10.0e-3)};

    EXPECT_NEAR((high - low) - resistive, 0.120, 0.010);
}

#endif
