/**
 * @brief Tests for ael::ssm, the small-signal model.
 *
 * Dormant until `ael/ssm/model.hpp` exists.
 *
 * Two of these check something other than a number. `CascodeIsResistanceIntoCollector` requires
 * the cascode result to be the general expression evaluated at R_E = r_o, to machine precision,
 * which it can only be if one function calls the other; a separate formula agrees to a few digits
 * and fails at the fifteenth. `OutputResistanceNeverExceedsTheLoad` asserts the bound that
 * refutes the tempting rule, over a sweep rather than at a point.
 */
#if __has_include("ael/ssm/model.hpp")

#include "ael/ssm/model.hpp"

#include "qacademy/test/test.hpp"

#include <cmath>

namespace
{
constexpr double Current{1.0e-3};
constexpr double CollectorResistor{10.0e3};
constexpr double EmitterResistor{234.0};
constexpr double Beta{50.0};
constexpr double EarlyVoltage{100.0};
} // namespace

/** @brief 26 millivolts over the collector current, and nothing else in it. */
TEST(SmallSignal, IntrinsicEmitterResistance)
{
    EXPECT_NEAR(ael::ssm::intrinsicEmitterResistance(Current), 26.0, 0.01);
    EXPECT_NEAR(ael::ssm::intrinsicEmitterResistance(10.0e-3), 2.6, 0.001);

    // It is inversely proportional, exactly. A model with any offset in it fails here.
    EXPECT_NEAR(ael::ssm::intrinsicEmitterResistance(Current) /
                    ael::ssm::intrinsicEmitterResistance(10.0e-3),
                10.0, 1.0e-9);
}

/** @brief The source resistance is the reciprocal of the transconductance, and nothing else. */
TEST(SmallSignal, IntrinsicSourceResistance)
{
    EXPECT_NEAR(ael::ssm::intrinsicSourceResistance(4.0e-3), 250.0, 1.0e-9);
    EXPECT_NEAR(ael::ssm::intrinsicSourceResistance(1.0 / 26.0), 26.0, 1.0e-9);
}

/** @brief The emitter factor, and that it is one when there is no emitter resistor. */
TEST(SmallSignal, EmitterFactor)
{
    EXPECT_NEAR(ael::ssm::emitterFactor(Current, EmitterResistor), 10.0, 0.01);
    EXPECT_NEAR(ael::ssm::emitterFactor(Current, 220.0), 9.4615, 0.001);
    EXPECT_NEAR(ael::ssm::emitterFactor(Current, 0.0), 1.0, 1.0e-12);
}

/**
 * @brief The source factor is the same construction, and 220 mV gives 2 rather than 10.
 *
 * The correspondence between the two factors. It comes from the transconductances differing by
 * about ten, and this is where that shows up as a number.
 */
TEST(SmallSignal, SourceFactor)
{
    EXPECT_NEAR(ael::ssm::sourceFactor(4.0e-3, 220.0), 1.88, 0.001);
    EXPECT_NEAR(ael::ssm::sourceFactor(4.0e-3, 0.0), 1.0, 1.0e-12);

    // Same drop, same construction, ten times the factor, because r_e is a tenth of r_s.
    EXPECT_TRUE(ael::ssm::emitterFactor(Current, 220.0) >
                (4.0 * ael::ssm::sourceFactor(4.0e-3, 220.0)));
}

/** @brief The gain inverts, and the emitter resistor divides it by the emitter factor. */
TEST(SmallSignal, Gain)
{
    const double degenerated{ael::ssm::gain(CollectorResistor, Current, EmitterResistor)};
    const double bypassed{ael::ssm::gain(CollectorResistor, Current, 0.0)};

    EXPECT_TRUE(std::isfinite(degenerated));
    EXPECT_TRUE(degenerated < 0.0);
    EXPECT_NEAR(degenerated, -38.4615, 0.001);
    EXPECT_NEAR(bypassed, -384.615, 0.01);

    // Divided by exactly the emitter factor. That equality is the whole of Appendix A.5.
    EXPECT_NEAR(bypassed / degenerated, ael::ssm::emitterFactor(Current, EmitterResistor), 1.0e-9);
}

