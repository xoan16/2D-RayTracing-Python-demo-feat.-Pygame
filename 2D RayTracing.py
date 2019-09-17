import pygame
import math
import sys
import time
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (20,30)

#to do = [2d raytracing game, 3d raytracing engine]

pygame.init()
screen = pygame.display.set_mode((1500, 700), pygame.NOFRAME)
screen.fill((0, 0, 0))
blocks =[[(100, 100), (150, 400), (200, 150)],
[(292, 442), (386, 240), (514, 487)],
[(611, 61), (847, 77), (793, 319)],
[(10, 10), (10, 690), (1490, 690), (1490, 10)]]
r1 = [(0, 0), (0, 0)]
r2 = [(0, 0), (0, 0)]
mod = 10000
angles = []
points = []
dis = 100000
point = (0, 0)
frames = []
fps = 0
for x in range(360):
    angles.append(x)


def closer():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F4 and alt_held:
                sys.exit()

def hitboxes(blocks):
    for y in range(len(blocks)):
        for x in range(len(blocks[y])):
            pygame.draw.aalines(screen, (100, 100, 100), False, (blocks[y][x - 1], blocks[y][x]))

def toast(r1, r2):
    try:
        q = ((r1[0][0] - r1[1][0])*(r2[0][1] - r2[1][1]) - (r1[0][1] - r1[1][1])*(r2[0][0] - r2[1][0]))
        t = ((r1[0][0] - r2[0][0])*(r2[0][1] - r2[1][1]) - (r1[0][1] - r2[0][1])*(r2[0][0] - r2[1][0]))/q
        u = -((r1[0][0] - r1[1][0])*(r1[0][1] - r2[0][1]) - (r1[0][1] - r1[1][1])*(r1[0][0] - r2[0][0]))/q

        if 0 < t < 1 and 0 < u < 1: return True
        else: return False
    except ZeroDivisionError: pass



def touchpoint(r1, r2):
    try:
        z = ((r1[0][0] - r1[1][0])*(r2[0][1] - r2[1][1]) - (r1[0][1] - r1[1][1])*(r2[0][0] - r2[1][0]))
        v = (((r1[0][0]*r1[1][1] - r1[0][1]*r1[1][0])*(r2[0][0] - r2[1][0])) - ((r1[0][0] - r1[1][0])*(r2[0][0]*r2[1][1] - r2[0][1]*r2[1][0])))
        w = (((r1[0][0]*r1[1][1] - r1[0][1]*r1[1][0])*(r2[0][1] - r2[1][1])) - ((r1[0][1] - r1[1][1])*(r2[0][0]*r2[1][1] - r2[0][1]*r2[1][0])))

        return (round(v/z), round(w/z))
    except ZeroDivisionError: pass

while True:
    atime = time.process_time()
    hitboxes(blocks)
    for g in angles:
        r1[0] = pygame.mouse.get_pos()
        r1[1] = (r1[0][0] + math.sin(g) * mod, r1[0][1] + math.cos(g) * mod)
        for j in blocks:
            for k in range(len(j)):
                r2 = [j[k], j[k - 1]]
                if toast(r1, r2):
                    points.append(touchpoint(r1, r2))
                else:
                    pass

        for h in points:
            d = math.sqrt((r1[0][0] - h[0])**2 + (r1[0][1] - h[1])**2)
            if d < dis:
                dis = d
                point = h

        if len(points) != 0:
            if point != (0, 0):
                pygame.draw.aaline(screen, (100, 100, 100), r1[0], point)
                pygame.draw.circle(screen, (220, 220, 220), point, 3)
        else: pygame.draw.aaline(screen, (100, 100, 100), r1[0], r1[1])

        points = []
        point = (0, 0)
        dis = 10000

    try: frames.append(1/(time.process_time() - atime))
    except ZeroDivisionError: pass

    i = 0
    if len(frames) == 50:
        for x in frames:
            i += x
        try:
            fps = i/len(frames)
        except ZeroDivisionError: pass
        frames = []
    screen.blit(pygame.font.Font(None, 20).render("Avg. FPS: " + str(round(fps, 2)), True, (255, 255, 255)), (1350, 50))

    closer()
    pygame.display.flip()
    screen.fill((0, 0, 0))
