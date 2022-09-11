# prop-graph
A graph structure that can take arbitrary properties.

## Usage

In the examples that follow, I'll be working with a graph that looks as follows:

```
                a                               g
            /       \                       /       \
        b               c               h               i
    /       \       /       \       /
d               e               f
```

### Build graph

``` python
graph = Graph([
    ("a", "b"),
    ("a", "c"),
    ("b", "d"),
    ("b", "e"),
    ("c", "e"),
    ("c", "f"),
    ("g", "h"),
    ("g", "i"),
    ("h", "f"),
])

graph.print()
# a 
#         b 
#                 d 
#                 e 
#         c 
#                 e 
#                 f 
# g 
#         h 
#                 f 
#         i
```

### Add properties

``` python
props = {
    "c": "interesting",
    "g": "interesting",
}
graph.add_property("type", props)
```

### Finding nodes

``` python
parent_ids = graph.find_by(lambda n: len(n.children) > 0)
print(parent_ids)
# ['a', 'b', 'c', 'g', 'h']

root_ids = graph.find_by(lambda n: len(n.parents) == 0)
print(root_ids)
# ['a', 'g']

interesting_ids = graph.find_by(lambda n: n["type"] == "interesting")
print(interesting_ids)
# ['c', 'g']
```

### Deleting nodes

``` python
graph.delete_by(lambda n: n["type"] == "interesting")
graph.print()
# a 
#         b 
#                 d 
#                 e 
#         e 
#         f 
# h 
#         f 
# i
```