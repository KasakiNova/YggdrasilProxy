import logging
import sys
from time import sleep

from colorama import Fore, Style
from paste.translogger import TransLogger
from waitress import serve

import modules.globalVariables as gVar
from modules.configs.config import Config
from modules.services.defWebapp import WebApp
from modules.services.publickeys import PublicKeys
from modules.utils.proxies import Proxies
from modules.utils.sysinfo import sysinfo

# Print system and python information
sysinfo()

# Init Config Class
cfg = Config()

sleep(0.001)
if cfg.init():
    gVar.cfgContext = cfg.read()
    print(Fore.GREEN + "[Config File Loaded]" + Style.RESET_ALL)
else:
    sys.exit(Fore.RED + "[Please check your config and try again]" + Style.RESET_ALL)

# Init Proxies
proxies = Proxies()
if gVar.proxies != {}:
    if not proxies.check_proxies():
        sys.exit(Fore.RED + "[Proxy is incorrect]" + Style.RESET_ALL)

# Init WebApp
webapp = WebApp()

# Init PublicKeys Class and Services
publickeys = PublicKeys()
publickeys.start_thread()

# if debugMode is enable
if gVar.debugMode:
    print("Config: \n", gVar.cfgContext)
    if gVar.cfgContext['Proxy']['enable']:
        print("ProxiesLink: \n", gVar.proxies)


from modules.services.httpLogic import app
if __name__ == '__main__':
    if gVar.debugMode:
        app.run(host=gVar.cfgContext["General"]["ip"],
                port=gVar.cfgContext["General"]["port"],
                debug=True,
                threaded=True
        )
    else:
        logger = logging.getLogger("waitress")
        logger.setLevel(logging.INFO)
        try:
            serve(
                TransLogger(app, setup_console_handler=False),
                host=gVar.cfgContext["General"]["ip"],
                port=gVar.cfgContext["General"]["port"],
                threads=10,
                ident= "YggdrasilProxyServer"
            )
        except KeyboardInterrupt:
            print("\nStopped by user")