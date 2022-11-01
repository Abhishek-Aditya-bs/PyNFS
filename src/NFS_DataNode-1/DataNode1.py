# Date: 30-10-2022
# Description: NFS Data Node Class Implementation
# Authors: Abhishek Aditya BS, Vishal R
# License: MIT License
# Version: 1.0.0

import os
import rpyc
from datetime import datetime as dt
from rpyc.utils.server import ThreadedServer
from rpyc.lib import setup_logger
from colorama import Fore

global IP_ADDR, PORT_NUM, DIR_PATH

IP_ADDR = "127.0.0.1"
PORT_NUM = 8888
DIR_PATH = r'/Users/abhishekadityabs/Distributed Systems/PyNFS/src/NFS_DataNode-1'
FTP_ADDR = "127.0.0.1"

timeFormat = "%d-%m-%Y %H:%M:%S"

class DataNode(rpyc.Service):
    
    class exposed_DataNode():
        @staticmethod
        def exposed_filequery():
            fileList = []
            for (dirpath, dirnames, filenames) in os.walk(DIR_PATH):
                for file in filenames:
                    file_path = os.path.join(dirpath, file)
                    file_size = os.path.getsize(file_path)
                    file_time = dt.fromtimestamp(os.path.getmtime(file_path)).strftime(timeFormat)
                    file_dict = {"Name": file, "IP": FTP_ADDR, "Port": PORT_NUM, "Path": file_path, "Size": file_size, "Time": file_time}
                    fileList.append(file_dict)

            print(Fore.GREEN + "FILE LIST: " + Fore.RESET)
            print("*"*50)
            print(fileList)
            return (fileList)

if __name__ == "__main__":
    print(Fore.GREEN + "DATA NODE (1) - CONFIGURATION " + Fore.RESET)
    print("-"*50)
    print("Data Node (1) IP: " + Fore.YELLOW + IP_ADDR + Fore.RESET)
    print("Data Node (1) Port: " + Fore.YELLOW + str(PORT_NUM) + Fore.RESET)
    print("Data Node (1) Directory Path: " + Fore.YELLOW + DIR_PATH + Fore.RESET)
    print("\n")
    print(Fore.GREEN + "DATA NODE (1) - LOGS" + Fore.RESET)
    print("-"*50)
    t = ThreadedServer(DataNode, hostname = IP_ADDR, port = PORT_NUM, protocol_config={'allow_public_attrs': True})
    setup_logger(quiet=False, logfile=None)
    t.start()