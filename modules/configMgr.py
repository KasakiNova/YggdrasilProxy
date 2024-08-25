import os

import modules.globalVariables as Var
from modules.configTools import ConfigTools, load_config_to_var


# 判断配置文件类型
class ConfigParsing:
    def __init__(self, import_path: str, import_config_extension: str):
        self.configData = dict()
        self.configDir = import_path
        self.configFile = str()
        self.configFileList = set()
        self.selectExtension = import_config_extension
        self.endswith = ('toml', 'json', 'json5', 'yaml')

    def check_config(self) -> bool:
        # 检查文件夹是否存在,不存在则创建
        if not os.path.exists(self.configDir):
            os.mkdir(self.configDir)
        if not os.path.exists(str(Var.workDir + os.sep + "static")):
            os.mkdir(f"{Var.workDir}{os.sep}static")
        # 检查文件夹内是否存在配置文件
        # 不存在则创建默认配置文件并退出程序
        if len(os.listdir(self.configDir)) == 0:
            from modules.defaultConfig import create_config_file as def_config
            def_config(str(self.configDir + os.sep))
            return False
        else:
            config_list = set(os.listdir(self.configDir))
        # 检查static文件夹内index.json是否存在
        if not os.path.exists(str(Var.workDir + os.sep + "static" + os.sep + "index.json")):
            from modules.defaultConfig import create_index_file as def_index
            def_index(str(Var.workDir + os.sep + "static" + os.sep))
        # 检查文件扩展名
        for filename in config_list:
            if filename.endswith(self.endswith):
                config_list.add(filename)
        if len(config_list) == 0:
            return False
        # 对配置文件列表进行排序
        # 0为toml，1为json，2为json5，3为yaml
        suffix_order = {'.toml': 0, '.json': 1, 'json5': 2, 'yaml': 3}

        def reordering(file):
            _, ext = file.split('.')
            return suffix_order.get('.' + ext, float('inf'))

        self.configFileList = sorted(config_list, key=reordering)
        return True

    # 加载配置文件
    def load_config(self, import_config_file):
        # 选择默认扩展名
        default_config_file = ConfigTools.select_extension(self.selectExtension, self.configFileList)
        # 检查输入参数是否为空，空则将默认配置文件覆盖进来
        if import_config_file is None:
            self.configFile = self.configDir + os.sep + default_config_file[0]
        else:
            self.configFile = import_config_file

        # 尝试打开配置文件
        try:
            self.configData = ConfigTools.open_config(self.configFile)
            load_config_to_var(self.configData)
        # 无法打开则切换配置文件进行打开
        except FileNotFoundError:
            print(f"Can not open {self.configFile},try next")
            self.configFileList.remove(default_config_file)
            for alt_file_name in self.configFileList:
                try:
                    self.configData = ConfigTools.open_config(self.configFile)
                    load_config_to_var(self.configData)
                    self.configFile = self.configDir + os.sep + alt_file_name
                    break
                except FileNotFoundError:  # 这更是个小丑
                    print(f"Can not open {alt_file_name},try next")
        return self.configFileList, self.configFile, self.configData


# 加载Server块配置文件
def read_server_config(config_serial: int):
    from modules.configTools import server_type_judgment
    server_data = Var.configData["Server"]
    def_name = server_data[str(config_serial)]["Name"]
    def_proxy = server_data[str(config_serial)]["NeedProxy"]
    def_url = server_data[str(config_serial)]["Url"]
    def_type = server_type_judgment(def_url)
    return def_name, def_proxy, def_url, def_type
