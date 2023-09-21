import customtkinter as ctk,pandas as pd,numpy as np
from tkinter import *
from PIL import Image,ImageTk
import tkinter.ttk
import PIL,time,socket,sqlalchemy,pyodbc,fsspec,urllib,mysql.connector,cv2,threading
import tkvideo
import pygame,os,pyaudio
from vosk import Model, KaldiRecognizer

#global var
i=1
photo="myimage_log.png"

def speak_recog():
    model = Model("C:/Users/Administrator/PycharmProjects/pythonProject2/vosk/vosk-model-small-en-in-0.4")
    recognizer = KaldiRecognizer(model, 16000)

    mic = pyaudio.PyAudio()
    print("your voice is recorded")
    time.sleep(1.5)
    stream = mic.open(rate=16000, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=8192)
    stream.start_stream()

    while True:
        data = stream.read(4096)
        if len(data) == 0:
            print("unable to recognizze your voice")

        elif recognizer.AcceptWaveform(data):
            result_1 = recognizer.Result()
            result_final= result_1[14:-3]
            print(result_final)
            break

def register_page():
    login_frame.configure(height=250, width=300)
    for widgets in login_frame.winfo_children():
        widgets.destroy()
    reg_name=ctk.CTkLabel(login_frame,text="Name",text_color=("white","black"))
    reg_name.grid(row=0,column=0)
    reg_phone = ctk.CTkLabel(login_frame, text="phone No.", text_color=["white","black"])
    reg_phone.grid(row=1, column=0)
    reg_email = ctk.CTkLabel(login_frame, text="Email", text_color=["white","black"])
    reg_email.grid(row=2, column=0)
    reg_username = ctk.CTkLabel(login_frame, text="UserName", text_color=["white","black"])
    reg_username.grid(row=3, column=0)
    reg_password = ctk.CTkLabel(login_frame, text="PassWord", text_color=["white","black"])
    reg_password.grid(row=4, column=0)
    reg_entry_name = ctk.CTkEntry(login_frame, text_color=["black", "white"])
    reg_entry_name.grid(row=0, column=1)
    reg_entry_phone = ctk.CTkEntry(login_frame, text_color=["black", "white"])
    reg_entry_phone.grid(row=1, column=1)
    reg_entry_email = ctk.CTkEntry(login_frame, text_color=["black", "white"])
    reg_entry_email.grid(row=2, column=1)
    reg_entry_username = ctk.CTkEntry(login_frame, text_color=["black", "white"])
    reg_entry_username.grid(row=3, column=1)
    reg_entry_password = ctk.CTkEntry(login_frame, text_color=["black", "white"])
    reg_entry_password.grid(row=4, column=1)
    submit_reg_button=ctk.CTkButton(login_frame,text="Submit",command=lambda:reg_submit(reg_entry_password.get(),reg_entry_username.get(),reg_entry_name.get(),reg_entry_phone.get(),reg_entry_email.get()))
    submit_reg_button.grid(row=5,column=0,columnspan=2)

def reg_submit(EP,EU,EN,EPN,EE):
    print("password:->",EP)
    print("username:->",EU)
    print("Name:->",EN)
    print("PHOne:->",EPN)
    print("EMAIL:->",EE)
    mydb=mysql.connector.connect(host='localhost', password='vishal', user='root', database='data')
    mycursor=mydb.cursor()
    try:
        mycursor.execute("insert into login values("+'''"'''+EN+'''","'''+EPN+'''","'''+EE+'''","'''+EU+'''","'''+EP+'''")''')
        print("sucess updated ")
        mydb.commit()
    except:
        print("ERROR !!!")
    login_frame.destroy()
    main()

def main():
    get_audio()
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("play_current.mp3")
    my_lect_label=Label(Nav_bar)
    player = tkvideo.tkvideo("C://Users//Admin//Downloads//Heartbeat.S01e06.720p.x264.Korean.Msubs.MoviesMod.com.mkv",my_lect_label, loop=1, size=(1280, 720))
    pygame.mixer.music.play()
    player.play()

    my_lect_label.place(relx=.05,y=0,relwidth=.9,relheight=.9,rely=0.05)

