/**
 * @brief Tests for ael::nr, the nonlinear DC solve.
 *
 * Dormant until `ael/nr/solve.hpp` and `ael/net/netlist.hpp` both exist.
 *
 * This is the Cross-check circuit and the machinery under it. The expectations are the
 * transcendental solution, computed here by hand iteration, so the solver is checked against
 * arithmetic rather than against a previous run of itself.
 */
#if __has_include("ael/nr/solve.hpp") && __has_include("ael/net/netlist.hpp")

#include "ael/net/netlist.hpp"
#include "ael/nr/solve.hpp"

#include "qacademy/test/test.hpp"

#include <cmath>

namespace
{
using ael::net::Netlist;
using ael::net::Node;

constexpr Node Top{1U};
constexpr Node Out{2U};
constexpr double Saturation{1.0e-14};
constexpr double ThermalVoltage{0.026};

/**
 * @brief The diode voltage of a supply through a resistor, by fixed-point iteration.
 *
 * Independent of the solver under test: it iterates the transcendental equation directly rather
 * than linearising it, so agreement between the two is evidence rather than a tautology.
 */
[[nodiscard]] double byHand(const double supply, const double resistance)
{
    double voltage{0.65};
    for (int i{0}; i < 200; ++i)
    {
        const double current{(supply - voltage) / resistance};
        voltage = ThermalVoltage * std::log((current / Saturation) + 1.0);
    }
    return voltage;
}

[[nodiscard]] Netlist diodeThrough(const double supply, const double resistance)
{
    Netlist netlist{};
    netlist.addVoltageSource(Top, ael::net::Ground, supply);
    netlist.addResistor(Top, Out, resistance);
    netlist.addDiode(Out, ael::net::Ground, Saturation);
    return netlist;
}
} // namespace

/**
 * @brief A netlist with no diodes must give the linear answer, in one iteration.
 *
 * A nonlinear solver that cannot reproduce the linear one on a linear circuit has a defect that
 * is far harder to find once there is a diode in the way.
 */
TEST(Nr, LinearCircuitsAreUnchanged)
{
    Netlist netlist{};
    netlist.addVoltageSource(Top, ael::net::Ground, 10.0);
    netlist.addResistor(Top, Out, 33.0e3);
    netlist.addResistor(Out, ael::net::Ground, 6.8e3);

    const auto solution{ael::nr::solve(netlist)};

    EXPECT_TRUE(solution.converged);
    EXPECT_NEAR(solution.nodeVoltages[Out], (10.0 * 6.8e3) / (33.0e3 + 6.8e3), 1.0e-9);
    EXPECT_TRUE(solution.iterations <= std::size_t{2U});
}

/**
 * @brief Five volts through a kilohm: 0.6965 V and 4.303 mA.
 */
TEST(Nr, DiodeThroughAKilohm)
{
    const auto solution{ael::nr::solve(diodeThrough(5.0, 1.0e3))};

    EXPECT_TRUE(solution.converged);
    EXPECT_NEAR(solution.nodeVoltages[Out], byHand(5.0, 1.0e3), 1.0e-9);
    EXPECT_NEAR(solution.nodeVoltages[Out], 0.6964846, 1.0e-6);
    EXPECT_NEAR((5.0 - solution.nodeVoltages[Out]) / 1.0e3, 4.303515e-3, 1.0e-9);
}

/**
 * @brief And through ten megohms: 0.458 V, where the constant-drop model errs the other way.
 */
TEST(Nr, DiodeThroughTenMegohms)
{
    const auto solution{ael::nr::solve(diodeThrough(5.0, 10.0e6))};

    EXPECT_TRUE(solution.converged);
    EXPECT_NEAR(solution.nodeVoltages[Out], byHand(5.0, 10.0e6), 1.0e-9);
    EXPECT_NEAR(solution.nodeVoltages[Out], 0.4584157, 1.0e-6);

    // The real drop is now well below 0.65 V, so the constant-drop model underestimates.
    EXPECT_TRUE(solution.nodeVoltages[Out] < 0.65);
}

/**
 * @brief The limiting is what makes it converge in single figures rather than in hundreds.
 *
 * Seven iterations against a hundred and sixty-eight. A solver reporting anything near a hundred
 * here is not limiting, and it will fail outright on the first transistor circuit in L06.
 */
TEST(Nr, ConvergesInSingleFigures)
{
    const auto solution{ael::nr::solve(diodeThrough(5.0, 1.0e3))};

    EXPECT_TRUE(solution.converged);
    EXPECT_TRUE(solution.iterations < std::size_t{15U});
}

/**
 * @brief Failure to converge is reported rather than returned as an answer.
 *
 * L01's `solved` flag again, and for the same reason: a number that is not a solution must not be
 * indistinguishable from one that is.
 */
TEST(Nr, RunningOutOfIterationsIsReported)
{
    const auto solution{ael::nr::solve(diodeThrough(5.0, 1.0e3), 1.0e-15, std::size_t{2U})};

    EXPECT_FALSE(solution.converged);
}

/**
 * @brief Where the constant-drop model should not be used at all.
 *
 * A one volt supply through a hundred ohms: the drop is most of the supply, so the subtraction no
 * longer buries the model's error and it comes out 12 per cent high.
 */
TEST(Nr, TheModelFailsWhenTheDropIsMostOfTheSupply)
{
    const auto solution{ael::nr::solve(diodeThrough(1.0, 100.0))};

    EXPECT_TRUE(solution.converged);

    const double real{(1.0 - solution.nodeVoltages[Out]) / 100.0};
    const double model{(1.0 - 0.65) / 100.0};

    EXPECT_NEAR(real, 3.118865e-3, 1.0e-8);
    EXPECT_TRUE((model - real) / real > 0.10);
}

#endif