/**
 * @brief The gain is insensitive to current once the emitter resistor dominates.
 *
 * Ten times the current changes the degenerated gain by 10 per cent and the bypassed gain by a
 * factor of ten. That insensitivity is the reason degeneration is used, and it is not obvious
 * from the formula until it is measured.
 */
TEST(SmallSignal, DegeneratedGainBarelyMovesWithCurrent)
{
    const double low{ael::ssm::gain(CollectorResistor, Current, EmitterResistor)};
    const double high{ael::ssm::gain(CollectorResistor, 10.0e-3, EmitterResistor)};

    EXPECT_NEAR(std::fabs(high / low), 1.1, 0.02);

    const double bypassedLow{ael::ssm::gain(CollectorResistor, Current, 0.0)};
    const double bypassedHigh{ael::ssm::gain(CollectorResistor, 10.0e-3, 0.0)};

    EXPECT_NEAR(std::fabs(bypassedHigh / bypassedLow), 10.0, 1.0e-9);
}

/** @brief Looking into the base: beta times the emitter branch, and the one result beta decides. */
TEST(SmallSignal, InputResistance)
{
    EXPECT_NEAR(ael::ssm::inputResistance(Current, EmitterResistor, Beta), 13.0e3, 1.0);
    EXPECT_NEAR(ael::ssm::inputResistance(Current, 0.0, Beta), 1.3e3, 0.1);

    // It scales with beta, which is why an input resistance is a range and not a number.
    EXPECT_NEAR(ael::ssm::inputResistance(Current, EmitterResistor, 200.0) /
                    ael::ssm::inputResistance(Current, EmitterResistor, Beta),
                4.0, 1.0e-9);
}

/**
 * @brief The resistance looking into the collector, which is what the emitter factor multiplies.
 */
TEST(SmallSignal, ResistanceIntoCollector)
{
    const double bare{ael::ssm::resistanceIntoCollector(Current, 0.0, Beta, EarlyVoltage)};
    const double degenerated{
        ael::ssm::resistanceIntoCollector(Current, EmitterResistor, Beta, EarlyVoltage)};

    EXPECT_TRUE(std::isfinite(degenerated));
    EXPECT_NEAR(bare, 100.0e3, 1.0);
    EXPECT_NEAR(degenerated, 862910.0, 500.0);

    // Most of the nominal factor of ten arrives, and it arrives short, never over.
    const double nominal{ael::ssm::emitterFactor(Current, EmitterResistor)};

    EXPECT_TRUE((degenerated / bare) > (0.8 * nominal));
    EXPECT_TRUE((degenerated / bare) < nominal);
}

/**
 * @brief The boost saturates at beta however large the degeneration resistor is.
 *
 * The base resistance shunts the degeneration, so a thousandfold emitter resistor does not give a
 * thousandfold boost. This is the ceiling that makes the cascode a factor of fifty rather than a
 * factor of four thousand.
 */
TEST(SmallSignal, TheBoostCeilingIsBeta)
{
    const double output{EarlyVoltage / Current};

    for (const double emitter : {1.0e6, 1.0e9, 1.0e12})
    {
        const double actual{
            ael::ssm::resistanceIntoCollector(Current, emitter, Beta, EarlyVoltage)};

        EXPECT_TRUE(std::isfinite(actual));
        EXPECT_TRUE(actual < (1.05 * (1.0 + Beta) * output));
    }
}

/**
 * @brief The stage's output resistance, and the bound that refutes the tempting rule.
 *
 * The sweep is the assertion. A parallel combination is smaller than either part, so this must
 * hold at every current, every load and every degeneration resistor, and a formula that ever
 * returns more than the load has multiplied where it should have divided.
 */
TEST(SmallSignal, OutputResistanceNeverExceedsTheLoad)
{
    for (const double current : {0.1e-3, 1.0e-3, 10.0e-3})
    {
        for (const double load : {1.0e3, 10.0e3, 100.0e3})
        {
            for (const double emitter : {0.0, 26.0, 234.0, 2340.0})
            {
                const double actual{
                    ael::ssm::outputResistance(load, current, emitter, Beta, EarlyVoltage)};

                EXPECT_TRUE(std::isfinite(actual));
                EXPECT_TRUE(actual < load);
            }
        }
    }
}

