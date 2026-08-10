/**
 * @brief Tests for the VCVS L03 adds to ael::net::Netlist.
 *
 * Dormant until `ael/net/netlist.hpp` gains it.
 */
#if __has_include("ael/net/netlist.hpp")

#include "ael/net/netlist.hpp"

#include "qacademy/test/test.hpp"

namespace
{
using ael::net::Netlist;
using ael::net::Node;
} // namespace

/** @brief A VCVS is counted like every other element kind, and mentions four nodes. */
TEST(NetlistVcvs, CountsAndNodes)
{
    Netlist netlist{};
    netlist.addVcvs(Node{3U}, ael::net::Ground, Node{1U}, Node{2U}, 1.0e5);

    EXPECT_EQ(netlist.vcvsCount(), std::size_t{1U});
    EXPECT_EQ(netlist.voltageSourceCount(), std::size_t{0U});
    EXPECT_EQ(netlist.nodeCount(), std::size_t{4U});
}

#endif
