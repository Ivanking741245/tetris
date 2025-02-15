import pygame
pygame.init()
import Game
FPS = 60
BOARD_ROWS = 20
BOARD_COLS = 10
BLOCK_SIZE = 40
BORDER_WIDTH = int(BLOCK_SIZE/15)
WIDTH = BLOCK_SIZE*BOARD_COLS
HEIGHT = BLOCK_SIZE*BOARD_ROWS
window = pygame.display.set_mode( (WIDTH, HEIGHT) )
clock = pygame.time.Clock()
board = Game.Board(BOARD_ROWS, BOARD_COLS)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(pygame.quit())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z or event.key == pygame.K_UP:
                board.rotate(-1)
            if event.key == pygame.K_x:
                board.rotate(1)
            if event.key == pygame.K_LEFT:
                board.move(-1)
            if event.key == pygame.K_RIGHT:
                board.move(1)
            if event.key == pygame.K_SPACE:
                board.drop()
            if event.key == pygame.K_LSHIFT:
                board.hold()
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_DOWN]:
        board.fall()
    window.fill("#000000")
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            if board.board[i][j]:
                pygame.draw.rect(
                    window,
                    board.board[i][j],
                    (
                        j*BLOCK_SIZE + BORDER_WIDTH,
                        i*BLOCK_SIZE + BORDER_WIDTH,
                        BLOCK_SIZE - BORDER_WIDTH*2,
                        BLOCK_SIZE - BORDER_WIDTH*2,
                    )
                )
    for i in range(board.loadedTiles[0].size):
        for j in range(board.loadedTiles[0].size):
            if board.loadedTiles[0].mass[i][j]: 
                pygame.draw.rect(
                    window,
                    board.loadedTiles[0].color,
                    (
                        (board.cursor_x + j)*BLOCK_SIZE + BORDER_WIDTH,
                        (board.cursor_y+ i)*BLOCK_SIZE + BORDER_WIDTH,
                        BLOCK_SIZE - BORDER_WIDTH*2,
                        BLOCK_SIZE - BORDER_WIDTH*2,
                    )
                )
    board.update()
    pygame.display.update()
    clock.tick(FPS)