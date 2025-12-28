import numpy as np
import matplotlib.pyplot as plt
import LAN_Com
import threading
import os
import json
CONFIG_FILE = "config/IP.json"
def ModulationFSK(BinaryDATA = None,Fp1 = None,Fp2 = None,baud = 0.75):
    Fe = 50000
    #Fp1 = 19000
    #Fp2 = 20000
    
    Nbits = len(BinaryDATA)
    Ns = int(Fe/baud)
    N = Ns*Nbits
    M_Dup = np.repeat(BinaryDATA, Ns)
    binary_data = np.array(M_Dup)
    inverted_data = 1 - binary_data
    t = np.arange(0, N/Fe, 1/Fe)

    Porteuse1 = np.sin(2*np.pi*Fp1*t)
    Porteuse2 = np.sin(2*np.pi*Fp2*t)
    Port1mult = np.multiply(Porteuse1, M_Dup)
    Port2mult = np.multiply(Porteuse2, inverted_data)

    FSK = np.add(Port1mult, Port2mult)
    data = '192.0.0.0'
    
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            data = json.load(file)
            data = data.get("IP", '192.0.0.0')  # Default to 192.0.0.0 if not found
    return FSK
    threading.Thread(target=lambda:LAN_Com.Host(FSK,data), daemon=True).start()
    plt.ion()
    plt.figure(figsize=(12, 6))
    plt.plot(t, FSK)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("FSK Modulated Signal")
    plt.show()

   
    plt.pause(len(FSK) / Fe)
    plt.ioff()

   


def DemodulationFSK(FSK,Fp1,Fp2,baud = 0.75):
    Fe = 50000
    #Fp1 = 19000
    #Fp2 = 20000
    
    Ns = int(Fe / baud)  # Number of samples per bit
    Nbits = len(FSK) // Ns  # Number of bits
    t = np.arange(0, len(FSK) / Fe, 1 / Fe)  # Time axis
    
    # Generate reference signals
    carrier1 = np.sin(2 * np.pi * Fp1 * t)
    carrier2 = np.sin(2 * np.pi * Fp2 * t)
    
    # Multiply received signal by carriers (coherent detection)
    demod1 = FSK * carrier1
    demod2 = FSK * carrier2
    
    # Integrate over each bit period
    bit_values = []
    for i in range(Nbits):
        segment1 = np.sum(demod1[i * Ns : (i + 1) * Ns])  # Sum energy in Fp1
        segment2 = np.sum(demod2[i * Ns : (i + 1) * Ns])  # Sum energy in Fp2
        bit_values.append(1 if segment1 > segment2 else 0)  # Decide based on stronger frequency

    return np.array(bit_values)  # Return recovered binary data