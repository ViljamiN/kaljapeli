import pygame
from drawer import *
from timer import Timer
from helper_functions import *
from player import *
from game_logic import *


def main():

    pygame.init()
    surface_height = 700
    surface_width = 1200
    main_surface = pygame.display.set_mode((surface_width, surface_height))

    def manual_input():
        ask = "Press Enter for new player, or anything else to start"
        fontobject = pygame.font.Font(None, 46)
        main_surface.blit(fontobject.render(ask, 1, (255, 255, 255)), (main_surface.get_width(
        )/2-fontobject.size(ask)[0]/2, main_surface.get_height()/2-75))
        pygame.display.flip()

        for evt in pygame.event.get():
            if evt.type == KEYDOWN:
                if evt.key == K_RETURN:
                    main_surface.fill((0, 0, 0))
                    players.append(addPlayer(main_surface))
                else:
                    more_players = False

    def select_game_mode():
        options = ["Minute Beer Mode - Lehtisaari",
                   "Classic Minute Beer Mode",
                   "Optimized BAC Mode"]
        question = "Select game mode"
        selection = 0

        while True:
            for evt in pygame.event.get():
                if evt.type == KEYDOWN:
                    if evt.key == K_LEFT:
                        if selection == 0:
                            selection = len(options) - 1
                        else:
                            selection -= 1
                    elif evt.key == K_RIGHT:
                        if selection == len(options) - 1:
                            selection = 0
                        else:
                            selection += 1
                    elif evt.key == K_RETURN:
                        if selection == 0:
                            return MinuteBeerModeLehtisaari(players)
                        elif selection == 1:
                            return ClassicMinuteBeerMode(players)
                        elif selection == 2:
                            return OptimizedBACMode(players)

            main_surface.fill((0, 0, 0))

            for i in range(len(options)):
                block_width = main_surface.get_width()/len(options)
                block = pygame.Rect(i*block_width + 10,
                                    main_surface.get_height()/2, block_width - 20, 75)
                if i == selection:
                    pygame.draw.rect(main_surface, (100, 100, 255), block, 3)
                else:
                    pygame.draw.rect(main_surface, (255, 255, 255), block, 1)
                fontobject = pygame.font.Font(None, 40)
                main_surface.blit(fontobject.render(options[i], 1, (255, 255, 255)), (
                    i*block_width + block_width/2 - fontobject.size(options[i])[0]/2, main_surface.get_height()/2 + 25))

            fontobject = pygame.font.Font(None, 40)
            main_surface.blit(fontobject.render(question, 1, (255, 255, 255)), (main_surface.get_width(
            )/2-fontobject.size(question)[0]/2, main_surface.get_height()/2-75))
            pygame.display.flip()

    players = []
    more_players = True
    while more_players:
        manual_input()

    # draw a screen where the user can choose a game mode
    game_mode = None
    while game_mode == None:
        game_mode = select_game_mode(main_surface)

    drawer = Drawer(main_surface, players, game_mode)

    Timer.reset_clock()
    Timer.round_time = 5

    # Count down loop
    while Timer.get_elapsed_time() < Timer.round_time:
        game_mode.update_game()
        drawer.draw_count_down()
        pygame.display.flip()

    Timer.reset_clock()
    Timer.round_time = 20
    # Main loop
    while True:
        game_mode.update_game()
        drawer.draw()
        pygame.display.flip()


main()
