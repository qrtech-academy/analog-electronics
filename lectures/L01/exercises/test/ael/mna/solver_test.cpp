/**
 * @brief Tests for ael::mna::solve, the DC nodal solver L01 builds.
 *
 * Dormant until `ael/mna/solver.hpp` exists. See ../../README.md.
 *
 * Every expectation here is a closed form computed in the test, not a number copied from a
 * previous run. That is the whole design: the solver knows nothing about dividers, and the test
 * knows nothing about matrices, so agreement between them is evidence rather than tautology. It
 * is also the shape of every Cross-check in the course.
 */
// Both headers, not just the solver: this file includes the netlist too, and a guard that
// names only one of them leaves the other unguarded here while it is guarded elsewhere.
// Compilation then depends on which half of the toolkit exists, which is not a state
// anybody should have to reason about.
#if __has_include("ael/mna/solver.hpp") && __has_include("ael/net/netlist.hpp")

#include "ael/mna/solver.hpp"
#include "ael/net/netlist.hpp"

#include "qacademy/test/test.hpp"

namespace
{
using ael::net::Netlist;
using ael::net::Node;

constexpr Node Out{1U};

/** Tolerances. A direct solve of a well-conditioned 3x3 has no business being loose. */
struct Test
{
    static constexpr double VoltageTolerance{1.0e-9};
    static constexpr double CurrentTolerance{1.0e-12};
};

/**
 * @brief Two resistances in parallel.
 *
 * @param[in] a First resistance.
 * @param[in] b Second resistance.
 *
 * @return The parallel combination.
 */
[[nodiscard]] constexpr double parallel(const double a, const double b)
{
    return (a * b) / (a + b);
}
} // namespace

/**
 * @brief One resistor and one current source is Ohm's law, and it pins the current convention.
 *
 * A current source added as `addCurrentSource(from, to, current)` drives current through itself
 * from `from` to `to`, so it *injects* at `to`. Injecting 1 mA into a node with 1 kilohm to
 * ground puts that node at +1 V. If your solver gives -1 V, the convention is inverted, and every
 * bias calculation in Part 2 will come out with the wrong sign.
 */
TEST(Mna, CurrentSourceIntoResistor)
{
    Netlist netlist{};
    netlist.addResistor(Out, ael::net::Ground, 1.0e3);
    netlist.addCurrentSource(ael::net::Ground, Out, 1.0e-3);

    const auto solution{ael::mna::solve(netlist)};

    EXPECT_TRUE(solution.solved);
    EXPECT_NEAR(solution.nodeVoltages[ael::net::Ground], 0.0, Test::VoltageTolerance);
    EXPECT_NEAR(solution.nodeVoltages[Out], 1.0, Test::VoltageTolerance);
}

/**
 * @brief A voltage source appears at its own node, and its current leaves the positive terminal.
 *
 * `sourceCurrents[k]` is the current flowing out of source k's positive terminal into the
 * circuit, in the order the sources were added. A 10 V source driving 1 kilohm therefore reports
 * +10 mA, which is the sign a reader expects and the opposite of the one that falls out of the
 * MNA stamp if it is written down without thinking about it.
 */
TEST(Mna, VoltageSourceAndItsCurrent)
{
    Netlist netlist{};
    netlist.addVoltageSource(Out, ael::net::Ground, 10.0);
    netlist.addResistor(Out, ael::net::Ground, 1.0e3);

    const auto solution{ael::mna::solve(netlist)};

    EXPECT_TRUE(solution.solved);
    EXPECT_NEAR(solution.nodeVoltages[Out], 10.0, Test::VoltageTolerance);
    EXPECT_EQ(solution.sourceCurrents.size(), std::size_t{1U});
    EXPECT_NEAR(solution.sourceCurrents[0], 10.0e-3, Test::CurrentTolerance);
}

/**
 * @brief The worked divider, against the closed form.
 *
 * The solver has never heard of a divider. It assembles conductances and solves a matrix. That it
 * lands on supply * lower / (upper + lower) is the first evidence in the course that the two ways
 * of thinking about a circuit are the same thing.
 */
TEST(Mna, VoltageDividerMatchesTheClosedForm)
{
    constexpr double supply{10.0};
    constexpr double upper{33.0e3};
    constexpr double lower{6.8e3};

    Netlist netlist{};
    const Node top{2U};
    netlist.addVoltageSource(top, ael::net::Ground, supply);
    netlist.addResistor(top, Out, upper);
    netlist.addResistor(Out, ael::net::Ground, lower);

    const auto solution{ael::mna::solve(netlist)};

    EXPECT_TRUE(solution.solved);
    EXPECT_NEAR(solution.nodeVoltages[Out], (supply * lower) / (upper + lower),
                Test::VoltageTolerance);
}

/**
 * @brief The same divider with a load, which is what the closed form stops predicting.
 *
 * Hang 10 kilohms across the lower leg and the answer moves by a third. The closed form still
 * works if you remember to substitute the parallel combination; the solver needs no reminding,
 * which is exactly why it is worth having.
 */
