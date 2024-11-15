import cmd
import sys

from paste.wsgilib import intercept_output

import modules.globalVariables as gVar

from print_color import print

class MainConsole(cmd.Cmd):
    intro_message = (
        "Welcome to Minecraft Yggdrasil Proxy!\n"
        "Created by KasakiNova and open-sourced under the Apache-2.0 license.\n"
        "GitHub Repository: https://github.com/KasakiNova/YggdrasilProxy")
    intro = intro_message
    prompt = '--> '

    def do_echo(self, message):
        """Echo the given message."""
        # just for fun. XD
        # command: echo {message}
        if message:
            print(message)
        else:
            print("Please provide a message to print")

    def do_ban(self, name):
        pass

    def do_quit(self, _):
        """Quit Application"""
        print("Goodbye")
        sys.exit(0)


    def do_exit(self, _):
        """Exit Application"""
        print("Goodbye")
        sys.exit(0)


    def default(self, line):
        """Unknown Command"""
        print(f"Unknown Command: {line}", color='red')