# Date: 30-10-2022
# Description: NFS Server Class Implementation
# Authors: Abhishek Aditya BS, Vishal R
# License: MIT License
# Version: 1.0.0

import random
import rpyc
import pandas as pd
from rpyc.utils.server import ThreadedServer
from rpyc.lib import setup_logger
from colorama import Fore

class NFS_Server(rpyc.Service):

    class exposed_Master():
        # Enter the List of all Data Nodes
        DATA_NODE_LIST = [["127.0.0.1",8888,r'/Users/abhishekadityabs/Distributed Systems/PyNFS/src/NFS_DataNode-1'],  
                          ["127.0.0.1",8000,r'/Users/abhishekadityabs/Distributed Systems/PyNFS/src/NFS_DataNode-2']] 
        global filemap

        @staticmethod
        def exposed_MatchFile(file_name):
            nfs_server = NFS_Server.exposed_Master.exposed_filemap()
            result = nfs_server[nfs_server['Name'].str.contains(file_name)]
            results_dict = result.to_dict('records')
            print(Fore.GREEN + "FILES FOUND IN DATA NODES: " + Fore.RESET)
            print("*"*50)
            print(results_dict)
            return (results_dict)

        @staticmethod
        def exposed_select_dataNode():
            data_node = random.choice(__class__.DATA_NODE_LIST)
            return (data_node)

        @staticmethod
        def exposed_filemap():
            fileTable = []
            for data_node in __class__.DATA_NODE_LIST:
                dataNode_Connection = rpyc.connect(data_node[0], data_node[1])
                dataNode = dataNode_Connection.root.DataNode()
                tempTable = fileTable
                filemap = dataNode.filequery()
                print(type(filemap), "\n", filemap)
                filemap = list(filemap)
                fileTable = tempTable + filemap
            df = pd.DataFrame(fileTable)
            print(Fore.GREEN + "FILE MAP: " + Fore.RESET)
            print("*"*50)
            print(df.to_string(index=False))
            return (df)

if __name__ == "__main__":
    print(Fore.GREEN + "NFS COMMUNICATION SERVER - CONFIGURATION" + Fore.RESET)
    print("-"*50)
    host = '127.0.0.1'
    print("NFS Server IP: " + Fore.YELLOW + host + Fore.RESET)
    port = input("Enter the port number for the NFS Server " + Fore.YELLOW + "[Default: 18812]" + Fore.RESET + ": ")
    if port == "":
        port = 18812
    else:
        try:
            port = int(port)
        except:
            print(Fore.RED + "Invalid Port Number. Using Default Port Number: 18812" + Fore.RESET)
            port = 18812
    print("NFS Server Port: " + Fore.YELLOW + str(port) + Fore.RESET)
    print("\n")
    print(Fore.GREEN + "NFS COMMUNICATION SERVER - LOGS" + Fore.RESET)
    print("-"*50)
    t = ThreadedServer(NFS_Server, hostname=host, port=port, protocol_config={'allow_public_attrs': True})
    setup_logger(quiet=False, logfile=None)
    t.start()