from cassandra.cluster import Cluster

class CassandraCRUD:
    def __init__(self, keyspace, table):
        self.cluster = Cluster(['localhost'])
        self.session = self.cluster.connect()
        self.keyspace = keyspace
        self.table = table
        self._create_keyspace()
        self._create_table()

    def _create_keyspace(self):
        self.session.execute(f"CREATE KEYSPACE IF NOT EXISTS {self.keyspace} WITH REPLICATION = {{ 'class' : 'SimpleStrategy', 'replication_factor' : 1 }}")
        self.session.set_keyspace(self.keyspace)

    def _create_table(self):
        self.session.execute(f"CREATE TABLE IF NOT EXISTS {self.table} (id UUID PRIMARY KEY, name TEXT, age INT)")

    def create(self, id, name, age):
        query = f"INSERT INTO {self.table} (id, name, age) VALUES (%s, %s, %s)"
        self.session.execute(query, (id, name, age))

    def read(self, id):
        query = f"SELECT * FROM {self.table} WHERE id = %s"
        return self.session.execute(query, (id,)).one()

    def update(self, id, name, age):
        query = f"UPDATE {self.table} SET name = %s, age = %s WHERE id = %s"
        self.session.execute(query, (name, age, id))

    def delete(self, id):
        query = f"DELETE FROM {self.table} WHERE id = %s"
        self.session.execute(query, (id,))

    def close(self):
        self.cluster.shutdown()

if __name__ == "__main__":
    import uuid

    crud = CassandraCRUD("example_keyspace", "users")

    # Create
    user_id = uuid.uuid4()
    crud.create(user_id, "John Doe", 30)
    print("User created")

    # Read
    user = crud.read(user_id)
    print(f"Read user: {user}")

    # Update
    crud.update(user_id, "John Doe", 31)
    print("User updated")

    # Read again to verify update
    user = crud.read(user_id)
    print(f"Updated user: {user}")

    # Delete
    crud.delete(user_id)
    print("User deleted")

    # Try to read the deleted user
    user = crud.read(user_id)
    print(f"Deleted user: {user}")

    crud.close()