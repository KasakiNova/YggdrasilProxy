# coding=utf-8
import logging
import os
import sys
import threading
from time import sleep

from paste.translogger import TransLogger
from print_color import print
from waitress import serve

import modules.globalVariables as gVar
from modules.configs.config import Config
from modules.console.mainConsole import MainConsole
from modules.services.defWebapp import WebApp
from modules.services.publickeys import PublicKeys
from modules.utils.proxies import Proxies
from modules.utils.sysinfo import sysinfo


def initialize_config() -> None:
    """Init Config"""
    cfg = Config()
    sleep(0.001)
    if cfg.init():
        gVar.cfgContext = cfg.read()
        print("Config File Loaded", tag='Success', tag_color='green', color='white')
    else:
        sys.exit(print("Please check your config and try again", tag='ERROR', tag_color='red', color='white'))


def initialize_services() -> None:
    """Init WebApp and PublicKeys"""
    # setup static dir and index.json
    WebApp()
    # try to init publickeys
    publickeys = PublicKeys()
    publickeys.start_thread()

    # Init Proxies Link
    proxies = Proxies()
    if gVar.proxies and not proxies.check_proxies():
        sys.exit("Proxy is incorrect")


def start_waitress(thread=10) -> None:
    """Start server with waitress"""
    from modules.webapp.httpLogic import app
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
    except PermissionError as e:
        # # Maybe for Windows
        if e.winerror == 10013: # This error code 10013 for windows Port is in use
            print(f"Error: Port {gVar.cfgContext['General']['port']} is already in use.")
        print(f"Permission Error: {e}")
    except OSError as e:
        # This error maybe for unix system, like Linux or macOS
        if e.errno == 98: # Error code 98 is port already use
            print(f"Error: Port {gVar.cfgContext['General']['port']} is already in use.")
        print(f"OS Error: {e}")
    finally:
        print("Yggdrasil server stopped.")
        os._exit(0)  # Exit the program

# Don't use other WSGI server, just use flask
def start_flask_app() -> None:
    from modules.webapp.httpLogic import app
    app.run(host=gVar.cfgContext["General"]["ip"],
            port=gVar.cfgContext["General"]["port"],
            debug=True,threaded=True,use_reloader=False
            )


# Start WSGI Server thread
def run_wsgi_server() -> None:
    if gVar.debugMode:
        # Just start flask Server
        start_flask_app()
    else:
        # not debug, run waitress
        start_waitress()


def main() -> None:
    """Main Service"""

    # init config and services
    initialize_config()
    initialize_services()

    # If debugMode is true, print all config
    if gVar.debugMode:
        print("Config: \n", gVar.cfgContext)
        if gVar.cfgContext['Proxy']['enable']:
            print("ProxiesLink: \n", gVar.proxies)

    # print System info
    try:
        if not gVar.cfgContext["General"]["disableSysInfo"]:
            sysinfo()
    except Exception:
        sysinfo()

    # Create a new thread to run http server
    http_thread = threading.Thread(target=run_wsgi_server)
    http_thread.daemon=True
    http_thread.start()

    # Running Console
    sleep(0.5)
    MainConsole().cmdloop()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down...")
        print("Bye~")
