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
from modules.services.blacklistService import BlacklistService
from modules.utils.proxies import Proxies
from modules.utils.sysinfo import sysinfo


def initialize_config() -> None:
    """Init Config"""
    cfg = Config()
    sleep(0.001)
    if cfg.init():
        gVar.cfgContext = cfg.read()
        print(Fore.GREEN + "[Config File Loaded]" + Style.RESET_ALL)
    else:
        sys.exit(Fore.RED + "[Please check your config and try again]" + Style.RESET_ALL)


def initialize_services() -> None:
    """Init WebApp and PublicKeys"""
    # setup static dir and index.json
    WebApp()
    # try to init publickeys
    publickeys = PublicKeys()
    publickeys.start_thread()
    # init blacklist service
    blacklist = BlacklistService('blacklist.json')
    # blacklist.add_blacklist_by_name("wdsda")
    # Init Proxies Link
    proxies = Proxies()
    if gVar.proxies and not proxies.check_proxies():
        sys.exit(Fore.RED + "[Proxy is incorrect]" + Style.RESET_ALL)


def start_waitress(thread=10) -> None:
    """Start server with waitress"""
    from modules.services.httpLogic import app
    # Set waitress log level
    logger = logging.getLogger("waitress")
    logger.setLevel(logging.INFO)
    try:
        serve(
            TransLogger(app, setup_console_handler=False),
            host=gVar.cfgContext["General"]["ip"],
            port=gVar.cfgContext["General"]["port"],
            threads=thread,
            ident="YggdrasilProxyServer",
            channel_timeout=20,
            max_request_body_size=10 * 1024 * 1024
        )
    except KeyboardInterrupt:
        print("\nStopped by user")
    except PermissionError as e:
        # # Maybe for Windows
        if hasattr(e, 'winerror') and e.winerror == 10013: # This error code 10013 for windows Port is in use
            print(f"Error: Port {gVar.cfgContext['General']['port']} is already in use.")
        print(f"Permission Error: {e}")
    except OSError as e:
        # This error maybe for unix system, like Linux or macOS
        if e.errno == 98: # Error code 98 is port already use
            print(f"Error: Port {gVar.cfgContext['General']['port']} is already in use.")
        print(f"OS Error: {e}")


def main() -> None:
    """Main Service"""
    # print System info
    sysinfo()

    # init config and services
    initialize_config()
    initialize_services()

    # If debugMode is true, print all config
    if gVar.debugMode:
        print("Config: \n", gVar.cfgContext)
        if gVar.cfgContext['Proxy']['enable']:
            print("ProxiesLink: \n", gVar.proxies)
    # Start Server
        from modules.services.httpLogic import app
        app.run(host=gVar.cfgContext["General"]["ip"],
                port=gVar.cfgContext["General"]["port"],
                debug=True,
                threaded=True
                )
    else:
        start_waitress()


if __name__ == '__main__':
    main()