TEST(Mna, LoadedDividerMatchesTheClosedForm)
{
    constexpr double supply{10.0};
    constexpr double upper{33.0e3};
    constexpr double lower{6.8e3};
    constexpr double load{10.0e3};

    Netlist netlist{};
    const Node top{2U};
    netlist.addVoltageSource(top, ael::net::Ground, supply);
    netlist.addResistor(top, Out, upper);
    netlist.addResistor(Out, ael::net::Ground, lower);
    netlist.addResistor(Out, ael::net::Ground, load);

    const auto solution{ael::mna::solve(netlist)};

    const double expected{(supply * parallel(lower, load)) / (upper + parallel(lower, load))};

    EXPECT_TRUE(solution.solved);
    EXPECT_NEAR(solution.nodeVoltages[Out], expected, Test::VoltageTolerance);
}

/**
 * @brief Resistors in series add, and the solver should not need to be told so.
 */
TEST(Mna, SeriesResistorsAdd)
{
    Netlist netlist{};
    const Node top{3U};
    const Node middle{2U};
    netlist.addVoltageSource(top, ael::net::Ground, 12.0);
    netlist.addResistor(top, middle, 1.0e3);
    netlist.addResistor(middle, Out, 2.0e3);
    netlist.addResistor(Out, ael::net::Ground, 3.0e3);

    const auto solution{ael::mna::solve(netlist)};

    EXPECT_TRUE(solution.solved);
    EXPECT_NEAR(solution.nodeVoltages[Out], 12.0 * 3.0 / 6.0, Test::VoltageTolerance);
    EXPECT_NEAR(solution.nodeVoltages[middle], 12.0 * 5.0 / 6.0, Test::VoltageTolerance);

    // Twelve volts across six kilohms, and the source reports it.
    EXPECT_NEAR(solution.sourceCurrents[0], 2.0e-3, Test::CurrentTolerance);
}

/**
 * @brief Two resistors between the same pair of nodes are one parallel combination.
 *
 * Worth its own test because it is where a solver that assigns one row per *element* rather than
 * one row per *node* goes wrong, and it goes wrong quietly.
 */
TEST(Mna, ParallelResistorsCombine)
{
    Netlist netlist{};
    netlist.addCurrentSource(ael::net::Ground, Out, 1.0e-3);
    netlist.addResistor(Out, ael::net::Ground, 1.0e3);
    netlist.addResistor(Out, ael::net::Ground, 3.0e3);

    const auto solution{ael::mna::solve(netlist)};

    EXPECT_TRUE(solution.solved);
    EXPECT_NEAR(solution.nodeVoltages[Out], 1.0e-3 * parallel(1.0e3, 3.0e3),
                Test::VoltageTolerance);
}

/**
 * @brief Two sources superpose, because the network is linear and nothing in it knows otherwise.
 *
 * Solve with each source alone, add the answers, and compare against solving with both. This is
 * superposition stated as a test rather than as a theorem, and it fails loudly for any solver
 * that has accidentally introduced a nonlinearity.
 */
TEST(Mna, SourcesSuperpose)
{
    const auto build{[](const double left, const double right)
                     {
                         Netlist netlist{};
                         const Node a{1U};
                         const Node b{2U};
                         netlist.addCurrentSource(ael::net::Ground, a, left);
                         netlist.addCurrentSource(ael::net::Ground, b, right);
                         netlist.addResistor(a, ael::net::Ground, 1.0e3);
                         netlist.addResistor(a, b, 2.2e3);
                         netlist.addResistor(b, ael::net::Ground, 4.7e3);
                         return ael::mna::solve(netlist);
                     }};

    const auto both{build(1.0e-3, 0.5e-3)};
    const auto first{build(1.0e-3, 0.0)};
    const auto second{build(0.0, 0.5e-3)};

    EXPECT_TRUE(both.solved);
    for (std::size_t node{0U}; node < both.nodeVoltages.size(); ++node)
    {
        EXPECT_NEAR(both.nodeVoltages[node], first.nodeVoltages[node] + second.nodeVoltages[node],
                    Test::VoltageTolerance);
    }
}

/**
 * @brief The Thevenin resistance of a divider, measured the way you would measure it.
 *
 * Kill the source, inject a test current, read the voltage. That is the definition rather than
 * the formula, and getting the two to agree is the exercise this test closes.
 */
TEST(Mna, TheveninResistanceByTestCurrent)
{
    constexpr double upper{33.0e3};
    constexpr double lower{6.8e3};
    constexpr double probe{1.0e-3};

    Netlist netlist{};
    // The supply is dead, so its node is a short to ground and the upper leg lands on ground too.
    netlist.addResistor(Out, ael::net::Ground, upper);
    netlist.addResistor(Out, ael::net::Ground, lower);
    netlist.addCurrentSource(ael::net::Ground, Out, probe);

    const auto solution{ael::mna::solve(netlist)};

    EXPECT_TRUE(solution.solved);
    EXPECT_NEAR(solution.nodeVoltages[Out] / probe, parallel(upper, lower), Test::VoltageTolerance);
}

/**
 * @brief A floating node has no path to ground, and the solver must say so rather than guess.
 *
 * The matrix is singular. A solver that returns zeros, or a NaN, or whatever the last iteration
 * happened to hold, will be believed. `solved` is false and the caller finds out.
 */
TEST(Mna, FloatingNodeIsReportedRatherThanGuessed)
{
    Netlist netlist{};
    netlist.addResistor(Out, Node{2U}, 1.0e3);

    const auto solution{ael::mna::solve(netlist)};

    EXPECT_FALSE(solution.solved);
}

#endif
