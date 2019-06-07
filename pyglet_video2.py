# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 15:35:46 2019

@author: Admin
"""
import pyglet,os,time
from pyglet.gl import *
from os.path import abspath, isfile
from pyglet import clock

#pyglet.options['audio'] = ('pulseaudio', 'alsa', 'openal', 'silent')
#pyglet.have_avbin=False
key = pyglet.window.key

class main(pyglet.window.Window):

    def __init__ (self):
        super(main, self).__init__(800, 600, fullscreen = False)
        self.x, self.y = 0, 0
        self.player = pyglet.media.Player()
        self.player.queue(pyglet.media.load(os.path.join("Star_Trim.mp4")))
        self.sprites = {'video' : None}
        self.alive = 1
        self.buff = []
        self.first_round = True
        self.count = 0

    def on_draw(self):
        self.render()

    def on_close(self):
        self.alive = 0

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE: # [ESC]
            self.alive = 0
        elif symbol == key.SPACE:
            if self.player.playing:
                self.player.pause()
            else:
                self.player.play()
        elif symbol == key.RIGHT:
            print('Skipping to:',self.player.time+2)
            self.player.source.seek(self.player.time+2)
        elif symbol == key.LEFT:
            print('Rewinding to:',self.player.time-2)
            self.player.source.seek(self.player.time-2)
        
    def render(self):
        self.clear()
        print(pyglet.clock.tick())
        #source = pyglet.text.Label(str(self.player.source.info.title.decode('UTF-8')), x=20, y=300-30)
        volume = pyglet.text.Label(str(self.player.volume*100)+'% volume', x=20, y=40)
        p_time = pyglet.text.Label(str(self.player.time), x=20, y=20)
        if self.player.time > 30:
           self.player.pause()
           self.player.source.seek(0.01)
           self.player.play()
           self.first_round = False
           self.count = 0
           time.sleep(2)

        if self.player.playing and self.first_round:
           texture = None
           texture = self.player.get_texture()
           if texture:
              self.buff.append(texture.get_image_data()) 
              texture.blit(20,100)
        if not self.first_round:
           texture = self.player.get_texture()
           if texture and self.count<len(self.buff):                            
              texture.blit_into(self.buff[self.count],0,0,0)
              self.count+=1
              texture.blit(20,100)


        #source.draw()
        volume.draw()
        p_time.draw()
        time.sleep(0.02)
        self.flip()
        

    def run(self):
        while self.alive == 1:
            self.render()

            # -----------> This is key <----------
            # This is what replaces pyglet.app.run()
            # but is required for the GUI to not freeze
            #
            event = self.dispatch_events()

x = main()
x.run()
exit(0)