# -*- coding: utf-8 -*-
"""
moviePy on Pygame screen
Created on Sat Jun  8 08:41:04 2019

@author: Bunnavit Sawangpiriyakij
"""

from moviepy.editor import *
import pygame,os,time
import numpy as np
import threading

pygame.display.set_caption('Hello World!')

clip = VideoFileClip(os.path.join("Star_Trim.mp4"))


audio_fps = 5000
audio_buffersize = 4000
audio_nbytes = 2
audioFlag = 1
videoFlag = None
audiothread = threading.Thread(target=clip.audio.preview,
                               args=(audio_fps,
                               audio_buffersize,
                               audio_nbytes,
                               audioFlag, videoFlag))
audiothread.daemon=True
audiothread.start()

pygame.init()
screen = pygame.display.set_mode([600,400])
pygame.display.set_caption("Video in Pygame!")
done = False
clock = pygame.time.Clock()
sec = time.time()
while not done:
   for event in pygame.event.get():  # User did something
      if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_ESCAPE or event.unicode == 'q':
            done = True  # Flag that we are done so we exit this loop
            break
   second = time.time()
   if clip.is_playing(second-sec):
      buf = clip.get_frame(second-sec)
      video = pygame.image.frombuffer(buf, (clip.w, clip.h), 'RGB')
   else:
      sec = second
      audiothread.join()
      audiothread = threading.Thread(target=clip.audio.preview,
                               args=(audio_fps,
                               audio_buffersize,
                               audio_nbytes,
                               audioFlag, videoFlag))
      audiothread.daemon=True
      audiothread.start()




   screen.blit(video, [0, 0])
   pygame.display.flip()
   clock.tick(30) 
pygame.quit()