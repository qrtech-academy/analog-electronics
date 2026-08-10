/**
 * @brief Tests for ael::report, the capstone.
 *
 * Dormant until `ael/report/amplifier.hpp` exists.
 *
 * `BudgetComposesTheEarlierComponents` is the load-bearing one. This component has no physics in
 * it at all: every number it produces belongs to a function written in L07, L08 or L09, and the
 * test requires agreement to machine precision, which only calling them can give.
 */
#if __has_include("ael/report/amplifier.hpp")

#include "ael/report/amplifier.hpp"

#include "qacademy/test/test.hpp"

#include <cmath>

#if __has_include("ael/diffpair/pair.hpp")
#include "ael/diffpair/pair.hpp"
#endif
#if __has_include("ael/follower/stage.hpp")
#include "ael/follower/stage.hpp"
#endif

namespace
{
[[nodiscard]] ael::report::Design design()
{
    ael::report::Design value{};
    value.tailCurrent      = 2.0e-3;
    value.bufferCurrent    = 1.0e-3;
    value.gainStageCurrent = 1.0e-3;
    value.idleCurrent      = 0.120;
    value.load             = 8.0;
    value.supply           = 15.0;
    value.beta             = 50.0;
    value.earlyVoltage     = 100.0;
    return value;
}
} // namespace

/** @brief Four stages, named, in order. */
TEST(Report, TheBudgetHasFourStages)
{
    const auto budget{ael::report::budget(design())};

    EXPECT_EQ(budget.stages.size(), std::size_t{4U});
    for (const auto& stage : budget.stages)
    {
        EXPECT_TRUE(!stage.name.empty());
        EXPECT_TRUE(std::isfinite(stage.unloaded));
        EXPECT_TRUE(std::isfinite(stage.loaded));
    }
}

/** @brief Every stage gain, at the design of Appendix A. */
TEST(Report, TheStageGains)
{
    const auto budget{ael::report::budget(design())};

    EXPECT_NEAR(budget.stages[0].unloaded, 1923.1, 1.0);
    EXPECT_NEAR(budget.stages[0].loaded, 1895.0, 2.0);
    EXPECT_NEAR(budget.stages[1].loaded, 0.9615, 0.001);
    EXPECT_NEAR(budget.stages[2].unloaded, 1923.1, 1.0);
    EXPECT_NEAR(budget.stages[2].loaded, 570.4, 1.0);
    EXPECT_NEAR(budget.stages[3].loaded, 0.9486, 0.001);
}

/**
 * @brief And the budget is a composition, not a restatement.
 *
 * Stage 1 must be `ael::diffpair::mirrorGain` and stage 4 must be
 * `ael::follower::darlingtonGain`, to the last bit. A component that recomputes them from r_e has
 * put physics into the one place in the toolkit that is supposed to have none, and it will
 * disagree with the rest of the toolkit as soon as anything in L07 to L09 is corrected.
 */
TEST(Report, BudgetComposesTheEarlierComponents)
{
    // Swept rather than checked at one point. A restatement that is algebraically identical to
    // the component it replaces cannot be detected by any test and is not worth detecting; what
    // this catches is a restatement that is *nearly* right, which is the realistic failure --
    // r_e read from the tail current rather than from one side, a factor of two on the wrong
    // term, or beta left out of the Darlington.
    for (const double tail : {0.5e-3, 2.0e-3, 8.0e-3})
    {
        for (const double early : {50.0, 100.0, 200.0})
        {
            for (const double beta : {20.0, 50.0, 200.0})
            {
                auto value{design()};
                value.tailCurrent  = tail;
                value.earlyVoltage = early;
                value.beta         = beta;

                const auto budget{ael::report::budget(value)};
                const double load{(early / (tail / 2.0)) / 2.0};

#if __has_include("ael/diffpair/pair.hpp")
                EXPECT_NEAR(budget.stages[0].unloaded,
                            std::fabs(ael::diffpair::mirrorGain(tail, load)), 1.0e-9);
#endif
#if __has_include("ael/follower/stage.hpp")
                EXPECT_NEAR(budget.stages[3].loaded,
                            ael::follower::darlingtonGain(value.idleCurrent, value.load), 1.0e-9);
                EXPECT_NEAR(
                    budget.stages[1].loaded,
                    ael::follower::darlingtonGain(value.bufferCurrent, budget.stages[1].loadedBy),
                    1.0e-9);
#endif
                EXPECT_TRUE(std::isfinite(budget.stages[0].unloaded));
            }
        }
    }
}