def get_audio():
    if "play_current.mp3" in os.listdir(os.getcwd()):
        pass
    else:
        from moviepy.editor import VideoFileClip
    # Load the MP4 file
        video = VideoFileClip("C://Users//Admin//Downloads//Heartbeat.S01e06.720p.x264.Korean.Msubs.MoviesMod.com.mkv")
    # Extract the audio
        audio = video.audio
    # Save the audio as an MP3 file
        audio.write_audiofile("play_current.mp3")


def check(user_get,pass_get):
    mydb = mysql.connector.connect(host='localhost', password='vishal', user='root', database='data')
    mycursor=mydb.cursor()

    try:
        mycursor.execute("select username from login")
    except:
        print("can't connect try again !!!")
        return
    users=mycursor.fetchall()
    print(users)
    j=0
    try:
        while (len(users[j][0])!=0):
            user=users[j][0]
            print(user)
            j=j+1
            if (user_get.get()==user):
                mycursor.execute("select password from login where username="+'''"'''+user+'''"''')
                Correct_pas=mycursor.fetchall()
                print(Correct_pas)
                if (pass_get.get()==Correct_pas[0][0]):
                    print("login sucessful")
                    login_frame.place_forget()
                    background_log_label.destroy()
                    main()
                    # for widgets in login_frame.winfo_children():
                    #     widgets.destroy()
                    break
                else:
                    print("enter correct password")
                    break
            elif(user_get.get()!=user):(
                print("enter correct user name"))
            else:
                pass
    except:
        print("error ocured vishal")
        pass


def Appear(self):
    global i
    i=i+1
    if (i%2)==0:
        main_window._set_appearance_mode("dark")
        Nav_bar.configure(fg_color=color[1])
        login_frame.configure(fg_color=color[1])
        user_label.configure(text_color=color[0])
        pass_label.configure(text_color=color[0])
    else:
        main_window._set_appearance_mode("light")
        Nav_bar.configure(fg_color=color[0])
        login_frame.configure(fg_color=color[0])
        user_label.configure(text_color=color[1])
        pass_label.configure(text_color=color[1])

color=("white","black")


main_window=ctk.CTk()
main_window.maxsize(880,580)
main_window._set_appearance_mode("light")
main_window.geometry("360x480")

def image_resizer(event):
    global photo
    image=Image.open("log_bag.jpeg")
    win_hei=main_window.winfo_height()
    win_wid=main_window.winfo_width()
    new_image =image.resize((win_hei,win_wid))
    new_image. save('myimage_log1.png')
    photo="myimage_log1.png"
    return photo

photo1=tkinter.PhotoImage(file='myimage_500.png')
photo_log=tkinter.PhotoImage(file=photo)

# intialation
Nav_bar=ctk.CTkFrame(main_window,fg_color=color[0])

background_log_label=ctk.CTkLabel(Nav_bar,text="",image=photo_log)
background_log_label.place(relx=0.5,rely=0.5,anchor="center")

login_frame=ctk.CTkFrame(Nav_bar,fg_color=color[0],height=200,width=250)

user_label=ctk.CTkLabel(login_frame,text="USERNAME",text_color=color[1])
user_label.grid(row=0,column=0)
pass_label=ctk.CTkLabel(login_frame,text="PASSWORD",text_color=color[1])
pass_label.grid(row=1,column=0)
pass_get=ctk.StringVar()
pass_entry=ctk.CTkEntry(login_frame,text_color="red",textvariable=pass_get)
pass_entry.grid(row=1,column=1)
user_get=ctk.StringVar()
user_entry=ctk.CTkEntry(login_frame,text_color="blue",textvariable=user_get)
user_entry.grid(row=0,column=1)

login_butt=ctk.CTkButton(login_frame,text="login",corner_radius=50,hover_color='blue',command=lambda:check(user_get,pass_get))
login_butt.grid(row=2,column=0)
register_butt=ctk.CTkButton(login_frame,text="register",corner_radius=50,hover_color='blue',command=register_page)
register_butt.grid(row=2,column=1)

login_frame.place(anchor="center",relx=0.5,rely=0.5)

Nav_bar.pack(side='top',fill='both',expand=True)

button1=ctk.CTkButton(main_window,text="",image=photo1,corner_radius=55,bg_color=color[0],fg_color=color[0],width=30,command=lambda:Appear(main_window))
button1.pack(side="right")

#main_window.bind('<Configure>',image_resizer)
main_window.mainloop()