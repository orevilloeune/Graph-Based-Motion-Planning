import pygame
import tkinter as tk
import math

class Eune:
    def __init__(self, window, rows, width, pos, color, type_of_block=0, cost=999, leading_cube=None):
        self.color = color
        self.pos = pos
        self.window = window
        self.rows = rows
        self.width = width
        self.width_of_row = self.width//self.rows
        self.cost = cost
        self.leading_cube = leading_cube
        self.type = type_of_block

    def draw_point(self):
        pygame.draw.rect(self.window, self.color, (self.pos[0] * self.width_of_row + 1,
                                                   self.pos[1] * self.width_of_row + 1, self.width_of_row - 1,
                                                   self.width_of_row - 1))

class Button(tk.Tk):
    def __init__(self, text):
        self.answer = None
        tk.Tk.__init__(self)
        self.entry = tk.Entry(self)
        self.button = tk.Button(self, text=text, command=self.on_button)
        self.button.pack()
        self.entry.pack()

    def on_button(self):
        self.answer = self.entry.get()
        self.quit()

    def get_answer(self):
        return self.answer

def get_info(text, rows):
    out = rows + 1
    is_int = False
    while 1:
        button = Button(text)
        button.mainloop()
        button.destroy()
        button.get_answer()
        try:
            out = int(button.get_answer())
        except ValueError as v:
            print("Given number must be integer")
        else:
            is_int = True
        if is_int is True:
            if 0 <= out < rows:
                break
            else:
                print("Positions have to be in range <{},{}>".format(0, rows-1))
                is_int = False
    return out

def draw_board(window, rows, width, cubes, labels, alg, started, end_cube=None, start_cube=None):
    window.fill((0, 0, 0))
    width_of_row = width//rows
    x = 0
    for cube in cubes.items():
        cube[1].draw_point()
    if end_cube is not None:
        end_cube.draw_point()
    if start_cube is not None:
        start_cube.draw_point()

    for i in range(rows):
        x += width_of_row
        pygame.draw.line(window,(224,224,224), (x, 0), (x, width))
        pygame.draw.line(window, (224,224,224), (0, x), (width, x))
    x = 0
    for j in range(4):
        window.blit(labels[j], (x+20, width + 20))
        x += width // 4
        pygame.draw.line(window, (224,224,224), (x, width), (x, width+100))
    width_of_alg = width // 4
    pygame.draw.line(window, (3, 253, 39), (width_of_alg*alg+2, width+80), (width_of_alg*(alg+1)-2, width+80))
    if started is True:
        pygame.draw.line(window, (3, 253, 39), (0 + 2, width + 80),
                         (width_of_alg - 2, width + 80))

