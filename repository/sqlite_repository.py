import sqlite3
import os

class SQLiteRepository:
    
    def __init__(self, db_path="sqlite/database.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.connection = sqlite3.connect(db_path)
        self.create_table()
        
    def create_table(self):
        """Create the file_index table if it doesn't exist."""
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS file_index (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                chroma_id TEXT NOT NULL
            );
        """)
        self.connection.commit()
        
    def insert_index(self, file_path, chroma_ids):
        """Insert a new index entry."""
        for chroma_id in chroma_ids:
            with self.connection:
                self.connection.execute(
                    "INSERT INTO file_index (file_path, chroma_id) VALUES (?, ?)",
                    (file_path, chroma_id)
                )

    def delete_by_file_path(self, file_path):
        """Delete index entries by file path and return the associated chroma_ids."""
        with self.connection:
            cursor = self.connection.execute(
                "SELECT chroma_id FROM file_index WHERE file_path = ?",
                (file_path,)
            )
            ids = [row[0] for row in cursor.fetchall()]

            self.connection.execute(
                "DELETE FROM file_index WHERE file_path = ?",
                (file_path,)
            )

        return ids
    
    def delete_all(self):
        """Delete all entries in the file_index table."""
        with self.connection:
            self.connection.execute("DELETE FROM file_index")
            self.connection.execute("DELETE FROM sqlite_sequence WHERE name='file_index'")
            self.connection.commit()

    def close(self):
        """Close the database connection."""
        self.connection.close()