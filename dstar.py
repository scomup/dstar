import numpy as np
import time
import threading
import drawer
import matplotlib.pyplot as plt
import operator

import cv2
START = 10
GOAL  = 0
OBSTACLE = 1
FREE = 3
CLOSE = 8

INF = float("inf")

class map_cell:
    def __init__(self,x,y):
        
        self.back_point = self
        self.tag = 'NEW'
        self.stat = 'FREE' # FREE OBSTACLE GOAL START
        self.h = 0
        self.k = 0
        self.x = x # rows
        self.y = y # cols

    def cost(self,to_ceil):                  
        a = abs(to_ceil.x - self.x)
        b = abs(to_ceil.y - self.y)
        if a > 1 or b > 1:
            print 'COST ERROR'
            return -1
        elif to_ceil.stat == 'OBSTACLE':
            return INF
        elif a == 0 or b == 0:
            return 1
        else:
            return 1.4

class grid_map:
    def __init__(self,rows,cols):
        self.map_data = []
        self.map_show_data = np.zeros((rows, cols))
        self.map_show_data.fill(FREE)

        for i in range(rows):
            line = []
            for j in range(cols):
                cell = map_cell(i,j)
                line.append(cell)
            self.map_data.append(line)

    def set_goal(self,y,x):
        self.map_data[y][x].stat = 'GOAL'
        self.goal = self.map_data[y][x]
        
    def set_start(self,y,x):
        self.map_data[y][x].stat = 'START'
        self.start = self.map_data[y][x]
                    

class dstar_planner(threading.Thread):
    def __init__(self,g_map):
        threading.Thread.__init__(self)
        self.open = []
        self.drawer = drawer.map_drawer(g_map)
        self.grid_map = g_map
    def insert(self,cell,h_new):
        if cell.tag == 'NEW':
            cell.k = h_new
        else:
            cell.k = min(h_new,cell.k)
        cell.h = h_new
        if cell.tag != 'OPEN':
            cell.tag = 'OPEN'
            self.open.append(cell)
        self.open.sort(key=operator.attrgetter('k'))
    def neighbor(self,cell):
        tmp = []
        rows = len(self.grid_map.map_data)
        cols = len(self.grid_map.map_data[0])
        for i in range(-1,2):
            for j in range(-1,2):
                if (cell.x + i < rows ) and (cell.x + i >= 0 ) and (cell.y + j < cols ) and (cell.y + j >= 0 ): 
                    if i == 0 and j == 0:
                        break
                    if self.grid_map.map_data[cell.x + i][cell.y + j].tag == 'CLOSE':
                        break
                    print cell.x,cell.y
                    tmp.append(self.grid_map.map_data[cell.x + i][cell.y + j])
        return tmp
    def process_state(self):
        if len(self.open) == 0:
            return -1
        self.open.sort(key=operator.attrgetter('k'))
        #sorted(self.open, key=lambda cell: cell.k)
        cell_c = self.open[0]
        del self.open[0]
        cell_c.tag = 'CLOSE'
        if cell_c.stat == 'START':
            return -1
        if cell_c == None or cell_c.stat == 'START':
            return -1
        k_old = cell_c.k
        neighbor = self.neighbor(cell_c)
        if k_old < cell_c.h:
            for cell in neighbor:
                if cell.tag == 'NEW' and cell.h < k_old and cell_c.h > cell_c.cost(cell) + cell.h:
                    cell_c.back_point = cell
                    cell_c.h = cell_c.cost(cell) + cell.h
        if k_old == cell_c.h:
            for cell in neighbor:
                if cell.tag == 'NEW' or (cell.back_point == cell_c and cell.h != cell.x + cell_c.cost(cell) + cell_c.h) or (cell.back_point != cell_c and cell.h >  cell_c.cost(cell) + cell_c.h):
                    cell.back_point = cell_c
                    self.insert(cell, cell_c.cost(cell) + cell_c.h)
                    
        return k_old
    def run(self):
        k = 0
        while k != -1:
            #time.sleep(1)
            raw_input('pause : press any key ...')
            k = planner.process_state()
            self.drawer.update_plot()
            self.drawer.fig.canvas.draw()
            print 'RUN'

            
                
if __name__ == '__main__':
    g_map = grid_map(6,7)
    g_map.set_goal(0,6)
    g_map.set_start(5,1)
    planner = dstar_planner(g_map)
    planner.insert(g_map.goal,0)
    #planner.drawer.run()
    #test = showTrajectory()
    #test.start()
    #planner.drawer.start()    
    #self.fig.canvas.draw() 
    planner.start()
    #drawer = drawer.map_drawer(g_map)
    planner.drawer.run()
    #while k != -1:
    #    k = planner.process_state()
    #    planner.drawer.update_plot()
    #    planner.drawer.fig.canvas.draw()
    #    plt.cla()   
    #    time.sleep(1)
        #raw_input('pause : press any key ...')
    print 'end'
            
    

#g_map = grid_map(6,7)
#g_map.set_goal(0,6)
#g_map.set_start(5,1)
#planner = dstar_planner(g_map)
#planner.insert(g_map.goal,0)
#planner.drawer.update_plot()
#planner.drawer.start()
#k = 0
#i = 0
#step =300
##while k != -1 and i <step:
##    k = planner.process_state()
#    #if i == step -1 or k == -1:
#    #    g_map.update_plot(show_map)
#     #   fig.canvas.draw()
##    i = i+1
#
## 
##plt.quiver(1,1,-1,1,color ='white'); plt.quiver(2,1,0,1,color ='white'); plt.quiver(3,1,1,1,color ='white')
##plt.quiver(1,2,-1,0,color ='white');                                      plt.quiver(3,2,1,0,color ='white')
##plt.quiver(1,3,-1,-1,color ='red');  plt.quiver(2,3,0,-1,color ='white'); plt.quiver(3,3,1,-1,color ='white')        
#
#
##cid = fig.canvas.mpl_connect('button_press_event', onclick)
#while True:
#    time.sleep(1e-6)
#print 'end'
#plt.show()



