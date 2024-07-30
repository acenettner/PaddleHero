import pygame
import random
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

# Other game variables
score = 0
font = pygame.font.Font('4x3-pixel.ttf', 16)
game_started = False
game_over = False
game_paused = False

class Paddle:
    def __init__(self, position):
        self.sprite = pygame.transform.scale(block_img, (SCALE * 6, SCALE))
        self.size = pygame.math.Vector2(SCALE * 6, SCALE)
        self.position = position
        self.limits = (-self.size.x/2, cv_width - self.size.x/2)
        self.tag = "Paddle"
        self.clear_used = False

class Ball:
    last = 0

    def __init__(self, position):
        self.sprite = pygame.transform.scale(block_img, (SCALE, SCALE))
        self.size = pygame.math.Vector2(SCALE, SCALE)
        self.velocity = pygame.math.Vector2(0, -1).normalize()
        self.position = position
        self.speed = 5
        self.tag = "Ball"
    
    def bounce(self, side_collision):
        pygame.mixer.Sound.play(bounce_sound)
        if side_collision:
            self.velocity.x = -self.velocity.x
        else:
            self.velocity.y = -self.velocity.y

    def collide(self, object):
        # If the x and y positions overlap
        if (((self.position.x > object.position.x and 
            self.position.x < object.position.x + object.size.x) 
            or 
            (object.position.x > self.position.x and 
             object.position.x < self.position.x + self.size.x))
            and
            ((self.position.y > object.position.y and 
            self.position.y < object.position.y + object.size.y) 
            or 
            (object.position.y > self.position.y and 
             object.position.y < self.position.y + self.size.y))):
                if object.tag == "Paddle":
                    pygame.mixer.Sound.play(bounce_sound)
                    # Change velocity based on paddle location
                    if self.position.x < object.position.x + 8:
                        self.velocity = pygame.math.Vector2(-1, -0.5).normalize()
                    elif self.position.x < object.position.x + 24:
                        self.velocity = pygame.math.Vector2(-1, -1).normalize()
                    elif self.position.x < object.position.x + 56:
                        self.velocity = pygame.math.Vector2(0, -1).normalize()
                    elif self.position.x < object.position.x + 72:
                        self.velocity = pygame.math.Vector2(1, -1).normalize()
                    else:
                        self.velocity = pygame.math.Vector2(1, -0.5).normalize()

class Enemy:
    last = 0
    def __init__(self, position):
        self.sprite = self.sprite = pygame.transform.scale(block_img, (SCALE * 2, SCALE * 2))
        self.position = position
        self.size = pygame.math.Vector2(SCALE * 2, SCALE * 2)
        self.velocity = pygame.math.Vector2(0, 1).normalize()
        self.tag = "Enemy"

    def move_to_back(self):
        self.position.x = random.randrange(0, cv_width - SCALE * 2)
        self.position.y = enemies[Enemy.last].position.y - SCALE * 6
        Enemy.last = i
    
    def collide(self, object):
        if (((self.position.x > object.position.x and 
        self.position.x < object.position.x + object.size.x) 
        or 
        (object.position.x > self.position.x and 
        object.position.x < self.position.x + self.size.x))

        and

        ((self.position.y > object.position.y and 
        self.position.y < object.position.y + object.size.y) 
        or 
        (object.position.y > self.position.y and 
        object.position.y < self.position.y + self.size.y))):
            
            if object.tag == "Ball":
                self.move_to_back()
                global score
                score += 1
                pygame.mixer.Sound.play(die_sound)
            elif object.tag == "Paddle":
                global game_over
                game_over = True

# Init
SCALE = 16
bg_color = (85, 130, 97)
main_color = (49, 49, 49)
block_img = pygame.image.load("block.png").convert()

move_right = False
move_left = False

paddle = Paddle(pygame.math.Vector2(cv_width / 2, cv_height - SCALE))
ball = Ball(pygame.math.Vector2(cv_width/2, cv_height/2))
bounce_sound = pygame.mixer.Sound("bounce.wav")
die_sound = pygame.mixer.Sound("die.wav")

enemies = []
for i in range(6):
    # Need the - SCALE at the end because of i = 0; We don't want the enemy to spawn on screen immediately
    enemy = Enemy(pygame.math.Vector2(random.randrange(0, cv_width - SCALE * 2), -i * SCALE * 5 - SCALE))
    enemies.append(enemy)

# Index of last enemy in array. Needed for object pooling
Enemy.last = len(enemies) - 1

while running:
    # Title Screen
    if not game_started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    game_started = True
        canvas.fill(bg_color)
        display_title = font.render("Paddle Hero", False, main_color, bg_color)
        display_start = font.render(" Enter to Begin", False, main_color, bg_color)
        title_rect = display_title.get_rect(center=(cv_width/2, cv_height/2-40))
        canvas.blit(display_title, title_rect)
        start_rect = display_start.get_rect(center=(cv_width/2, cv_height/2+20))
        canvas.blit(display_start, start_rect)
    # Game
    else:
        if score % 20 == 0:
            paddle.clear_used = False
        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    move_right = True
                if event.key == pygame.K_LEFT:
                    move_left = True
                # Clear all enemies on screen
                if event.key == pygame.K_SPACE and not paddle.clear_used:
                    for i in range(len(enemies)):
                        if enemies[i].position.y > -enemies[i].size.y:
                            enemies[i].move_to_back()
                            score += 1
                    paddle.clear_used = True
                if event.key == pygame.K_RETURN:
                    # Reset game
                    if game_over:
                        for i in range(len(enemies)):
                            if enemies[i].position.y > -enemies[i].size.y:
                                enemies[i].move_to_back()
                        ball.position = pygame.math.Vector2(cv_width/2, cv_height/2)
                        ball.velocity = pygame.math.Vector2(0, -1)
                        score = 0
                        game_over = False
                    else:
                        game_paused = not game_paused
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    move_right = False
                if event.key == pygame.K_LEFT:
                    move_left = False

        if not game_paused and not game_over:
            # Update positions         
            if paddle.position.x > paddle.limits[1]:
                move_right = False
            if paddle.position.x < paddle.limits[0]:
                move_left = False    
            if move_right:
                paddle.position[0] += 3
            if move_left:
                paddle.position[0] -= 3

            ball.position += ball.velocity * ball.speed
            if ball.position.y > cv_height:
                game_over = True

            for i in range (len(enemies)):
                enemies[i].position.y += 1
                if enemies[i].position.y > cv_height:
                    enemies[i].move_to_back()

            # Check collisiosn
            if  ball.position.x < 0 or ball.position.x > cv_width - SCALE:
                ball.bounce(True)
            if  ball.position.y < 0:
                ball.bounce(False)

            ball.collide(paddle)
            for i in range (len(enemies)):
                enemies[i].collide(ball)
                enemies[i].collide(paddle)

            # Update sprites
            canvas.fill(bg_color)
            canvas.blit(paddle.sprite, paddle.position)
            canvas.blit(ball.sprite, ball.position)
            for i in range(len(enemies)):
                canvas.blit(enemies[i].sprite, enemies[i].position)

            display_score = font.render("Score: " + str(score), False, main_color, bg_color)
            canvas.blit(display_score, (0, 0))
    # Use pygame.display.update for specific portions of screen to change
    pygame.display.flip()
    # run at 60 fps
    clock.tick(60)