#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 23:08:15 2020

@author: user
"""

from tkinter import *
import re
import tkinter as tk
from tkinter import filedialog as fd 


files=[]

def callback_text():
    name= fd.askopenfilename() 
    print(name)
    print()
    return files.append(name)
def callback_image():
    name= fd.askopenfilename() 
    print(name)
    print()
    
    return files.append(name)
def callback_sound():
    name= fd.askopenfilename() 
    print(name)
    print()
    
    return files.append(name)

def callback_save():
    name= fd.asksaveasfilename() 
    print(name)
    print()
    
    return files.append(name)

def callback_process():
    for i in files:
        print(i)
    if len(files)==4:
        txt_file=files[0]
        image_file=files[1]
        sound_file=files[2]
        save_file=files[3]
        return video_render(txt_file, image_file, sound_file, save_file)
    else:
        print('Not all files have been selected')
        
def video_render(txt_file,image_file,sound_file,save_file):
        from moviepy.editor import ImageClip
        from moviepy.editor import CompositeVideoClip
        from moviepy.editor import CompositeAudioClip
        from moviepy.editor import TextClip
        from moviepy.editor import AudioFileClip
        from moviepy.editor import concatenate
        from moviepy.config import change_settings
        change_settings({"IMAGEMAGICK_BINARY": "/usr/local/bin/convert"})
        text=[]
        
        with open(txt_file,'r') as file:
            for lines in file:
                if lines!="\n":
                    text.append(lines.rstrip('\n'))
        durs=[]
        for i in text:            
            res = len(re.findall(r'\w+', i)) 
            if res/2>3:
                durs.append(res/2)
            else:
                durs.append(3)
        total_duration=sum(durs)
        
        a_clip = AudioFileClip(sound_file)
        if a_clip.duration<total_duration:
            new_audioclip = CompositeAudioClip([a_clip, a_clip.set_start(a_clip.duration-1)]).set_duration(total_duration+3)
        else:
            new_audioclip=a_clip.set_duration(total_duration+3)
        
        screen=(1920,1080)
        clip_list = []
        i=0
        for string in text:
            duration=durs[i]
            i+=1
            try:
                txt_clip = TextClip(string, fontsize = 70, color = 'white', method='caption',size=screen ).set_duration(duration).set_pos('center')
                clip_list.append(txt_clip)
            except UnicodeEncodeError:
                txt_clip = TextClip("Issue with text", fontsize = 70, color = 'white').set_duration(2) 
                clip_list.append(txt_clip)
        
        final_text_clip = concatenate(clip_list, method = "compose").set_start(3)  
            
        v_clip = ImageClip(image_file).set_duration(total_duration+3)
        video=CompositeVideoClip([v_clip, final_text_clip])
        # video = video.set_audio(AudioFileClip('sound/Serenity (1).mp3'))
        video = video.set_audio(new_audioclip)
        video.write_videofile(save_file, 
                              codec='libx264',
                              fps=10, 
                              threads=4,
                              audio_codec='aac', 
                              temp_audiofile='temp-audio.m4a', 
                              remove_temp=True
                              )

    

window=Tk()
window.wm_title('Title-Image-Sound --> Video automatic unit')
  
errmsg = 'Error!'

b0=Button(window,text="Click to Process", width=40,
          command=callback_process)
b0.grid(row=5,column=2)

b1=Button(window,text='Click to Open Text File',width=40, 
       command=callback_text)
b1.grid(row=2,column=1)
b2=Button(window,text='Click to Open Image File', width=40,
       command=callback_image)
b2.grid(row=3,column=1)
b3=Button(window,text='Click to Open Sound File', width=40,
       command=callback_sound)
b3.grid(row=4,column=1)
b4=Button(window,text='Choose save-file path', width=40,
       command=callback_save)
b4.grid(row=4,column=2)

window.mainloop()

