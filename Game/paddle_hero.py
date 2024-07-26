import pygame
pygame.init()

# clock
clock = pygame.time.Clock()
# Create Canvas
canvas = pygame.display.set_mode((400, 400))

# Title
pygame.display.set_caption("PADDLE HERO")
running = True

bg_color = (85, 130, 97)
block_img = pygame.image.load("block.png").convert()
paddle = pygame.transform.scale(block_img, (16, 16))
move_right = False
move_left = False
pos_x = 0
pos_y = 0
pos = (pos_x, pos_y)

while running:
    canvas.fill(bg_color)
    canvas.blit(paddle, pos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:
                move_left = False
    if move_right:
        pos_x += 3
    if move_left:
        pos_x -= 3
    pos = (pos_x, pos_y)
    # Use pygame.display.update for specific portions of screen to change
    pygame.display.flip()
    # run at 60 fps
    clock.tick(60)
