import os
import json
import time
import uuid
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from termcolor import colored
from web3 import Web3
import platform

w3 = Web3(Web3.HTTPProvider("https://worldchain-mainnet.g.alchemy.com/v2/eyG6-pMprH5o2nHBsjPbK"))

os.makedirs("wallets/live", exist_ok=True)

def clear():
    os.system("cls" if platform.system()=="Windows" else "clear")

def banner():
    art = """ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣶⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⡟⠉⠛⠻⠿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀
⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣅⠀⠀⠀⠀⠀⠉⠛⠻⠿⠿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡿⠿⠟⠛⠉⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀
⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀
⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣠⣶⣿⣷⡄⠀⠐⣦⣤⣤⣤⣤⣤⣤⠄⠀⠀⢤⣤⣤⣤⡀⠀⠀⣠⣤⣤⣤⣤⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀
⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢁⣤⠀⢻⠟⣿⣿⣿⣿⠋⢀⣴⣶⣄⠈⢿⣿⡇⠀⠀⡿⠟⠛⠛⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀
⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⢠⣿⣿⡧⠀⠀⣿⡿⠟⠁⣠⣾⣿⡏⠉⡇⢸⣹⣿⠀⠀⣠⠞⠋⠉⣂⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠘⢿⡿⠗⠀⢀⣀⠀⢤⣾⣿⣿⣿⣿⡿⠁⡜⣽⣿⣧⠀⣇⠐⢿⣿⡸⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷
⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⣠⣴⣶⣿⣿⣿⣷⣄⠉⠛⠛⠋⢁⣠⣮⣾⣿⣿⣿⣇⠘⣷⠀⢻⢇⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢁⣴⣿⣿⣿⣿⡿⠛⢁⣤⣤⠈⠋⠁⠀⠀⠀⠀⠉⠙⠻⢿⣿⡄⠘⢠⣮⣾⠇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢀⣾⣿⣿⣿⣿⠏⣠⣾⣿⣿⡿⠇⢀⣠⣤⠂⠀⣤⣀⠀⠀⠀⠈⠳⠀⠿⠟⠋⣠⣿⡿⠋⠁⣀⣀⡀⠈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣅⣴⣿⣿⡿⠋⣠⣶⣿⣿⠃⢰⡄⠘⣿⣿⣶⣄⠀⠀⠀⠐⢶⣿⣿⣿⠀⢠⣾⣿⣿⣿⣷⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇
⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⢸⣿⣿⣿⣿⣿⣿⣿⠟⠀⣸⣿⣿⣿⡏⠀⢿⣿⣆⠈⢿⣿⣿⡇⠀⠀⠀⠀⠻⣿⣧⡀⣾⣿⣿⣿⣿⡟⠀⢸⣿⣿⣿⣿⣿⣿⣿⠃
⠀⠀⠀⢿⣿⣿⡿⠿⠛⠿⣿⣿⣿⡿⠋⠀⠀⢸⣿⣿⣿⣿⣿⡿⠁⡀⣼⣿⣿⣿⣿⠁⣆⠘⣿⣿⣦⠈⢻⣿⠇⢸⠀⠀⠀⠀⠈⠙⠻⢿⣿⣿⠿⠋⠀⠀⣼⣿⣿⣿⣿⣿⣿⡿⠀
⠀⠀⠀⠘⡿⠃⢀⣴⣶⣶⣾⣿⠏⠀⠀⠀⣀⠀⢿⣿⣿⣿⠋⢀⠀⣿⣿⣿⣿⡿⠁⢸⣿⡆⠹⣿⣿⣧⡀⠻⠀⣿⠀⠿⠦⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⠃⠀
⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⠃⠀⠀⣠⣾⣿⣷⡀⠙⠿⠃⡰⠃⠸⠿⠟⠋⢁⣤⡄⢸⣿⣿⡀⢹⣿⣿⣷⠀⢰⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠻⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀
⠀⠀⠀⠀⠀⠀⢿⣿⣿⡿⠃⠀⠀⣴⣿⣿⣿⣿⣿⣶⣤⣼⣿⣶⠀⢰⣶⡆⣿⣿⡇⢸⣿⣿⣷⠈⢿⣿⡏⢠⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⠏⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠁⣀⡈⠙⠁⢿⣿⡇⢸⣿⣿⣿⣇⠈⠏⢀⣾⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⠋⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢶⣾⣿⣿⣿⣿⣿⣿⣿⡿⠋⣀⣤⣶⣶⣿⣿⣿⣷⣶⣤⣌⠁⠘⠿⣿⣿⡿⠂⢠⣾⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⡟⠀⣾⣿⡿⠟⢻⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣈⣁⣴⣿⠿⠿⠟⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣷⡀⢻⣿⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠉⠁⢀⠀⠀⠀⠀⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣿⣷⣄⠉⠈⢿⣿⣿⣿⣿⣿⣿⠿⠛⠉⣁⡄⠀⠀⠀⣴⣿⠆⠀⣠⡄⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣶⣤⣈⣉⡉⠉⠉⠀⠐⠒⠛⠛⠀⠀⠀⢸⡿⠃⠀⣸⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⡿⠟⠉⣁⣤⣶⣶⣶⣶⣶⣶⠀⢀⡀⠈⠁⠀⠀⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⠛⢉⣉⣤⣤⣤⣤⣍⣉⣀⣾⡇⠀⠀⠀⠀⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⠀⣿⣿⠟⠛⠋⢉⣉⡉⠻⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣧⣈⣤⠶⠾⢿⣿⣿⡇⠀⡇⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⠀⣴⣶⡦⢤⣤⣤⣾⣿⠀⢻⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⢿⣦⣤⣤⣤⣤⣄⡉⢻⣿⠀⢸⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣆⠈⠻⠋⠀⠀⠀⠉⠁⠀⠉⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
|====================================================================|⠀⠀⠀⠀⠀
| █▀ █ █▀▀ █▀▄▀█ ▄▀█  █▀▀ █░█ █▀█ █▀ ▀█▀  █░█ ▄▀█ █▀▀ █▄▀ █ █▄░█ █▀▀ |
| ▄█ █ █▄█ █░▀░█ █▀█  █▄█ █▀█ █▄█ ▄█ ░█░  █▀█ █▀█ █▄▄ █░█ █ █░▀█ █▄█ |
|====================================================================|

𝗖𝗛𝗔𝗜𝗡 𝗛𝗨𝗡𝗧𝗘𝗥 Wållê† 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗢𝗥
"""
    print(colored(art, "cyan"))
    print(colored("🔗 Twitter:    https://twitter.com/safderkhan0800_", "blue"))
    print(colored("📸 Instagram:  https://www.instagram.com/safderkhan0800_/", "blue"))
    print(colored("🎥 YouTube:    https://www.youtube.com/@sigma_ghost_hacking", "blue"))
    print(colored("🛡️ Telegram:   https://t.me/Sigma_Cyber_Ghost", "blue"))
    print()

