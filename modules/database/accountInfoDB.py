# coding=utf-8
import sqlite3
import threading
import modules.globalVariables as gVar

class AccountInfoDB:
    def __init__(self):
        self._db_path = gVar.accountsInfoDB
        self.local = threading.local()
        self.create_table()


    def _get_connection(self):
        if not hasattr(self.local, "connection"):
            self.local.connection = sqlite3.connect(self._db_path)
        return self.local.connection


    def _get_cursor(self):
        conn = self._get_connection()
        return conn.cursor()


    def create_table(self):
        """Create Tables (If not exists)"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                uuid TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                server INTEGER NOT NULL,
                baned INTEGER NOT NULL CHECK (baned IN (0, 1))
            )
            ''')
            conn.commit()


    def insert_account(self, uuid, name, server, ban=False):
        """Insert new account"""
        ban_value = 1 if ban else 0
        sql = "INSERT INTO accounts (uuid, name, server, baned) VALUES (?, ?, ?, ?)"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (uuid, name, server, ban_value))


    def get_all_account(self):
        """Get all accounts"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM accounts")
            return cursor.fetchall()

    def get_user_by_uuid(self, uuid):
        """Query user by UUID"""
        sql = "SELECT * FROM accounts WHERE uuid = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (uuid,))
            return cursor.fetchone()

    def get_account_by_name(self, name):
        """Query account by name"""
        sql = "SELECT * FROM accounts WHERE name = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (name,))
            return cursor.fetchall()

    def get_name_by_uuid(self, uuid, server):
        """Query user by UUID"""
        sql = "SELECT name FROM accounts WHERE uuid = ? AND server = ? LIMIT 1"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (uuid, server))
            result = cursor.fetchone()
            return result[0] if result else None

    def get_baned_by_uuid(self, uuid, server):
        """Query ban by UUID and ServerId"""
        sql = "SELECT baned FROM accounts WHERE uuid = ? AND server = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (uuid, server))
            result = cursor.fetchone()
            return bool(result[0]) if result else None

    def update_account_name(self, uuid, new_name):
        """Update the account's name based on UUID"""
        sql = "UPDATE accounts SET name = ? WHERE uuid = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (new_name, uuid))

    def ban_account(self, uuid, server):
        """Ban the account"""
        sql = "UPDATE accounts SET baned = ? WHERE uuid = ? AND server = ?"
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (1, uuid, server))
            return True
        except sqlite3.Error:
            return False
        finally:
            self.close()

    def check_uuid_exists(self, user_uuid, server_id):
        """Check if a user with the given UUID exists in the database"""
        sql = "SELECT * FROM accounts WHERE uuid = ? AND server = ? LIMIT 1"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (user_uuid, server_id))
            return cursor.fetchone() is not None

    def close(self):
        """Close the database connection for the current thread."""
        if hasattr(self.local, "connection"):
            self.local.connection.close()
            del self.local.connection
