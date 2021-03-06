from settings import Settings
from colors import Colors
from button import Button
import pygame as pg
import random
import pickle

colors = Colors()
BARRIER = -1
BEDROCK = 0
DIRT = 1
GRASS = 2
WATER = 3
COAL = 4
DIAMOND = 5
ROCK = 6
STONE = 7
GOLD = 8
WOOD = 9
BRICK = 10
WOOL = 11
PINK_WOOL = 12
BLUE_WOOL = 13
GREEN_WOOL = 14
LIME_WOOL = 15
YELLOW_WOOL = 16
LAPIS = 17
RUBY = 18
EMERALD = 19
AMETHYST = 20

settings = Settings('minecraft')
resources = [DIRT, GRASS, WATER, COAL, DIAMOND, ROCK, STONE, GOLD, WOOD, BRICK, WOOL, PINK_WOOL, BLUE_WOOL, GREEN_WOOL,
             LIME_WOOL, YELLOW_WOOL, LAPIS, RUBY, EMERALD, AMETHYST]
renderables = [DIRT, GRASS, WATER, COAL, ROCK, WOOD]
colors.new_color(75, 75, 75)
colors.new_color(225, 175, 135)
colormap = {
    BEDROCK: colors.custom[0],
    DIRT: colors.brown,
    GRASS: colors.green,
    WATER: colors.blue,
    COAL: colors.black,
    DIAMOND: colors.light_blue,
    ROCK: colors.very_dark_gray,
    STONE: colors.dark_gray,
    GOLD: colors.orange,
    WOOD: colors.light_brown,
    BRICK: colors.red,
    WOOL: colors.white,
    PINK_WOOL: colors.pink,
    BLUE_WOOL: colors.very_light_blue,
    GREEN_WOOL: colors.light_green,
    LIME_WOOL: colors.lime,
    YELLOW_WOOL: colors.a_bit_darker_yellow,
    LAPIS: colors.dark_blue,
    RUBY: colors.dark_red,
    EMERALD: colors.dark_green,
    AMETHYST: colors.magenta,
}
inventory = {
    DIRT: 0,
    GRASS: 0,
    WATER: 0,
    COAL: 0,
    DIAMOND: 0,
    ROCK: 0,
    STONE: 0,
    GOLD: 0,
    WOOD: 0,
    BRICK: 0,
    WOOL: 0,
    PINK_WOOL: 0,
    BLUE_WOOL: 0,
    GREEN_WOOL: 0,
    LIME_WOOL: 0,
    YELLOW_WOOL: 0,
    LAPIS: 0,
    RUBY: 0,
    EMERALD: 0,
    AMETHYST: 0
}
craft = {
    DIRT: {DIRT: 0},
    GRASS: {DIRT: 1},
    WATER: {WATER: 1},
    COAL: {COAL: 1},
    DIAMOND: {COAL: 2, WOOD: 3},
    ROCK: {DIRT: 3},
    STONE: {ROCK: 2},
    GOLD: {WOOD: 2, COAL: 1},
    WOOD: {WOOD: 1},
    BRICK: {STONE: 2},
    WOOL: {GRASS: 2},
    PINK_WOOL: {WOOL: 1},
    BLUE_WOOL: {WOOL: 1},
    GREEN_WOOL: {WOOL: 1},
    LIME_WOOL: {WOOL: 1},
    YELLOW_WOOL: {WOOL: 1},
    LAPIS: {WATER: 1, COAL: 1},
    RUBY: {DIAMOND: 1, GOLD: 1, LAPIS: 1},
    EMERALD: {DIAMOND: 2, GRASS: 4},
    AMETHYST: {DIAMOND: 1, GRASS: 2}
}
barrier_colors = (colors.red, colors.blue, colors.yellow, colors.green, colors.purple)
barrier_color = 0
selection = 0
field = [[random.choice(renderables) for i in range(settings.mapwidth)] for j in range(settings.mapheight)]
entity_field = [[0 for i in range(settings.mapwidth)] for j in range(settings.mapheight)]
small_entity_field = [[0 for i in range(settings.mapwidth)] for j in range(settings.mapheight)]
for r in range(settings.mapheight):
    for c in range(settings.mapwidth):
        if random.randint(1, 100) > 90:
            field[r][c] = DIAMOND
