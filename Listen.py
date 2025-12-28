import pyaudio
import wave
import numpy as np
from scipy.signal import periodogram
import threading
import sounddevice as sd
import time
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
import State
Running = False
Recording = False
HighAVRG = 0
testDONE = False
Recorded = []
RecordTimeMarker = 0


def DrawGraph(t,Recorded):
    
    plt.figure(figsize=(12, 8))
    plt.plot(t, Recorded)
    plt.show()  # Allows Tkinter to continue running

def filter_frequencies(audio_data, rate, keep_freqs, tol=1.0):
    # Compute FFT of the signal
    audio_data = audio_data.astype(np.float32) / np.iinfo(np.int16).max
    spectrum = fft(audio_data)
    freqs = np.fft.fftfreq(len(audio_data), d=1/rate)

    # Create a mask to keep only desired frequencies (allowing a small tolerance)
    mask = np.zeros_like(freqs, dtype=bool)
    for f in keep_freqs:
        mask |= np.abs(freqs - f) < tol  # Allow some tolerance in frequency matching

    # Apply mask to keep only selected frequencies
    filtered_spectrum = np.zeros_like(spectrum, dtype=complex)
    filtered_spectrum[mask] = spectrum[mask]

    # Convert back to time-domain
    filtered_audio = np.real(ifft(filtered_spectrum))
    
    return filtered_audio



def MAX(Val):
    global HighAVRG
    if Val>HighAVRG:
        HighAVRG = Val
def Calibrate(TargetFreq):
    global testDONE,HighAVRG
    RATE = 50000 
    t = np.arange(0,10,1/RATE)
    SinWAVE = 0.01*np.sin(2*np.pi*TargetFreq*t)
    sd.play(SinWAVE,samplerate=RATE)
    sd.wait()
    time.sleep(1)
    HighAVRG = HighAVRG/1.2
    testDONE = True

def Listen_MIC(TargetFreq):
  global Running,Recorded,Recording,RecordTimeMarker,testDONE
  Running = True
  testDONE = False
  # Audio Settings
  FORMAT = pyaudio.paInt16  # 16-bit audio format
  CHANNELS = 1  # Mono audio
  RATE = 50000  # Sampling rate (Hz)
  CHUNK = 1024  # Buffer size
  Findex = int(CHUNK*TargetFreq[0]/RATE)
  # Initialize PyAudio
  audio = pyaudio.PyAudio()

  # Open the Microphone Stream
  stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

 
  thread = threading.Thread(target=Calibrate, args=(TargetFreq[0],))
  thread.daemon = True  # Allows program to exit without waiting for thread
  thread.start()
  
  try:
      while Running == True:
         
         raw_data = stream.read(CHUNK)  # Read microphone input (raw bytes)
         audio_data = np.frombuffer(raw_data, dtype=np.int16)  # Convert to NumPy array (int16)
            
         f,PXX = periodogram(audio_data,RATE)
         if testDONE == False:
            try:
                State.Status.configure(text="Calibrating...")
            except:
                print("Shutting down mic listen")
                Running = False
            MAX(np.average(PXX[Findex])) 
         elif testDONE == True:
            
            if PXX[Findex] > HighAVRG:
                Recording = True
                RecordTimeMarker = time.time()
            elif PXX[Findex] < HighAVRG and Recording == True:
                if time.time() - RecordTimeMarker > 10:
                    Recording = False
                    Running = False
            else:
              try:
                State.Status.configure(text="Ready to record")
              except:
                print("Shutting down mic listen")
                Running = False
       
         if Recording == True:
             Recorded.extend(filter_frequencies(audio_data, RATE, TargetFreq, tol=100))
             try:
                State.Status.configure(text=f"Magnitude de fréquence:{int(PXX[Findex])},seuil:{int(HighAVRG)}")
             except:
                print("Shutting down mic listen")
                Running = False
         print(f[Findex],PXX[Findex],HighAVRG)
         
        
  except: 
      print("Error while trying to listen to mic")

  # Cleanup
  stream.stop_stream()
  stream.close()
  audio.terminate()
  try:
                State.Status.configure(text="Status")
  except:
                print("Where is the status?")
                
  
  t = np.linspace(0, len(Recorded) / RATE, len(Recorded))
  State.GraphThread = threading.Thread(target=DrawGraph, args=(t,Recorded)).start()
  Saved = Recorded
  Recorded = []
  return Saved
def Stop():
    Running = False


def PlaySound(DATA):
    Fe = 50000
    
    
    sd.play(DATA,Fe)
    sd.wait()