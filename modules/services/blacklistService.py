import os.path
import ujson

import modules.globalVariables as gVar


class BlacklistService:
    def __init__(self, filename):
        self._web_dir = gVar.webDir
        self._filepath = os.path.join(gVar.webDir, filename)
        self._blacklist = self.init_list()
        print(self._blacklist)


    def init_list(self) -> dict:
        try:
            with open(self._filepath, 'r') as file:
                data = ujson.load(file)
                file.close()
                return data
            pass
        except FileNotFoundError:
            # If blackListFile not exists, just create it (Just do it!)
            with open(self._filepath, 'w') as file:
                file.write('{}')
                file.close()
                return {}
        except ujson.JSONDecodeError:
            # If ujson cannot read this file, just backup this and recreate this bs
            base, ext = os.path.splitext(self._filepath)
            bak_ext = f'{ext}.bak'
            bak_base = f'{base}{bak_ext}'
            try:
                os.rename(self._filepath, bak_base)
            except FileExistsError:
                i = 1
                while True:
                    try:
                        os.rename(self._filepath, f'{base}{bak_ext}{i}')
                        break
                    except FileExistsError:
                        i += 1
                        continue
            with open(self._filepath, 'w') as file:
                file.write('{}')
                file.close()
                return {}


# Save new data to file
    def write2file(self, data) -> None:
        self._blacklist['user'].append(data)
        with open(self._filepath, 'w') as file:
            file.write(ujson.dumps(self._blacklist, indent=4))
            file.close()
            pass


    def add_user_by_name(self, name) -> bool:
        if name not in self._blacklist['user']:
            # self.write2file({'name': name, 'uuid': ''})
            return True
        else:
            return False


    def add_user_by_uuid(self, uuid) -> bool:
        if uuid not in self._blacklist['user']:
            self.write2file({'name': '', 'uuid': uuid})
            return True
        else:
            return False


    def check_uuid(self, uuid):
        pass
