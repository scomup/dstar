import numpy as np
import matplotlib.pyplot as plt
import time

START = 10
GOAL  = 0
OBSTACLE = 1
FREE = 3

class map_cell:
    def __init__(self,x,y):
        self.back_point = self
        self.tag = 'NEW'
        self.stat = 'FREE' # FREE OBSTACLE GOAL START
        self.h = 0
        self.k = 0
        self.x = x
        self.y = y

    def cost(self,to_ceil):                   # getName()メソッド
        a = abs(to_ceil.x - self.x)
        b = abs(to_ceil.y - self.y)
        if a > 1 or b > 1:
            return -1
        elif a == 0 or b == 0:
            return 1
        else:
            return -1

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
        
    def set_start(self,y,x):
        self.map_data[y][x].stat = 'START'
    
    def update_plot(self,subfig):
        for i in range(len(self.map_data)):
            for j in range(len(self.map_data[0])):
                if self.map_data[i][j].stat == 'GOAL':
                    subfig.text(j, i, 'Goal', va='center', ha='center',color='white')
                    self.map_show_data[i,j] = GOAL
                elif self.map_data[i][j].stat == 'START':
                    subfig.text(j, i, 'Start', va='center', ha='center',color='white')
                    self.map_show_data[i,j] = START
                elif self.map_data[i][j].stat == 'FREE':   
                    self.map_show_data[i,j] = FREE
                elif self.map_data[i][j].stat == 'OBSTACLE':   
                    self.map_show_data[i,j] = OBSTACLE
                else:
                    print 'ERROR!'
                subfig.imshow(self.map_show_data, interpolation='none')


g_map = grid_map(6,7)
g_map.set_goal(0,6)
g_map.set_start(5,1)

fig, show_map = plt.subplots()

g_map.update_plot(show_map)


# 矢印（ベクトル）
#plt.quiver(1,1,-1,1,color ='white'); plt.quiver(2,1,0,1,color ='white'); plt.quiver(3,1,1,1,color ='white')
#plt.quiver(1,2,-1,0,color ='white');                                      plt.quiver(3,2,1,0,color ='white')
#plt.quiver(1,3,-1,-1,color ='red');  plt.quiver(2,3,0,-1,color ='white'); plt.quiver(3,3,1,-1,color ='white')


def onclick(event):
    x, y = event.xdata, event.ydata
    if x == None or y == None:
        return
    ix = int(x+0.5)
    iy = int(y+0.5)
    redraw_flag = 0
    if(event.button == 1):
        if g_map.map_show_data[iy,ix] != GOAL and g_map.map_show_data[iy,ix] != START:
            g_map.map_show_data[iy,ix] = OBSTACLE
            redraw_flag = 1
    else:
        if g_map.map_show_data[iy,ix] != GOAL and g_map.map_show_data[iy,ix] != START:
            g_map.map_show_data[iy,ix] = FREE
            redraw_flag = 1

    if( redraw_flag == 1):
        show_map.imshow(g_map.map_show_data, interpolation='none')
        fig.canvas.draw()
        time.sleep(1e-8)

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()

