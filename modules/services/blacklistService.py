from modules.database.accountInfoDB import AccountInfoDB

class BlacklistService:
    def __init__(self):
        self.db_account = AccountInfoDB()

    def check_is_blacklisted(self, uuid, server):
        if self.db_account.get_baned_by_uuid(uuid, server):
            return True
        else:
            return False

    def add_ban_account(self, name):
        account_in_db = self.db_account.get_account_by_name(name.lower())
        account = account_in_db[0]
        if len(account_in_db) == 1:
            uuid = account[0]
            server_id = account[2]
            if account[3] == 0:
                return {'msg': "Success"} if self.db_account.ban_account(uuid,server_id) else {'msg': "SetError"}
            else:
                return {'msg': "isBaned"}
        elif len(account_in_db) > 1:
            return {'msg': "sameName", 'data': account_in_db}
        else:
            return {'msg': "Error"}