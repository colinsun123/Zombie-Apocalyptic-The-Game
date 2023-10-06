import pygame
from pygame.locals import *
import time
import math
import random

# Initialize pygame and conditions
pygame.init()
pygame.mixer.init()

# Constants that need to be fixed
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PLAYER_SPEED = 0.35
BULLET_SPEED = 2.3
ZOMBIE_SPEED = 0.55
SPAWN_RATE = 1000
MEDKIT_CHANCE = 15
MUTANT_SPAWN_RATE = 3000
MUTANT_SPEED = 0.85
current_level = 1
MAX_LEVEL = 4


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Zombie Apocalyptic")

# preLoad images, sound and other stuffs to the game
background_image = pygame.image.load('main.jpg').convert_alpha()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
player_image = pygame.image.load('mcharacter1.png').convert_alpha()
bullet_image = pygame.image.load('bullet.png').convert_alpha()
dead_image = pygame.image.load('dead1.png').convert_alpha()
zombie_image = pygame.image.load('zombie.png').convert_alpha()
medkit_image = pygame.image.load('medkit.png').convert_alpha()
level1_background = pygame.image.load('level1.png').convert_alpha()
level1_background = pygame.transform.scale(level1_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
mutant_image = pygame.image.load('mutant.png').convert_alpha()
level2_background = pygame.image.load('level2.png').convert_alpha()
level2_background = pygame.transform.scale(level2_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
tyrant_image = pygame.image.load('tyrant.png').convert_alpha()
t_bullet_image = pygame.image.load('t_bullet.png').convert_alpha()
level3_background = pygame.image.load('level3.png').convert_alpha()
level3_background = pygame.transform.scale(level3_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
mcharacter2_image = pygame.image.load('mcharcter2.png').convert_alpha()
button_sound = pygame.mixer.Sound('press.mp3')
footstep_sound = pygame.mixer.Sound('footstep.mp3')
med_pick_sound = pygame.mixer.Sound('med_pick.mp3')
zombie_sound = pygame.mixer.Sound('zombiesound.mp3')
mutant_sound = pygame.mixer.Sound('mutantsound.mp3')
handgun_sound = pygame.mixer.Sound('handgun.mp3')
rifle_sound = pygame.mixer.Sound('level3gun.mp3')

font = pygame.font.SysFont(None, 72)



class Zombie:
    def __init__(self):
        self.x, self.y = self.random_spawn()
        self.hp = 2

    def random_spawn(self):
        side = random.randint(1, 4)
        if side == 1:  # Top
            return random.randint(0, SCREEN_WIDTH), 0
        elif side == 2:  # Right
            return SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT)
        elif side == 3:  # Bottom
            return random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT
        elif side == 4:  # Left
            return 0, random.randint(0, SCREEN_HEIGHT)

    def move(self, target_x, target_y):
        angle = math.atan2(target_y - self.y, target_x - self.x)
        self.x += ZOMBIE_SPEED * math.cos(angle)
        self.y += ZOMBIE_SPEED * math.sin(angle)

    def render(self):
        screen.blit(zombie_image, (self.x, self.y))

    def hit_by_bullet(self):
        self.hp -= 1
        return self.hp <= 0

class Mutant:
    def __init__(self):
        self.image = pygame.image.load("mutant.png")
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = -self.image.get_height()
        self.speed = MUTANT_SPEED


    def move(self):
        self.y += self.speed

    def render(self):
        screen.blit(self.image, (self.x, self.y))

    def is_out_of_bound(self):
        return self.y > SCREEN_HEIGHT or self.y < -self.image.get_height()









def show_loading_screen(area_name):
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 55)
    loading_text = font.render(f'Loading {area_name}...', True, WHITE)
    screen.blit(loading_text, (SCREEN_WIDTH // 2 - loading_text.get_width() // 2, SCREEN_HEIGHT // 2 - loading_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(5500)




def start_interface():
    text_visible = True
    clock = pygame.time.Clock()

    pygame.mixer.music.load('main_lobby.mp3')
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)

    button_sound = pygame.mixer.Sound('press.mp3')

    dev_font = pygame.font.SysFont(None, 24)
    dev_text = dev_font.render("Developer: Wenhao Sun - University of Washington", True, WHITE)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit(0)
            if event.type == KEYDOWN:
                button_sound.play() # play the button sound when any key is pressed
                pygame.mixer.music.stop()
                return

        screen.blit(background_image, (0, 0))
        title_text = font.render("Zombie Apocalyptic", True, RED)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
        screen.blit(title_text, title_rect)

        if text_visible:  # only blit the text if it's set to be visible
            instruction_text = pygame.font.SysFont(None, 36).render("Press any button to start", True, WHITE)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(instruction_text, instruction_rect)


        screen.blit(dev_text, (SCREEN_WIDTH - dev_text.get_width() - 10, SCREEN_HEIGHT - dev_text.get_height() - 10))

        pygame.display.flip()

        text_visible = not text_visible
        clock.tick(1)  # blink every second






def clamp(value, min_value, max_value):
    """Ensure the value stays between min_value and max_value"""
    return max(min_value, min(value, max_value))

MAX_LEVEL = 4

def handle_gameplay(current_level):
    #pre-conditions
    player_position = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
    player_velocity = [0, 0]
    health = 100
    bullets = []
    last_shot_time = 0
    zombies = []
    medkits = []
    mutants = []
    last_mutant_spawn_time = pygame.time.get_ticks()
    last_spawn_time = pygame.time.get_ticks()
    angle = 0
    score = 0
    last_footstep_time = 0
    last_zombie_sound_time = 0
    last_mutant_sound_time = 0
    last_gun_sound_time = 0

    pygame.mixer.music.load('battle_song.mp3')
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)




    is_player_alive = True



    while is_player_alive :
        current_time = pygame.time.get_ticks()

        player_position[0] = clamp(player_position[0] + player_velocity[0], 0, SCREEN_WIDTH)
        player_position[1] = clamp(player_position[1] + player_velocity[1], 0, SCREEN_HEIGHT)

        if current_level == 1:
            screen.blit(level1_background, (0, 0))
        elif current_level == 2:
            screen.blit(level2_background, (0, 0))
        elif current_level == 3:
            screen.blit(level3_background, (0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit(0)



            if score >= 500:
                return "WIN"


        keys = pygame.key.get_pressed()




        # Movement of character
        if keys[K_w]:
            player_velocity[1] = -PLAYER_SPEED
        elif keys[K_s]:
            player_velocity[1] = PLAYER_SPEED
        else:
            player_velocity[1] = 0

        if keys[K_a]:
            player_velocity[0] = -PLAYER_SPEED
        elif keys[K_d]:
            player_velocity[0] = PLAYER_SPEED
        else:
            player_velocity[0] = 0

        # Check if the player is moving
        if player_velocity[0] != 0 or player_velocity[1] != 0:
            if current_time - last_footstep_time >= 750:
                footstep_sound.play()
                pygame.mixer.music.set_volume(0.6)
                last_footstep_time = current_time

        player_position[0] += player_velocity[0]
        player_position[1] += player_velocity[1]









        # Calculate shooting angle
        mouse_position = pygame.mouse.get_pos()
        dx = mouse_position[0] - player_position[0]
        dy = mouse_position[1] - player_position[1]
        angle = math.degrees(-math.atan2(dy, dx))

        # about Shooting

        shoot_time = pygame.time.get_ticks()
        shooting_delay = 1000
        gun_sound = handgun_sound
        handgun_sound.set_volume(0.65)
        rifle_sound.set_volume(0.65)

        if current_level == 3:
            shooting_delay = 250
            gun_sound = rifle_sound

        if keys[K_f] and shoot_time - last_shot_time > shooting_delay:
            bullets.append([player_position[0], player_position[1], angle])
            last_shot_time = shoot_time


            if shoot_time - last_gun_sound_time > 1000:
                gun_sound.play()
                last_gun_sound_time = shoot_time








        # Bullet mechanics
        new_bullets = []
        for bullet in bullets:
            bullet_dx = BULLET_SPEED * math.cos(math.radians(-bullet[2]))
            bullet_dy = BULLET_SPEED * math.sin(math.radians(-bullet[2]))
            bullet[0] += bullet_dx
            bullet[1] += bullet_dy

            if 0 < bullet[0] < SCREEN_WIDTH and 0 < bullet[1] < SCREEN_HEIGHT:
                new_bullets.append(bullet)
                screen.blit(bullet_image, (bullet[0], bullet[1]))

        bullets = new_bullets

        # Render player


        if current_level == 3:
            actual_player_image = mcharacter2_image
        else:
            actual_player_image = player_image

        rotated_player_image = pygame.transform.rotate(actual_player_image, angle)
        new_rect = rotated_player_image.get_rect(center=player_position)
        screen.blit(rotated_player_image, new_rect.topleft)

        # This is the health bar part
        outline_thickness = 5
        health_bar_width = 204
        health_bar_height = 40


        pygame.draw.rect(screen, WHITE,
                         (10 - outline_thickness, 10 - outline_thickness, health_bar_width + 2 * outline_thickness,
                          health_bar_height + 2 * outline_thickness))


        gradient = pygame.Surface((health * 2, health_bar_height))
        for x in range(health * 2):
            red = int(255 - (x / 200) * 255)
            green = int((x / 200) * 255)
            gradient.fill((red, green, 0), rect=pygame.Rect(x, 0, 1, health_bar_height))
        screen.blit(gradient, (10, 10))

        # Display health percentage
        health_font = pygame.font.SysFont(None, 36)
        health_text = health_font.render(f"{health}%", True, BLACK)
        health_rect = health_text.get_rect(
            center=(health_bar_width / 2 + 10, 10 + health_bar_height / 2))
        screen.blit(health_text, health_rect)

        # Display score at top left
        score_text = pygame.font.SysFont(None, 36).render(f"Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(score_text, score_rect)


        # Zombie spawning mechanism

        SOUND_COOLDOWN = 10000

        if current_time - last_zombie_sound_time > SOUND_COOLDOWN:
            zombie_sound.play()
            last_zombie_sound_time = current_time




        current_time = pygame.time.get_ticks()
        if current_level == 1 and current_time - last_spawn_time >= SPAWN_RATE:
            zombies.append(Zombie())
            last_spawn_time = current_time

        if current_level == 2 and current_time - last_spawn_time >= SPAWN_RATE:
            zombies.append(Zombie())
            last_spawn_time = current_time






        # Zombie movement and attacking mechsiams
        for zombie in zombies[:]:
            zombie.move(player_position[0], player_position[1])
            zombie_distance = math.sqrt((player_position[0] - zombie.x)**2 + (player_position[1] - zombie.y)**2)

            if zombie_distance < 60:  # Adjust the value for the distance to initiate attack
                health -= 25
                zombies.remove(zombie)
                if health <= 0:
                    return "LOST"  # end of the game

        zombies_to_remove = []
        bullets_to_remove = []
        # Bullet-Zombie collision
        for bullet in bullets:
            for zombie in zombies[:]:
                distance = math.sqrt((bullet[0] - zombie.x)**2 + (bullet[1] - zombie.y)**2)
                if distance < 100:
                    if zombie.hit_by_bullet():
                        zombies_to_remove.append(zombie)
                        bullets_to_remove.append(bullet)
                        score += 10
                        if random.randint(1, 100) <= MEDKIT_CHANCE:
                            medkits.append([zombie.x, zombie.y])
                        break

        for bullet in bullets_to_remove:
            if bullet in bullets:  # Check if bullet still exists in the bullets list before removing
                bullets.remove(bullet)

        for zombie in zombies_to_remove:
            if zombie in zombies:  # Check if zombie still exists in the zombies list before removing
                zombies.remove(zombie)




                # Player-Medkit collision
        for medkit in medkits[:]:
            distance = math.sqrt((player_position[0] - medkit[0]) ** 2 + (player_position[1] - medkit[1]) ** 2)
            if distance < 60:
             health += 25
             medkits.remove(medkit)
             med_pick_sound.play()
            if health > 100:
             health = 100

        # Render medkits
        for medkit in medkits:
            screen.blit(medkit_image, (medkit[0], medkit[1]))

        # Render zombies
        for zombie in zombies:
            zombie.render()

            # Mutant spawning mechanism
        SOUND_COOLDOWN = 7000

        if current_level == 2:
            if current_time - last_mutant_sound_time > SOUND_COOLDOWN:
                mutant_sound.play()
                last_mutant_sound_time = current_time

        if current_level == 3:
            if current_time - last_mutant_sound_time > SOUND_COOLDOWN:
                mutant_sound.play()
                last_mutant_sound_time = current_time


        if current_level == 2 and current_time - last_mutant_spawn_time >= MUTANT_SPAWN_RATE:
            mutants.append(Mutant())
            last_mutant_spawn_time = current_time

            # how does Mutant movement
        for mutant in mutants[:]:
            mutant.move()
            if mutant.is_out_of_bound():
                mutants.remove(mutant)

            # Render mutants
        for mutant in mutants:
            mutant.render()

            # Mutant-player collision
        for mutant in mutants[:]:
            distance = math.sqrt((player_position[0] - mutant.x) ** 2 + (player_position[1] - mutant.y) ** 2)
            if distance < 100:
                health -= 25
                mutants.remove(mutant)
                if health <= 0:
                    return False





        if current_time - last_spawn_time >= SPAWN_RATE:
            print("Zombie spawn condition met!")
            number_of_zombies = 2 if current_level == 3 else 1
            for _ in range(number_of_zombies):
                zombies.append(Zombie())
            last_spawn_time = current_time

        if current_level == 3 and current_time - last_mutant_spawn_time >= MUTANT_SPAWN_RATE:
            number_of_mutants = 2  # spawn 2 mutants at once for level 3 for upgrade difficulity
            for _ in range(number_of_mutants):
                mutants.append(Mutant())
            last_mutant_spawn_time = current_time








        pygame.display.flip()


def game_over_screen():
    scream_sound = pygame.mixer.Sound('endsound.mp3')
    scream_sound.play()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit(0)
            if event.type == MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if retry_button.collidepoint((mx, my)):
                    start_interface()

                    running = False

        screen.fill(BLACK)

        # The "Game Over" text
        game_over_text = font.render("Game Over", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        # The "Retry" button
        retry_button = pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2, 140, 40))
        retry_text = pygame.font.SysFont(None, 36).render("Retry", True, BLACK)
        screen.blit(retry_text, (retry_button.x + 20, retry_button.y + 10))

        pygame.display.flip()

def loading_screen(area_name):
    screen.fill(BLACK)
    loading_text = font.render(f"{area_name}...", True, WHITE)
    loading_rect = loading_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(loading_text, loading_rect)
    pygame.display.flip()
    pygame.time.wait(8000)

def end_page():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit(0)
            if event.type == MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if retry_button.collidepoint((mx, my)):
                    start_interface()
                    running = False

        screen.fill(BLACK)

        # the "Thank you for playing!" Thank you!
        thank_you_text = font.render("Thank you for playing!", True, RED)
        screen.blit(thank_you_text, (SCREEN_WIDTH // 2 - thank_you_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        # The developer's name, me
        dev_text = pygame.font.SysFont(None, 36).render("Developer: Wenhao Sun", True, WHITE)
        screen.blit(dev_text, (SCREEN_WIDTH // 2 - dev_text.get_width() // 2, SCREEN_HEIGHT // 2))

        # THE "Back to Lobby" button
        retry_button = pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, 220, 40))
        retry_text = pygame.font.SysFont(None, 36).render("Back to Lobby", True, BLACK)
        screen.blit(retry_text, (retry_button.x + 20, retry_button.y + 10))

        pygame.display.flip()



game_in_progress = True


while game_in_progress:
    start_interface()
    while True:  # Level loop
        if current_level == 1:
            show_loading_screen("Area 1, kill 50 zombies to proof you are worthy")
        elif current_level == 2:
            show_loading_screen("Area 2, new zombies are incoming")
        elif current_level == 3:
            show_loading_screen("Area 3, upgraded weapons but more zombies")
        elif current_level == 4:
            scream_sound = pygame.mixer.Sound('endsound.mp3')
            scream_sound.play()
            pygame.mixer.music.stop()
            show_loading_screen(",but it's the end,too many of them,even you can't survive")
            end_page()
            break

        result = handle_gameplay(current_level)

        if result == "LOST":
            pygame.mixer.music.stop()
            game_over_screen()
            break  # the game end
        elif result == "WIN":
            current_level += 1
            if current_level > MAX_LEVEL:
                current_level = 1
                break  # If the max level is exceeded, return to the starting interface



