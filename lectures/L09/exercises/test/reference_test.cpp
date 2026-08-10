/**
 * @brief The numbers L09 quotes, pinned. Needs no toolkit and is never guarded.
 *
 * The load-bearing one is `CollectorResistorCancels`, which is written as a sweep rather than a
 * pair of points: the collector resistor divides out of the rejection ratio identically, at every
 * load, every tail and every current, and that is the lecture's central claim.
 */
#include "qacademy/test/test.hpp"

#include <cmath>

namespace
{
constexpr double ThermalVoltage{0.026};
constexpr double Tail{2.0e-3};
constexpr double Load{10.0e3};
constexpr double TailResistance{10.0e3};
constexpr double Beta{50.0};

[[nodiscard]] constexpr double sideResistance(const double tail)
{
    return ThermalVoltage / (tail / 2.0);
}

[[nodiscard]] constexpr double differentialGain(const double load, const double tail)
{
    return -load / (2.0 * sideResistance(tail));
}

[[nodiscard]] constexpr double commonModeGain(const double load, const double tail,
                                              const double tailResistance)
{
    return -load / ((2.0 * tailResistance) + sideResistance(tail));
}

[[nodiscard]] double decibels(const double ratio) { return 20.0 * std::log10(ratio); }
} // namespace

/**
 * @brief Each side carries half the tail, so a 2 mA tail gives 26 ohm and not 13.
 */
TEST(ReferencePair, HalfTheTailPerSide)
{
    EXPECT_NEAR(sideResistance(Tail), 26.0, 0.01);
    EXPECT_NEAR(sideResistance(20.0e-3), 2.6, 0.001);

    // The slip this guards against: reading r_e from the tail current itself.
    EXPECT_TRUE(sideResistance(Tail) > (ThermalVoltage / Tail));
}

/** @brief The differential gain to one collector, and to both. */
TEST(ReferencePair, TheTwoFactorsOfTwo)
{
    EXPECT_NEAR(differentialGain(Load, Tail), -192.31, 0.01);
    EXPECT_NEAR(2.0 * differentialGain(Load, Tail), -384.62, 0.01);

    // The single-ended answer is exactly half the differential one, by construction.
    EXPECT_NEAR((2.0 * differentialGain(Load, Tail)) / differentialGain(Load, Tail), 2.0, 1.0e-12);
}

/**
 * @brief The collector resistor cancels out of the rejection ratio, identically.
 *
 * The sweep is the assertion. This has to hold at every load, tail current and tail resistance,
 * because R_C appears in the numerator of both gains, and a designer who reaches for a larger
 * collector resistor to improve rejection has to be wrong at every point rather than at one.
 */
TEST(ReferencePair, CollectorResistorCancels)
{
    for (const double tail : {0.2e-3, 2.0e-3, 20.0e-3})
    {
        for (const double tailResistance : {1.0e3, 10.0e3, 1.0e6})
        {
            const double reference{std::fabs(differentialGain(1.0e3, tail) /
                                             commonModeGain(1.0e3, tail, tailResistance))};

            for (const double load : {100.0, 10.0e3, 1.0e6})
            {
                const double rejection{std::fabs(differentialGain(load, tail) /
                                                 commonModeGain(load, tail, tailResistance))};

                EXPECT_TRUE(std::isfinite(rejection));
                EXPECT_NEAR(rejection / reference, 1.0, 1.0e-12);
            }
        }
    }
}

/** @brief And its value at the worked point: 385, which is 52 decibels. */
TEST(ReferencePair, RejectionOfTheWorkedPair)
{
    const double rejection{
        std::fabs(differentialGain(Load, Tail) / commonModeGain(Load, Tail, TailResistance))};

    EXPECT_NEAR(rejection, 385.1, 0.5);
    EXPECT_NEAR(decibels(rejection), 51.71, 0.05);

    // And it is very nearly the tail resistance over r_e, which is the form worth remembering.
    EXPECT_NEAR(rejection / (TailResistance / sideResistance(Tail)), 1.0, 0.005);
}

/**
 * @brief Rejection from a resistor tail is a supply-voltage question, and an impossible one.
 *
 * 80 decibels needs 260 kilohm carrying 2 mA. That is 520 V across the tail, and it is the whole
 * argument for a current source.
 */
