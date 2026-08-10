/**
 * @brief The numbers L02 quotes, pinned. Needs no toolkit and is never guarded.
 *
 * Every other test file in this suite is dormant behind an `#if __has_include(...)` until you
 * write the component it tests. This one is not, so that the suite reports something on the day
 * you start rather than reporting red in silence. See ../../../L01/exercises/test/README.md for
 * why that matters.
 *
 * The first-order response is reimplemented here in one line. It is not a solution to anything:
 * the exercise is a complex nodal solve over an arbitrary netlist, and a single closed form for
 * one topology is exactly the thing the solver exists to stop you relying on.
 */
#include "qacademy/test/test.hpp"

#include <cmath>
#include <complex>

namespace
{
/** The RC section L02 uses throughout. */
constexpr double Resistance{1.0e3};
constexpr double Capacitance{159.0e-9};

/** Tolerances. These are closed forms, so the slack is floating point rather than physics. */
struct Test
{
    static constexpr double TightTolerance{1.0e-9};
    static constexpr double DecibelTolerance{1.0e-3};
    static constexpr double DegreeTolerance{1.0e-6};
};

/**
 * @brief The corner frequency of an RC section.
 *
 * @param[in] resistance  Series resistance.
 * @param[in] capacitance Shunt capacitance.
 *
 * @return The corner, in hertz.
 */
[[nodiscard]] double corner(const double resistance, const double capacitance)
{
    return 1.0 / (2.0 * M_PI * resistance * capacitance);
}

/**
 * @brief The complex response of a first-order low-pass at one frequency.
 *
 * @param[in] frequency Frequency of interest.
 * @param[in] cornerHz  The section's corner frequency.
 *
 * @return The response, as a phasor ratio.
 */
[[nodiscard]] std::complex<double> lowpass(const double frequency, const double cornerHz)
{
    return 1.0 / std::complex<double>{1.0, frequency / cornerHz};
}

/**
 * @brief A voltage ratio in decibels.
 *
 * @param[in] ratio The ratio.
 *
 * @return The ratio in dB.
 */
[[nodiscard]] double decibels(const double ratio) { return 20.0 * std::log10(ratio); }
} // namespace

/**
 * @brief The corner is where the reactance equals the resistance, and nowhere else.
 *
 * Worth pinning as an identity rather than a number: it is the definition the whole lecture rests
 * on, and it makes the 1001 Hz below a consequence rather than a constant to be trusted.
 */
TEST(ReferenceResponse, CornerIsWhereReactanceEqualsResistance)
{
    const double cornerHz{corner(Resistance, Capacitance)};
    const double reactance{1.0 / (2.0 * M_PI * cornerHz * Capacitance)};

    EXPECT_NEAR(reactance, Resistance, Test::TightTolerance);
    EXPECT_NEAR(cornerHz, 1000.9745, 1.0e-3);
}

/**
 * @brief Three decibels down and forty-five degrees, at the corner.
 *
 * The two numbers this course expects a reader to have memorised. Everything else on a first-order
 * response follows from them.
 */
TEST(ReferenceResponse, ThreeDecibelsAndFortyFiveDegrees)
{
    const double cornerHz{corner(Resistance, Capacitance)};
    const auto response{lowpass(cornerHz, cornerHz)};

    EXPECT_NEAR(decibels(std::abs(response)), -3.0103, Test::DecibelTolerance);
    EXPECT_NEAR(std::arg(response) * 180.0 / M_PI, -45.0, Test::DegreeTolerance);
}

/**
 * @brief A decade below the corner the magnitude has done nothing and the phase has not.
 *
 * The point of the lecture's insistence that the phase is the half people skip: 0.04 dB is
 * invisible on any plot, and 5.7 degrees is a real contribution to a loop's stability margin.
 */
TEST(ReferenceResponse, ADecadeBelowTheCorner)
{
    const double cornerHz{corner(Resistance, Capacitance)};
    const auto response{lowpass(cornerHz / 10.0, cornerHz)};

    EXPECT_NEAR(decibels(std::abs(response)), -0.0432, Test::DecibelTolerance);
    EXPECT_NEAR(std::arg(response) * 180.0 / M_PI, -5.7106, 1.0e-3);
}

/**
 * @brief The phase curve is odd about the corner on a logarithmic axis.
 *
 * So whatever the phase has done a decade below, it has ninety degrees minus that much left to do
 * a decade above. Pinned because it is the reason only two of the six numbers in D.2 need
 * remembering.
 */
TEST(ReferenceResponse, PhaseIsOddAboutTheCorner)
{
    const double cornerHz{corner(Resistance, Capacitance)};
    const double below{std::arg(lowpass(cornerHz / 10.0, cornerHz)) * 180.0 / M_PI};
    const double above{std::arg(lowpass(cornerHz * 10.0, cornerHz)) * 180.0 / M_PI};

    EXPECT_NEAR(below + above, -90.0, 1.0e-9);
}

/**
 * @brief Settling accuracy is bought logarithmically, and that is the surprising part.
 *
 * Every further decade of accuracy costs the same 2.3 time constants, so fourteen bits costs only
 * 1.75 times what eight bits does. Guessing that it costs 64 times as much is the error this pins
 * against.
 */
TEST(ReferenceSettling, AccuracyCostsTimeConstantsLogarithmically)
{
    EXPECT_NEAR(std::log(100.0), 4.6052, 1.0e-4);
    EXPECT_NEAR(std::log(1.0e4) / std::log(100.0), 2.0, Test::TightTolerance);

    const double eightBits{8.0 * std::log(2.0)};
    const double fourteenBits{14.0 * std::log(2.0)};

    EXPECT_NEAR(eightBits, 5.5452, 1.0e-4);
    EXPECT_NEAR(fourteenBits, 9.7041, 1.0e-4);

    // The ratio of the two is 14/8 with the log(2) cancelling, so asserting that proves nothing.
    // What is worth pinning is that the cost is logarithmic rather than exponential in the bit
    // count: under two time constants more, against the factor of 64 a linear guess would give.
    EXPECT_TRUE((fourteenBits / eightBits) < 2.0);
    EXPECT_TRUE(std::pow(2.0, 14.0 - 8.0) > 60.0);
}
