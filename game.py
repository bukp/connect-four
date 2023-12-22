import pygame
from pw4 import *

def display_board():
    pygame.draw.rect(window, "blue", (0, 0, 600, 600))
    for i in range(8):
        for j in range(8):
            pygame.draw.circle(window, "yellow" if brd[i, j] == "X" else "red" if brd[i, j] == "O" else "black",((600/8)*i + (600/16),(600/8)*j + (600/16)), (600/16)*0.90)
    pygame.display.flip()
brd = board()
running = True
setting = ("player", "bot")
state = "waiting"
pygame.init()
window = pygame.display.set_mode((600, 600))
display_board()
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if state == "waiting" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if brd.can_play(int(event.pos[0]//(600/8))+1):
                brd.play(int(event.pos[0]//(600/8))+1)
                display_board()
                if brd.state() != 0:
                    print(f"Player {brd.state()} won")
                    running = False
                    break
                brd.play(brd.eval()[0])
                display_board()
                if brd.state() != 0:
                    print(f"Player {brd.state()} won")
                    running = False
                #state = "animation"

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False