def dijkstra2(starting_cube_pos, ending_cube_pos, covered_positions, rows, width, window, labels, algorithm, started):
    covered_positions[starting_cube_pos].cost = 0
    covered_positions[starting_cube_pos].leading_cube = None
    covered_positions[ending_cube_pos].cost = 0
    covered_positions[ending_cube_pos].leading_cube = None
    finishcube1 = 0
    finishcube2 = 0
    draw_the_road = False
    c = 0

    starting_cube = covered_positions[starting_cube_pos]
    ending_cube = covered_positions[ending_cube_pos]
    VS = [covered_positions[starting_cube_pos]]
    VE = [covered_positions[ending_cube_pos]]
    found = False

    del (covered_positions[starting_cube_pos])
    del (covered_positions[ending_cube_pos])
    while (VE and VS) and not found:
        pygame.event.get()
        draw_board(window, rows, width, covered_positions, labels, algorithm, started, starting_cube, ending_cube)

        minve = min(VE, key=lambda x: x.cost)
        minvs = min(VS, key=lambda x: x.cost)
        VE.remove(minve)
        VS.remove(minvs)

        ves = []
        vss = []

        minv = [minve, minvs]
        V = [VE, VS]
        v = [ves, vss]

        for i in range(2):
            for c in [(minv[i].pos[0]+1, minv[i].pos[1]), (minv[i].pos[0]-1, minv[i].pos[1]),
                      (minv[i].pos[0], minv[i].pos[1]+1), (minv[i].pos[0], minv[i].pos[1]-1)]:
                if -1 < c[0] < rows and -1 < c[1] < rows:
                    if c not in covered_positions:
                        cube = Eune(window, rows, width, c, (223, 254, 100), type_of_block=i)
                        v[i].append(cube)
                        covered_positions[c] = cube
                    elif i == 1 and covered_positions[c].type == 0:
                        found = True
                        break

        if found is True:
            finishcube2 = minv[1]
            finishcube1 = covered_positions[c]
            draw_the_road = True

        for i in range(2):
            for ve in v[i]:
                if ve.cost > minv[i].cost + 1:
                    ve.cost = minv[i].cost + 1
                    ve.leading_cube = minv[i]
                if ve.pos == ending_cube_pos and i ==1:
                    found = True
                    ending_cube.cost = ve.cost
                    ending_cube.leading_cube = ve.leading_cube
                V[i].append(ve)
        pygame.time.delay(10)
        pygame.display.update()
    if draw_the_road:
        draw_the_way = finishcube1
        while found is True and draw_the_way != ending_cube:
            draw_the_way.color = (3, 253, 39)
            draw_the_way = draw_the_way.leading_cube
        draw_the_way = finishcube2
        while found is True and draw_the_way != starting_cube:
            draw_the_way.color = (3, 253, 39)
            draw_the_way = draw_the_way.leading_cube

    covered_positions[starting_cube_pos] = starting_cube
    covered_positions[ending_cube_pos] = ending_cube

def dijkstra(starting_cube_pos, ending_cube_pos, covered_positions, rows,width, window, labels,
             algorithm, started, dijkstra):
    covered_positions[starting_cube_pos].cost = 0
    covered_positions[starting_cube_pos].leading_cube = None

    starting_cube = covered_positions[starting_cube_pos]
    ending_cube = covered_positions[ending_cube_pos]
    V = [covered_positions[starting_cube_pos]]
    found = False

    del(covered_positions[starting_cube_pos])
    del(covered_positions[ending_cube_pos])
    while V and not found:
        pygame.event.get()
        draw_board(window, rows, width, covered_positions, labels, algorithm, started, starting_cube, ending_cube)
        if dijkstra:
            minv = min(V, key= lambda x: x.cost)
        else:
            minv = min(V, key=lambda x: x.cost + math.fabs(x.pos[0] - ending_cube_pos[0]) + math.fabs(x.pos[1] - ending_cube_pos[1]))
            #minv = min(V, key=lambda x: math.sqrt((x.pos[0] - ending_cube_pos[0]) * (x.pos[0] - ending_cube_pos[0]) + (x.pos[1] - ending_cube_pos[1]) * (x.pos[1] - ending_cube_pos[1])))
            # finds not optimal way but does is faster
        V.remove(minv)

        v = []
        for c in [(minv.pos[0]+1, minv.pos[1]), (minv.pos[0]-1, minv.pos[1]), (minv.pos[0], minv.pos[1]+1),
                  (minv.pos[0], minv.pos[1] - 1)]:
            if -1<c[0] < rows and -1 < c[1] < rows:
                if c not in covered_positions:
                    cube = Eune(window, rows, width, c, (223, 254, 100))
                    v.append(cube)
                    covered_positions[c] = cube

        for ve in v:
            if ve.cost > minv.cost +1:
                ve.cost = minv.cost +1
                ve.leading_cube = minv

            if ve.pos == ending_cube_pos:
                found = True
                ending_cube.cost = ve.cost
                ending_cube.leading_cube = ve.leading_cube

            V.append(ve)

        pygame.time.delay(10)
        pygame.display.update()

    draw_the_way = ending_cube.leading_cube
    while found is True and draw_the_way != starting_cube:
        draw_the_way.color = (102, 0, 0)
        draw_the_way = draw_the_way.leading_cube

    covered_positions[starting_cube_pos] = starting_cube
    covered_positions[ending_cube_pos] = ending_cube

