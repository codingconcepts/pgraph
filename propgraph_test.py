from propgraph import Graph


def test_graph_init():
    graph = build_graph(["a", "e", "f", "i"], "x", "y")

    # Assert parent-child relationships.
    assert len(graph.nodes) == 10

    assert graph.nodes["a"].id == "a"
    assert [n.id for n in graph.nodes["a"].parents] == []
    assert [n.id for n in graph.nodes["a"].children] == ["b", "c", "d"]

    assert graph.nodes["b"].id == "b"
    assert [n.id for n in graph.nodes["b"].parents] == ["a"]
    assert [n.id for n in graph.nodes["b"].children] == ["e"]

    assert graph.nodes["c"].id == "c"
    assert [n.id for n in graph.nodes["c"].parents] == ["a"]
    assert [n.id for n in graph.nodes["c"].children] == ["e"]

    assert graph.nodes["d"].id == "d"
    assert [n.id for n in graph.nodes["d"].parents] == ["a"]
    assert [n.id for n in graph.nodes["d"].children] == ["e"]

    assert graph.nodes["e"].id == "e"
    assert [n.id for n in graph.nodes["e"].parents] == ["b", "c", "d"]
    assert [n.id for n in graph.nodes["e"].children] == ["f", "g"]

    assert graph.nodes["f"].id == "f"
    assert [n.id for n in graph.nodes["f"].parents] == ["e"]
    assert [n.id for n in graph.nodes["f"].children] == ["h"]

    assert graph.nodes["g"].id == "g"
    assert [n.id for n in graph.nodes["g"].parents] == ["e"]
    assert [n.id for n in graph.nodes["g"].children] == ["i"]

    assert graph.nodes["h"].id == "h"
    assert [n.id for n in graph.nodes["h"].parents] == ["f"]
    assert [n.id for n in graph.nodes["h"].children] == ["j"]

    assert graph.nodes["i"].id == "i"
    assert [n.id for n in graph.nodes["i"].parents] == ["g"]
    assert [n.id for n in graph.nodes["i"].children] == ["j"]

    assert graph.nodes["j"].id == "j"
    assert [n.id for n in graph.nodes["j"].parents] == ["h", "i"]
    assert [n.id for n in graph.nodes["j"].children] == []


def test_graph_properties():
    graph = build_graph(["a", "e", "f", "i"], "x", "y")

    # Assert properties.
    assert graph.nodes["a"]["x"] == "y"
    assert graph.nodes["e"]["x"] == "y"
    assert graph.nodes["f"]["x"] == "y"
    assert graph.nodes["i"]["x"] == "y"


def test_graph_delete_by():
    graph = build_graph(["a", "e", "f", "i"], "x", "y")

    # Remove non-prop nodes.
    graph.delete_by(lambda n: n["x"] != "y")

    assert len(graph.nodes) == 4
    assert [n for n in graph.nodes] == ["a", "e", "f", "i"]


#     b     f - h
#   /   \  /     \
# a - c - e       j
#   \   /  \     /
#     d     g - i
def build_graph(prop_nodes, prop_name, prop_value):
    graph = Graph([
        ("a", "b"),
        ("a", "c"),
        ("a", "d"),
        ("b", "e"),
        ("c", "e"),
        ("d", "e"),
        ("e", "f"),
        ("e", "g"),
        ("f", "h"),
        ("g", "i"),
        ("h", "j"),
        ("i", "j"),
    ])

    props = dict([(n, prop_value) for n in prop_nodes])
    graph.add_property(prop_name, props)

    return graph
