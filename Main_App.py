import tkinter
import tkinter.filedialog
import customtkinter
import os
import json
from PIL import Image, ImageTk
from ctypes import windll
import UI_Drawer
import State
import Text_Converter as TC
import ASK
import FSK
import LAN_Com
import Trame_Send
import Trame_Recieve
import Codage_Manchester
import threading
import Listen
import sys
#from threading import Thread, Event
# Function to get the base directory for accessing files
def get_base_path():
    if getattr(sys, 'frozen', False):  # If running as a compiled .exe
        return sys._MEIPASS  # Temporary folder used by PyInstaller
    return os.path.dirname(os.path.abspath(__file__))  # Normal script directory

# Resolve config file paths
BASE_PATH = get_base_path()
CONFIG_FILE = os.path.join(BASE_PATH, "config", "config.json")
IP_FILE = os.path.join(BASE_PATH, "config", "IP.json")
f_FILE = os.path.join(BASE_PATH, "config", "Freq1.json")
f2_FILE = os.path.join(BASE_PATH, "config", "Freq2.json")

# Ensure the config directory exists
os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)

customtkinter.set_default_color_theme(os.path.join(BASE_PATH, "themes", "custom_theme.json"))

# Function to save the selected theme
def save_theme(theme):
    with open(CONFIG_FILE, "w") as file:
        json.dump({"theme": theme}, file)

# Function to load the saved theme
def load_theme():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            data = json.load(file)
            return data.get("theme", "Dark")  # Default to "Dark" if not found
    return "Dark"

# Function to save the IP address
def save_IP(IP):
    with open(IP_FILE, "w") as file:
        json.dump({"IP": IP}, file)

# Function to load the saved IP
def load_IP():
    if os.path.exists(IP_FILE):
        with open(IP_FILE, "r") as file:
            data = json.load(file)
            return data.get("IP", '192.0.0.0')  
    return '192.0.0.0'

# Function to save frequency f1
def save_f(F):
    with open(f_FILE, "w") as file:
        json.dump({"f": F if 0 < F < 23000 else 1000}, file)

# Function to load frequency f1
def load_f():
    if os.path.exists(f_FILE):
        with open(f_FILE, "r") as file:
            data = json.load(file)
            val = data.get("f", 1000)
            return val if 0 < val < 23000 else 1000
    return 1000

# Function to save frequency f2
def save_f2(F):
    with open(f2_FILE, "w") as file:
        json.dump({"f": F if 0 < F < 23000 else 2000}, file)

# Function to load frequency f2
def load_f2():
    if os.path.exists(f2_FILE):
        with open(f2_FILE, "r") as file:
            data = json.load(file)
            val = data.get("f", 2000)
            return val if 0 < val < 23000 else 2000
    return 2000

customtkinter.set_appearance_mode(load_theme())
# Get the path to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the script
image_dir = os.path.join(script_dir, "images")  # Path to the 'images' folder

# Create the main window
app = customtkinter.CTk()
app.resizable(False,False)

# Get the screen width and height
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Set the window size to cover the whole screen but keep borders (taskbar and window controls visible)
app.attributes("-fullscreen", True)
app.title("Prototype Signal")
GroupeCredit = customtkinter.CTkLabel(app,text="Groupe 4",font=("Arial",20,"bold"),width=screen_width/9,height=screen_height/12,text_color="#3FAFF1")
GroupeCredit.place(relx = 0.01,rely = 0.9)
# Global variable to store image label and opacity level
currentMod = None
logo_label = None
opacity = 0
posX = 0.5
z = 1
Debounce = True
ExistingButtons = ()

#col = 0
#row = 0



#FUNCTION TO GET IMAGE LABELS
def GetIMG(IMG, IMGlabel, sizex, sizey):
    global logo_label  # Ensure we're working with the global logo_label
  
    if os.path.exists(image_dir):
        image_path = os.path.join(image_dir, IMG)
        if os.path.exists(image_path):
            img = Image.open(image_path).convert("RGBA")
            r, g, b, alpha = img.split()
            alpha = alpha.point(lambda p: int(p * opacity))
            img = Image.merge("RGBA", (r, g, b, alpha))

            # Create a CTkImage instead of PhotoImage
            img_tk = customtkinter.CTkImage(img, size=(sizex, sizey))

            # If the label already exists, just update its image
            if logo_label:
                logo_label.configure(image=img_tk)
                logo_label.image = img_tk
            else:
                # Create a new label if it doesn't exist
                image_label = customtkinter.CTkLabel(app, image=img_tk, text="")
                image_label.image = img_tk
                image_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
                logo_label = image_label

            return logo_label
        else:
            print("Image not found!")
            return False
    else:
        print("Images folder does not exist!")
        return False




