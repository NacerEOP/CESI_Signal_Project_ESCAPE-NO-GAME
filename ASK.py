import numpy as np
import matplotlib.pyplot as plt
import Text_Converter
import LAN_Com
import threading
import os
import json
CONFIG_FILE = "config/IP.json"
def ModulationASK(BinaryDATA = None,Fp = None,baud = 0.75):
    Fe = 50000
    #Fp = 19000
    
    Nbits = len(BinaryDATA)
    Ns = int(Fe/baud)
    N = Ns*Nbits
    M_Dup = np.repeat(BinaryDATA,Ns)
    t = np.arange(0,N/Fe,1/Fe)
    
    Porteuse = np.sin(2*np.pi*Fp*t)
    data = '192.0.0.0'
    ASK = np.multiply(Porteuse,M_Dup)
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            data = json.load(file)
            data = data.get("IP", '192.0.0.0')  # Default to 192.0.0.0 if not found
    return ASK
    threading.Thread(target=lambda:LAN_Com.Host(ASK,data), daemon=True).start()
    plt.ion()  # Enable interactive mode
    plt.figure(figsize=(12, 6))
    plt.plot(t, ASK)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("ASK Modulated Signal")
    plt.draw()

    
    plt.pause(len(ASK) / Fe)  # Pause for the duration of the sound
    plt.ioff()  # Disable interactive mode after
     


def DemodulationASK(DATA,Fp, baud = 0.75,num = 0.09):
    Fe = 50000
    #Fp = 19000
    
    Limit = np.max(DATA)/2
    for i in DATA:
      if i<Limit:
        i = 0
    Ns = int(Fe/baud)
    Nbits = len(DATA)/Ns
    N = len(DATA)
    t = np.arange(0,N/Fe,1/Fe)
    
    Porteuse = np.sin(2*np.pi*Fp*t)
    Produit = np.abs(DATA)
    y= []           # Résultat de l'intégration    

    for i in range(0,N,Ns):
      y.append (np.trapezoid(Produit[i:i+Ns],t[i:i+Ns]))
    print(y)
    message_demodule = np.array(y) > num   #renvoie True (si >0) ou False sinon
    
    # Decodage du signal démodulé

    message_recu_decode= []

    for ii in range (0,len(message_demodule)):
    
      if message_demodule [ii] > 0:
        
         message_recu_decode.extend([int(1)]) 
      else:
         message_recu_decode.extend([int(-1)]) 
    message_recu_bin =  [0 if i==-1 else 1 for i in message_recu_decode]  #
    return message_recu_bin
    
    