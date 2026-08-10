/**
 * @brief The numbers L01 quotes, pinned. Needs no toolkit and is never guarded.
 */
#include "qacademy/test/test.hpp"

namespace
{
/** Supply voltage in V. */
constexpr double Supply{10.0};

/** Upper leg resistance in Ohm. */
constexpr double Upper{33.0e3};

/** Lower leg resistance in Ohm.. */
constexpr double Lower{6.8e3};

/** Thevenin resistance in Ohm. */
constexpr double TheveninResistance{5638.19095477387};

/**
 * @brief Test parameters.
 */
struct Test
{
    /** Exact tolerance. */
    static constexpr double ExactTolerance{1.0e-12};

    /** Voltage tolerance. */
    static constexpr double VoltageTolerance{1.0e-9};
};

/**
 * @brief Two resistances in parallel.
 *
 * @param[in] a First resistance.
 * @param[in] b Second resistance.
 *
 * @return The parallel combination.
 */
[[nodiscard]] constexpr double parallel(const double a, const double b)
{
    const auto div = a + b;
    return 0.0 != div ? (a * b) / div : 0.0;
}

/**
 * @brief The output of an unloaded resistive divider.
 *
 * @param[in] supply Supply voltage.
 * @param[in] upper Upper leg resistance.
 * @param[in] lower Lower leg resistance.
 *
 * @return The output voltage.
 */
[[nodiscard]] constexpr double divider(const double supply, const double upper, const double lower)
{
    const auto div = upper + lower;
    return 0.0 != div ? (supply * lower) / div : 0.0;
}
} // namespace

/**
 * @brief The divider L01 quotes gives 1.709 V, not the 1.65 V that looks right.
 *
 * This one is worth stating twice, because it is easy to get wrong: 33k over 6.8k on a 10 V
 * supply is 1.709 V. There is no E12 pair that gives 1.65 V here, and the value matters in L06,
 * where it decides the collector current of the worked stage.
 */
TEST(ReferenceDivider, UnloadedOutput)
{
    constexpr double expectedResistance{1.708542713567839};
    EXPECT_NEAR(divider(Supply, Upper, Lower), expectedResistance, Test::VoltageTolerance);
}

/**
 * @brief A divider's Thevenin resistance is its two legs in parallel.
 *
 * Not the upper leg, not the lower leg, and smaller than either. It is also symmetric in the two,
 * which surprises people who expect the source impedance to depend on which way round they are.
 */
TEST(ReferenceDivider, TheveninResistance)
{
    EXPECT_NEAR(parallel(Upper, Lower), TheveninResistance, Test::VoltageTolerance);
    EXPECT_NEAR(parallel(Upper, Lower), parallel(Lower, Upper), Test::ExactTolerance);
    EXPECT_TRUE(parallel(Upper, Lower) < Lower);
}

/**
 * @brief Loading the divider with its own Thevenin resistance halves the output.
 *
 * The definition of the Thevenin resistance, restated as something you can measure, and the first
 * appearance of the idea that decides the whole course: what a stage delivers depends on what is
 * hanging on it.
 */
TEST(ReferenceDivider, LoadedByTheveninResistance)
{
    const double thevenin{parallel(Upper, Lower)};
    const double loaded{divider(Supply, Upper, parallel(Lower, thevenin))};

    EXPECT_NEAR(loaded, divider(Supply, Upper, Lower) / 2.0, Test::VoltageTolerance);
}

/**
 * @brief Ten kilohms on the same divider costs it a third of its output.
 *
 * The number the appendix quotes, and the reason the appendix quotes it: 10k sounds like a light
 * load until you notice the divider's own resistance is 5.6k.
 */
TEST(ReferenceDivider, LoadedByTenKilohm)
{
    EXPECT_NEAR(divider(Supply, Upper, parallel(Lower, 10.0e3)), 1.09254498714653,
                Test::VoltageTolerance);
}
