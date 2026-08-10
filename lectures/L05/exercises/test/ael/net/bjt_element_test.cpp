/**
 * @brief Tests for the BJT L05 adds to ael::net::Netlist.
 */
#if __has_include("ael/net/netlist.hpp") && __has_include("ael/device/bjt.hpp")

#include "ael/device/bjt.hpp"
#include "ael/net/netlist.hpp"

#include "qacademy/test/test.hpp"

/** @brief A BJT is counted like every other element kind, and mentions three nodes. */
TEST(NetlistBjt, Counts)
{
    ael::net::Netlist netlist{};
    netlist.addBjt(ael::net::Node{3U}, ael::net::Node{2U}, ael::net::Ground,
                   ael::device::bjt::Parameters{});

    EXPECT_EQ(netlist.bjtCount(), std::size_t{1U});
    EXPECT_EQ(netlist.nodeCount(), std::size_t{4U});
}

#endif