x = 0
y = 0


def render_entities():
    for r in range(settings.mapheight):
        for c in range(settings.mapwidth):
            if entity_field[r][c] > 0:
                pg.draw.rect(screen, colormap[entity_field[r][c]],
                             [settings.tilesize * c + settings.playersize // 2,
                              settings.tilesize * r + settings.playersize // 2,
                              settings.tilesize - settings.playersize,
                              settings.tilesize - settings.playersize])
    for r in range(settings.mapheight):
        for c in range(settings.mapwidth):
            if small_entity_field[r][c] > 0:
                pg.draw.rect(screen, colormap[small_entity_field[r][c]],
                             [settings.tilesize * c + (settings.playersize // 3 * 2) * 1.5,
                              settings.tilesize * r + (settings.playersize // 3 * 2) * 1.5,
                              settings.tilesize - (settings.playersize // 3 * 2) * 3,
                              settings.tilesize - (settings.playersize // 3 * 2) * 3])


def render_clouds():
    for i in range(settings.cloudnum):
        if cloudx[i] > settings.mapwidth * settings.tilesize + settings.cloudwidth:
            cloudx[i] = settings.cloudwidth * -1
            cloudy[i] = random.randint(0, settings.mapheight * settings.tilesize)
        pg.draw.rect(screen, colors.white, [cloudx[i], cloudy[i], settings.cloudwidth, settings.cloudheight], 10)
        cloudx[i] += i + 1


def render_field():
    screen.fill(colors.gray)
    for r in range(settings.mapheight):
        for c in range(settings.mapwidth):
            pg.draw.rect(screen, colormap[field[r][c]],
                         [settings.tilesize * c, settings.tilesize * r, settings.tilesize, settings.tilesize])
    render_entities()
    render_player()


def render_inventory():
    # length == 27 blocks
    x_pos = 10
    for i in inventory:
        pg.draw.rect(screen, colormap[i], [x_pos, settings.mapheight * settings.tilesize + settings.tilesize // 2,
                                           settings.tilesize, settings.tilesize])
        if mode == 's':
            text = font.render(str(inventory[i]), False, colors.black, colors.white)
            screen.blit(text, [x_pos, settings.mapheight * settings.tilesize + settings.tilesize // 3])
        x_pos += settings.tilesize + settings.tilesize // 3
    x_pos = 10
    for i in range(selection):
        x_pos += settings.tilesize + settings.tilesize // 3
    pg.draw.rect(screen, colors.yellow,
                 [x_pos + settings.tilesize // 3, settings.mapheight * settings.tilesize + settings.tilesize // 3,
                  settings.tilesize // 3, settings.tilesize // 3])
    render_clouds()


def render_player():
    pg.draw.rect(screen, colors.custom[1],
                 [settings.tilesize * x + settings.playersize, settings.tilesize * y + settings.playersize,
                  settings.tilesize - settings.playersize * 2, settings.tilesize - settings.playersize * 2])
    render_inventory()


def save_world():
    save_file = open('/home/andrew/world1.txt', 'wb')
    pickle.dump(field, save_file)
    save_file = open('/home/andrew/entities1.txt', 'wb')
    pickle.dump(entity_field, save_file)
    save_file = open('/home/andrew/smallentities1.txt', 'wb')
    pickle.dump(small_entity_field, save_file)
    save_file.close()
    if mode == 's':
        save_file = open('/home/andrew/inventory.txt', 'wb')
        pickle.dump(inventory, save_file)
        save_file.close()


pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode(
    [200, 150])
cloudx = []
cloudy = []
for i in range(settings.cloudnum):
    cloudx.append(settings.cloudwidth * -1)
    cloudy.append(random.randint(0, settings.mapheight * settings.tilesize))
pg.display.set_caption('MINECRAFT -- 2D!!!')
creative_button = Button(screen, 'Creative', 100, 25, colors.green)
survival_button = Button(screen, 'Survival', 100, 125, colors.red)
font = pg.font.SysFont("FreeSansBold.tff", 20)
done = False
mode = 's'
while not done:
    creative_button.draw_button()
    survival_button.draw_button()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            if creative_button.rect.collidepoint(mouse_x, mouse_y):
                field = [[BEDROCK for i in range(settings.mapwidth)] for j in range(settings.mapheight)]
                mode = 'c'
                done = True
            elif survival_button.rect.collidepoint(mouse_x, mouse_y):
                done = True
    pg.display.flip()
screen = pg.display.set_mode(
    [settings.mapwidth * settings.tilesize, settings.mapheight * settings.tilesize + settings.tilesize * 2])
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        elif event.type == pg.KEYDOWN:

            # movement
            if event.key == pg.K_UP:
                if not y == 0:
                    y -= 1
            elif event.key == pg.K_DOWN:
                if not y == settings.mapheight - 1:
                    y += 1
            elif event.key == pg.K_LEFT:
                if not x == 0:
                    x -= 1
            elif event.key == pg.K_RIGHT:
                if not x == settings.mapwidth - 1:
                    x += 1

            # interaction with blocks
            elif event.key == pg.K_SPACE:
                current_block = field[y][x]
                current_entity = entity_field[y][x]
                current_small_entity = small_entity_field[y][x]
                if current_small_entity > 0:
                    if mode == 's':
                        inventory[current_entity] += 1
                    small_entity_field[y][x] = 0
                elif current_entity > 0:
                    if mode == 's':
                        inventory[current_entity] += 1
                    entity_field[y][x] = 0
                elif not current_block == BEDROCK:
                    if mode == 's':
                        inventory[current_block] += 1
                    field[y][x] = BEDROCK
            elif event.key == pg.K_1:
                current_block = field[y][x]
                if mode == 's':
                    if inventory[resources[selection]] > 0:
                        if not current_block == BEDROCK:
                            inventory[current_block] += 1
                        field[y][x] = resources[selection]
                        inventory[resources[selection]] -= 1
                else:
                    field[y][x] = resources[selection]

            # crafting
            elif event.key == pg.K_2 and mode == 's':
                canBeMade = True
                for i in craft[selection + 1]:
                    if inventory[i] < craft[selection + 1][i]:
                        canBeMade = False
                        break

                if canBeMade:
                    for i in craft[selection + 1]:
                        inventory[i] -= craft[selection + 1][i]
                    inventory[selection + 1] += 1
            # entities placement
            elif event.key == pg.K_3:
                current_entity = entity_field[y][x]
                if mode == 's':
                    if inventory[resources[selection]] > 0:
                        if current_entity > 0:
                            inventory[current_entity] += 1
                        entity_field[y][x] = resources[selection]
                        inventory[resources[selection]] -= 1
                else:
                    entity_field[y][x] = resources[selection]
            elif event.key == pg.K_4:
                current_entity = small_entity_field[y][x]
                if mode == 's':
                    if inventory[resources[selection]] > 0:
                        if current_entity > 0:
                            inventory[current_entity] += 1
                        small_entity_field[y][x] = resources[selection]
                        inventory[resources[selection]] -= 1
                else:
                    small_entity_field[y][x] = resources[selection]

            # selection movement
            elif event.key == pg.K_LEFTBRACKET:
                selection -= 1
                if selection < 0:
                    selection = len(inventory) - 1
            elif event.key == pg.K_RIGHTBRACKET:
                selection += 1
                if selection > len(inventory) - 1:
                    selection = 0

            # saving and loading
            elif event.key == pg.K_s:
                save_world()
            elif event.key == pg.K_l:
                load_file = open('/home/andrew/world1.txt', 'rb')
                field = pickle.load(load_file)
                load_file = open('/home/andrew/entities1.txt', 'rb')
                entity_field = pickle.load(load_file)
                load_file = open('/home/andrew/smallentities1.txt', 'rb')
                small_entity_field = pickle.load(load_file)
                load_file.close()
                if mode == 's':
                    save_file = open('/home/andrew/inventory.txt', 'rb')
                    inventory = pickle.load(save_file)
                    save_file.close()

        # mouse wheel selection movement
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:
                selection -= 1
                if selection < 0:
                    selection = len(inventory) - 1
            elif event.button == 5:
                selection += 1
                if selection > len(inventory) - 1:
                    selection = 0

    # rendering stuff
    render_field()
    pg.display.flip()
    clock.tick(20)
    barrier_color += 1
    if barrier_color == len(barrier_colors):
        barrier_color = 0
