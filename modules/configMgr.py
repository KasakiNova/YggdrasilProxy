import os

from modules.tools import ConfigTools

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


# 判断配置文件类型
class ConfigParsing:
    def __init__(self, import_path: str, import_config_extension: str):
        self.configData = dict()
        self.configDir = import_path
        self.configFile = str()
        self.configFileList = set()
        self.selectExtension = import_config_extension
        self.endswith = ('toml', 'json', 'json5', 'yaml')
        # 检查文件夹是否存在,不存在则创建
        if not os.path.exists(self.configDir):
            os.mkdir(self.configDir)

    def check_config(self) -> bool:
        # 检查文件夹内是否存在配置文件
        if len(os.listdir(self.configDir)) == 0:
            return False
        else:
            config_list = set(os.listdir(self.configDir))
            pass

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
            print(self.configFile)
        else:
            self.configFile = import_config_file
            print(self.configFile)

        # 初始化临时保存配置变量
        def_logs = bool()
        def_debuglevel = int()
        def_ip = str()
        def_port = int()
        def_prefix = str()

        # 尝试打开配置文件
        try:
            self.configData = ConfigTools.open_config(self.configFile)
            def_logs: bool = self.configData["General"]["logs"]
            def_debuglevel: int = self.configData["General"]["debuglevel"]
            def_ip: str = self.configData["General"]["ip"]
            def_port: int = self.configData["General"]["port"]
            def_prefix: str = self.configData["General"]["prefix"]
        # 无法打开则切换配置文件进行打开
        except FileNotFoundError:
            print(f"Can not open {self.configFile},try next")
            self.configFileList.remove(default_config_file)
            for alt_file_name in self.configFileList:
                try:
                    self.configData = ConfigTools.open_config(self.configDir + os.sep + alt_file_name)
                    def_logs: bool = self.configData["General"]["logs"]
                    def_debuglevel: int = self.configData["General"]["debuglevel"]
                    def_ip: str = self.configData["General"]["ip"]
                    def_port: int = self.configData["General"]["port"]
                    def_prefix: str = self.configData["General"]["prefix"]
                    self.configFile = self.configDir + os.sep + alt_file_name
                    break
                # 这更是个小丑
                except FileNotFoundError:
                    print(f"Can not open {alt_file_name},try next")
        return (self.configFileList, self.configFile, self.configData,
                def_logs, def_debuglevel, def_ip, def_port, def_prefix)

    def read_server_config(self, config_serial):
        server_data = self.configData["Server"]
        pass
