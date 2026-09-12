/**
 * @brief Tests for ael::output, the class-AB stage.
 *
 * Dormant until `ael/output/classab.hpp` exists.
 *
 * `RoundTripsThroughTheBias` and `BiasIsNotTheConstantDropAnswer` are the two that matter.
 * Together they require `idleCurrent` to be a real inverse of `biasVoltage` and require
 * `biasVoltage` to use the exponential, which is the whole subject of Appendix B.5.
 */
#if __has_include("ael/output/classab.hpp")

#include "ael/output/classab.hpp"

#include "qacademy/test/test.hpp"

#include <cmath>

namespace
{
constexpr double Idle{0.120};
constexpr double Degeneration{0.22};
constexpr double VbeOn{0.65};
} // namespace

/** @brief The 26 mV rule, and that it lands on E12 across the useful decade. */
TEST(ClassAb, DegenerationResistor)
{
    EXPECT_NEAR(ael::output::degenerationResistor(Idle), 0.2167, 0.0005);
    EXPECT_NEAR(ael::output::degenerationResistor(0.1), 0.26, 0.0005);

    // One thermal voltage across it at the idle current, at any idle current.
    for (const double idle : {1.0e-3, 0.12, 10.0})
    {
        EXPECT_NEAR(idle * ael::output::degenerationResistor(idle), 0.026, 1.0e-9);
    }
}

/** @brief The bias voltage, from the exponential. */
TEST(ClassAb, BiasVoltage)
{
    const double bias{ael::output::biasVoltage(Idle, Degeneration)};

    EXPECT_TRUE(std::isfinite(bias));
    EXPECT_NEAR(bias, 1.6188, 0.002);
    EXPECT_NEAR(ael::output::biasVoltage(0.1, 0.27), 1.6105, 0.002);
}

/**
 * @brief The bias is not two constant drops, and the gap is the point of the lecture.
 *
 * 1.619 against 1.353. A `biasVoltage` that returns the constant-drop answer passes nothing else
 * in this file and would make the Cross-check compare a model with itself.
 */
TEST(ClassAb, BiasIsNotTheConstantDropAnswer)
{
    const double bias{ael::output::biasVoltage(Idle, Degeneration)};
    const double naive{2.0 * (VbeOn + (Idle * Degeneration))};

    EXPECT_TRUE((bias - naive) > 0.2);
    EXPECT_NEAR(bias - naive, 0.266, 0.005);
}

/**
 * @brief The bias rises by 60 mV per decade of idle current, which is 2 V_T ln 10.
 *
 * Two junctions in series, so twice the decade of a single one. A model with any constant in it
 * fails this, and so does one that has the factor of two wrong.
 */
TEST(ClassAb, TheBiasRisesByADecadeRule)
{
    const double low{ael::output::biasVoltage(1.0e-3, 0.0)};
    const double high{ael::output::biasVoltage(10.0e-3, 0.0)};

    EXPECT_NEAR(high - low, 2.0 * 0.026 * std::log(10.0), 1.0e-6);
}

/**
 * @brief idleCurrent is a real inverse of biasVoltage, not a second approximation.
 *
 * Round-tripping over five decades. This is the load-bearing test of the file: the two functions
 * describe an equation with an exponential and a linear term that do not separate, so the only
 * way to satisfy this is to solve rather than to rearrange.
 */
TEST(ClassAb, RoundTripsThroughTheBias)
{
    for (const double idle : {1.0e-5, 1.0e-3, 0.02, Idle, 1.0})
    {
        const double bias{ael::output::biasVoltage(idle, Degeneration)};
        const double recovered{ael::output::idleCurrent(bias, Degeneration)};

        EXPECT_TRUE(std::isfinite(recovered));
        EXPECT_NEAR(recovered / idle, 1.0, 1.0e-6);
    }
}

/**
 * @brief And the headline: two constant drops of bias give 2 mA where 120 was wanted.
 */
TEST(ClassAb, TheConstantDropBiasGivesTheWrongStageEntirely)
{
    const double naive{2.0 * (VbeOn + (Idle * Degeneration))};
    const double resulting{ael::output::idleCurrent(naive, Degeneration)};

    EXPECT_TRUE(std::isfinite(resulting));
    EXPECT_NEAR(resulting * 1.0e3, 1.955, 0.05);
    EXPECT_NEAR(Idle / resulting, 61.0, 1.5);
}

/** @brief Thermal drift at a fixed bias, and the factor of two the resistors buy. */
TEST(ClassAb, DriftPerDegree)
{
    const double degenerated{ael::output::driftPerDegree(Idle, Degeneration)};
    const double bare{ael::output::driftPerDegree(Idle, 0.0)};

    EXPECT_TRUE(std::isfinite(degenerated));
    EXPECT_NEAR(100.0 * degenerated, 3.82, 0.05);
    EXPECT_NEAR(bare / degenerated, 2.0, 0.05);

    // Still a runaway, which is why the bias generator goes on the heatsink.
    EXPECT_TRUE(std::pow(1.0 + degenerated, 30.0) > 2.5);
}

/** @brief The transfer curve: a dead band without bias, a straight line with it. */
TEST(ClassAb, Transfer)
{
    EXPECT_NEAR(ael::output::transfer(0.5, 0.0, VbeOn, 8.0), 0.0, 1.0e-9);
    EXPECT_NEAR(ael::output::transfer(-0.5, 0.0, VbeOn, 8.0), 0.0, 1.0e-9);
    EXPECT_NEAR(ael::output::transfer(1.0, 0.0, VbeOn, 8.0), 0.35, 1.0e-9);

    for (const double input : {-1.0, -0.2, 0.0, 0.2, 1.0})
    {
        EXPECT_NEAR(ael::output::transfer(input, 2.0 * VbeOn, VbeOn, 8.0), input, 1.0e-9);
    }
}

#endif