/** @brief And its value at the worked point: 9.89 kilohm, against a tempting 100. */
TEST(SmallSignal, OutputResistanceOfTheWorkedStage)
{
    const double degenerated{ael::ssm::outputResistance(CollectorResistor, Current, EmitterResistor,
                                                        Beta, EarlyVoltage)};
    const double bare{
        ael::ssm::outputResistance(CollectorResistor, Current, 0.0, Beta, EarlyVoltage)};

    EXPECT_NEAR(degenerated, 9885.4, 2.0);
    EXPECT_NEAR(bare, 9090.9, 2.0);

    // Nine per cent, for a factor of ten in gain. That is the trade the correction exposes.
    EXPECT_TRUE((degenerated / bare) < 1.15);
}

/** @brief With a mirror load the same degeneration nearly doubles it, and now it is worth having.
 */
TEST(SmallSignal, MirrorLoadIsWhereTheBoostBecomesVisible)
{
    const double output{EarlyVoltage / Current};

    const double degenerated{
        ael::ssm::outputResistance(output, Current, EmitterResistor, Beta, EarlyVoltage)};
    const double bare{ael::ssm::outputResistance(output, Current, 0.0, Beta, EarlyVoltage)};

    EXPECT_NEAR(bare, 50.0e3, 1.0);
    EXPECT_NEAR(degenerated, 89.6e3, 300.0);
    EXPECT_TRUE((degenerated / bare) > 1.5);
}

/**
 * @brief The cascode result must *be* the general expression at R_E = r_o, not agree with it.
 *
 * This is the load-bearing test of the suite. The lecture's claim is that a cascode introduces no
 * new machinery, and the only way code can demonstrate that rather than restate it is for
 * `cascodeOutputResistance` to call `resistanceIntoCollector`. A separately derived formula will
 * agree to three or four digits and fail here, which is the point.
 */
TEST(SmallSignal, CascodeIsResistanceIntoCollector)
{
    const double output{EarlyVoltage / Current};

    EXPECT_NEAR(ael::ssm::cascodeOutputResistance(Current, Beta, EarlyVoltage),
                ael::ssm::resistanceIntoCollector(Current, output, Beta, EarlyVoltage), 1.0e-6);
}

/** @brief And its value: five megohm, against a beta times r_o ceiling of five. */
TEST(SmallSignal, CascodeOutputResistance)
{
    const double cascode{ael::ssm::cascodeOutputResistance(Current, Beta, EarlyVoltage)};

    EXPECT_TRUE(std::isfinite(cascode));
    EXPECT_NEAR(cascode, 5.037e6, 0.02e6);

    // The nominal emitter factor here is 3847 and the boost is fifty. The ceiling, again.
    EXPECT_TRUE(ael::ssm::emitterFactor(Current, EarlyVoltage / Current) > 3000.0);
    EXPECT_TRUE((cascode / (EarlyVoltage / Current)) < 60.0);
}

/** @brief Miller: the capacitance times one plus the gain, and the sign of the gain is ignored. */
TEST(SmallSignal, MillerCapacitance)
{
    EXPECT_NEAR(ael::ssm::millerCapacitance(-384.615, 4.0e-12), 1.5425e-9, 0.001e-9);

    // A gain given as positive must give the same answer; the multiplication uses its magnitude.
    EXPECT_NEAR(ael::ssm::millerCapacitance(384.615, 4.0e-12),
                ael::ssm::millerCapacitance(-384.615, 4.0e-12), 1.0e-18);

    // A stage with no gain leaves the capacitance alone, apart from the one.
    EXPECT_NEAR(ael::ssm::millerCapacitance(0.0, 4.0e-12), 4.0e-12, 1.0e-18);
}

/** @brief Degeneration is one way to buy the bandwidth back, and it costs the gain to do it. */
TEST(SmallSignal, DegenerationBuysBandwidthAtTheGainsExpense)
{
    const double bypassed{
        ael::ssm::millerCapacitance(ael::ssm::gain(CollectorResistor, Current, 0.0), 4.0e-12)};
    const double degenerated{ael::ssm::millerCapacitance(
        ael::ssm::gain(CollectorResistor, Current, EmitterResistor), 4.0e-12)};

    EXPECT_TRUE(bypassed > (9.0 * degenerated));
}

#endif
