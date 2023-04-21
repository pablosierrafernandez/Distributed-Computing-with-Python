# Distributed-Computing-with-Python
🌍This project is a basic example of distributed computing with Python. The goal is to calculate the minimum and maximum price of an asset, given a csv file containing the price history. 

The project uses xmlrpc to communicate between the different servers.

## 👍Requirements

-   Python 3
-   NumPy
-   tkinter
-   xmlrpc

## 🤗Usage

1.  Clone the repository
2.  Run the command `python xmlrpc_cluster.py` in a terminal to start the cluster
3.  Run the command `python xmlrpc_server.py` in a separate terminal to start a worker (you can start multiple workers on different ports)
4.  Run the command `python gui.py` to start the GUI
5.  Choose a CSV file containing the price history of an asset
6.  Choose the type of price (Ask, Bid, AskVolume, BidVolume) you want to compute the min and max values for
7.  Click the "Compute Low Price" or "Compute High Price" button to calculate the min and max prices, respectively

## 🤔How it works

The `xmlrpc_cluster.py` file starts an XML-RPC server that listens for incoming connections from the workers. When a worker connects, the server adds it to a list of available workers.

The `xmlrpc_server.py` file starts an XML-RPC server on a specified port and waits for incoming requests from the GUI. When a request is received, the server reads a chunk of the CSV file and computes the min or max value for the specified price type. The result is returned to the GUI via XML-RPC.

The `gui.py` file starts a GUI using tkinter. The user selects a CSV file and a price type and clicks a button to compute the min or max value. The GUI uses XML-RPC to send a request to a worker server to compute the value. The result is displayed in the GUI.

The CSV file is divided into chunks and each worker is responsible for computing the min or max value for a particular chunk. The results are collected and combined to produce the final result.

## 😒Limitations

-   The project assumes that the CSV file is small enough to fit in memory. If the file is too large, it may need to be processed in chunks.
-   The project assumes that the price history is sorted by time. If this is not the case, the min and max values may not be accurate.
-   The project assumes that the price history contains only valid prices. If there are invalid prices (e.g. negative prices), the min and max values may not be accurate.
-   The project assumes that the workers are running on the same machine as the cluster server. If the workers are running on different machines, their IP addresses will need to be specified in the GUI.
