import pygame
import random
import math
from pygame import mixer

# initialize PyGame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((1280, 720))


# Title and Icon
pygame.display.set_caption("Snakes on a spaceship")
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)
background = pygame.image.load("images/background.jpg")

# Sound
mixer.music.load("sound/background_music.mp3")
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Player variables
img_player = pygame.image.load("images/rocket.png")
player_x = 635
player_y = 600
player_x_change = 0

# Enemy variables
img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 9

for e in range(number_of_enemies):
    img_enemy.append(pygame.image.load("images/alien.png"))
    enemy_x.append(random.randint(0, 1216))
    enemy_y.append(random.randint(50, 200))
    enemy_x_change.append(0.7)
    enemy_y_change.append(75)

# Bullet variables
img_bullet = pygame.image.load("images/missile.png")
bullet_x = 0
bullet_y = 600
bullet_x_change = 0
bullet_y_change = 5.5
visible_bullet = False


# Score
score = 0
my_font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 20
text_y = 20

# End of game text
end_font = pygame.font.Font("freesansbold.ttf", 60)

def final_text():
    my_final_font = end_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(my_final_font, (450, 200))

# Show score
def show_score(x,y):
    text = my_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (x,y))



# Player functions
def player(x, y):
    screen.blit(img_player, (x, y))

# Player functions
def enemy(x, y, en):
    screen.blit(img_enemy[en], (x, y))



# Shoot Bullet
def shoot (x, y):
    global visible_bullet
    visible_bullet = True
    screen.blit(img_bullet, (x + 32, y + 15))


# Detect collision
def there_is_a_collision(x_1, y_1, x_2, y_2):
    distance = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distance < 30:
        return True
    else:
        return False



# Game loop
is_running = True
while is_running:
    screen.blit(background, (0, 0))

    # Events iteration
    for event in pygame.event.get():

        # Closing event
        if event.type == pygame.QUIT:
            is_running = False

        # Press keys event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -1.7
            if event.key == pygame.K_RIGHT:
                player_x_change = 1.7
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound("sound/shot.mp3")
                mixer.music.set_volume(0.7)
                bullet_sound.play()
                if not visible_bullet:
                    bullet_x = player_x
                    shoot(bullet_x, bullet_y)

        # Release key event
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Modify player location
    player_x += player_x_change

    # Keep player inside screen
    if player_x <= 0:
        player_x = 0
    elif player_x >= 1216:
        player_x = 1216


    # Modify enemy location
    for enem in range(number_of_enemies):
        # The End
        if enemy_y[enem] > 600:
            for k in range(number_of_enemies):
                enemy_y[k] = 1500
            final_text()
            break
        enemy_x[enem] += enemy_x_change[enem]


    # Keep enemy inside screen
        if enemy_x[enem] <= 0:
            enemy_x_change[enem] = 1
            enemy_y[enem] += enemy_y_change[enem]
        elif enemy_x[enem] >= 1216:
            enemy_x_change[enem] = -1
            enemy_y[enem] += enemy_y_change[enem]

        # Collision
        collision = there_is_a_collision(enemy_x[enem], enemy_y[enem], bullet_x, bullet_y)
        if collision:
            collision_sound = mixer.Sound("sound/punch.mp3")
            mixer.music.set_volume(0.7)
            collision_sound.play()
            bullet_y = 600
            visible_bullet = False
            score += 1
            enemy_x[enem] = random.randint(0, 1216)
            enemy_y[enem] = random.randint(50, 200)
        enemy(enemy_x[enem], enemy_y[enem], enem)


    # Bullet movement
    if bullet_y <= - 32:
        bullet_y = 600
        visible_bullet = False
    if visible_bullet:
        shoot(bullet_x, bullet_y)
        bullet_y -= bullet_y_change







    player(player_x, player_y)

    show_score(text_x, text_y)


    # Update
    pygame.display.update()
