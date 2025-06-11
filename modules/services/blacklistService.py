# coding=utf-8
import modules.globalVariables as gVar

from modules.database.accountInfoDB import AccountInfoDB

class BlacklistService:
    def __init__(self):
        self.db_account = AccountInfoDB()
        self._server_info = gVar.cfgContext['Server']

    def check_is_blacklisted(self, uuid, server):
        if self.db_account.get_baned_by_uuid(uuid, server):
            return True
        else:
            return False

    def set_account_status(self, name, status: int):
        """Set account status, 1 is baned, 0 is unbanned"""
        account_in_db = self.db_account.get_account_by_name(name.lower())
        account_in_db.set_status(status)
        account = account_in_db[0]
        if len(account_in_db) == 1:
            uuid = account[0]
            server_id = account[2]
            if account[3] == 0:
                return {'msg': "Success"} if self.db_account.set_account_baned(uuid, server_id, status) else {'msg': "SetError"}
            else:
                return {'msg': "isBanedOrUnbanned"}
        elif len(account_in_db) > 1:
            return {'msg': "sameName", 'data': account_in_db}
        else:
            return {'msg': "Error"}

    def same_name_ban_account(self, data, server_name):
        uuid, srv_id, baned = self._find_uuid_and_server_id(data, server_name)
        if (uuid is not None and
                srv_id is not None and
                baned is not None):
            if baned == 0:
                success = self.db_account.set_account_baned(uuid, srv_id, 1)
                return {'msg': "Success"} if success else {'msg': "SetError"}
            else:
                return {'msg': "isBaned"}
        else:
            return {'msg': "Error"}

    def _find_uuid_and_server_id(self, data, server_name):
        """Find UUID and server ID by server name."""
        # Iterate through the server information to find the server ID that matches the provided server name
        for server_id, attributes in self._server_info.items():
            if attributes.get('Name').lower() == server_name.lower():  # Compare server name in a case-insensitive manner
                # Once the server ID is found, search for the corresponding UUID in the data list
                for entry in data:
                    uuid_d, _, sid, baned = entry  # Unpack the tuple to get the UUID, server ID and Ban Status
                    if str(sid) == str(server_id):  # Ensure both IDs are compared as strings
                        return uuid_d, sid, baned  # Return the found UUID and server ID
        return None, None, None  # If no match is found, return None
