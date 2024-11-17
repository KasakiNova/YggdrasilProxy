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
        """Create Tables（If not exists）"""
        cursor = self._get_cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            uuid TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            server INTEGER NOT NULL,
            baned INTEGER NOT NULL CHECK (baned IN (0, 1))
        )
        ''')
        self._get_connection().commit()


    def insert_account(self, uuid, name, server, ban=False):
        """Insert new account"""
        cursor = self._get_cursor()
        ban_value = 1 if ban else 0
        sql = "INSERT INTO accounts (uuid, name, server, baned) VALUES (?, ?, ?, ?)"
        cursor.execute(sql, (uuid, name, server, ban_value))
        self._get_connection().commit()


    def get_all_account(self):
        """Get all account"""
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM accounts")
        result = cursor.fetchone()
        return result is not None


    def get_user_by_uuid(self, uuid):
        """Query user by UUID"""
        cursor = self._get_cursor()
        sql = "SELECT * FROM accounts WHERE uuid = ?"
        cursor.execute(sql, uuid)
        result = cursor.fetchone()
        return result is not None


    def get_name_by_uuid(self, uuid, server):
        """Query user by UUID"""
        cursor = self._get_cursor()
        sql = "SELECT name FROM accounts WHERE uuid = ? AND server = ? LIMIT 1"
        cursor.execute(sql, (uuid, server))
        result = cursor.fetchone()
        return result[0] if result else None


    def get_baned_by_uuid(self, uuid, server):
        """Query ban by UUID and ServerId"""
        cursor = self._get_cursor()
        sql = "SELECT baned FROM accounts WHERE uuid = ? AND server = ?"
        cursor.execute(sql, (uuid, server))
        result = cursor.fetchone()
        return bool(result[0]) if result else None


    def update_account_name(self, uuid, new_name):
        """Update the account's name based on UUID"""
        cursor = self._get_cursor()
        sql = "UPDATE accounts SET name = ? WHERE uuid = ?"
        cursor.execute(sql, (new_name, uuid))
        self._get_connection().commit()


    def check_uuid_exists(self, user_uuid, server_id):
        """Check if a user with the given UUID exists in the database"""
        cursor = self._get_cursor()
        sql = "SELECT 1 FROM accounts WHERE uuid = ? AND server = ? LIMIT 1"
        cursor.execute(sql, (user_uuid, server_id))
        return cursor.fetchone() is not None


    def close(self):
        """Close the database connection for the current thread."""
        if hasattr(self.local, "connection"):
            self.local.connection.close()
            del self.local.connection