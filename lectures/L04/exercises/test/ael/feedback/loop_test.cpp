/**
 * @brief Tests for ael::feedback, the loop-gain results.
 *
 * Dormant until `ael/feedback/loop.hpp` exists.
 */
#if __has_include("ael/feedback/loop.hpp")

#include "ael/feedback/loop.hpp"

#include "qacademy/test/test.hpp"

namespace
{
struct Test
{
    static constexpr double Tolerance{1.0e-9};
};
} // namespace

/** @brief The loop gain is the open-loop gain times the fed-back fraction. */
TEST(Feedback, LoopGain)
{
    EXPECT_NEAR(ael::feedback::loopGain(1.0e5, 0.1), 1.0e4, Test::Tolerance);
    EXPECT_NEAR(ael::feedback::loopGain(1.0e5, 1.0e-3), 100.0, Test::Tolerance);
}

/** @brief The closed-loop gain approaches one over beta, from below, never from above. */
TEST(Feedback, ClosedLoopApproachesIdealFromBelow)
{
    for (const double openLoop : {1.0e3, 1.0e5, 1.0e7})
    {
        const double closed{ael::feedback::closedLoopGain(openLoop, 0.1)};
        EXPECT_TRUE(closed < 10.0);
        EXPECT_TRUE(closed > 9.0);
    }

    // More open-loop gain gets closer.
    EXPECT_TRUE(ael::feedback::closedLoopGain(1.0e7, 0.1) >
                ael::feedback::closedLoopGain(1.0e3, 0.1));
}

/** @brief The error is one part in one plus the loop gain. */
TEST(Feedback, ErrorIsOnePartInOnePlusLoopGain)
{
    EXPECT_NEAR(ael::feedback::gainError(1.0e5, 0.1), 1.0 / (1.0 + 1.0e4), 1.0e-12);
    EXPECT_NEAR(ael::feedback::gainError(1.0e5, 0.1) * 100.0, 0.01, 1.0e-5);

    // A gain of 1000 from the same amplifier is a hundred times worse.
    EXPECT_NEAR(ael::feedback::gainError(1.0e5, 1.0e-3) * 100.0, 0.9901, 1.0e-4);
}

/**
 * @brief Accuracy has a bandwidth of its own, far narrower than the closed-loop bandwidth.
 *
 * The result D.3 exists for: an amplifier that meets 0.1 per cent at DC meets it only to about
 * a hundred hertz, on a part whose datasheet says one megahertz.
 */
TEST(Feedback, AccuracyHasItsOwnBandwidth)
{
    constexpr double product{1.0e6};
    constexpr double closedLoop{100.0};
    constexpr double beta{1.0 / closedLoop};

    // Open-loop gain falls as the product over frequency.
    const auto openLoopAt{[&](const double frequency) { return product / frequency; }};

    // At DC-ish the error is small; at a kilohertz it is not.
    EXPECT_TRUE(ael::feedback::gainError(1.0e5, beta) < 1.1e-3);
    EXPECT_TRUE(ael::feedback::gainError(openLoopAt(1.0e3), beta) > 0.05);

    // One per cent is reached around a hundred hertz.
    EXPECT_NEAR(ael::feedback::gainError(openLoopAt(101.0), beta), 0.01, 2.0e-3);
}

#endif
