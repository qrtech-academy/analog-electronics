/**
 * @brief The numbers L08 quotes, pinned. Needs no toolkit and is never guarded.
 *
 * Two of these are scale-free and are written as sweeps rather than as points: the 26 mV rule
 * gives an emitter factor of two at *every* current, and a parallel load always costs gain. Both
 * would still hold if every constant in this course changed.
 */
#include "qacademy/test/test.hpp"

#include <cmath>

namespace
{
constexpr double ThermalVoltage{0.026};
constexpr double SaturationCurrent{1.0e-14};
constexpr double VbeOn{0.65};
constexpr double Beta{50.0};

constexpr double Speaker{8.0};
constexpr double Idle{0.120};
constexpr double Degeneration{0.22};

/// The L07 stage this lecture has to get a signal out of.
constexpr double StageGain{38.4615};
constexpr double StageOutputResistance{9885.44};

[[nodiscard]] constexpr double intrinsicEmitterResistance(const double current)
{
    return ThermalVoltage / current;
}

[[nodiscard]] constexpr double loadedGain(const double gain, const double source, const double load)
{
    return (gain * load) / (source + load);
}

[[nodiscard]] double baseEmitterVoltage(const double current)
{
    return ThermalVoltage * std::log(current / SaturationCurrent);
}

/// 2(V_BE + I R_E), with V_BE from the exponential.
[[nodiscard]] double biasFor(const double idle, const double degeneration)
{
    return 2.0 * (baseEmitterVoltage(idle) + (idle * degeneration));
}

/// The inverse, by bisection in the logarithm. There is no closed form.
[[nodiscard]] double idleFor(const double bias, const double degeneration)
{
    double low{1.0e-12};
    double high{100.0};

    for (int iteration{0}; iteration < 200; ++iteration)
    {
        const double middle{std::sqrt(low * high)};

        if (biasFor(middle, degeneration) < bias) { low = middle; }
        else { high = middle; }
    }

    return std::sqrt(low * high);
}
} // namespace

/**
 * @brief A follower's gain is a question about current and about nothing else.
 *
 * Into 8 ohms it is 0.24 at a milliamp and 0.97 at 120. The load is fixed, the device does not
 * enter, and the only lever is r_e.
 */
TEST(ReferenceFollower, GainIsAQuestionAboutCurrent)
{
    const auto gainAt{[](const double current)
                      { return Speaker / (intrinsicEmitterResistance(current) + Speaker); }};

    EXPECT_NEAR(gainAt(1.0e-3), 0.2353, 0.001);
    EXPECT_NEAR(gainAt(10.0e-3), 0.7547, 0.001);
    EXPECT_NEAR(gainAt(Idle), 0.9736, 0.001);

    // Monotone in current, and never one.
    for (const double current : {0.1e-3, 1.0e-3, 10.0e-3, 0.1, 1.0})
    {
        EXPECT_TRUE(gainAt(current) < 1.0);
        EXPECT_TRUE(gainAt(current) > gainAt(current / 2.0));
    }
}

/**
 * @brief The eight ohm problem, and the two fixes, measured.
 *
 * 0.08 per cent, 4 per cent, 68 per cent. This is L01's loading arithmetic for the fifth time and
 * it is the only occurrence where it costs everything.
 */
TEST(ReferenceFollower, WhatALoudspeakerCostsAndWhatRecoversIt)
{
    const double follower{Beta * (intrinsicEmitterResistance(Idle) + Speaker)};

    // A Darlington's effective emitter resistance is twice one device's: the input transistor
    // runs at the output transistor's base current, so its own r_e is beta times larger, and it
    // is seen through the output transistor's gain, so it contributes r_e again. Both betas
    // cancel and the answer does not depend on beta at all.
    const double darlington{Beta * Beta * ((2.0 * intrinsicEmitterResistance(Idle)) + Speaker)};

    EXPECT_NEAR(follower, 410.8, 0.5);
    EXPECT_NEAR(darlington, 21083.3, 5.0);
    EXPECT_NEAR(darlington, Beta * ((Beta * intrinsicEmitterResistance(Idle)) + follower), 1.0e-6);

    const auto kept{[](const double load)
                    { return (100.0 * load) / (StageOutputResistance + load); }};

    EXPECT_NEAR(kept(Speaker), 0.081, 0.002);
    EXPECT_NEAR(kept(follower), 4.0, 0.1);
    EXPECT_NEAR(kept(darlington), 68.1, 0.5);

    // And the loaded gains those correspond to.
    EXPECT_NEAR(loadedGain(StageGain, StageOutputResistance, darlington), 26.18, 0.05);
    EXPECT_TRUE(loadedGain(StageGain, StageOutputResistance, Speaker) < 0.05);
}

/**
 * @brief A parallel load always costs gain, whatever the numbers are.
 *
 * The sweep rather than the point, for the same reason L07's output-resistance bound is a sweep:
 * a divider's output is smaller than its input, and no arrangement of transistors changes that.
 */
TEST(ReferenceFollower, LoadingAlwaysCosts)
{
    for (const double source : {10.0, 1.0e3, 100.0e3})
    {
        for (const double load : {1.0, 100.0, 10.0e3, 1.0e6})
        {
            const double kept{load / (source + load)};

            EXPECT_TRUE(kept < 1.0);
            EXPECT_TRUE(kept > 0.0);
        }
    }
}

/**
 * @brief The Darlington's answer spans a factor of four across an ordinary beta spread.
 *
 * Which is why an output stage is a circuit that works inside a feedback loop rather than one
 * that works on its own.
 */
