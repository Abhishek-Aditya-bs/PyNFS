# PyNFS - Python Implementation of a Network File System

## Introduction 

![NFS Architecture](https://developer.ibm.com/developer/default/tutorials/l-network-filesystems/images/figure2.gif)

NFS supports file sharing between multiple peer clients serving on highly available cluster services, NAS clients can potentially access file shares
from anywhere in the organization. Because file access is,
typically low volume and less sensitive to response times,
predictable performance and distance are less of a concern in
NAS implementations. NFS is designed to support UNIX file system
semantics. However, its design also allows it to
support the possibly less rich semantics of other file
systems. It was originally built using the UDP
datagram protocol, it was easily moved to the TCP
stream protocol. It has also been ported to run over
numerous other non IP-based protocols.

NFS works well for organizations that need to deliver
file data to multiple clients over a network. NAS appliances
also function well in environments where data must be
transferred over very long distances. Because most NAS
requests are for smaller amounts of data, distance and
network delays are less critical to data transfer. Properly configured, NAS
provides reliable file-level data integrity, because file locking
is handled by the appliance itself. Although deployment is
fairly straightforward, organizations must be careful to
ensure that appropriate levels of file security are provided
during NFS configuration.

NFS can be used to communicate
onto storage for highly available application, which can be
implemented in any data centre where data guarantee is more
admitted than the speed of the data, since the data that flows
via NFS; whenever a client/ server goes and comes back,
during the recovery time the data travel is delayed. More
over single lock file function is tolerated in this method.

## Implementation

1. Two Data Nodes, One NFS Communication Server, One NFS CLient has been implemented.
2. The Data Nodes store the file system metadata and run FTP Servers to communicate with the NFS Server to fetch and retreive the requested files and perform other actions requested.
3. The Client is given options after successful connection to the NFS Server
    1. List Files
    2. Download File
    3. Upload File
    4. Delete File
    5. Exit
4. The Client can perform the above mentioned actions on the files stored in the Data Nodes.
5. The Data Nodes are connected to the NFS Server via FTP Servers. The NFS Server is connected to the Client via TCP Sockets.
6. The data is stored on either of the Data Nodes in a random fashion. When retreived by the Client, the Data from all the Data Nodes is combined and sent to the Client.
7. When the Client requests for a file, the NFS Server checks the metadata of the file and sends the file to the Client from the Data Node where the file is stored.
8. Python Package **RPyC** (pronounced as are-pie-see), or Remote Python Call is used to implement the Client-Server-DataNodes communication. It is a transparent python library for symmetrical remote procedure calls, clustering and distributed-computing. RPyC makes use of object-proxying, a technique that employs python’s dynamic nature, to overcome the physical boundaries between processes and computers, so that remote objects can be manipulated as if they were local.

## Usage

### Running on localhost
1. Clone the repository
2. Change the directory path in the following files:
    1. In `NFS_Server/nfsServer.py` change the Data Node paths in the `DATA_NODE_LIST`.
    ```python
    DATA_NODE_LIST = [["127.0.0.1",8888,r'/Users/abhishekadityabs/Distributed Systems/PyNFS/src/NFS_DataNode-1'],  
                      ["127.0.0.1",8000,r'/Users/abhishekadityabs/Distributed Systems/PyNFS/src/NFS_DataNode-2']] 
    ```
    2. In `NFS_DataNode-1/DataNode1.py`, change the `DIR_PATH` variable to the path of the directory `NFS_DataNode-1/` in your system.
    Similarly, do the same change in `NFS_DataNode-2/DataNode2.py` for the `DIR_PATH` variable.
    3. In `NFS_DataNode-1/FTPServer1.py`, change the `HOME_DIR` variable to the path of the directory `NFS_DataNode-1/` in your system.
    Similarly, do the same change in `NFS_DataNode-2/FTPServer2.py` for the `HOME_DIR` variable.
    4. In `NFS_Client/NFS_Client.py`, change the `CLIENT_DIR` directory path to the path of the directory `NFS_Client/` in your system.
3. Create a virtual Environment/ Conda Environment and install the dependencies using `pip3 install -r requirements.txt`
4. In Seperate Terminal Windows, run the following commands:
    1. `python3 NFS_Server/nfsServer.py`
    2. `python3 NFS_DataNode-1/DataNode1.py`
    3. `python3 NFS_DataNode-1/FTPServer1.py`
    4. `python3 NFS_DataNode-2/DataNode2.py`
    5. `python3 NFS_DataNode-2/FTPServer2.py`
    6. `python3 NFS_Client/NFS_Client.py`
5. The Client will be prompted to enter the IP Address and Port Number of the NFS Server. Leave it default if running on localhost. 
6. The FTP username and password is `user` and `12345` respectively. You can change it in the `NFS_DataNode-1/FTPServer1.py` and `NFS_DataNode-2/FTPServer2.py` files.
7. The Client can now perform the actions mentioned above.

### Running on different machines
1. Clone the repository
2. In `NFS_Server/nfsServer.py` change the Data Node paths in the `DATA_NODE_LIST`.
    ```python
    DATA_NODE_LIST = [[" <IP Address of Data Node 1> ",
                         <Port Number of Data Node1>,
                         r'<Path of Data Node 1>'],  
                      [" <IP Address of Data Node 2> ",
                         <Port Number of Data Node 2>,
                         r'<Path of Data Node 2>']] 
    ```
3. In `NFS_DataNode-1/FTPServer1.py`, change the `FTP_ADDR` variable to the IP Address of the Data Node 1. Similarly, do the same change in `NFS_DataNode-2/FTPServer2`.py for the `FTP_ADDR` variable.
4. Repeat the steps from 2 to 7 in the above section.

## Limitations
1. The Client can only perform the actions mentioned above.
2. Minimal Implementation of a simple NFS.
3. Not suitable for large scale applications.
4. No security features implemented except for the FTP username and password.
5. No support for multiple clients via Load Balancing, Locking, etc.

## License
MIT 

<!-- Write a github description -->

    








