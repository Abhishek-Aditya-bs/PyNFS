# Date: 30-10-2022
# Description: NFS Client Class Implementation
# Authors: Abhishek Aditya BS, Vishal R
# License: MIT License
# Version: 1.0.0

import os, rpyc, sys
import pandas as pd
import ftplib
from colorama import Fore
import datetime, time

CLIENT_DIR = r'/Users/abhishekadityabs/Distributed Systems/PyNFS/src/NFS_Client'

def connect(HOST, PORT, FLAG, FILE):
    print(Fore.GREEN + "CONNECED TO THE FTP SERVER" + Fore.RESET)
    print("FTP HOST: " + Fore.YELLOW + HOST + Fore.RESET)
    print("FTP PORT: " + Fore.YELLOW + str(PORT) + Fore.RESET)
    print("FTP OPT CODE: " + Fore.YELLOW + str(FLAG) + Fore.RESET)
    print("FILE: " + Fore.YELLOW + FILE + Fore.RESET)

    try:
        ftp = ftplib.FTP()
        ftp.connect(HOST, int(PORT))
        while True:
            print()
            USERNAME = input(Fore.MAGENTA + "ENTER THE FTP USERNAME: " + Fore.RESET)
            PASSWORD = input(Fore.MAGENTA + "ENTER THE FTP PASSWORD FOR " + Fore.YELLOW + USERNAME + Fore.RESET + ": ")
            print()
            try:
                ftp.login(str(USERNAME), str(PASSWORD))
                print(Fore.GREEN + "LOGIN SUCCESSFUL!" + Fore.RESET)
                print()
                print(Fore.MAGENTA + "FILES IN THE CURRENT WORKING DIRECTORY (CWD)" + Fore.RESET + ": ")
                ftp.dir()
                if FLAG == 2:
                    RETURN_CODE = upload(ftp, FILE)
                elif FLAG == 3:
                    RETURN_CODE = download(ftp, FILE)
                elif FLAG == 4:
                    RETURN_CODE = delete(ftp, FILE)
                else:
                    print(Fore.RED + "INVALID OPT CODE!" + Fore.RESET)
                return (RETURN_CODE)
            except:
                print(Fore.RED + "LOGIN FAILED! TRY AGAIN..." + Fore.RESET)
    except ftplib.all_errors as e:
        print(Fore.RED + "CONNECTION FAILED! TRY AGAIN..." + Fore.RESET)
        return (e)

def upload(ftp, FILE):
    print("\n" + Fore.GREEN + "UPLOADING FILE..." + Fore.RESET)
    print("-"*50)
    print("FILE: " + Fore.YELLOW + FILE + Fore.RESET)
    try:
        ftp.storbinary('STOR ' + FILE, open(FILE, 'rb'))
        print("\n" + Fore.GREEN + "UPLOAD SUCCESSFUL!" + Fore.RESET + "\n")
        print(Fore.MAGENTA + "UPDATED FILES IN THE CURRENT WORKING DIRECTORY (CWD)" + Fore.RESET + ": ")
        ftp.dir()
        print("\n" + Fore.GREEN + "DISCONNECTING FROM THE FTP SERVER..." + Fore.RESET)
        ftp.quit()
        return ('250-Requested file action okay, completed')
    except ftplib.all_errors as e:
        print(Fore.RED + "UPLOAD FAILED! TRY AGAIN..." + Fore.RESET)
        return ('426-Connection closed; File action aborted')

def download(ftp, FILE):
    print("\n" + Fore.GREEN + "DOWNLOADING FILE..." + Fore.RESET)
    print("-"*50)
    print("FILE: " + Fore.YELLOW + FILE + Fore.RESET)
    try:
        ftp.retrbinary('RETR ' + FILE, open(FILE, 'wb').write, 1024)
        print("\n" + Fore.GREEN + "DOWNLOAD SUCCESSFUL!" + Fore.RESET + "\n")
        print(Fore.GREEN + "DISCONNECTING FROM THE FTP SERVER..." + Fore.RESET)
        ftp.quit()
        return ('250-Requested file action okay, completed')
    except ftplib.all_errors as e:
        print(Fore.RED + "DOWNLOAD FAILED! TRY AGAIN..." + Fore.RESET)
        return ('426-Connection closed; File action aborted')

