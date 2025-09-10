import hashlib

def hash_key(key, m):
    """Hash key string -> integer in [0, 2^m)."""
    return int(hashlib.sha1(key.encode()).hexdigest(), 16) % (2**m)

class Node:
    def __init__(self, node_id, m):
        self.id = node_id
        self.m = m
        self.finger = [None] * m
        self.successor = None
        self.predecessor = None
        self.data = {}  # key->value store

    def __repr__(self):
        return f"Node({self.id})"

class Chord:
    def __init__(self, m):
        if m <= 0:
            raise ValueError("m must be > 0")
        self.m = m
        self.max_id = 2**m
        self.nodes = []

    def _check_id_valid(self, node_id):
        if not (0 <= node_id < self.max_id):
            raise ValueError(f"node_id must be in [0, {self.max_id - 1}]")

    def add_node(self, node_id):
        """Add a node and transfer keys for which it becomes successor."""
        self._check_id_valid(node_id)
        if any(n.id == node_id for n in self.nodes):
            print(f"Node {node_id} already exists. Skipping add.")
            return next(n for n in self.nodes if n.id == node_id)

        new_node = Node(node_id, self.m)
        self.nodes.append(new_node)
        self.nodes = sorted(self.nodes, key=lambda n: n.id)

        # update finger tables so find_successor works
        self.update_finger_tables()

        # Transfer keys from successor to new_node if new_node is the responsible successor
        succ = self.find_successor(node_id)
        if succ and succ != new_node:
            # keys whose hash k satisfy: new_node is first node >= k (mod space)
            keys_to_move = []
            for k in list(succ.data.keys()):
                kid = hash_key(k, self.m)
                # find successor of kid after insertion (already updated)
                responsible = self.find_successor(kid)
                if responsible.id == new_node.id:
                    keys_to_move.append(k)
            for k in keys_to_move:
                new_node.data[k] = succ.data.pop(k)

        # final update to ensure fingers/predecessors ok
        self.update_finger_tables()
        return new_node

    def remove_node(self, node_id):
        """Remove a node; transfer its data to its successor."""
        self._check_id_valid(node_id)
        node = next((n for n in self.nodes if n.id == node_id), None)
        if node is None:
            print(f"Node {node_id} not found.")
            return

        # find successor after removal: current successor is the recipient
        if node.successor and node.successor != node:
            node.successor.data.update(node.data)

        self.nodes.remove(node)
        if self.nodes:
            self.update_finger_tables()

    def find_successor(self, key):
        """Find successor node for integer key in [0, 2^m)."""
        if not self.nodes:
            return None
        for node in self.nodes:
            if node.id >= key:
                return node
        # wrap-around
        return self.nodes[0]

    def update_finger_tables(self):
        """Recompute finger table, successor, predecessor for all nodes."""
        if not self.nodes:
            return
        for node in self.nodes:
            for i in range(self.m):
                start = (node.id + 2**i) % self.max_id
                node.finger[i] = self.find_successor(start)
            node.successor = self.find_successor((node.id + 1) % self.max_id)
        # compute predecessor: node whose successor is this node and with closest id < node.id
        for node in self.nodes:
            preds = [n for n in self.nodes if n.successor == node and n != node]
            # choose the predecessor with largest id < node.id if any, else None
            node.predecessor = preds[-1] if preds else None

    def store(self, key, value):
        """Store key->value on the node responsible for hash(key)."""
        kid = hash_key(key, self.m)
        succ = self.find_successor(kid)
        if succ is None:
            print("No nodes in the ring. Store failed.")
            return
        succ.data[key] = value
        print(f"Stored key='{key}' (id={kid}) at Node {succ.id}")

    def lookup(self, key):
        """Return (value, node_id) or (None, node_id) if not present."""
        kid = hash_key(key, self.m)
        succ = self.find_successor(kid)
        if succ is None:
            return None, None
        return (succ.data.get(key, None), succ.id)

    def print_fingers(self):
        if not self.nodes:
            print("(no nodes)")
            return
        for node in self.nodes:
            finger_ids = [f.id if f is not None else None for f in node.finger]
            print(f"Node {node.id:>3}: succ={node.successor.id if node.successor else None:>3}, pred={node.predecessor.id if node.predecessor else None:>3}, fingers={finger_ids}")

    def print_data(self):
        if not self.nodes:
            print("(no nodes)")
            return
        for node in self.nodes:
            print(f"Node {node.id:>3} data: {node.data}")

# -------------------------
# Test case thực nghiệm
# -------------------------
if __name__ == "__main__":
    # Thời gian làm bài (theo đề): 13:10 - 15:40 -> bạn sẽ ghi vào báo cáo
    chord = Chord(m=5)  # không gian 0..31

    # Thêm các node ban đầu (IDs phải nằm trong [0..31])
    initial_nodes = [1, 5, 9, 12, 16]
    for nid in initial_nodes:
        chord.add_node(nid)

    print("Finger tables ban đầu:")
    chord.print_fingers()

    # Lưu dữ liệu
    chord.store("user1", "Alice")
    chord.store("user2", "Bob")
    chord.store("fileA", "data123")

    print("\nDữ liệu đang lưu:")
    chord.print_data()

    # Tra cứu dữ liệu
    val, node_id = chord.lookup("user1")
    print(f"\nLookup 'user1' → Node {node_id}, value = {val}")

    val, node_id = chord.lookup("fileA")
    print(f"Lookup 'fileA' → Node {node_id}, value = {val}")

    # Thêm node mới (7)
    print("\nThêm node 7:")
    chord.add_node(7)
    chord.print_fingers()
    chord.print_data()

    # Xóa node 5
    print("\nXóa node 5:")
    chord.remove_node(5)
    chord.print_fingers()
    chord.print_data()