/** @brief The open-loop gain is the product of the loaded gains and nothing else. */
TEST(Report, OpenLoopGainIsTheProduct)
{
    const auto budget{ael::report::budget(design())};
    double product{1.0};
    for (const auto& stage : budget.stages)
    {
        product *= stage.loaded;
    }

    EXPECT_NEAR(ael::report::openLoopGain(design()), product, 1.0e-6 * product);
    EXPECT_NEAR(ael::report::openLoopGain(design()), 986000.0, 5000.0);
}

/**
 * @brief Loading costs 11.5 dB, and the report has to be able to say so.
 *
 * The unloaded product is the two gain stages alone. A `budget` whose `loaded` and `unloaded`
 * fields are the same number has not modelled loading at all, which is the one thing this
 * lecture is about.
 */
TEST(Report, LoadingIsAccountedFor)
{
    const auto budget{ael::report::budget(design())};

    // The two *gain* stages, on their own. That is what "unloaded" means here: the followers
    // have no gain to be unloaded of, and including them would fold their 0.8 dB of signal loss
    // into a figure that is supposed to be about loading.
    const double unloaded{budget.stages[0].unloaded * budget.stages[2].unloaded};
    const double actual{ael::report::openLoopGain(design())};

    EXPECT_TRUE(unloaded > actual);
    EXPECT_NEAR(20.0 * std::log10(unloaded / actual), 11.5, 0.5);

    // And the largest single loss is stage 3, by a long way.
    EXPECT_TRUE((budget.stages[2].unloaded / budget.stages[2].loaded) > 3.0);
    EXPECT_TRUE((budget.stages[0].unloaded / budget.stages[0].loaded) < 1.1);
}

/** @brief Closing the loop, which is L04's expression applied to L10's amplifier. */
TEST(Report, ClosedLoopGain)
{
    EXPECT_NEAR(ael::report::closedLoopGain(design(), 1.0 / 20.0), 20.0, 0.001);
    EXPECT_TRUE(ael::report::closedLoopGain(design(), 1.0 / 20.0) < 20.0);

    // The error is two thousandths of a per cent, and it falls as the open-loop gain rises.
    const double error{100.0 * (20.0 - ael::report::closedLoopGain(design(), 1.0 / 20.0)) / 20.0};

    EXPECT_NEAR(error, 0.00203, 0.0003);
}

/**
 * @brief The closed loop does not care what beta is, and the open loop cares a great deal.
 *
 * The last assertion in the toolkit.
 */
TEST(Report, TheClosedLoopIsInsensitiveToBeta)
{
    auto weak{design()};
    weak.beta = 20.0;
    auto strong{design()};
    strong.beta = 200.0;

    const double openWeak{ael::report::openLoopGain(weak)};
    const double openStrong{ael::report::openLoopGain(strong)};

    EXPECT_TRUE((openStrong / openWeak) > 5.0);

    const double closedWeak{ael::report::closedLoopGain(weak, 1.0 / 20.0)};
    const double closedStrong{ael::report::closedLoopGain(strong, 1.0 / 20.0)};

    EXPECT_TRUE(std::fabs((closedStrong / closedWeak) - 1.0) < 1.0e-3);
}

/** @brief The formatted report names every stage and quotes every gain. */
TEST(Report, FormatIsUsable)
{
    const std::string text{ael::report::format(ael::report::budget(design()))};

    EXPECT_TRUE(text.size() > 100U);
    for (const auto& stage : ael::report::budget(design()).stages)
    {
        EXPECT_TRUE(text.find(stage.name) != std::string::npos);
    }
}

#endif
