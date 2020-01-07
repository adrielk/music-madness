# -*- coding: utf-8 -*-
"""
Youtube Music MP3 Downloader
Created on Sun Jan  5 17:20:22 2020

@author: thead
"""
from __future__ import unicode_literals
import youtube_dl
import os
os.chdir(r"C:\Users\thead\Desktop\MusicPlayer\Songs")

url = 'https://www.youtube.com/playlist?list=PL4o29bINVT4EG_y-k5jGoOu3-Am8Nvi10'#url of playlist of video

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')
        
#options playliststart and playlistend determine starting and ending videos of playlist
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    'playliststart': 1,
   # 'playlistend' : 100,
    'hls_prefer_native': False,
    'prefer_ffmpeg':True,
    
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])