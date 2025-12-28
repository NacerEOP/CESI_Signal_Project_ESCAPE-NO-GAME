import customtkinter
import State
import tkinter


#FUNCTION TO CREATE BUTTONS
def CreateButton(Parent,Text,Width,Height,posx,posy,ANCHOR,command = None):
     # Create and place a button in the window
    custom_font = customtkinter.CTkFont(family="Arial", size=20, weight="bold")
    button = customtkinter.CTkButton(Parent, text=Text,font=custom_font, width=Width, height=Height, command=command)
    button.place(relx = posx ,rely = posy,anchor = ANCHOR)






#FUNCTION TO DRAW THE OPTIONS WINDOW
def OptionsWindow(app,OptionsFrame,func1 = None,func2 = None):
   screen_width = app.winfo_screenwidth()
   screen_height = app.winfo_screenheight()
   if OptionsFrame == None:
       OptionsFrame = customtkinter.CTkFrame(app,width= screen_width/3,height=screen_height*0.7)
       OptionsFrame.place(relx = 0.5,rely = 0.5,anchor = tkinter.CENTER)
       Header = customtkinter.CTkFrame(OptionsFrame,width=OptionsFrame._current_width,height=OptionsFrame._current_height/8)
       Header.place(relx = 0,rely = 0)
       label = customtkinter.CTkLabel(Header,text="Options Menu",font=("Arial",18,"bold"))
       label.place(relx = 0.5,rely =0.5,anchor = tkinter.CENTER)
       #ThemeSwitch = customtkinter.CTkSwitch(OptionsFrame,text="Light Mode",command=lambda: ChangeTheme(ThemeSwitch))
       #ThemeSwitch.place(relx = 0.5,rely =0.15,anchor = tkinter.CENTER)
       ThemeOptionsMenu = customtkinter.CTkOptionMenu(OptionsFrame,values=["Dark Mode","Light Mode"],command=lambda selected: func1(selected))
       ThemeOptionsMenu.place(relx = 0.5,rely =0.25,anchor = tkinter.CENTER)
       if customtkinter.get_appearance_mode() == "Light":
           ThemeOptionsMenu.set("Light Mode")
       CreateButton(OptionsFrame,"Changer de mode",screen_width/10,screen_height/20,0.5,0.7,tkinter.CENTER,command = func2)
   else:
       OptionsFrame.destroy()
       OptionsFrame = None
   State.OptionsFrame = OptionsFrame
   
   
   #FUNCTION TO CREATE AN OPTION BUTTON
def CreateOptionsButton(Parent,app,f1,f2):
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    custom_font = customtkinter.CTkFont(family="Arial", size=20, weight="bold")
    button = customtkinter.CTkButton(Parent, text="Options",font=custom_font, width=screen_width/19, height=screen_height/20, command=lambda: OptionsWindow(app,State.OptionsFrame,func1=f1,func2=f2))
    button.place(relx = 0.01 ,rely = 0.5,anchor = tkinter.W)



#FUNCTION TO CREATE A HEADER
def CreateHeader(app):
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    Header = customtkinter.CTkFrame(app,width=screen_width,height=screen_height/15)
    Header.place(relx =0,rely = 0)    
    return Header


