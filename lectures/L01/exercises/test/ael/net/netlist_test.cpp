/**
 * @brief Tests for ael::net::Netlist, the container every later component is handed.
 *
 * Dormant until `ael/net/netlist.hpp` exists. See ../../README.md.
 *
 * A netlist is not an interesting class and it is not meant to be. What it is meant to be is
 * unambiguous: two sign conventions and a node numbering, fixed once, in L01, because every
 * component in the rest of the course reads them and a change here in L07 would be a change to
 * ten lectures.
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
 * @brief Node zero is ground, and it is a constant rather than a convention to remember.
 */
TEST(Netlist, GroundIsNodeZero) { EXPECT_EQ(ael::net::Ground, Node{0U}); }

/**
 * @brief An empty netlist has one node, because ground always exists.
 *
 * The alternative, an empty netlist with zero nodes, makes `nodeCount()` mean two different
 * things depending on whether anything has been added yet.
 */
TEST(Netlist, EmptyHasGroundOnly)
{
    const Netlist netlist{};

    EXPECT_EQ(netlist.nodeCount(), std::size_t{1U});
    EXPECT_EQ(netlist.resistorCount(), std::size_t{0U});
    EXPECT_EQ(netlist.voltageSourceCount(), std::size_t{0U});
    EXPECT_EQ(netlist.currentSourceCount(), std::size_t{0U});
}

/**
 * @brief The node count is the highest index used plus one, ground included.
 *
 * Nodes are not declared, they are mentioned. A netlist that required them to be declared first
 * would put a bookkeeping step in front of every exercise in the course.
 */
TEST(Netlist, NodeCountFollowsTheHighestIndexUsed)
{
    Netlist netlist{};
    netlist.addResistor(Node{1U}, ael::net::Ground, 1.0e3);

    EXPECT_EQ(netlist.nodeCount(), std::size_t{2U});

    netlist.addResistor(Node{4U}, Node{1U}, 2.2e3);

    EXPECT_EQ(netlist.nodeCount(), std::size_t{5U});
}

/**
 * @brief Elements are counted by kind, and each kind is counted independently.
 */
TEST(Netlist, CountsEachKindSeparately)
{
    Netlist netlist{};
    netlist.addResistor(Node{1U}, ael::net::Ground, 1.0e3);
    netlist.addResistor(Node{2U}, Node{1U}, 1.0e3);
    netlist.addVoltageSource(Node{2U}, ael::net::Ground, 5.0);
    netlist.addCurrentSource(ael::net::Ground, Node{1U}, 1.0e-3);

    EXPECT_EQ(netlist.resistorCount(), std::size_t{2U});
    EXPECT_EQ(netlist.voltageSourceCount(), std::size_t{1U});
    EXPECT_EQ(netlist.currentSourceCount(), std::size_t{1U});
    EXPECT_EQ(netlist.nodeCount(), std::size_t{3U});
}

#endif