def delete(ftp, FILE):
    print("\n" + Fore.GREEN + "DELETING FILE..." + Fore.RESET)
    print("-"*50)
    print("FILE: " + Fore.YELLOW + FILE + Fore.RESET)
    try:
        ftp.delete(FILE)
        print("\n" + Fore.GREEN + "DELETE SUCCESSFUL!" + Fore.RESET + "\n")
        print(Fore.MAGENTA + "UPDATED FILES IN THE CURRENT WORKING DIRECTORY (CWD)" + Fore.RESET + ": ")
        ftp.dir()
        print("\n" + Fore.GREEN + "DISCONNECTING FROM THE FTP SERVER..." + Fore.RESET)
        ftp.quit()
        return ('250-Requested file action okay, completed')
    except ftplib.all_errors as e:
        print(Fore.RED + "DELETE FAILED! TRY AGAIN..." + Fore.RESET)
        return ('426-Connection closed; File action aborted')

def getLocalFiles():
    print("\n" + Fore.GREEN + "GETTING LOCAL FILES..." + Fore.RESET)
    print("-"*50)
    fileList = []
    for (root, dirs, files) in os.walk(CLIENT_DIR):
        for file in files:
            fileList.append(file)
    return (fileList)

def getDataNodeInfo(NFS_SERVER):
    print(Fore.GREEN + "GETTING DATA NODE INFO..." + Fore.RESET)
    print("-"*50)
    dataNode = NFS_SERVER.select_dataNode()
    print(Fore.GREEN + "SELECTED DATA NODE CONFIGURATION:" + Fore.RESET)
    print("HOST: " + Fore.YELLOW + dataNode[0] + Fore.RESET)
    print("PORT: " + Fore.YELLOW + str(dataNode[1]) + Fore.RESET)
    print("DIRECTORY: " + Fore.YELLOW + dataNode[2] + Fore.RESET)
    return (dataNode[0], dataNode[1], dataNode[2])

