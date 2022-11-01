# Date: 30-10-2022
# Description: NFS FTP Server Class Implementation
# Authors: Abhishek Aditya BS, Vishal R
# License: MIT License
# Version: 1.0.0

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from colorama import Fore

IP_ADDR = '127.0.0.1'
PORT_NUM = 8001
USERNAME = 'user'
PASSWORD = '12345'
HOME_DIR = r'/Users/abhishekadityabs/Distributed Systems/PyNFS/src/NFS_DataNode-2'

def main():
    authorizer = DummyAuthorizer()
    authorizer.add_user(USERNAME, PASSWORD, homedir=HOME_DIR, perm='elradfmwMT')

    handler = FTPHandler
    handler.authorizer = authorizer

    server = ThreadedFTPServer((IP_ADDR, PORT_NUM), handler)
    print(Fore.GREEN + "FTP SERVER FOR DATA NODE (2) - CONFIGURATION" + Fore.RESET)
    print("-"*50)
    print("FTP Server IP: " + Fore.YELLOW + IP_ADDR + Fore.RESET)
    print("FTP Server Port: " + Fore.YELLOW + str(PORT_NUM) + Fore.RESET)
    print("FTP Server Home Directory: " + Fore.YELLOW + HOME_DIR + Fore.RESET)
    print("\n")
    print(Fore.GREEN + "FTP SERVER FOR DATA NODE (2) - LOGS" + Fore.RESET)
    print("-"*50)
    server.serve_forever()

def stopFTP():
    print(Fore.RED + "FTP SERVER FOR DATA NODE (2) - STOPPED" + Fore.RESET)
    server.close_all()

if __name__ == "__main__":
    main()