def main():
    width = 500
    rows = 10
    starting_position =[5, 5]
    ending_position = [10, 10]
    pressed = False
    mode = 0
    width_of_row = width // rows
    covered_positions = dict()
    started = False
    labelwidth = width//4
    algorithm = 1
    config = False

    pygame.font.init()
    myfont = pygame.font.SysFont("Comic Sans MS", 20)
    labelS= myfont.render("Start", 1, (153, 255, 0))
    labelD = myfont.render("Dijkstra", 1, (153, 255, 0))
    labelD2 = myfont.render("Dijkstra 2", 1, (153, 255, 0))
    labelA = myfont.render("A*", 1, (153, 255, 0))
    labels = [labelS, labelD, labelD2, labelA]

    window = pygame.display.set_mode((width, width + 100))

    starting_position[0] = int(get_info("Starting Position X", rows))
    starting_position[1] = int(get_info("Starting Position Y", rows))

    while 1:
        ending_position[0] = int(get_info("Ending Position X", rows))
        ending_position[1] = int(get_info("Ending Position Y", rows))
        if starting_position[0] == ending_position[0] and starting_position[1] == ending_position[1]:
            print("Ending and starting positions must be different")
        else:
            break
    starting_position = tuple(starting_position)
    ending_position = tuple(ending_position)

    starting_cube = Eune(window, rows, width, starting_position, (0, 0, 153), 0)
    ending_cube =Eune(window, rows, width, ending_position, (0, 0, 153))
    covered_positions[(starting_position[0],starting_position[1])] = starting_cube
    covered_positions[(ending_position[0],ending_position[1])] = ending_cube

    while 1:
        pygame.event.get()
        draw_board(window, rows, width, covered_positions, labels, algorithm, started)

        if pygame.mouse.get_pressed()[0] and not started:
            c = pygame.mouse.get_pos()
            y = c[1]
            x = c[0]
            c = ((c[0] - c[0] % width_of_row) // width_of_row, (c[1] - c[1] % width_of_row) // width_of_row)
            if pressed is False:
                pressed = True
                if c == starting_cube.pos:
                    mode = 1
                elif c == ending_cube.pos:
                    mode = 2
                elif y > width:
                    if x < labelwidth:
                        started = True
                        print("show must go on")
                    elif x < 2*labelwidth:
                        algorithm = 1
                        print("Dijkstra")
                    elif x < 3*labelwidth:
                        algorithm = 2
                        print("Dijkstra2")
                    else:
                        algorithm = 3
                        print("A*")
                else:
                    mode = 3
            elif c not in covered_positions and c[1] < rows:
                if mode == 1:
                    del(covered_positions[starting_cube.pos])
                    starting_cube.pos = c
                    covered_positions[c] = starting_cube
                elif mode == 2:
                    del(covered_positions[ending_cube.pos])
                    ending_cube.pos = c
                    covered_positions[c] = ending_cube
                elif mode == 3:
                    cube = Eune(window, rows, width, c, (0, 51, 0), type_of_block=4)
                    covered_positions[c] = cube
        else:
            pressed = False

        if started is True and config is False:
            config = True
            if algorithm == 1:
                dijkstra(starting_cube.pos, ending_cube.pos, covered_positions, rows, width, window, labels,
                         algorithm, started, 1)
                break
            elif algorithm == 2:
                dijkstra2(starting_cube.pos, ending_cube.pos, covered_positions, rows, width, window, labels,
                          algorithm, started)
                break
            else:
                dijkstra(starting_cube.pos, ending_cube.pos, covered_positions, rows, width, window, labels,
                         algorithm, started, 0)
                break

        pygame.time.delay(5)
        pygame.display.update()

    draw_board(window, rows, width, covered_positions, labels, algorithm, started)
    pygame.display.update()

    pygame.time.delay(3000)
    pygame.quit()


main()