def main():
    print(Fore.GREEN + "CONNECTING TO THE NFS COMMUNICATION SERVER..." + Fore.RESET)
    print("-"*50)
    HOST = input("Enter the NFS Communication Server IP" + Fore.YELLOW + " [Default: 127.0.0.1]" + Fore.RESET + ": ")
    if HOST == '':
        HOST = '0.0.0.0'
    PORT = input("Enter the NFS Communication Server Port" + Fore.YELLOW + " [Default: 18812]" + Fore.RESET + ": ")
    if PORT == '':
        PORT = 18812
    connection = rpyc.connect(HOST, int(PORT))
    print("\n" + Fore.GREEN + "CONNECTED TO THE NFS COMMUNICATION SERVER AT " + Fore.YELLOW + HOST + Fore.RESET + ":" + Fore.YELLOW + str(PORT) + Fore.RESET + "\n")
    NFS_SERVER = connection.root.Master()
    connection._config['sync_request_timeout'] = 20

    print(Fore.MAGENTA + "PLEASE SELECT AN OPTION [0-4]:" + Fore.RESET)
    print(Fore.YELLOW + "0. EXIT" + Fore.RESET)
    print(Fore.YELLOW + "1. GET FILE LIST" + Fore.RESET)
    print(Fore.YELLOW + "2. UPLOAD FILE" + Fore.RESET)
    print(Fore.YELLOW + "3. DOWNLOAD FILE" + Fore.RESET)
    print(Fore.YELLOW + "4. DELETE FILE" + Fore.RESET + "\n")

    while NFS_SERVER:
        try:
            print()
            FLAG = int(input(Fore.MAGENTA + "ENTER YOUR OPTION: " + Fore.RESET))
            print()
            FLAG = int(FLAG)
            if FLAG in range(5):
                if FLAG == 0:
                    print("\n" + Fore.GREEN + "DISCONNECTING FROM THE NFS COMMUNICATION SERVER..." + Fore.RESET)
                    connection.close()
                    print(Fore.GREEN + "DISCONNECTED FROM THE NFS COMMUNICATION SERVER AT " + Fore.YELLOW + HOST + Fore.RESET + ":" + Fore.YELLOW + str(PORT) + Fore.RESET + "\n")
                    print(Fore.RED + "EXITING..." + Fore.RESET)
                    break
                elif FLAG == 1:
                    print(Fore.GREEN + "GETTING FILE LIST..." + Fore.RESET)
                    print("-"*50)
                    fileList = NFS_SERVER.filemap()
                    with pd.option_context('max_colwidth', 1000, 'display.max_columns', 500):
                        print (fileList,"\n")        
                elif FLAG == 2:
                    HOST, PORT, DIR = getDataNodeInfo(NFS_SERVER)
                    FTP_PORT = int(PORT + 1)
                    localFiles = getLocalFiles()
                    for file in localFiles:
                        print(Fore.YELLOW + file + Fore.RESET)
                    FILE = input("\n" + Fore.MAGENTA + "ENTER THE FILE NAME TO UPLOAD: " + Fore.RESET)
                    if FILE in localFiles:
                        try:
                            print("\n" + Fore.GREEN + "CONNECTING TO THE FTP SERVER..." + Fore.RESET)
                            print("-"*50)
                            # print(Fore.GREEN + "CONNECTED TO THE FTP SERVER AT " + Fore.YELLOW + HOST + Fore.RESET + ":" + Fore.YELLOW + str(FTP_PORT) + Fore.RESET)
                            MSGCODE = connect(HOST, FTP_PORT, FLAG, str(FILE))
                            print(Fore.GREEN + "MSGCODE: " + Fore.YELLOW + MSGCODE + Fore.RESET)
                        except ftplib.error_perm as e:
                            print(Fore.RED + "FTP CONNECTION FAILED! TRY AGAIN..." + Fore.RESET)
                    else:
                        print(Fore.RED + "FILE DOES NOT EXIST! TRY AGAIN..." + Fore.RESET)
                elif FLAG == 3:
                    FILE_NAME = input("\n" + Fore.MAGENTA + "ENTER THE KEYWORD TO SEARCH FOR THE REQUIRED FILE [DEFAULT: LIST ALL FILES]: " + Fore.RESET)
                    if FILE_NAME:
                        try:
                            match = NFS_SERVER.MatchFile(FILE_NAME)
                            match_df = pd.DataFrame(match)
                            print(match_df)
                        except:
                            print(Fore.RED + "FILE DOES NOT EXIST! TRY AGAIN..." + Fore.RESET)  
                    else:
                        match = NFS_SERVER.filemap()
                        print(match, "\n")

                    download_file = input("\n" + Fore.MAGENTA + "ENTER THE FILE NAME TO DOWNLOAD: " + Fore.RESET)
                    try:
                        match_dict = NFS_SERVER.MatchFile(download_file)
                        match_df = pd.DataFrame(match_dict)
                        host, port = match_df.at[0, 'IP'], match_df.at[0, 'Port'] + 1
                        print("\n" + Fore.GREEN + "CONNECTING TO THE FTP SERVER..." + Fore.RESET)
                        print("-"*50)
                        MSGCODE = connect(host, port, FLAG, str(download_file))
                        print(Fore.GREEN + "MSGCODE: " + Fore.YELLOW + MSGCODE + Fore.RESET)
                    except:
                        print(Fore.RED + "FILE DOES NOT EXIST! TRY AGAIN..." + Fore.RESET)

                elif FLAG == 4:
                    FILE_LIST = NFS_SERVER.filemap()
                    print(Fore.GREEN + "FILE LIST:" + Fore.RESET)
                    print("-"*50)
                    print(FILE_LIST)
                    FILE = input("\n" + Fore.MAGENTA + "ENTER THE FILE NAME TO DELETE: " + Fore.RESET)
                    try:
                        file_dict = NFS_SERVER.MatchFile(FILE)
                        file_df = pd.DataFrame(file_dict)
                        host, port = file_df.at[0, 'IP'], file_df.at[0, 'Port'] + 1
                        print(Fore.GREEN + "CONNECTING TO THE FTP SERVER..." + Fore.RESET)
                        print("-"*50)
                        MSGCODE = connect(host, port, FLAG, str(FILE))
                        print(Fore.GREEN + "MSGCODE: " + Fore.YELLOW + MSGCODE + Fore.RESET)
                    except:
                        print(Fore.RED + "FILE DOES NOT EXIST! TRY AGAIN..." + Fore.RESET)
            else:
                print(Fore.RED + "INVALID OPTION! TRY AGAIN..." + Fore.RESET)
        except:
            print(Fore.RED + "OOPS SOMETHING WENT WRONG!" + Fore.RESET)
        
if __name__ == "__main__":
    main()

        
                    