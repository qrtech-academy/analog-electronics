/**
 * @brief The numbers L05 quotes, pinned. Needs no toolkit and is never guarded.
 */
#include "qacademy/test/test.hpp"

#include <cmath>

namespace
{
constexpr double ThermalVoltage{0.026};
constexpr double Saturation{1.0e-14};
constexpr double Beta{50.0};

[[nodiscard]] double baseEmitterVoltage(const double collectorCurrent)
{
    return ThermalVoltage * std::log((collectorCurrent / Saturation) + 1.0);
}
} // namespace

/**
 * @brief The base-emitter voltage is 0.659 V at 1 mA, not the 0.7 V everyone quotes.
 *
 * Sixty millivolts per decade either side of it. The 0.7 V figure belongs to a few milliamps, and
 * the difference is why L06 uses a constant drop for bias and never for anything sensitive.
 */
TEST(ReferenceBjt, BaseEmitterVoltageAtThreeCurrents)
{
    EXPECT_NEAR(baseEmitterVoltage(1.0e-5), 0.5388, 1.0e-4);
    EXPECT_NEAR(baseEmitterVoltage(1.0e-3), 0.6585, 1.0e-4);
    EXPECT_NEAR(baseEmitterVoltage(1.0e-2), 0.7184, 1.0e-4);

    EXPECT_NEAR(baseEmitterVoltage(1.0e-2) - baseEmitterVoltage(1.0e-3),
                ThermalVoltage * std::log(10.0), 1.0e-9);
}

/**
 * @brief The base-emitter junction's incremental resistance is 26 ohm at 1 mA.
 *
 * The same number as the diode of L04, and the r_e that every result in Part 2 is written in
 * terms of from L07. It arrives here three lectures early as a property of a diode.
 */
TEST(ReferenceBjt, IncrementalResistanceIsTwentySixOhms)
{
    EXPECT_NEAR(ThermalVoltage / 1.0e-3, 26.0, 1.0e-9);
    EXPECT_NEAR(ThermalVoltage / 1.0e-2, 2.6, 1.0e-9);
}

/**
 * @brief The emitter carries both currents, so it exceeds the collector by 2 per cent at beta 50.
 *
 * Which is why this course writes them as equal and why that is allowed: the error is smaller
 * than any resistor tolerance in the circuit.
 */
TEST(ReferenceBjt, EmitterExceedsCollectorByTwoPerCent)
{
    const double collector{1.0e-3};
    const double emitter{collector * (1.0 + (1.0 / Beta))};

    EXPECT_NEAR(emitter / collector, 1.02, 1.0e-9);
    EXPECT_TRUE((emitter - collector) / collector < 0.021);
}

/**
 * @brief The forced-beta method never mentions h_FE, which is the whole point of it.
 */
TEST(ReferenceSwitch, ForcedBetaDoesNotUseHfe)
{
    constexpr double load{0.1};
    constexpr double forced{10.0};
    constexpr double drive{5.0};

    const double baseCurrent{load / forced};
    const double resistor{(drive - 0.7) / baseCurrent};

    EXPECT_NEAR(baseCurrent, 10.0e-3, 1.0e-12);
    EXPECT_NEAR(resistor, 430.0, 1.0e-9);

    // With the E12 value the forced beta lands near eleven, still far below any real h_FE.
    EXPECT_NEAR(load / ((drive - 0.7) / 470.0), 10.93, 1.0e-2);
}

/**
 * @brief A MOSFET's transconductance goes as the square root of current, a BJT's as the current.
 *
 * A factor of ten apart at 1 mA, which is the reason L07's source factor is two where its emitter
 * factor is ten.
 */
TEST(ReferenceMosfet, TransconductanceRatioAtOneMilliamp)
{
    constexpr double k{8.0e-3};
    const double bjt{1.0e-3 / ThermalVoltage};
    const double mosfet{std::sqrt(2.0 * k * 1.0e-3)};

    EXPECT_NEAR(bjt * 1.0e3, 38.46, 1.0e-2);
    EXPECT_NEAR(mosfet * 1.0e3, 4.0, 1.0e-9);
    EXPECT_NEAR(bjt / mosfet, 9.6, 0.1);

    // And the gap widens with current, because the ratio goes as the square root.
    const double atTen{(1.0e-2 / ThermalVoltage) / std::sqrt(2.0 * k * 1.0e-2)};
    EXPECT_TRUE(atTen > bjt / mosfet);
}
