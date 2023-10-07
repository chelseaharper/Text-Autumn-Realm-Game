import sys
import buttons
import bestiary
import itemoptions
from time import sleep
import pygame
import characterbuilder
import old_game
import config
import utilities
from utilities import game_state
import map_functions
import old_menus

#Initialize pygame, define screen, and create needed variables for while loop
pygame.init()
screen = pygame.display.set_mode((config.screen_width, config.screen_height))
pygame.display.set_caption("Autumn's Realm")
clock = pygame.time.Clock()

game_menu = True
player_menu = False
charclass = 0
class_selected = False
stats_chosen = False
charstats = {}
player_named = False
player = ""

map = map_functions.Map()
map.load_map("map01")
gameinstance = old_game.Game(screen, map)

#Functions and variables for preparing a game either by creating a new game or loading a saved game
def start_game():
    global game_menu
    global game_state

    game_menu = False
    gameinstance.set_up()
    game_state = utilities.update_game_state(game_state)

def load_game():
    pass

update_start = pygame.USEREVENT + 0
update_quit = pygame.USEREVENT + 1

#Primary game loop
while game_state != utilities.GameState.ENDED:
    clock.tick(50)
    #Allow players to choose whether or not to play. TODO: Add Load Game option
    if game_menu == True:
        screen.blit(old_menus.startscreen_text, old_menus.startscreen_textRect)
        for events in pygame.event.get():
            if old_menus.start_button.draw(screen):
                game_menu = False
                player_menu = True
            elif old_menus.quit_button.draw(screen):
                utilities.end_game()
    #Allow players who choose a new game to select what clas they wish to play. POSSIBLE EXPANSION: Allow players to select image
    elif player_menu == True and class_selected == False:
        for events in pygame.event.get():
            screen.fill(config.black)
            screen.blit(old_menus.charclass_text, old_menus.charclass_textRect)
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_ESCAPE:
                    utilities.end_game()
            elif old_menus.figher_button.draw(screen):
                charclass = [1, "melee"]
                charstats = characterbuilder.buildstatblock(charclass[1])
                class_selected = True
            elif old_menus.archer_button.draw(screen):
                charclass = [2, "ranged"]
                charstats = characterbuilder.buildstatblock(charclass[1])
                class_selected = True
            elif old_menus.wizard_button.draw(screen):
                charclass = [3, "caster"]
                charstats = characterbuilder.buildstatblock(charclass[1])
                class_selected = True
    #Allow players who choose a new game to see and approve their character stats
    elif player_menu == True and class_selected == True and stats_chosen == False:
        for events in pygame.event.get():
            screen.fill(config.black)
            stat_display = old_menus.display_stats(charstats)
            screen.blit(old_menus.stats_text, old_menus.stats_textRect)
            for k in stat_display:
                screen.blit(k, stat_display[k])
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_ESCAPE:
                    utilities.end_game()
            elif old_menus.yes_button.draw(screen):
                reroll = 'n'
                stats_chosen = True
            elif old_menus.no_button.draw(screen):
                reroll = 'y'
                charstats = characterbuilder.buildstatblock(charclass[1])
    #Get character name from players in order to create their character and start the game     
    elif player_menu == True and class_selected == True and stats_chosen == True and player_named == False:
        screen.fill(config.black)
        pygame.draw.rect(screen, config.white, old_menus.name_input_rect, 4)
        screen.blit(old_menus.player_name_text, old_menus.player_name_textRect)
        text_screen = old_menus.font.render(player, False, (255, 255, 255))
        screen.blit(text_screen, (old_menus.name_input_rect.x +5, old_menus.name_input_rect.y +5))
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                utilities.end_game()
            elif events.type == pygame.KEYDOWN:
                if events.key == pygame.K_ESCAPE:
                    utilities.end_game()
                elif events.key == pygame.K_BACKSPACE:
                    player = player[:-1]
                elif events.key == pygame.K_RETURN and player == "":
                    pass
                elif events.key == pygame.K_RETURN:
                    player_named = True
                else:
                    player += events.unicode
    #Set up game using information collected in previous menus
    elif game_menu == False and gameinstance.playstate == utilities.PlayState.MENU:
        gameinstance.set_up(charclass[0], charstats, player)
        game_state = utilities.GameState.RUNNING
    #Main gameplay; includes moving and allows random encounters. TODO: add travel to towns and other areas
    if gameinstance.playstate == utilities.PlayState.MAP:
        gameinstance.update()
    #Battle processing to resolve rnadon encounters
    elif gameinstance.playstate == utilities.PlayState.BATTLE:
        gameinstance.update()
    #TODO: Allows players to raise a stat (when written)
    elif gameinstance.playstate == utilities.PlayState.STATMENU:
        gameinstance.update()
    pygame.display.flip()
