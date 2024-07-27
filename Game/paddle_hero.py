import pygame
pygame.init()

# clock
clock = pygame.time.Clock()
# Create Canvas
cv_width = 250
cv_height = 400
canvas = pygame.display.set_mode((cv_width, cv_height))

# Title
pygame.display.set_caption("PADDLE HERO")
running = True

scale = 16
bg_color = (85, 130, 97)
block_img = pygame.image.load("block.png").convert()
ball = pygame.transform.scale(block_img, (scale, scale))

class Paddle:
    def __init__(self, position, limits):
        self.sprite = pygame.transform.scale(block_img, (scale * 5, scale))
        self.position = position
        self.limits = limits

class Ball:
    def __init__(self, position):
        self.sprite = pygame.transform.scale(block_img, (scale, scale))
        self.velocity = pygame.math.Vector2(1, -1)
        self.position = position
        self.speed = 3
    
    def bounce(self, side_collision):
        if side_collision:
            self.velocity.x = -self.velocity.x
        else:
            self.velocity.y = -self.velocity.y

move_right = False
move_left = False

paddle = Paddle(pygame.math.Vector2(cv_width / 2, cv_height - scale), (0, cv_width - (scale * 5)))
ball = Ball(pygame.math.Vector2(cv_width/2, cv_height/2))

while running:
    canvas.fill(bg_color)
    
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
                
    if paddle.position.x > paddle.limits[1]:
        move_right = False
    if paddle.position.x < paddle.limits[0]:
        move_left = False
                
    if move_right:
        paddle.position[0] += 3
    if move_left:
        paddle.position[0] -= 3

    ball.position += ball.velocity * ball.speed
    if  ball.position.x < 0 or ball.position.x > cv_width - scale:
        ball.bounce(True)
    if  ball.position.y < 0 or ball.position.y > cv_height - scale:
        ball.bounce(False)
    canvas.blit(paddle.sprite, paddle.position)
    canvas.blit(ball.sprite, ball.position)
    # Use pygame.display.update for specific portions of screen to change
    pygame.display.flip()
    # run at 60 fps
    clock.tick(60)