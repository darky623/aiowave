import sqlite3

db_path = "db.db"


class DatabaseConnection:
    def __init__(self):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)

    def execute_query(self, query, params=None):
        with self.conn:
            cur = self.conn.cursor()
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            data = cur.fetchall()
        return data

    def create(self, table, params, values):
        query = f"INSERT INTO {table} {params} VALUES {str(values)}"
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(query)
            last_inserted_id = cur.lastrowid

        return last_inserted_id

    def update(self, table, item_id, update_params):
        query = f"UPDATE {table} SET "

        set_statements = []
        values = []

        for param, new_value in update_params.items():
            set_statements.append(f"{param}=?")
            values.append(new_value)

        query += ", ".join(set_statements)
        query += " WHERE id=?"

        values.append(item_id)

        self.execute_query(query, tuple(values))

    def delete(self, table, item_id):
        query = f"DELETE FROM {table} WHERE id=?"
        self.execute_query(query, (item_id,))

    def read(self, table, params):
        query = f"SELECT * FROM {table} WHERE "
        conditions = []

        for param, value in params.items():
            conditions.append(f"{param}=?")

        query += " AND ".join(conditions)

        result = []
        rows = self.execute_query(query, tuple(params.values()))
        columns = [column[0] for column in self.conn.cursor().description]

        for row in rows:
            row_dict = dict(zip(columns, row))
            result.append(row_dict)

        return result
