import os

sep = os.sep
runningDir = os.getcwd()
webDir = os.path.join(runningDir, 'static')
configFileName = "config.toml"
configFilePath = os.path.join(runningDir, configFileName)

debugMode = False

cfgContext = {}
publickey= {}
proxies = {}
