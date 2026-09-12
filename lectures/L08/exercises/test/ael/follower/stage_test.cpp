/**
 * @brief Tests for ael::follower.
 *
 * Dormant until `ael/follower/stage.hpp` exists.
 */
#if __has_include("ael/follower/stage.hpp")

#include "ael/follower/stage.hpp"

#include "qacademy/test/test.hpp"

#include <cmath>

namespace
{
constexpr double Speaker{8.0};
constexpr double Idle{0.120};
constexpr double Beta{50.0};

constexpr double StageGain{-38.4615};
constexpr double StageOutputResistance{9885.44};
} // namespace

/** @brief The gain, at the three currents the lecture tabulates. */
TEST(Follower, Gain)
{
    EXPECT_NEAR(ael::follower::gain(1.0e-3, Speaker), 0.2353, 0.001);
    EXPECT_NEAR(ael::follower::gain(10.0e-3, Speaker), 0.7547, 0.001);
    EXPECT_NEAR(ael::follower::gain(Idle, Speaker), 0.9736, 0.001);
}

/**
 * @brief It is never one, at any current or into any load.
 *
 * A gain of exactly one means r_e has been dropped from the denominator, which is the one term
 * the whole of Appendix A is about.
 */
TEST(Follower, TheGainIsNeverOne)
{
    for (const double current : {1.0e-6, 1.0e-3, 1.0, 100.0})
    {
        for (const double load : {1.0, 8.0, 1.0e3, 1.0e6})
        {
            const double gain{ael::follower::gain(current, load)};

            EXPECT_TRUE(std::isfinite(gain));
            EXPECT_TRUE(gain > 0.0);
            EXPECT_TRUE(gain < 1.0);
        }
    }
}

/**
 * @brief The output resistance is the driving resistance divided by beta, plus r_e.
 *
 * At 120 mA from a kilohm the r_e term is a fifth of an ohm and the source term is twenty, so the
 * answer is a property of the source. That is the more useful way to state what a follower does.
 */
TEST(Follower, OutputResistance)
{
    EXPECT_NEAR(ael::follower::outputResistance(1.0e-3, 1.0e3, Beta), 46.0, 0.1);
    EXPECT_NEAR(ael::follower::outputResistance(Idle, 1.0e3, Beta), 20.22, 0.02);

    // With nothing driving it, r_e alone.
    EXPECT_NEAR(ael::follower::outputResistance(1.0e-3, 0.0, Beta), 26.0, 0.01);

    // And the source term scales as one over beta, exactly.
    EXPECT_NEAR(ael::follower::outputResistance(Idle, 1.0e3, 100.0) -
                    ael::follower::outputResistance(Idle, 1.0e3, 200.0),
                5.0, 0.01);
}

/** @brief Looking into the base: beta times whatever hangs on the emitter. */
TEST(Follower, InputResistance)
{
    EXPECT_NEAR(ael::follower::inputResistance(Idle, Speaker, Beta), 410.8, 0.5);
    EXPECT_NEAR(ael::follower::inputResistance(1.0e-3, Speaker, Beta), 1700.0, 1.0);

    // Proportional to beta, exactly.
    EXPECT_NEAR(ael::follower::inputResistance(Idle, Speaker, 200.0) /
                    ael::follower::inputResistance(Idle, Speaker, Beta),
                4.0, 1.0e-9);
}

/**
 * @brief A Darlington is the input device's r_e plus a whole follower, all multiplied by beta.
 *
 * Asserted as that identity rather than as a number. The tempting shortcut, beta times the single
 * follower's answer, is out by 2.6 per cent into 8 ohms and by 2 per cent into a following base:
 * it forgets the input device's own r_e, which is beta times larger because that device runs at
 * beta times less current.
 */
TEST(Follower, DarlingtonIsAFollowerDrivingAFollower)
{
    for (const double beta : {20.0, 50.0, 200.0})
    {
        const double inputDevice{beta * ael::follower::intrinsicEmitterResistance(Idle)};

        EXPECT_NEAR(ael::follower::darlingtonInputResistance(Idle, Speaker, beta),
                    beta * (inputDevice + ael::follower::inputResistance(Idle, Speaker, beta)),
                    1.0e-6);

        // Which is strictly more than the shortcut, at every beta.
        EXPECT_TRUE(ael::follower::darlingtonInputResistance(Idle, Speaker, beta) >
                    (beta * ael::follower::inputResistance(Idle, Speaker, beta)));
    }

    EXPECT_NEAR(ael::follower::darlingtonInputResistance(Idle, Speaker, Beta), 21083.3, 5.0);
}

/** @brief And its effective emitter resistance is twice one device's, whatever beta is. */
TEST(Follower, DarlingtonEmitterResistanceIsTwiceOneDevices)
{
    EXPECT_NEAR(ael::follower::darlingtonEmitterResistance(Idle),
                2.0 * ael::follower::intrinsicEmitterResistance(Idle), 1.0e-12);
    EXPECT_NEAR(ael::follower::darlingtonEmitterResistance(1.0e-3), 52.0, 0.01);
}

/**
 * @brief The loading divider, which is the most-used function in the toolkit from here on.
 */
TEST(Follower, LoadedGain)
{
    EXPECT_NEAR(ael::follower::loadedGain(StageGain, StageOutputResistance, Speaker), -0.0311,
                0.0005);
    EXPECT_NEAR(
        ael::follower::loadedGain(StageGain, StageOutputResistance,
                                  ael::follower::darlingtonInputResistance(Idle, Speaker, Beta)),
        -26.18, 0.05);

    // An infinite load costs nothing, and the sign of the gain is carried through untouched.
    EXPECT_NEAR(ael::follower::loadedGain(StageGain, StageOutputResistance, 1.0e12), StageGain,
                0.001);
    EXPECT_TRUE(ael::follower::loadedGain(StageGain, StageOutputResistance, Speaker) < 0.0);
}

/**
 * @brief And it never returns more gain than it was given.
 *
 * The same bound as L07's output resistance, one lecture on: a divider's output is smaller than
 * its input, whatever is on either side of it.
 */
TEST(Follower, LoadedGainNeverExceedsTheUnloadedGain)
{
    for (const double source : {10.0, 1.0e3, 100.0e3})
    {
        for (const double load : {1.0, 100.0, 10.0e3, 1.0e6})
        {
            const double loaded{ael::follower::loadedGain(100.0, source, load)};

            EXPECT_TRUE(std::isfinite(loaded));
            EXPECT_TRUE(loaded < 100.0);
            EXPECT_TRUE(loaded > 0.0);
        }
    }
}

#endif
