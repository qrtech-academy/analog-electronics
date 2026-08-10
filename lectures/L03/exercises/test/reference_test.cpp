/**
 * @brief The numbers L03 quotes, pinned. Needs no toolkit and is never guarded.
 *
 * The identities here are the ones the lecture leans on hardest: that a low-pass and a high-pass
 * built from the same parts sum to unity, and that loading a cascade moves its two poles apart
 * while leaving their product alone. Both are cheap to check and both catch a whole class of
 * algebra error before it reaches a figure.
 */
#include "qacademy/test/test.hpp"

#include <cmath>
#include <complex>

namespace
{
constexpr double Resistance{1.0e3};
constexpr double Capacitance{159.0e-9};

struct Test
{
    static constexpr double ExactTolerance{1.0e-12};
    static constexpr double LooseTolerance{1.0e-9};
};

[[nodiscard]] double corner(const double resistance, const double capacitance)
{
    return 1.0 / (2.0 * M_PI * resistance * capacitance);
}

[[nodiscard]] std::complex<double> lowpass(const double frequency, const double cornerHz)
{
    return 1.0 / std::complex<double>{1.0, frequency / cornerHz};
}

[[nodiscard]] std::complex<double> highpass(const double frequency, const double cornerHz)
{
    const std::complex<double> ratio{0.0, frequency / cornerHz};
    return ratio / (1.0 + ratio);
}
} // namespace

/**
 * @brief A low-pass and its complementary high-pass sum to the input at every frequency.
 *
 * Two outputs each 0.707 of the input summing to exactly the input is only a paradox if the phase
 * is ignored, which is the habit this course spends L02 arguing against.
 */
TEST(ReferenceFilter, ComplementaryOutputsSumToUnity)
{
    const double cornerHz{corner(Resistance, Capacitance)};

    for (const double ratio : {0.01, 0.5, 1.0, 2.0, 100.0})
    {
        const auto sum{lowpass(ratio * cornerHz, cornerHz) + highpass(ratio * cornerHz, cornerHz)};

        EXPECT_NEAR(std::abs(sum), 1.0, Test::ExactTolerance);
        EXPECT_NEAR(std::arg(sum), 0.0, Test::ExactTolerance);
    }
}

/**
 * @brief At the corner they are 90 degrees apart, one lagging and one leading.
 */
TEST(ReferenceFilter, AtTheCornerTheyAreNinetyDegreesApart)
{
    const double cornerHz{corner(Resistance, Capacitance)};
    const double low{std::arg(lowpass(cornerHz, cornerHz)) * 180.0 / M_PI};
    const double high{std::arg(highpass(cornerHz, cornerHz)) * 180.0 / M_PI};

    EXPECT_NEAR(low, -45.0, Test::LooseTolerance);
    EXPECT_NEAR(high, 45.0, Test::LooseTolerance);
    EXPECT_NEAR(high - low, 90.0, Test::LooseTolerance);
}

/**
 * @brief Loading a cascade splits its poles apart but leaves their product at the corner squared.
 *
 * The sanity check the appendix recommends: two poles that do not multiply back to the
 * single-section corner squared mean the arithmetic is wrong.
 */
TEST(ReferenceFilter, CascadePolesMultiplyBackToTheCorner)
{
    const double cornerHz{corner(Resistance, Capacitance)};
    const double low{cornerHz * (3.0 - std::sqrt(5.0)) / 2.0};
    const double high{cornerHz * (3.0 + std::sqrt(5.0)) / 2.0};

    EXPECT_NEAR(low * high, cornerHz * cornerHz, 1.0e-3);
    EXPECT_NEAR(low / cornerHz, 0.3819660, 1.0e-6);
    EXPECT_NEAR(high / cornerHz, 2.6180340, 1.0e-6);
}

/**
 * @brief Two sections cascaded directly are 3 dB down well below where independence would say.
 *
 * 375 Hz against 644 Hz, a factor of 1.72. Pinned here because it is the Cross-check's answer and
 * the whole reason the lecture introduces a buffer.
 */
TEST(ReferenceFilter, CascadedIsLowerThanBuffered)
{
    const double cornerHz{corner(Resistance, Capacitance)};
    const double buffered{cornerHz * std::sqrt(std::sqrt(2.0) - 1.0)};

    // The loaded cascade's half-power point solves u^4 + 7u^2 - 1 = 0, which is where the second
    // section's loading of the first ends up. `buffered < cornerHz` on its own is a tautology:
    // the factor is 0.644 by construction. The comparison worth pinning is against the cascade.
    const double cascaded{cornerHz * std::sqrt((-7.0 + std::sqrt(53.0)) / 2.0)};

    EXPECT_NEAR(buffered, 644.2, 0.1);
    EXPECT_NEAR(cascaded, 374.6, 0.1);
    EXPECT_NEAR(buffered / cascaded, 1.71974, 1.0e-4);
}

/**
 * @brief Q is the voltage multiplication inside the filter, not only the sharpness of its peak.
 *
 * Five volts in, a Q of ten, and fifty volts across a component the transfer function never
 * mentions.
 */
TEST(ReferenceResonance, QIsAlsoAVoltageMultiplier)
{
    constexpr double inductance{10.0e-3};
    constexpr double capacitance{1.0e-6};
    constexpr double resistance{10.0};

    const double resonance{1.0 / (2.0 * M_PI * std::sqrt(inductance * capacitance))};
    const double reactance{2.0 * M_PI * resonance * inductance};
    const double quality{std::sqrt(inductance / capacitance) / resistance};

    EXPECT_NEAR(reactance, 100.0, 1.0e-6);
    EXPECT_NEAR(quality, 10.0, 1.0e-9);

    // Five volts in, so half an amp, so fifty volts across the inductor.
    const double current{5.0 / resistance};
    EXPECT_NEAR(current * reactance, quality * 5.0, 1.0e-6);
}
