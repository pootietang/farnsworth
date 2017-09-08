#! /usr/bin/env python

#The jellyfish screenhack is intended to imitate the panels
#found in the starship Jellyfish in the movie Star Trek

from time import sleep
import random
import farnsworth
import constants
import config
import math

sign = farnsworth.sign( provides_logo = False,
                        is_dynamic=True,
                        preferred_duration=15.0 )

color_idle = (206,228,232)
color_right = (183,225,255)
color_left = (255,183,207)

#========================================================================
class primative_square:
    #This class of object is a square pixel grid that will travel back and forth
    
    def __init__(self,size,start_x,y,end_x,move_frames,dwell_frames,start_frame):
        self.size = size
        self.x=start_x
        self.start_x=start_x
        self.end_x=end_x
        self.y=y
        self.step=0
        self.move_frames=move_frames
        self.dwell_frames=dwell_frames
        self.start_frame=start_frame
        self.stop_step = move_frames
        self.restart_step = move_frames+dwell_frames
        self.restop_step = 2*move_frames+dwell_frames
        self.period=move_frames*2+dwell_frames*2
        #set initial conditions to not move right or left
        if start_x<end_x:
            #default motion will be moving right
            self.moving_right = True
            self.moving_left = False
            self.travel = self.end_x-self.start_x
        else:
            #motin will be moving left
            self.moving_right = False
            self.moving_left = True
            self.travel = self.start_x - self.end_x

        #set the amplitude for movement calc
        self.amplitude = float(self.travel)/float(self.move_frames)
        
        #initialize colors as idle
        self.colors = list()
        for i in range(self.size*self.size):
            self.colors.append(0)
        #initialize row offset as zero
        self.row_offset=list()
        for i in range(self.size):
            #initially set all rows idle
            self.set_color_idle(i)
            #set row offset to l
            self.row_offset.append(0)
    #------------------------------------------------------------                
    def set_color_idle(self,row):
        #set the colors of a row to idle
        #row will go from 0 to self.size
        for i in range(self.size):
            #set all the colors to idle colors
            self.colors[row*self.size+i] = color_idle
    
    #------------------------------------------------------------
    def set_color_right(self,row):
        #set the row color of a row to move right
        for i in range(self.size):
            #set all the colors to move right
            self.colors[row*self.size+i] = color_right
    #------------------------------------------------------------
    def set_color_left(self,row):
        #set the row color of a row to move left
        for i in range(self.size):
            #set all the colors to move right
            self.colors[row*self.size+i] = color_left
    #------------------------------------------------------------        
    def advance(self,frame):
        #calling this function will cause the item to move in the appropriate direction
        if frame>=self.start_frame:
            #if the step exceeds the period, then sit it back to 0 
            if self.step>self.period:
                self.step=0
            
            #increment the step timer
            self.step+=1
            
            #set color based on movement
            if self.step==1 or self.step==self.restart_step:
                if self.moving_right == True:
                    for i in range(self.size):
                        self.set_color_right(i)
                else:
                    for i in range(self.size):
                        self.set_color_left(i)
            elif self.step==self.stop_step or self.step == self.restop_step:
                for i in range(self.size):
                    self.set_color_idle(i)
            
            #check it see which phase the system is in
            if self.step<self.stop_step:
                #set the input phase function ordinate
                ord = self.step
                #in this case, we're moving in the first direction
                calc = int(round(-1*self.amplitude*float(self.move_frames) \
                       /(2*math.pi) * math.sin(2*math.pi*float(ord) \
                       / float(self.move_frames)) + self.amplitude*float(ord)))

                
                if self.moving_right == True:
                    self.x= self.start_x + calc
                elif self.moving_left == True:
                    self.x= self.start_x - calc
            elif self.step == self.stop_step:
                if self.moving_right == True:
                    self.moving_left = True
                    self.moving_right = False
                else:
                    self.moving_right = True
                    self.moving_left = False

            elif self.step<self.restart_step:
                #this is the dwell phase
                #do nothing
                nothing = 0
                
            elif self.step<self.restop_step:
                #this is the second moving phase
                ord = self.step-self.move_frames-self.dwell_frames
                #in this case, we're moving in the first direction
                calc = int(round(-1*self.amplitude*float(self.move_frames) \
                       /(2*math.pi) * math.sin(2*math.pi*float(ord) \
                       / float(self.move_frames)) + self.amplitude*float(ord)))
                
                
                if self.moving_right == True:
                    self.x= self.end_x + calc
                elif self.moving_left == True:
                    self.x= self.end_x - calc
            elif self.step == self.restop_step:
                
                #second dwell phase
                if self.moving_right ==True:
                    self.moving_left = True
                    self.moving_right = False
                else:
                    self.moving_right = True
                    self.moving_left = False

    #------------------------------------------------------------
    def paint(self):
        for i in range(self.size):
            #draw pixel rows
            for j in range(self.size):
                #draw pixel colums
                sign.front_layer().set_pixel(j+self.x+self.row_offset[i],i+self.y,self.colors[i*self.size+j])
                #print "X= " + str(j+self.x) + ", Y= " + str(i+self.y)
    #------------------------------------------------------------
    def spotlight(self):
        for i in range(self.size):
            #draw pixel rows
            for j in range(self.size):
                #draw pixel columns
                #first read the color from the image painted to the back layer
                color = sign.back_layer().read_pixel(j+self.x+self.row_offset[i], i+self.y)
                #then draw it to the object
                sign.front_layer().set_pixel(j+self.x+self.row_offset[i], i+self.y,color)