def get_balance(address, retries=2, delay=0.5):
    for _ in range(retries):
        try:
            wei = w3.eth.get_balance(address)
            return float(w3.fromWei(wei, 'ether'))
        except:
            time.sleep(delay)
    return None

def generate_wallets():
    clear(); banner()
    try:
        count = int(input(colored("How many wallets to generate? ", "cyan")))
    except:
        print(colored("Invalid number.", "red")); time.sleep(1); return

    for i in range(count):
        acct = w3.eth.account.create()
        data = {
            "wallet_name": f"Wallet_{i}",
            "address": acct.address,
            "private_key": acct.key.hex(),
            "real_balance": "0 ETH"
        }
        with open(f"wallets/{acct.address}.json", "w") as f:
            json.dump(data, f, indent=4)

    print(colored(f"\n✅ {count} valid wallets generated.", "green"))
    input(colored("Press Enter to return to menu.", "yellow"))

def scan_wallets():
    clear(); banner()
    if not w3.is_connected():
        print(colored("❌ RPC connection failed", "red")); input(); return

    files = [f for f in os.listdir("wallets") if f.endswith(".json")]
    live_count = 0

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {}
        for fn in files:
            path = os.path.join("wallets", fn)
            try:
                data = json.load(open(path))
                futures[executor.submit(get_balance, data["address"])] = (fn, data)
            except Exception as e:
                print(colored(f"[Dead Wallet] Loading {fn} — {e}", "red"))

        for future in as_completed(futures):
            fn, data = futures[future]
            bal = future.result()
            data["real_balance"] = f"{bal:.6f} ETH" if bal is not None else "ERROR"
            path = os.path.join("wallets", fn)
            with open(path, "w") as f:
                json.dump(data, f, indent=4)

            addr = data["address"]
            if bal is None:
                print(colored(f"[Dead] {addr}", "red"))
            elif bal > 0:
                os.makedirs("wallets/live", exist_ok=True)
                with open(f"wallets/live/{fn}", "w") as f:
                    json.dump(data, f, indent=4)
                print(colored(f"[LIVE] {addr} | {bal:.6f} ETH", "green"))
                live_count += 1
            else:
                print(colored(f"[DEAD] {addr} | 0 ETH", "red"))

    print(colored(f"\n✅ Scan finished. {live_count} LIVE wallets.", "yellow"))
    input(colored("Press Enter to return to menu.", "cyan"))

def main():
    while True:
        clear(); banner()
        print(colored("1. Generate Wallets", "cyan"))
        print(colored("2. Check Wallets", "cyan"))
        print(colored("3. Exit", "red"))
        choice = input(colored("Select: ", "yellow")).strip()
        if choice == "1":
            generate_wallets()
        elif choice == "2":
            scan_wallets()
        elif choice == "3":
            break
        else:
            print(colored("Invalid choice.", "red")); time.sleep(1)

if __name__ == "__main__":
    main()
