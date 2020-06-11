from pygame.locals import *
import pygame as pg
import sys

clock = pg.time.Clock()
pg.init()
WINDOW_SIZE = (400, 400)

screen = pg.display.set_mode(WINDOW_SIZE, 0, 32)

jump = False
moving_right = False
moving_left = False

player_loc = [50, 50]
player_momentum = [0, 0]

while True:
    screen.fill((0, 0, 0))
    pg.draw.rect(screen, (40, 40, 40), pg.Rect(
        int(player_loc[0]), int(player_loc[1]), 40, 50))

    if player_loc[1] > WINDOW_SIZE[1] - 50:
        print(player_loc)
        player_loc[1] = WINDOW_SIZE[1] - 50
        player_momentum[1] = 0
        print(WINDOW_SIZE[1])
    else:
        player_momentum[1] += 0.2

    player_loc[1] += player_momentum[1]

    if moving_right:
        player_loc[0] += 4
    if moving_left:
        player_loc[0] -= 4
    if jump:
        player_loc[1] -= 20

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                moving_left = True
            elif event.key == K_RIGHT:
                moving_right = True
            elif event.key == K_UP:
                jump = True
        if event.type == KEYUP:
            if event.key == K_LEFT:
                moving_left = False
            elif event.key == K_RIGHT:
                moving_right = False
            elif event.key == K_UP:
                jump = False

    pg.display.update()
    clock.tick(60)
