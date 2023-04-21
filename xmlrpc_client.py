import xmlrpc.client
import config
import tkinter as tk
from tkinter.filedialog import askopenfilename
import subprocess
import numpy as np
import time
proxy_cluster = xmlrpc.client.ServerProxy('http://localhost:'+str(config.CLUSTER))

# esto lo metemos en un for y vamos tratando uno a uno + tratamiento de errores
# proxy_server1 = xmlrpc.client.ServerProxy('http://localhost:9001')
# proxy_server2 = xmlrpc.client.ServerProxy('http://localhost:9002')
import os

m_list=[]
filename =None
price=None
#---in_csv: path del archivo
#---rowsize: numero de linias por archivo ó numero de nodos
def UploadAction(event=None):
    global filename
    filename = askopenfilename(initialdir='.')
    # Cut path to the file off
    filename = filename.split('/')[len(filename.split('/'))-1]
    print('Selected:', filename)
    label1['text'] = filename


def UploadAction2(min_max):
      
      global filename
      number_lines = sum(1 for row in (open(filename)))
      list_servers=proxy_cluster.get_servers()
      chunksize = round(number_lines/len(list_servers))
      since=0
      totaltime=0
      time_worker=0
      start_time = time.time()
      if min_max == "min":
            for server in list_servers:
                  minn,time_worker=xmlrpc.client.ServerProxy('http://localhost:'+str(server)).get_min(filename, since, chunksize, price)
                  totaltime=totaltime+float(time_worker)
                  m_list.append(minn)
                  since=since+chunksize
            x = np.array(m_list)
            y = x.astype(np.float64)
            min_value=min(y)
            label2['text'] = min_value
      elif min_max == "max":
            for server in list_servers:
                  maxx,time_worker=xmlrpc.client.ServerProxy('http://localhost:'+str(server)).get_max(filename, since, chunksize, price)
                  totaltime=totaltime+float(time_worker)
                  m_list.append(maxx)
                  since=since+chunksize
            x = np.array(m_list)
            y = x.astype(np.float64)
            max_value=max(y)
            label2['text'] = max_value
######elif --> more options"      
      else:     
            label2['text'] = "ERROR: Please, select min or max price"
      print("Total Time : "+str(time.time() - start_time)+" seconds in "+str(len(list_servers))+" worker/s")
      print("Time without connexions: "+str(totaltime)+" seconds in "+str(len(list_servers))+" worker/s")

def UploadAction3(price_input):
      global price
      price=price_input
      
      # Cut path to the file off
def UploadAction4(event=None):
     subprocess.call('start python xmlrpc_server.py', shell=True)
     label4['text'] = str(int(label4['text'])+1)
      
      # Cut path to the file off
        
        


subprocess.call('start python xmlrpc_cluster.py', shell=True)
root= tk.Tk(className='Tick prices')
root.geometry("500x500")  

button1 = tk.Button(text='Select File', command=UploadAction, bg='blue', fg='white')
button1.pack(padx=2, pady=5)
label1 = tk.Label(text='Please choose a file')
label1.pack(padx=2, pady=2)
label2 = tk.Label()

button7 = tk.Button(text='Add worker', command=UploadAction4, bg='blue', fg='white')
button7.pack(padx=2, pady=5)
label4 = tk.Label( text='0')
label4.pack(padx=2, pady=2)

label6 = tk.Label(text='----------------Select price type-----------------')
label6.pack(padx=2, pady=2)
button3 = tk.Button(text='Ask', command=lambda:UploadAction3('Ask'), bg='brown', fg='white')
button3.pack(padx=2, pady=5)
button4 = tk.Button(text='Bid', command=lambda:UploadAction3('Bid'), bg='brown', fg='white')
button4.pack(padx=2, pady=5)
button5 = tk.Button(text='AskVolume', command=lambda:UploadAction3('AskVolume'), bg='brown', fg='white')
button5.pack(padx=2, pady=5)
button6 = tk.Button(text='BidVolume', command=lambda:UploadAction3('BidVolume'), bg='brown', fg='white')
button6.pack(padx=2, pady=5)

label3 = tk.Label(text='---------------------------------------------------------')
label3.pack(padx=2, pady=2)
button2 = tk.Button(text='Compute Low price', command=lambda:UploadAction2("min"), bg='red', fg='white')
button2.pack(padx=2, pady=5)
button8 = tk.Button(text='Compute High price', command=lambda:UploadAction2("max"), bg='green', fg='white')
button8.pack(padx=2, pady=5)
label2.pack(padx=2, pady=2)

root.mainloop()
