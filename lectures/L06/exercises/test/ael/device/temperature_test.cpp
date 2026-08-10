/**
 * @brief Tests that the temperature coefficient emerges from the model rather than being inserted.
 *
 * Dormant until `ael/device/bjt.hpp` gains a temperature.
 */
#if __has_include("ael/device/bjt.hpp")

#include "ael/device/bjt.hpp"

#include "qacademy/test/test.hpp"

#include <cmath>

namespace
{
/**
 * @brief The base-emitter voltage needed for a given collector current, at a given temperature.
 *
 * Found by bisection on the device model, so it makes no assumption about how the model computes
 * anything.
 */
[[nodiscard]] double voltageFor(const double collectorCurrent,
                                const ael::device::bjt::Parameters& parameters)
{
    double low{0.2};
    double high{1.2};
    for (int i{0}; i < 200; ++i)
    {
        const double mid{(low + high) / 2.0};
        if (ael::device::bjt::currents(mid, -5.0, parameters).collector < collectorCurrent)
        {
            low = mid;
        }
        else { high = mid; }
    }
    return (low + high) / 2.0;
}
} // namespace

/**
 * @brief The base-emitter voltage falls about 1.8 mV per degree, and the model was not told to.
 *
 * The figure everyone quotes is 2 mV. The physics gives about 1.77 at 1 mA, and a model that
 * returns exactly 2.0 has had the coefficient inserted by hand, which would make L06's
 * Cross-check circular. The window here admits the physics and excludes the insertion.
 */
TEST(BjtTemperature, CoefficientEmergesRatherThanBeingInserted)
{
    ael::device::bjt::Parameters cold{};
    ael::device::bjt::Parameters warm{};
    warm.temperature = cold.temperature + 1.0;

    const double drift{voltageFor(1.0e-3, warm) - voltageFor(1.0e-3, cold)};

    EXPECT_TRUE(std::isfinite(drift));
    EXPECT_TRUE(drift < 0.0);
    EXPECT_NEAR(drift, -1.8e-3, 0.35e-3);

    // Exactly minus two millivolts would mean it was put in by hand.
    EXPECT_TRUE(std::fabs(drift + 2.0e-3) > 1.0e-5);
}

/** @brief The coefficient depends on the operating current, which a fixed constant could not. */
TEST(BjtTemperature, CoefficientDependsOnCurrent)
{
    ael::device::bjt::Parameters cold{};
    ael::device::bjt::Parameters warm{};
    warm.temperature = cold.temperature + 1.0;

    const double atOne{voltageFor(1.0e-3, warm) - voltageFor(1.0e-3, cold)};
    const double atTen{voltageFor(1.0e-2, warm) - voltageFor(1.0e-2, cold)};

    EXPECT_TRUE(std::fabs(atTen - atOne) > 1.0e-5);
    EXPECT_TRUE(atTen > atOne);
}

/** @brief At a fixed base-emitter voltage the current rises several per cent per degree. */
TEST(BjtTemperature, CurrentRisesSharplyAtFixedVoltage)
{
    ael::device::bjt::Parameters cold{};
    ael::device::bjt::Parameters warm{};
    warm.temperature = cold.temperature + 1.0;

    const double voltage{voltageFor(1.0e-3, cold)};
    const double before{ael::device::bjt::currents(voltage, -5.0, cold).collector};
    const double after{ael::device::bjt::currents(voltage, -5.0, warm).collector};

    const double perDegree{(after / before) - 1.0};

    EXPECT_TRUE(perDegree > 0.05);
    EXPECT_TRUE(perDegree < 0.10);
}

#endif