TEST(ReferenceFollower, BetaSquaredIsNotANumber)
{
    const auto keptWith{
        [](const double beta)
        {
            const double load{beta * beta * ((2.0 * intrinsicEmitterResistance(Idle)) + Speaker)};
            return load / (StageOutputResistance + load);
        }};

    EXPECT_NEAR(keptWith(20.0), 0.254, 0.005);
    EXPECT_NEAR(keptWith(200.0), 0.972, 0.005);
    EXPECT_NEAR(keptWith(200.0) / keptWith(20.0), 3.82, 0.05);
}

/**
 * @brief The 26 mV rule gives an emitter factor of two at every current, which is the point of it.
 *
 * R_E = V_T/I_q is r_e = V_T/I_C written the other way round, so the ratio is exactly two and it
 * is two at 1 mA and at 10 A alike. A rule that produced a different factor at different currents
 * would not be a rule.
 */
TEST(ReferenceOutput, TheRuleIsScaleFree)
{
    for (const double idle : {1.0e-3, 10.0e-3, 0.12, 1.0, 10.0})
    {
        const double resistor{ThermalVoltage / idle};
        const double factor{(intrinsicEmitterResistance(idle) + resistor) /
                            intrinsicEmitterResistance(idle)};

        EXPECT_NEAR(factor, 2.0, 1.0e-12);
        EXPECT_NEAR(idle * resistor, ThermalVoltage, 1.0e-15);
    }
}

/**
 * @brief The dead band is two drops wide, and biasing by two drops closes it exactly.
 */
TEST(ReferenceOutput, TheDeadBand)
{
    const auto transfer{[](const double input, const double bias)
                        {
                            const double threshold{VbeOn - (bias / 2.0)};
                            if (input > threshold) { return input - threshold; }
                            if (input < -threshold) { return input + threshold; }
                            return 0.0;
                        }};

    EXPECT_NEAR(transfer(0.5, 0.0), 0.0, 1.0e-12);
    EXPECT_NEAR(transfer(-0.5, 0.0), 0.0, 1.0e-12);
    EXPECT_NEAR(transfer(1.0, 0.0), 0.35, 1.0e-12);

    // Two drops of bias and the curve passes through the origin with unit slope.
    for (const double input : {-1.0, -0.2, 0.0, 0.2, 1.0})
    {
        EXPECT_NEAR(transfer(input, 2.0 * VbeOn), input, 1.0e-12);
    }
}

/**
 * @brief The bias a class-AB stage needs, and what the constant-drop model says instead.
 *
 * This is the Cross-check's arithmetic, and the load-bearing assertion is the last one: the same
 * model that was worth 12 per cent in L06 is worth a factor of sixty here.
 */
TEST(ReferenceOutput, TheConstantDropModelFailsHere)
{
    const double exact{biasFor(Idle, Degeneration)};
    const double naive{2.0 * (VbeOn + (Idle * Degeneration))};

    EXPECT_NEAR(baseEmitterVoltage(Idle), 0.7830, 0.0005);
    EXPECT_NEAR(exact, 1.6188, 0.001);
    EXPECT_NEAR(naive, 1.3528, 0.001);

    // Sixteen per cent in the voltage.
    EXPECT_NEAR(100.0 * (exact - naive) / exact, 16.4, 0.2);

    // A factor of sixty-one in the current, which is the same error read the other way.
    const double resulting{idleFor(naive, Degeneration)};

    EXPECT_TRUE(std::isfinite(resulting));
    EXPECT_NEAR(resulting * 1.0e3, 1.955, 0.01);
    EXPECT_NEAR(Idle / resulting, 61.0, 1.0);
}

/**
 * @brief And the emitter resistors are what keep that factor down to sixty rather than 166.
 *
 * They carry 26 of the 133 mV at the idle current and none at a couple of milliamps, so the
 * junction sees the smaller error. Local feedback acting where it is needed and nowhere else,
 * which is the third job the 26 mV rule does.
 */
TEST(ReferenceOutput, TheEmitterResistorsSoftenTheExponential)
{
    const double withResistors{Idle / idleFor(2.0 * (VbeOn + (Idle * Degeneration)), Degeneration)};
    const double without{Idle / idleFor(2.0 * VbeOn, 0.0)};

    EXPECT_NEAR(without, 166.0, 2.0);
    EXPECT_NEAR(withResistors, 61.0, 1.0);
    EXPECT_TRUE(withResistors < without);
}

/**
 * @brief Thermal drift at a fixed bias, and what the emitter resistors halve.
 *
 * A factor of three over thirty degrees is still a runaway. The resistors buy margin; the thermal
 * coupling of the bias generator is what buys stability.
 */
TEST(ReferenceOutput, DriftAtAFixedBias)
{
    const auto drift{[](const double idle, const double resistor) {
        return (2.0 * 2.0e-3) / (2.0 * (intrinsicEmitterResistance(idle) + resistor) * idle);
    }};

    EXPECT_NEAR(100.0 * drift(Idle, Degeneration), 3.82, 0.05);
    EXPECT_NEAR(100.0 * drift(Idle, 0.0), 7.69, 0.05);
    EXPECT_NEAR(drift(Idle, 0.0) / drift(Idle, Degeneration), 2.0, 0.05);

    // Over thirty degrees, and this is why the resistors are not the fix.
    EXPECT_TRUE(std::pow(1.0 + drift(Idle, Degeneration), 30.0) > 2.5);
}

/** @brief Class B reaches pi/4, and class A a quarter. Both at full output and no lower. */
TEST(ReferenceOutput, TheEfficiencies)
{
    EXPECT_NEAR(100.0 * M_PI / 4.0, 78.5, 0.1);
    EXPECT_TRUE((M_PI / 4.0) > 3.0 * 0.25);
}