#================================================================
class generator:
    def __init__(self,count):
        self.obs = list()
        for i in range(count):
            self.height = config.PIXELS_HIGH
            self.width = config.PIXELS_ACROSS
            self.isleft = self.is_left()
            self.size = self.set_size()
            self.start_x = self.set_start_x()
            self.y = self.set_y()
            self.end_x = self.set_end_x()
            self.move_frames = self.set_move_frames()
            self.dwell_frames = self.set_dwell_frames()
            self.start_frame = self.set_start_frame()
            self.obs.append(primative_square(self.size, self.start_x, \
                                                         self.y, self.end_x, self.move_frames, \
                                                         self.dwell_frames,self.start_frame))
    
    #------------------------------------------------------------
    def is_left(self):
        #this is the random generator to decide if the items start left and move right
        #or vice versa
        x = random.random()
        if x <=0.5:
            return True
        else:
            return False
    #-----------------------------------------------------------
    def set_size(self):
        x=0
        while x <=1 or x>self.height-8:
            x=int(round((self.height-8)*random.random()))
        return x
    #-----------------------------------------------------------
    def set_y(self):
        y=-1
        while y<0 or y>self.height-self.size:
            y = int(round((self.height-self.size)*random.random()))
        #print y, self.height, self.size, self.height-self.size
        return y
    #-----------------------------------------------------------
    def set_start_x(self):
        if self.isleft:
            return int(round(self.width/2*random.random()))
        else:
            return self.width/2+int(round(self.width/2*random.random()))
    #-----------------------------------------------------------
    def set_end_x(self):
        if self.isleft:
            return self.width/2 + int(round(self.width/2*random.random()))
        else:
            return int(round(self.width/2*random.random()))
    #------------------------------------------------------------
    def set_move_frames(self):
        x = 0
        while x<6 or x>120:
            x = int(round(350*random.random()))
        return x
    #------------------------------------------------------------
    def set_dwell_frames(self):
        x = 0
        while x>10 or x<1:
            x = int(round(10*random.random()))
        return x
    #------------------------------------------------------------
    def set_start_frame(self):
        x = 0
        while x >30:
            x = int(round(30*random.random()))
        return x
   
#================================================================
#sq1=primative_square(3,80,0,0,30,5,5)
#sq2=primative_square(5,2,4,90,120,0,25)
#sq3=primative_square(2,6,13,89,20,2,0)
#sq4=primative_square(2,91,1,20,35,4,7)
#sq5=primative_square(4,12,11,69,12,5,20)
#obs=(sq1,sq2,sq3,sq4,sq5)

gen = generator(25)
clock=farnsworth.clock(.08)
frame = 0
while True:
    
    sign.front_layer().blank()
    
    if clock.tick():
        for ob in gen.obs:
            ob.advance(frame)
        #sq1.advance(frame)
        frame+=1
    
    for ob in gen.obs:
        ob.paint()
    #sq1.paint()
    sign.paint()
    sleep(0.01)
