import csv


class Node:
    def __init__(self, id):
        self.id = id
        self.parents = []
        self.children = []
        self.additional_properties = {}

    def __setitem__(self, key, value):
        self.additional_properties[key] = value

    def __getitem__(self, key):
        if key in self.additional_properties:
            return self.additional_properties[key]
        return None

    def add_parent(self, node):
        self.parents.append(node)

    def add_child(self, node):
        self.children.append(node)


class Graph:
    def __init__(self, relationships=None):
        self.nodes = {}

        if relationships:
            for r in relationships:
                self.add_relationship(r)

    def add_relationship(self, r):
        pre, suc = r[0], r[1]
        pre_node, suc_node = None, None

        if pre not in self.nodes:
            pre_node = Node(pre)
            self.nodes[pre] = pre_node
        else:
            pre_node = self.nodes[pre]

        if suc not in self.nodes:
            suc_node = Node(suc)
            self.nodes[suc] = suc_node
        else:
            suc_node = self.nodes[suc]

        self.nodes[pre].add_child(suc_node)
        self.nodes[suc].add_parent(pre_node)

    def add_property(self, property_name, id_properties):
        for id, property in id_properties.items():
            if id in self.nodes:
                self.nodes[id][property_name] = property

    def find_by(self, pred):
        nodes = list(filter(pred, self.nodes.values()))
        return [n.id for n in nodes]

    def delete_by(self, pred):
        ids = self.find_by(pred)
        for id in ids:
            self.delete_node(id)

    def delete_node(self, name):
        if name not in self.nodes:
            return

        node = self.nodes[name]

        if node.children:
            for child in node.children:
                child.parents.remove(node)
                if node.parents:
                    for p in node.parents:
                        if p not in child.parents:
                            child.parents.append(p)

        if node.parents:
            for parent in node.parents:
                parent.children.remove(node)
                if node.children:
                    for c in node.children:
                        if c not in parent.children:
                            parent.children.append(c)

        del self.nodes[name]

    def write_csv(self, path):
        with open(path, "w", encoding="UTF8") as f:
            writer = csv.writer(f)

            writer.writerow(["parent_id", "child_id"])

            for parent_id, child_id in self.parent_child_pairs():
                writer.writerow([parent_id, child_id])

    def parent_child_pairs(self):
        relationships = []
        for n in self.nodes.values():
            if n.children:
                for c in n.children:
                    relationships.append((n.id, c.id))

        return relationships

    def print(self, additional_properties=[]):
        root_nodes = [n for n in self.nodes.values() if not n.parents]
        for n in root_nodes:
            Graph.print_node_line(n, 0, additional_properties)
            Graph.print_node(n, 1, additional_properties)

    def print_node(node, index, additional_properties=[]):
        for n in node.children:
            Graph.print_node_line(n, index, additional_properties)
            Graph.print_node(n, index + 1)

    def print_node_line(n, index, additional_properties):
        print("\t" * index + n.id, [n[p] for p in additional_properties] or "")
