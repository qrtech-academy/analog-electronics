/**
 * @brief Tests for ael::filter, the closed-form responses.
 *
 * Dormant until `ael/filter/response.hpp` exists.
 */
#if __has_include("ael/filter/response.hpp")

#include "ael/filter/response.hpp"

#include "qacademy/test/test.hpp"

#include <cmath>

namespace
{
constexpr double Resistance{1.0e3};
constexpr double Capacitance{159.0e-9};

struct Test
{
    static constexpr double Tolerance{1.0e-9};
};
} // namespace

/** @brief The corner is where the reactance equals the resistance. */
TEST(Filter, RcCorner)
{
    const double cornerHz{ael::filter::rcCorner(Resistance, Capacitance)};

    EXPECT_NEAR(cornerHz, 1000.9745, 1.0e-3);
    EXPECT_NEAR(1.0 / (2.0 * M_PI * cornerHz * Capacitance), Resistance, 1.0e-6);
}

/** @brief Low-pass and high-pass are complementary: their sum is unity at every frequency. */
TEST(Filter, LowAndHighPassAreComplementary)
{
    const double cornerHz{ael::filter::rcCorner(Resistance, Capacitance)};

    for (const double ratio : {0.01, 1.0, 100.0})
    {
        const auto sum{ael::filter::lowpass(ratio * cornerHz, cornerHz) +
                       ael::filter::highpass(ratio * cornerHz, cornerHz)};
        EXPECT_NEAR(std::abs(sum), 1.0, Test::Tolerance);
    }
}

/** @brief The low-pass lags and the high-pass leads, by 45 degrees each at the corner. */
TEST(Filter, PhaseSignsAtTheCorner)
{
    const double cornerHz{ael::filter::rcCorner(Resistance, Capacitance)};

    EXPECT_NEAR(std::arg(ael::filter::lowpass(cornerHz, cornerHz)) * 180.0 / M_PI, -45.0, 1.0e-6);
    EXPECT_NEAR(std::arg(ael::filter::highpass(cornerHz, cornerHz)) * 180.0 / M_PI, 45.0, 1.0e-6);
}

/** @brief Resonance depends on L and C only; Q depends on the resistance too. */
TEST(Filter, ResonanceAndQuality)
{
    EXPECT_NEAR(ael::filter::lcResonance(10.0e-3, 1.0e-6), 1591.5494, 1.0e-3);
    EXPECT_NEAR(ael::filter::seriesQ(10.0, 10.0e-3, 1.0e-6), 10.0, Test::Tolerance);

    // Halving the resistance doubles the Q and leaves the resonance alone.
    EXPECT_NEAR(ael::filter::seriesQ(5.0, 10.0e-3, 1.0e-6), 20.0, Test::Tolerance);
}

/** @brief A band-pass is unity at resonance and its bandwidth is the resonance over Q. */
TEST(Filter, BandpassPeaksAtResonance)
{
    const double resonance{ael::filter::lcResonance(10.0e-3, 1.0e-6)};
    const double quality{ael::filter::seriesQ(10.0, 10.0e-3, 1.0e-6)};

    EXPECT_NEAR(std::abs(ael::filter::bandpass(resonance, resonance, quality)), 1.0,
                Test::Tolerance);
    EXPECT_NEAR(std::arg(ael::filter::bandpass(resonance, resonance, quality)), 0.0, 1.0e-9);

    // Half a bandwidth either side of resonance is the half-power point.
    const double edge{resonance *
                      (std::sqrt(1.0 + 1.0 / (4.0 * quality * quality)) + 1.0 / (2.0 * quality))};
    EXPECT_NEAR(std::abs(ael::filter::bandpass(edge, resonance, quality)), 1.0 / std::sqrt(2.0),
                1.0e-9);
}

/**
 * @brief Two sections cascaded directly are 3 dB down at 0.374 of one section's corner.
 *
 * Not 1.0, which is one section, and not 0.644, which is two sections with a buffer between them.
 * This is the Cross-check's answer.
 */
TEST(Filter, CascadedCornerAccountsForLoading)
{
    const double single{ael::filter::rcCorner(Resistance, Capacitance)};
    const double cascaded{ael::filter::cascadedCorner(Resistance, Capacitance)};
    const double buffered{single * std::sqrt(std::sqrt(2.0) - 1.0)};

    EXPECT_NEAR(cascaded / single, 0.374239, 1.0e-4);
    EXPECT_TRUE(cascaded < buffered);
    EXPECT_NEAR(buffered / cascaded, 1.71974, 1.0e-3);
}

#endif
