/**
 * @brief The Cross-check: common-mode rejection through the solver.
 *
 * Dormant until the solver, the netlist, the BJT model and the pair model all exist.
 *
 * The last four tests are the lecture's point. An ideal current-source tail does **not** give
 * infinite rejection, the finite answer it gives comes from a mechanism the closed form knows
 * nothing about, and past a few megohms of tail resistance the rejection **falls** as the tail
 * rises. The closed form says that cannot happen.
 */
// clang-format off
#if __has_include("ael/nr/solve.hpp") && __has_include("ael/net/netlist.hpp") && \
    __has_include("ael/device/bjt.hpp") && __has_include("ael/diffpair/pair.hpp")
// clang-format on

#include "ael/device/bjt.hpp"
#include "ael/diffpair/pair.hpp"
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

constexpr Node Rail{1U};
constexpr Node Vee{2U};
constexpr Node Out1{3U};
constexpr Node Out2{4U};
constexpr Node TailNode{5U};
constexpr Node Base1{6U};
constexpr Node Base2{7U};

constexpr double Supply{20.0};
constexpr double Load{10.0e3};
constexpr double Tail{2.0e-3};
constexpr double TailResistance{10.0e3};
constexpr double Step{1.0e-4};

/**
 * @brief The pair. A tail resistance of zero means an ideal current source instead.
 *
 * `norton` puts a resistance in parallel with that source, which is what a real mirror is.
 */
struct Bias
{
    double tailResistance{TailResistance};
    double norton{0.0};
    double earlyVoltage{100.0};
    double beta{50.0};
};

[[nodiscard]] Netlist pair(const double first, const double second, const Bias& bias)
{
    ael::device::bjt::Parameters parameters{};
    parameters.earlyVoltage = bias.earlyVoltage;
    parameters.forwardBeta  = bias.beta;

    Netlist netlist{};
    netlist.addVoltageSource(Rail, Ground, Supply);
    netlist.addVoltageSource(Vee, Ground, -Supply);
    netlist.addVoltageSource(Base1, Ground, first);
    netlist.addVoltageSource(Base2, Ground, second);
    netlist.addResistor(Rail, Out1, Load);
    netlist.addResistor(Rail, Out2, Load);

    if (bias.tailResistance > 0.0) { netlist.addResistor(TailNode, Vee, bias.tailResistance); }
    else
    {
        netlist.addCurrentSource(TailNode, Vee, Tail);
        if (bias.norton > 0.0) { netlist.addResistor(TailNode, Vee, bias.norton); }
    }

    netlist.addBjt(Out1, Base1, TailNode, parameters);
    netlist.addBjt(Out2, Base2, TailNode, parameters);
    return netlist;
}

[[nodiscard]] double collector(const double first, const double second, const Bias& bias)
{
    return ael::nr::solve(pair(first, second, bias)).nodeVoltages[Out1];
}

/** @brief Gain from a differential input to one collector, by central difference. */
[[nodiscard]] double differentialGain(const Bias& bias)
{
    return (collector(Step / 2.0, -Step / 2.0, bias) - collector(-Step / 2.0, Step / 2.0, bias)) /
           (2.0 * Step);
}

/** @brief Gain from a common-mode input to the same collector. Sign matters here. */
[[nodiscard]] double commonModeGain(const Bias& bias)
{
    return (collector(Step, Step, bias) - collector(-Step, -Step, bias)) / (2.0 * Step);
}

[[nodiscard]] double rejection(const Bias& bias)
{
    return std::fabs(differentialGain(bias) / commonModeGain(bias));
}

/** @brief The tail current the resistor actually delivers, which is not quite 2 mA. */
[[nodiscard]] double tailCurrent(const Bias& bias)
{
    const auto solution{ael::nr::solve(pair(0.0, 0.0, bias))};
    return ((Supply - solution.nodeVoltages[Out1]) / Load) +
           ((Supply - solution.nodeVoltages[Out2]) / Load);
}
} // namespace

/**
 * @brief The resistor tail delivers 1.90 mA, not 2, and saying why is part of the Cross-check.
 *
 * The tail node sits about 0.65 V below ground, so the resistor has 19.35 V across it rather than
 * 20. Every gain below is smaller than the closed form's for that reason before any other.
 */
TEST(Rejection, TheResistorTailIsNotQuiteTwoMilliamps)
{
    const double current{tailCurrent(Bias{})};

    EXPECT_TRUE(std::isfinite(current));
    EXPECT_NEAR(current * 1.0e3, 1.90, 0.05);
    EXPECT_TRUE(current < Tail);
}

/**
 * @brief Leg 3 against legs 1 and 2: the solver and the closed form agree to about a decibel.
 *
 * Three named causes for the residue and nothing else: the tail current above, the device's
 * kT/q against the closed form's 26 mV, and r_o loading the collector resistor.
 */
