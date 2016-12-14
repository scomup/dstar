import numpy as np
import matplotlib.pyplot as plt
import time

class map_cell:
    def __init__(self,x,y):
        self.back_point = self
        self.tag = 'NEW'
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
        for i in range(rows):
            line = []
            for j in range(cols):
                cell = map_cell(i,j)
                line.append(cell)
            self.map_data.append(line)

g_map = grid_map(6,7)

fig, show_map = plt.subplots()

map_row = 6
map_col = 7

START = 10
GOAL  = 0
OBSTACLE = 1
FREE = 3

x = 5.5
y = 5.5

# 矢印（ベクトル）
plt.quiver(1,1,-1,1,color ='white'); plt.quiver(2,1,0,1,color ='white'); plt.quiver(3,1,1,1,color ='white')
plt.quiver(1,2,-1,0,color ='white');                                      plt.quiver(3,2,1,0,color ='white')
plt.quiver(1,3,-1,-1,color ='red');  plt.quiver(2,3,0,-1,color ='white'); plt.quiver(3,3,1,-1,color ='white')

#imshow portion
map_data = np.zeros((map_row, map_col))
map_data.fill(FREE)





#text portion

show_map.text(1, 5, 'Start', va='center', ha='center',color='white')
map_data[5,1] = START

show_map.text(6, 0, 'Goal', va='center', ha='center',color='white')
map_data[0,6] = GOAL


show_map.imshow(map_data, interpolation='none')

def onclick(event):
    x, y = event.xdata, event.ydata
    if x == None or y == None:
        return
    ix = int(x+0.5)
    iy = int(y+0.5)
    redraw_flag = 0
    if(event.button == 1):
        if map_data[iy,ix] != GOAL and map_data[iy,ix] != START:
            map_data[iy,ix] = OBSTACLE
            redraw_flag = 1
    else:
        if map_data[iy,ix] != GOAL and map_data[iy,ix] != START:
            map_data[iy,ix] = FREE
            redraw_flag = 1

    if( redraw_flag == 1):
        show_map.imshow(map_data, interpolation='none')
        fig.canvas.draw()
        time.sleep(1e-8)

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()