#FUNCTION TO SAVE THEME/LOAD THEME
def ChangeTheme(state):
    if state == "Dark Mode":
        customtkinter.set_appearance_mode("Dark")
        save_theme("Dark")
    elif state == "Light Mode":
        customtkinter.set_appearance_mode("Light")
        save_theme("Light")

def SignalTransmit(TextInput,ModType,IPin,TransmitTYPE,F1,F2):
    State.Status.configure(text = "Status")
    F1 = int(F1.get("1.0", "end-1c"))
    F2 = int(F2.get("1.0", "end-1c"))
    if not F1 > 0 and not F1 < 23000:
             F1 = 1000
    if not F2 > 0 and not F2 < 23000:
             F2 = 2000
    save_f(F1)
    save_f2(F2)
    message = TextInput.get("1.0", "end-1c")
    if TransmitTYPE.get() == "LAN":
     IP = IPin.get("1.0", "end-1c")
     save_IP(IP)
     if message != "":
         modulation_type = ModType.get()
         Binary_Msg = TC.text_to_binary(message)
         Tramed_Msg = Trame_Send.add_trame_to_message(Binary_Msg)
         Coded_Msg = Codage_Manchester.codage(Tramed_Msg)
         modulated = None
       
         if modulation_type == "ASK":
             modulated = ASK.ModulationASK(BinaryDATA=Coded_Msg,Fp=F1,baud=20)
         elif modulation_type == "FSK":
             modulated = FSK.ModulationFSK(BinaryDATA=Coded_Msg,Fp1=F1,Fp2=F2,baud=20)
         threading.Thread(target=lambda:LAN_Com.Host(modulated,IP), daemon=True).start()
     else:    
         print("there has to be a text input")
    elif TransmitTYPE.get() == "Son":
        
        
        if message != "":
         modulation_type = ModType.get()
         Binary_Msg = TC.text_to_binary(message)
         #Tramed_Msg = Trame_Send.add_trame_to_message(Binary_Msg)
         Coded_Msg = Codage_Manchester.codage(Binary_Msg)
         modulated = None
         
         if modulation_type == "ASK":
             modulated = ASK.ModulationASK(BinaryDATA=Coded_Msg,Fp=F1)
         elif modulation_type == "FSK":
             State.Status.configure(text = "La communication par son ne prend pas en charge la modulation FSK")
         try:    
            threading.Thread(target=lambda:Listen.PlaySound(modulated), daemon=True).start()
         except:
            print("No Sound to play")
     

def SignalRecieve(DemodType,TypeDeRec,F1,F2):   
      global currentMod
      State.Status.configure(text = "Status")
      F1 = int(F1.get("1.0", "end-1c"))
      F2 = int(F2.get("1.0", "end-1c"))
      if not F1 > 0 and not F1 < 23000:
             F1 = 1000
      if not F2 > 0 and not F2 < 23000:
             F2 = 2000
      save_f(F1)
      save_f2(F2)
      Label = State.RLabel
      modulation_type = DemodType.get()
      if TypeDeRec.get() == "LAN":
        Recept = LAN_Com.Client()    
        
        Unmod_Msg =  None
        if modulation_type == "ASK":
             Unmod_Msg = ASK.DemodulationASK(Recept,F1,baud = 20,num=0)
        elif modulation_type == "FSK":
             Unmod_Msg = FSK.DemodulationFSK(Recept,F1,F2,baud = 20)   
      
        DeCoded_Msg = Codage_Manchester.Decodage(Unmod_Msg)
        UnTramed_Msg = Trame_Recieve.retrieve_message_from_trame(DeCoded_Msg)
        print(UnTramed_Msg)
        Original_Msg = TC.binary_to_text(UnTramed_Msg)
        Label.configure(text=Original_Msg)
      
        print(Unmod_Msg,DeCoded_Msg,Original_Msg)
        print(currentMod)
        
      elif TypeDeRec.get() == "Son":
          
          Recept = None
         
          
          
          Unmod_Msg =  None
          if modulation_type == "ASK":
             Recept = Listen.Listen_MIC([F1])
             Unmod_Msg = ASK.DemodulationASK(Recept,F1)
          elif modulation_type == "FSK":
             State.Status.configure(text = "La communication par son ne prend pas en charge la démodulation FSK")
          try:
           DeCoded_Msg = Codage_Manchester.Decodage(Unmod_Msg)
           #UnTramed_Msg = Trame_Recieve.retrieve_message_from_trame(DeCoded_Msg)
           #print(UnTramed_Msg)
           Original_Msg = TC.binary_to_text(DeCoded_Msg)
           Label.configure(text=Original_Msg)
      
           print(Unmod_Msg,DeCoded_Msg,Original_Msg)
           print(currentMod)
          except:
            print("No message to demodulate")
           
            
