# coding=utf-8
import cmd
import sys

from prettytable import PrettyTable
from print_color import print

import modules.globalVariables as gVar
from modules.services.blacklistService import BlacklistService


def _quit_application():
    """Quit Application"""
    print("Goodbye")
    sys.exit(0)


def _get_server_name(server_id):
    return gVar.cfgContext['Server'][str(server_id)]['Name']


class MainConsole(cmd.Cmd):
    intro_message = (
        "Welcome to Minecraft Yggdrasil Proxy!\n"
        "Created by KasakiNova and open-sourced under the Apache-2.0 license.\n"
        "GitHub Repository: https://github.com/KasakiNova/YggdrasilProxy")
    intro = intro_message
    prompt = '--> '

    def __init__(self):
        super().__init__()
        self.has_new_data = False
        self.blacklistService = BlacklistService()
        self.table = PrettyTable()

    def do_ban(self, args):
        if not args:
            print("No arguments given, use: ban <player_name> <server_name>")
            return

        info = self.blacklistService.add_ban_account(args)
        if info['msg'] == "Success":
            print(f"Successfully banned player {args}") # Confirmation message for successful ban
        elif info['msg'] == "SetError":
            print(f"Failed to ban player {args}") # Error message if the ban fails
        elif info['msg'] == "isBaned":
            print(f"Player {args} has been banned") # Message if the player is already banned
        elif info['msg'] == "Error":
            print("An error occurred") # General error message
        elif info['msg'] == "sameName":
            print("Account with the same name") # Message for duplicate names
            self.table.clear_rows() # Clear previous rows in the table
            self.table.field_names = ["UUID", "Name", "Server", "Baned"] # Define table headers
            for row in info['data']:
                server_name = _get_server_name(row[2]) # Get server name from server ID
                baned = row[3] == 1 # Check if the account is banned
                if not baned:
                    self.table.add_row([row[0], row[1], server_name, baned]) # Add row to the table if not banned
                else:
                    pass # Skip adding if already banned
            print(self.table) # Print the formatted table
        else:
            print("No accounts found or An error occurred.") # Message if no matching accounts are found

    def do_quit(self, _):
        """Quit Application"""
        _quit_application()

    def do_exit(self, _):
        """Exit Application"""
        _quit_application()

    def do_stop(self, _):
        """Stop Application"""
        _quit_application()

    def emptyline(self):
        """Override the default behavior of repeating the last command on an empty line."""
        pass  # Do nothing

    def default(self, line):
        """Unknown Command"""
        print(f"Unknown Command: {line}", color='red')
