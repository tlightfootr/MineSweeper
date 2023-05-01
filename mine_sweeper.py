from cgitb import text
import pygame as pg
import random as rdm
import math as mth

pg.init()

#grid_size = (int(input("enter grid width: ")), int(input("enter grid height: ")))
grid_size = (12, 6)

scale = 1000
size = (scale, grid_size[1]/grid_size[0]*scale)
grid_length = size[0]/grid_size[0]
screen = pg.display.set_mode(size)
font = pg.font.Font(None, round(grid_length * 1.1))
fps = 60
line_list = []
mine_locations = []
squares_checked = []
text_list = []
game_lost = False

def generate_grid(grid_size):
    for i in range(grid_size[0]):
        line_list.append((((i+1)*(size[0]/grid_size[0]), 0), ((i+1)*(size[0]/grid_size[0]), size[1])))
    for i in range(grid_size[1]):
        line_list.append(((0, (i+1)*(size[1]/grid_size[1])), (size[0], (i+1)*(size[1]/grid_size[1]))))
generate_grid((grid_size))


def generate_mines(grid_size, mine_count, mine_locations):
    for i in range(mine_count):
        while True:
            location = (rdm.randint(1, grid_size[0]), rdm.randint(1, grid_size[1]))
            if location not in mine_locations:
                mine_locations.append(location)
                break
generate_mines(grid_size, 10, mine_locations)


def check_square():
    global game_lost
    if pg.mouse.get_pressed(3)[0]:
        mouse_pos = pg.mouse.get_pos()
        mouse_grid_pos = (mth.ceil(mouse_pos[0]/size[0]*grid_size[0]), mth.ceil(mouse_pos[1]/size[1]*grid_size[1]))
        if mouse_grid_pos not in squares_checked:
            if mouse_grid_pos in mine_locations:
                game_lost = True
                return
            squares_checked.append(mouse_grid_pos)
            mine_check_tuple = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))
            mines_counted = 0
            for i in mine_check_tuple:
                try:
                    if (mouse_grid_pos[0] + i[0], mouse_grid_pos[1] + i[1]) in mine_locations:
                        mines_counted += 1
                except:
                    continue
            text_list.append((font.render(str(mines_counted), False, (255, 255, 255)), mouse_grid_pos))
            

def auto_fill_zeros():
    pass
            

def draw_mines(mine_locations):
    for i in mine_locations:
        pg.draw.circle(screen, (255, 0, 0), (i[0]*(scale/grid_size[0]) - (scale/grid_size[0])/2, i[1]*(grid_size[1]/grid_size[0]*scale/grid_size[1]) - (grid_size[1]/grid_size[0]*scale/grid_size[1])/2), scale/grid_size[0]/2.3)


while True:
    pg.time.delay(round(1/fps * 1000))

    for event in pg.event.get():
        if event.type == pg.QUIT: exit()

    check_square()

    screen.fill((0, 0, 0))

    for i in line_list:
        pg.draw.line(screen, (150, 150, 150), i[0], i[1])

    for i in text_list:
        screen.blit(i[0], (i[1][0]*grid_length - grid_length/1.5, i[1][1]*grid_length - grid_length/1.2))

    if game_lost:
        draw_mines(mine_locations)

    pg.display.update()