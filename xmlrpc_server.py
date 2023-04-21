from distutils.command.config import config
from xmlrpc.server import SimpleXMLRPCServer
import logging
import xmlrpc.client
import config
import pandas as pd
import time
headers=['Local time','Ask','Bid','AskVolume','BidVolume']

# Start the server
try:
   proxy = xmlrpc.client.ServerProxy('http://localhost:'+str(config.CLUSTER))
   host=proxy.get_next_host()
   print(proxy.put_server(host))
   host_link="http://localhost:"+str(host)
   # Set up logging
   logging.basicConfig(level=logging.INFO)

   server = SimpleXMLRPCServer(
    ('localhost', int(host)),
    logRequests=True,
)
   def get_min(csv_file, since, to, price):
      global headers
      start_time = time.time()
      since=int(since)
      to=int(to)
      df=pd.read_csv(csv_file, skiprows=since, nrows=to)
      df.columns = headers
      min=df[price].min()
      print(min)
      return str(min),  time.time() - start_time

   server.register_function(get_min)
   
   def get_max(csv_file, since, to, price):
      global headers
      start_time = time.time()
      since=int(since)
      to=int(to)
      df=pd.read_csv(csv_file, skiprows=since, nrows=to)
      df.columns = headers
      max=df[price].max()
      print(max)
      return str(max), time.time() - start_time

   server.register_function(get_max)


   server.serve_forever()
except KeyboardInterrupt:
   proxy.close_server(host)
   server.shutdown() 
   print('Exiting')


########################################################################################



