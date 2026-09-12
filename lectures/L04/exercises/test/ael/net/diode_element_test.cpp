/**
 * @brief Tests for the diode L04 adds to ael::net::Netlist.
 */
#if __has_include("ael/net/netlist.hpp")

#include "ael/net/netlist.hpp"

#include "qacademy/test/test.hpp"

/** @brief A diode is counted like every other element kind. */
TEST(NetlistDiode, Counts)
{
    ael::net::Netlist netlist{};
    netlist.addDiode(ael::net::Node{1U}, ael::net::Ground, 1.0e-14);

    EXPECT_EQ(netlist.diodeCount(), std::size_t{1U});
    EXPECT_EQ(netlist.resistorCount(), std::size_t{0U});
    EXPECT_EQ(netlist.nodeCount(), std::size_t{2U});
}

#endif
