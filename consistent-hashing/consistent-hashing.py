import hashlib
import bisect

class ConsistentHashing:
    def __init__(self, servers, num_replicas=1):
        """
        Initialize the consistent hashing ring.

        - servers: List of initial server names (e.g. ["server1", "server2", "server3"])
        - num_replicas: number of virtual nodes per server for better load balancing
        """
        self.num_replicas = num_replicas # number of virtual nodes per server
        self.ring = {} # Hash ring storing virtual nodes maping
        self.sorted_keys = [] # Sorted list of has values (positions) in the ring
        self.server = set() # Set of physical server (used for tracking)

        for server in servers:
            self.add_server(server)

    def _hash(self, key):
        """Computes hash value for given key."""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
        
    def add_server(self, server):
        """
        Addd a server to the hash ring aling with its virtual nodes.
            
        - Each vurtual node is a different hash of the server id to distribute load 
        - The server is hashed multiple time and placed at different positions
        """
        self.server.add(server)
        for i in range(self.num_replicas):
            virtual_node = f"{server}-{i}"
            hash_val = self._hash(virtual_node)
            self.ring[hash_val] = server
            bisect.insort(self.sorted_keys, hash_val)

    def remove_server(self, server):
        """ Remove a server and all its virtual nodes from the hash ring."""
        if server in self.server:
            self.server.remove(server)
            for i in range(self.num_replicas):
                virtual_node = f"{server}-{i}"
                hash_val = self._hash(virtual_node)
                self.ring.pop(hash_val, None)
                self.sorted_keys.remove(hash_val)

    def get_server(self, key):
        """
        Finds the closest server for a given key.

        - Hash the key to get its position on the ring.
        - Move clockwise to find the nearest server.
        - If it exceeds the last node, wrap around to the first node.
        """
        if not self.ring:
            return None  # No servers available
            
        hash_val = self._hash(key)  # Hash the key
        index = bisect.bisect(self.sorted_keys, hash_val) % len(self.sorted_keys)  # Locate nearest server
        return self.ring[self.sorted_keys[index]]  # Return the assigned server

# ----------------- Usage Example -------------------

# Step 1: Initialize Consistent Hashing with servers
servers = ["S0", "S1", "S2"]
ch = ConsistentHashing(servers)

print(ch.ring)
print(ch.sorted_keys)
print(ch.server)

# Step 2: Assign requests (keys) to servers
print(ch.get_server("UserA"))  # Maps UserA to a server
print(ch.get_server("UserB"))  # Maps UserB to a server

# Step 3: Add a new server dynamically
ch.add_server("S6")
print(ch.get_server("UserA"))  # Might be reassigned if affected

# Step 4: Remove a server dynamically
ch.remove_server("S2")
print(ch.get_server("UserB"))  # Might be reassigned if affected