#FUNCTION TO DRAW THE SIGNAL SENDING SCREEN INTERFACE
def SendScreen():
    global currentMod
    currentMod = "Sscreen"
    for widget in app.winfo_children():
        widget.destroy()

    Header = UI_Drawer.CreateHeader(app)

    label = customtkinter.CTkLabel(Header, text="Send Screen", font=("Arial", 24, "bold"))
    label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
  
    UI_Drawer.CreateOptionsButton(Header, app, ChangeTheme, ChooseMODE)
    frame = customtkinter.CTkFrame(app,width=screen_width/1.5,height=screen_height/1.5)
    frame.place(relx = 0.5,rely = 0.5,anchor = tkinter.CENTER)
    TextInput = customtkinter.CTkTextbox(frame, width=screen_width/4, height=screen_height/15)
    TextInput.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    ModTypeSl = customtkinter.CTkOptionMenu(frame, values=["ASK", "FSK"])
    ModTypeSl.place(relx=0.7, rely=0.7, anchor=tkinter.CENTER)

    #NoiseCheckbox = customtkinter.CTkCheckBox(frame, text="Ajouter du bruit")
    #NoiseCheckbox.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
    TypeDeTransmi = customtkinter.CTkOptionMenu(frame,values=["LAN","Son"])
    TypeDeTransmi.place(relx  = 0.5,rely = 0.02,anchor = "n")
    IPLABEL = customtkinter.CTkLabel(frame,text="Client IP:")
    IPLABEL.place(relx=0.02, rely=0.5, anchor="w")
    FP1LABEL = customtkinter.CTkLabel(frame,text="Fp1:")
    FP1LABEL.place(relx=0.02, rely=0.6, anchor="w")
    FP2LABEL = customtkinter.CTkLabel(frame,text="Fp2:")
    FP2LABEL.place(relx=0.02, rely=0.7, anchor="w")
    IPInput = customtkinter.CTkTextbox(frame, width=screen_width/10, height=screen_height/15)
    IPInput.place(relx=0.1, rely=0.5, anchor="w")
    IPInput.delete("1.0", "end")  # Clear all text
    IPInput.insert("1.0", load_IP())  # Insert new text
    F1 = customtkinter.CTkTextbox(frame, width=screen_width/10, height=screen_height/15)
    F1.place(relx=0.1, rely=0.6, anchor="w")
    F1.delete("1.0", "end")  # Clear all text
    F1.insert("1.0", str(load_f()))  # Insert new text
    F2 = customtkinter.CTkTextbox(frame, width=screen_width/10, height=screen_height/15)
    F2.place(relx=0.1, rely=0.7, anchor="w")
    F2.delete("1.0", "end")  # Clear all text
    F2.insert("1.0", str(load_f2()))  # Insert new text
    State.ClientIPtext = IPInput
    State.Status = customtkinter.CTkLabel(frame,width=frame._current_width,height=frame._current_height/8,text="Status")
    State.Status.place(relx=0.5,rely=1,anchor = "s")
    
    TransmitButton = customtkinter.CTkButton(frame, text="Transmettre le signal",command=lambda:SignalTransmit(TextInput,ModTypeSl,IPInput,TypeDeTransmi,F1,F2))
    TransmitButton.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

def RunThread(DeModTypeSl,TypeDeRec,F1,F2):
    if State.RunningThread and State.RunningThread.is_alive():
        running_thread = None
    State.RunningThread = threading.Thread(target=lambda:SignalRecieve(DeModTypeSl,TypeDeRec,F1,F2), daemon=True)
    State.RunningThread.start()
    
    
