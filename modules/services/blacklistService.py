from modules.database.accountInfoDB import AccountInfoDB

class BlacklistService:
    def __init__(self):
        self.db_account = AccountInfoDB()

    def check_is_blacklisted(self, uuid, server):
        if self.db_account.get_baned_by_uuid(uuid, server):
            return True
        else:
            return False
