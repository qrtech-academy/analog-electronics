/**
 * @brief Tests for ael::device::mosfet, the square law.
 *
 * Dormant until `ael/device/mosfet.hpp` exists.
 */
#if __has_include("ael/device/mosfet.hpp")

#include "ael/device/mosfet.hpp"

#include "qacademy/test/test.hpp"

#include <cmath>

namespace
{
using ael::device::mosfet::Parameters;
using ael::device::mosfet::Region;
} // namespace

/** @brief Below threshold there is no channel and no current. */
TEST(Mosfet, CutoffBelowThreshold)
{
    const Parameters parameters{};

    EXPECT_NEAR(ael::device::mosfet::drainCurrent(parameters.threshold - 0.1, 5.0, parameters), 0.0,
                1.0e-15);
    EXPECT_TRUE(ael::device::mosfet::region(0.0, 5.0, parameters) == Region::Cutoff);
}

/** @brief In saturation the current is half k times the overdrive squared, and flat in Vds. */
TEST(Mosfet, SaturationIsFlatAndSquareLaw)
{
    const Parameters parameters{};
    const double overdrive{0.5};
    const double vgs{parameters.threshold + overdrive};
    const double expected{0.5 * parameters.transconductanceParameter * overdrive * overdrive};

    EXPECT_NEAR(ael::device::mosfet::drainCurrent(vgs, 5.0, parameters), expected, 1.0e-12);

    // Flat: doubling Vds well into saturation changes nothing.
    EXPECT_NEAR(ael::device::mosfet::drainCurrent(vgs, 10.0, parameters),
                ael::device::mosfet::drainCurrent(vgs, 5.0, parameters), 1.0e-15);
}

/** @brief The two regions meet without a step where Vds equals the overdrive. */
TEST(Mosfet, RegionsMeetContinuously)
{
    const Parameters parameters{};
    const double overdrive{0.5};
    const double vgs{parameters.threshold + overdrive};

    const double justBelow{ael::device::mosfet::drainCurrent(vgs, overdrive - 1.0e-9, parameters)};
    const double justAbove{ael::device::mosfet::drainCurrent(vgs, overdrive + 1.0e-9, parameters)};

    EXPECT_NEAR(justBelow, justAbove, 1.0e-9);
    EXPECT_TRUE(ael::device::mosfet::region(vgs, overdrive / 2.0, parameters) == Region::Triode);
    EXPECT_TRUE(ael::device::mosfet::region(vgs, overdrive * 2.0, parameters) ==
                Region::Saturation);
}

/**
 * @brief The transconductance goes as the square root of current: 4 mS at 1 mA.
 *
 * Against a BJT's 38.5 mS at the same current, which is the factor of ten the whole MOSFET half
 * of the course turns on.
 */
TEST(Mosfet, TransconductanceGoesAsSquareRootOfCurrent)
{
    const Parameters parameters{};

    EXPECT_NEAR(ael::device::mosfet::transconductance(1.0e-3, parameters), 4.0e-3, 1.0e-9);

    // Four times the current is twice the transconductance.
    EXPECT_NEAR(ael::device::mosfet::transconductance(4.0e-3, parameters) /
                    ael::device::mosfet::transconductance(1.0e-3, parameters),
                2.0, 1.0e-9);
}

#endif