TEST(Rejection, TheSolverAgreesWithTheClosedForm)
{
    const double measured{rejection(Bias{})};
    const double predicted{ael::diffpair::commonModeRejection(Load, Tail, TailResistance)};

    EXPECT_TRUE(std::isfinite(measured));
    EXPECT_NEAR(ael::diffpair::decibels(measured), ael::diffpair::decibels(predicted), 1.5);
}

/** @brief And the differential gain, once re-evaluated at the tail current actually delivered. */
TEST(Rejection, TheDifferentialGainIsExplainedByTheTailCurrent)
{
    const double measured{differentialGain(Bias{})};
    const double atTheRealTail{ael::diffpair::differentialGain(Load, tailCurrent(Bias{}))};

    EXPECT_TRUE(measured < 0.0);
    EXPECT_NEAR(measured, -169.0, 6.0);

    // Most of the gap closes on the tail current alone; what is left is r_o across the load.
    EXPECT_TRUE(std::fabs(measured / atTheRealTail) > 0.88);
    EXPECT_TRUE(std::fabs(measured / atTheRealTail) < 1.0);
}

/**
 * @brief An ideal current-source tail does not give infinite rejection.
 *
 * About 101 dB, and the common-mode gain comes out **positive** where the resistor tail's was
 * negative. It is a real number produced by a mechanism the closed form contains nothing about,
 * and a designer reading it would accept it.
 */
TEST(Rejection, AnIdealTailGivesAFiniteAndMisleadingNumber)
{
    Bias ideal{};
    ideal.tailResistance = 0.0;

    const double gain{commonModeGain(ideal)};

    EXPECT_TRUE(std::isfinite(gain));
    EXPECT_TRUE(gain > 0.0);
    EXPECT_TRUE(commonModeGain(Bias{}) < 0.0);

    const double decibels{ael::diffpair::decibels(rejection(ideal))};

    EXPECT_TRUE(decibels > 85.0);
    EXPECT_TRUE(decibels < 115.0);
}

/**
 * @brief And it comes from the Early effect, which is checkable in one line.
 *
 * The collector current carries the Early factor and the base current does not, so h_FE rises with
 * V_CE. An ideal source fixes the *emitter* current, and a common-mode input moves the tail node,
 * which moves V_CE, which moves the split. Remove the Early effect and the whole thing vanishes
 * into the solver's arithmetic floor.
 */
TEST(Rejection, TheIdealTailsResidueIsTheEarlyEffect)
{
    Bias ideal{};
    ideal.tailResistance = 0.0;

    Bias flat{ideal};
    flat.earlyVoltage = 1.0e9;

    const double withEarly{std::fabs(commonModeGain(ideal))};
    const double without{std::fabs(commonModeGain(flat))};

    EXPECT_TRUE(std::isfinite(without));
    EXPECT_TRUE(without < (withEarly / 1000.0));
}

/** @brief And it scales as one over beta, which the same account predicts. */
TEST(Rejection, TheIdealTailsResidueScalesWithBeta)
{
    Bias ideal{};
    ideal.tailResistance = 0.0;

    Bias strong{ideal};
    strong.beta = 5000.0;

    EXPECT_TRUE(std::fabs(commonModeGain(strong)) < (std::fabs(commonModeGain(ideal)) / 20.0));
}

/**
 * @brief The two mechanisms have opposite signs, so the common-mode gain passes through zero.
 *
 * Below a few megohms the resistive mechanism dominates and the gain is negative; above it the
 * beta mechanism dominates and it is positive. The closed form has one of these in it.
 */
TEST(Rejection, TheCommonModeGainChangesSign)
{
    const auto gainWith{[](const double norton)
                        {
                            Bias bias{};
                            bias.tailResistance = 0.0;
                            bias.norton         = norton;
                            return commonModeGain(bias);
                        }};

    EXPECT_TRUE(gainWith(1.0e6) < 0.0);
    EXPECT_TRUE(gainWith(10.0e6) > 0.0);
}

/**
 * @brief So more tail resistance is not always better, which the closed form says is impossible.
 *
 * This is the Cross-check's result. `commonModeRejection` rises monotonically without limit; the
 * circuit has a maximum near 3 megohm and declines above it. Neither is wrong: the closed form
 * describes one mechanism correctly and is silent about the other, and it stops describing the
 * circuit where the other takes over.
 */
TEST(Rejection, MoreTailResistanceIsNotAlwaysBetter)
{
    const auto rejectionWith{[](const double norton)
                             {
                                 Bias bias{};
                                 bias.tailResistance = 0.0;
                                 bias.norton         = norton;
                                 return rejection(bias);
                             }};

    const double peak{rejectionWith(3.0e6)};
    const double beyond{rejectionWith(10.0e6)};

    EXPECT_TRUE(std::isfinite(peak));
    EXPECT_TRUE(peak > rejectionWith(1.0e6));
    EXPECT_TRUE(beyond < peak);

    // The closed form, over the same range, does the opposite.
    EXPECT_TRUE(ael::diffpair::commonModeRejection(Load, Tail, 10.0e6) >
                ael::diffpair::commonModeRejection(Load, Tail, 3.0e6));
}

#endif
