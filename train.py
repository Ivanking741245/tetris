import pygame
pygame.init()
import Game
FPS = 60
BOARD_ROWS = 20
BOARD_COLS = 10
BLOCK_SIZE = 12
BORDER_WIDTH = max(1, int(BLOCK_SIZE/15))

POPULATION_ROWS = 4
POPULATION_COLS = 6

BOARD_WIDTH = BLOCK_SIZE*BOARD_COLS
BOARD_HEIGHT = BLOCK_SIZE*BOARD_ROWS
BOARD_GAP = BORDER_WIDTH*5
WIDTH = BOARD_WIDTH * POPULATION_COLS + BOARD_GAP*(POPULATION_COLS-1)
HEIGHT = BOARD_HEIGHT * POPULATION_ROWS + BOARD_GAP*(POPULATION_ROWS-1)
window = pygame.display.set_mode( (WIDTH, HEIGHT) )
clock = pygame.time.Clock()

surfaces = [

]
for i in range(POPULATION_ROWS):
    surfaces.append([])
    for j in range(POPULATION_COLS):
        surfaces[i].append(pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT)))

board = Game.Board(BOARD_ROWS, BOARD_COLS)






def drawBoard(b:Game.Board, surface:pygame.Surface):
    surface.fill("#000000")
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            if b.board[i][j]:
                pygame.draw.rect(
                    surface,
                    b.board[i][j],
                    (
                        j*BLOCK_SIZE + BORDER_WIDTH,
                        i*BLOCK_SIZE + BORDER_WIDTH,
                        BLOCK_SIZE - BORDER_WIDTH*2,
                        BLOCK_SIZE - BORDER_WIDTH*2,
                    )
                )
    for i in range(b.loadedTiles[0].size):
        for j in range(b.loadedTiles[0].size):
            if b.loadedTiles[0].mass[i][j]: 
                pygame.draw.rect(
                    surface,
                    b.loadedTiles[0].color,
                    (
                        (b.cursor_x + j)*BLOCK_SIZE + BORDER_WIDTH,
                        (b.cursor_y+ i)*BLOCK_SIZE + BORDER_WIDTH,
                        BLOCK_SIZE - BORDER_WIDTH*2,
                        BLOCK_SIZE - BORDER_WIDTH*2,
                    )
                )



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
    if not board.alive:
        board.reset()
    window.fill("#FFFFFF")

    for i in range(POPULATION_ROWS):
        for j in range(POPULATION_COLS):
            drawBoard(board, surfaces[i][j])
            surfaceX = j*(BOARD_WIDTH + BOARD_GAP)
            surfaceY = i*(BOARD_HEIGHT+ BOARD_GAP)
            window.blit(surfaces[i][j], (surfaceX, surfaceY))
    board.update()
    pygame.display.update()
    clock.tick(FPS)