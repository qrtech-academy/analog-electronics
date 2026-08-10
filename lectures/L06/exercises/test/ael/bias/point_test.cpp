/**
 * @brief Tests for ael::bias, the quiescent point and the drift results.
 *
 * Dormant until `ael/bias/point.hpp` exists.
 */
#if __has_include("ael/bias/point.hpp")

#include "ael/bias/point.hpp"

#include "qacademy/test/test.hpp"

#include <cmath>

namespace
{
constexpr double Supply{10.0};
constexpr double Upper{33.0e3};
constexpr double Lower{6.8e3};
constexpr double Emitter{1.0e3};
constexpr double Collector{4.7e3};
constexpr double Beta{50.0};
} // namespace

/**
 * @brief The quiescent point includes the base current's droop, so it is not the naive answer.
 *
 * 0.93 mA, not the 1.06 mA the unloaded divider suggests. A `quiescentPoint` that returns 1.06
 * has ignored the base current, which is the defect this test exists for.
 */
TEST(Bias, QuiescentPointAccountsForBaseCurrent)
{
    const auto point{ael::bias::quiescentPoint(Supply, Upper, Lower, Emitter, Collector)};

    EXPECT_TRUE(std::isfinite(point.collectorCurrent));
    EXPECT_NEAR(point.collectorCurrent, 0.934e-3, 0.02e-3);
    EXPECT_NEAR(point.baseVoltage, 1.60, 0.02);

    // The naive answer, which this must not be.
    EXPECT_TRUE(point.collectorCurrent < 1.0e-3);
}

/**
 * @brief The emitter sits one drop below the base, and the collector where the load line says.
 *
 * The emitter resistor carries the *emitter* current, which is (beta + 1)/beta times the collector
 * current. At beta = 50 that is two per cent, or 19 mV here, so it is not something this test can
 * round away: an implementation that puts I_C through the emitter resistor lands 18.7 mV out.
 * Appendix A.3 keeps the term, because the base current it comes from is the section's whole
 * subject.
 */
TEST(Bias, TheThreeVoltagesAreConsistent)
{
    const auto point{ael::bias::quiescentPoint(Supply, Upper, Lower, Emitter, Collector)};

    const double emitterCurrent{point.collectorCurrent * (Beta + 1.0) / Beta};

    EXPECT_NEAR(point.emitterVoltage, emitterCurrent * Emitter, 1.0e-4);
    EXPECT_NEAR(point.baseVoltage - point.emitterVoltage, 0.65, 0.01);
    EXPECT_NEAR(point.collectorVoltage, Supply - (point.collectorCurrent * Collector), 1.0e-6);
}

/** @brief A stiffer divider moves the answer towards the naive one. */
TEST(Bias, StiffnessReducesTheError)
{
    const auto soft{ael::bias::quiescentPoint(Supply, Upper, Lower, Emitter, Collector)};
    const auto stiff{
        ael::bias::quiescentPoint(Supply, Upper / 10.0, Lower / 10.0, Emitter, Collector)};

    EXPECT_TRUE(ael::bias::stiffness(Supply, Upper / 10.0, Lower / 10.0, stiff.collectorCurrent) >
                ael::bias::stiffness(Supply, Upper, Lower, soft.collectorCurrent));

    // And the stiffer one sits closer to the unloaded prediction.
    const double naive{(((Supply * Lower) / (Upper + Lower)) - 0.65) / Emitter};
    EXPECT_TRUE(std::fabs(stiff.collectorCurrent - naive) <
                std::fabs(soft.collectorCurrent - naive));
}

/** @brief The stiffness of the worked stage is about 13.4, and the rule of thumb is ten. */
TEST(Bias, StiffnessOfTheWorkedStage)
{
    EXPECT_NEAR(ael::bias::stiffness(Supply, Upper, Lower, 0.934e-3), 13.4, 0.5);
}

/**
 * @brief Drift suppression is the emitter factor, which is why the stability costs gain.
 */
TEST(Bias, SuppressionIsTheEmitterFactor)
{
    constexpr double current{1.0e-3};
    constexpr double emitter{1.0e3};

    const double suppression{ael::bias::driftSuppression(current, emitter)};
    const double re{0.026 / current};
    const double emitterFactor{(re + emitter) / re};

    EXPECT_NEAR(suppression, emitterFactor, emitterFactor * 0.05);
    EXPECT_TRUE(ael::bias::driftWithoutDegeneration() >
                ael::bias::driftWithDegeneration(current, emitter) * 30.0);
}

/** @brief The 220 mV rule, and the E12 value it lands on. */
TEST(Bias, DegenerationResistorFromTheRule)
{
    EXPECT_NEAR(ael::bias::degenerationResistor(1.0e-3), 220.0, 1.0e-9);
    EXPECT_NEAR(ael::bias::degenerationResistor(1.0e-2), 22.0, 1.0e-9);
    EXPECT_NEAR(ael::bias::degenerationResistor(2.0e-3, 0.220), 110.0, 1.0e-9);
}

#endif