#FUNCTION TO DRAW THE SIGNAL RECIEVING INTERFACE
def RecieveScreen():
    global currentMod
    currentMod = "Rscreen"
    State.RecieveState = False
    LAN_Com.stop_server()
    for widget in app.winfo_children():
        widget.destroy()
    Header = UI_Drawer.CreateHeader(app)
    label = customtkinter.CTkLabel(Header, text="Recieve Screen", font=("Arial", 24, "bold"))
    label.place(relx = 0.5,rely = 0.5,anchor = tkinter.CENTER)
    
    UI_Drawer.CreateOptionsButton(Header,app,ChangeTheme,ChooseMODE)
    #State.FileGrid = UI_Drawer.CreateFileDir(app,func = Files_Manager.Add_Row)
    #Files_Manager.UpdateImpFilesDisplay(app)
   
    frame = customtkinter.CTkFrame(app,width=screen_width/1.5,height=screen_height/1.5)
    frame.place(relx = 0.5,rely = 0.5,anchor = tkinter.CENTER)
    State.RLabel = customtkinter.CTkLabel(frame, width=screen_width/3, height=screen_height/15,text="le message recu s'affichera ici")
    State.RLabel.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    DeModTypeSl = customtkinter.CTkOptionMenu(frame, values=["ASK", "FSK"])
    DeModTypeSl.place(relx=0.7, rely=0.7, anchor="w")
    TypeDeRec = customtkinter.CTkOptionMenu(frame,values=["LAN","Son"])
    TypeDeRec.place(relx  = 0.5,rely = 0.02,anchor = "n")
    fLABEL = customtkinter.CTkLabel(frame,text="Frequences (Fp1&Fp2):")
    fLABEL.place(relx=0.02, rely=0.5, anchor="w")
    F1 = customtkinter.CTkTextbox(frame, width=screen_width/10, height=screen_height/15)
    F1.place(relx=0.1, rely=0.6, anchor="w")
    F1.delete("1.0", "end")  # Clear all text
    F1.insert("1.0", str(load_f()))  # Insert new text
    F2 = customtkinter.CTkTextbox(frame, width=screen_width/10, height=screen_height/15)
    F2.place(relx=0.1, rely=0.7, anchor="w")
    F2.delete("1.0", "end")  # Clear all text
    F2.insert("1.0", str(load_f2()))  # Insert new text
    State.Status = customtkinter.CTkLabel(frame,width=frame._current_width,height=frame._current_height/8,text="Status")
    State.Status.place(relx=0.5,rely=1,anchor = "s")
    LAN_Com.stop_server()
    Listen.Stop()
    if State.RunningThread and State.RunningThread.is_alive():
        running_thread = None
    State.RunningThread = threading.Thread(target=lambda:SignalRecieve(DeModTypeSl,TypeDeRec,F1,F2), daemon=True)
    
    RecButton = customtkinter.CTkButton(frame, text="Ecouter/Arreter",command=lambda:RunThread(DeModTypeSl,TypeDeRec,F1,F2))
    RecButton.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
       
       
   
    
#FUNCTION TO CHOOSE THE MODE (SENDER/RECIEVER)
def ChooseMODE():
    currentMod = None
    LAN_Com.stop_server()
    for widget in app.winfo_children():
        widget.destroy()
    UI_Drawer.CreateButton(app,"Transmeteur", screen_width / 2, screen_height, 0, 0, "nw",  command =SendScreen)
    UI_Drawer.CreateButton(app,"Recepteur", screen_width / 2, screen_height, 0.5, 0, "nw", command = RecieveScreen)
    label = customtkinter.CTkLabel(app,text="Choose a mode of operation",font=("Arial",24,"bold"))
    label.place(relx = 0.5,rely = 0.1, anchor = tkinter.CENTER)



#FUNCTION OF THE LOGO INTRO
def LOGOintro():
    global opacity, logo_label, z, Debounce

    # Gradually increase opacity
    if opacity < 1.0 and Debounce == True:
        opacity += 0.03  # Increase opacity slightly
        z += 1.5
        # If the logo_label doesn't exist, create it

        logo_label = GetIMG("MainLOGO.png", logo_label, 800 + z, 600 + z)

        app.after(50, LOGOintro)  # Call the function again after 50ms
    elif opacity < 10:
        Debounce = False
        opacity -= 0.2  # Increase opacity slightly
        z += 2
        # If the logo_label doesn't exist, create it

        logo_label = GetIMG("MainLOGO.png", logo_label, 800 + z, 600 + z)

        app.after(50, LOGOintro)  # Call the function again after 50ms

    if opacity < 0 and Debounce == False:
        Debounce = True
        opacity = 12
        if logo_label is not None:
            logo_label.destroy()
            logo_label = None  # Reset the global variable
            ChooseMODE()

#ChooseMODE()
LOGOintro()




# Run the app
app.mainloop()
