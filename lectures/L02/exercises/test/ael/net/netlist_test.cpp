/**
 * @brief Tests for the reactive elements L02 adds to ael::net::Netlist.
 *
 * Dormant until `ael/net/netlist.hpp` gains them. L01's own netlist tests still ship in L01's
 * suite and still have to pass; nothing here replaces them.
 */
#if __has_include("ael/net/netlist.hpp")

#include "ael/net/netlist.hpp"

#include "qacademy/test/test.hpp"

namespace
{
using ael::net::Netlist;
using ael::net::Node;
} // namespace

/**
 * @brief Capacitors and inductors are counted like every other element kind.
 */
TEST(NetlistReactive, CountsCapacitorsAndInductors)
{
    Netlist netlist{};
    netlist.addCapacitor(Node{1U}, ael::net::Ground, 100.0e-9);
    netlist.addCapacitor(Node{2U}, Node{1U}, 10.0e-9);
    netlist.addInductor(Node{2U}, ael::net::Ground, 10.0e-3);

    EXPECT_EQ(netlist.capacitorCount(), std::size_t{2U});
    EXPECT_EQ(netlist.inductorCount(), std::size_t{1U});
    EXPECT_EQ(netlist.resistorCount(), std::size_t{0U});
}

/**
 * @brief A reactive element mentions nodes like any other, so the node count follows it.
 */
TEST(NetlistReactive, ReactiveElementsExtendTheNodeCount)
{
    Netlist netlist{};
    netlist.addCapacitor(Node{4U}, ael::net::Ground, 1.0e-6);

    EXPECT_EQ(netlist.nodeCount(), std::size_t{5U});
}

#endif
