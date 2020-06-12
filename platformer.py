from pygame.locals import *
import pygame as pg
import sys

clock = pg.time.Clock()
pg.init()
WINDOW_SIZE = (600, 400)

screen = pg.display.set_mode(WINDOW_SIZE, 0, 32)
canvas = pg.Surface((300, 200))

jump = False
moving_right = False
moving_left = False

game_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
tile1_img = pg.image.load("assets/tile_1.png")
tile2_img = pg.image.load("assets/tile_2.png")

player_img = pg.image.load("assets/player/idle/idle_1.png").convert()
player_img.set_colorkey((0, 0, 0))

vertical_momentum = 0

player_rect = pg.Rect(150, 110, player_img.get_width(), player_img.get_height())
test_rect = pg.Rect(10, 10, 10, 50)


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collisions = {
        "top": False,
        "bottom": False,
        "left": False,
        "right": False,
    }
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)

    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collisions["right"] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collisions["left"] = True

    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collisions["bottom"] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collisions["top"] = True

    return rect, collisions


def render_map():
    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == 1:
                canvas.blit(tile1_img, (x * 16, y * 16))
            if tile == 2:
                canvas.blit(tile2_img, (x * 16, y * 16))
            if tile != 0:
                tile_rects.append(pg.Rect(x * 16, y * 16, x, y))
            x += 1
        y += 1

    return tile_rects


while True:
    canvas.fill((0, 0, 0))

    tile_rects = render_map()
    canvas.blit(player_img, (player_rect.x, player_rect.y))

    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

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
                vertical_momentum = -5
        if event.type == KEYUP:
            if event.key == K_LEFT:
                moving_left = False
            elif event.key == K_RIGHT:
                moving_right = False

    screen.blit(pg.transform.scale(canvas, WINDOW_SIZE), (0, 0))

    pg.display.update()
    clock.tick(60)
