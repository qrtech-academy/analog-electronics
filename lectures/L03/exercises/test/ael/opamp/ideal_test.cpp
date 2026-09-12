/**
 * @brief Tests for ael::opamp::ideal, the standard configurations.
 *
 * Dormant until `ael/opamp/ideal.hpp` exists. Three lines each, and worth having because from
 * here on they are what the solver gets checked against.
 */
#if __has_include("ael/opamp/ideal.hpp")

#include "ael/opamp/ideal.hpp"

#include "qacademy/test/test.hpp"

namespace
{
struct Test
{
    static constexpr double Tolerance{1.0e-12};
};
} // namespace

/** @brief The non-inverting gain is one plus the ratio, and can never be less than one. */
TEST(OpampIdeal, NonInverting)
{
    EXPECT_NEAR(ael::opamp::ideal::nonInvertingGain(90.0e3, 10.0e3), 10.0, Test::Tolerance);

    // With no feedback resistor it is a follower.
    EXPECT_NEAR(ael::opamp::ideal::nonInvertingGain(0.0, 10.0e3), 1.0, Test::Tolerance);

    // And it cannot be talked below one.
    EXPECT_TRUE(ael::opamp::ideal::nonInvertingGain(1.0e3, 1.0e6) > 1.0);
}

/** @brief The inverting gain is negative, and unlike the non-inverting one it can be small. */
TEST(OpampIdeal, Inverting)
{
    EXPECT_NEAR(ael::opamp::ideal::invertingGain(100.0e3, 10.0e3), -10.0, Test::Tolerance);
    EXPECT_NEAR(ael::opamp::ideal::invertingGain(1.0e3, 10.0e3), -0.1, Test::Tolerance);
    EXPECT_TRUE(ael::opamp::ideal::invertingGain(100.0e3, 10.0e3) < 0.0);
}

/** @brief The difference gain is the ratio, positive, and says nothing about matching. */
TEST(OpampIdeal, Difference)
{
    EXPECT_NEAR(ael::opamp::ideal::differenceGain(100.0e3, 10.0e3), 10.0, Test::Tolerance);
}

/**
 * @brief The Schmitt thresholds are symmetric about zero and their gap is the hysteresis.
 *
 * 100 kilohm over 1 kilohm on plus and minus 12 V rails gives plus and minus 119 millivolts,
 * which is the design in Appendix C.5.
 */
TEST(OpampIdeal, SchmittThresholds)
{
    const auto thresholds{ael::opamp::ideal::schmittThresholds(12.0, 100.0e3, 1.0e3)};

    EXPECT_NEAR(thresholds.second, 0.11881, 1.0e-5);
    EXPECT_NEAR(thresholds.first, -thresholds.second, Test::Tolerance);
    EXPECT_NEAR(thresholds.second - thresholds.first, 0.23762, 1.0e-5);
}

#endif