TEST(ReferencePair, EightyDecibelsNeedsFiveHundredVolts)
{
    const double required{((1.0e4 * 2.0 * sideResistance(Tail)) - sideResistance(Tail)) / 2.0};

    EXPECT_NEAR(required, 260.0e3, 1.0e3);
    EXPECT_NEAR(required * Tail, 520.0, 5.0);

    // A simple mirror at this tail current falls short: r_o is V_A/I, which is 50 kilohm.
    const double mirror{100.0 / Tail};

    EXPECT_NEAR(decibels(mirror / sideResistance(Tail)), 65.7, 0.2);
    EXPECT_TRUE(mirror < required);

    // A cascode multiplies that by beta and clears it with room to spare.
    EXPECT_TRUE(decibels((Beta * mirror) / sideResistance(Tail)) > 95.0);
}

/**
 * @brief Taking both collectors changes what limits the rejection, and by 46 decibels.
 *
 * Single-ended, the tail alone decides. Differentially, the common-mode motion is identical on
 * both collectors and subtracts out, so what survives is the load mismatch. Two arrangements of
 * one circuit, limited by different things.
 */
TEST(ReferencePair, TheDifferentialOutputIsADifferentQuestion)
{
    const double singleEnded{
        std::fabs(differentialGain(Load, Tail) / commonModeGain(Load, Tail, TailResistance))};
    const auto differential{[](const double mismatch)
                            { return (2.0 * TailResistance) / (mismatch * sideResistance(Tail)); }};

    EXPECT_NEAR(decibels(differential(0.01)), 97.7, 0.2);
    EXPECT_NEAR(decibels(differential(0.01)) - decibels(singleEnded), 46.0, 0.3);

    // Better matching helps the differential output and does nothing at all for the other.
    EXPECT_TRUE(differential(0.001) > differential(0.01));
}

/**
 * @brief The pair is linear over nine millivolts, and the tail current does not enter.
 *
 * The tail scales the whole curve and cancels out of the ratio between the tanh and its tangent.
 * So biasing the pair harder buys transconductance and buys no linearity whatever, which is the
 * opposite of the pattern L08 established and is worth a test of its own.
 */
TEST(ReferencePair, LinearRangeDoesNotDependOnTheTail)
{
    const auto rangeFor{[](const double tail)
                        {
                            double low{0.0};
                            double high{0.5};
                            for (int iteration{0}; iteration < 200; ++iteration)
                            {
                                const double middle{0.5 * (low + high)};
                                const double scaled{middle / (2.0 * ThermalVoltage)};
                                const double transfer{tail * std::tanh(scaled)};
                                const double tangent{tail * scaled};
                                if ((transfer / tangent) > 0.99) { low = middle; }
                                else { high = middle; }
                            }
                            return 0.5 * (low + high);
                        }};

    EXPECT_NEAR(rangeFor(Tail) * 1.0e3, 9.06, 0.05);

    for (const double tail : {0.2e-3, 2.0e-3, 20.0e-3})
    {
        EXPECT_NEAR(rangeFor(tail) / rangeFor(Tail), 1.0, 1.0e-9);
    }
}

/** @brief And it hard-limits: 96 per cent of the tail has moved at 100 millivolts. */
TEST(ReferencePair, ThePairHardLimits)
{
    const auto fraction{[](const double input)
                        { return std::tanh(input / (2.0 * ThermalVoltage)); }};

    EXPECT_NEAR(fraction(0.005), 0.0959, 0.001);
    EXPECT_NEAR(fraction(0.026), 0.4621, 0.001);
    EXPECT_NEAR(fraction(0.100), 0.9580, 0.001);

    // It is a ceiling rather than a compression: 50 per cent more input buys 4 per cent more out.
    EXPECT_TRUE((fraction(0.150) - fraction(0.100)) < 0.05);
}

/**
 * @brief Base current through a source imbalance dominates every other offset by two orders.
 */
TEST(ReferenceOffset, TheSourceImbalanceIsWhatMatters)
{
    const double baseCurrent{(Tail / 2.0) / Beta};

    EXPECT_NEAR(baseCurrent * 1.0e6, 20.0, 0.1);

    const double imbalance{baseCurrent * (10.0e3 - 1.0e3)};
    const double fromLoads{(0.01 * Load * (Tail / 2.0)) / std::fabs(differentialGain(Load, Tail))};
    const double fromDevices{1.0e-3};

    EXPECT_NEAR(imbalance * 1.0e3, 180.0, 1.0);
    EXPECT_NEAR(fromLoads * 1.0e3, 0.52, 0.01);

    EXPECT_TRUE(imbalance > (100.0 * fromDevices));
    EXPECT_TRUE(imbalance > (100.0 * fromLoads));
}
