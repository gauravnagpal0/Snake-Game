import pygame
import random
import os

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255)

pygame.init()

width = 900
height = 600

#background image
wel=pygame.image.load("welcome.jpeg")
wel=pygame.transform.scale(wel,(width,height))
bgimg=pygame.image.load("background3.jpg")
bgimg=pygame.transform.scale(bgimg,(width,height))
game_o=pygame.image.load("game.jpg")
game_o=pygame.transform.scale(game_o,(width,height))

# Game Window
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snakes with Gaurav")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)


def text_screen(t, color, x, y):
    text = font.render(t, True, color)
    window.blit(text, [x, y])


def plot_snake(window, color, snake_list, size):
    for x, y in snake_list:
        pygame.draw.rect(window, color, [x, y, size, size])


def welcome():
    pygame.mixer.music.load("bgm.mp3")
    pygame.mixer.music.play()
    exit_game = False
    while not exit_game:
        window.fill(white)
        window.blit(wel,[0,0])
        text_screen("Press enter to play", white, 60, 200)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.load("bgm.mp3")
                    pygame.mixer.music.play(loops=-1)
                    game_Loop()
        pygame.display.update()
        clock.tick(45)


def game_Loop():
    # Game Specific Variables
    exit_game = False
    game_over = False
    x_pos = 45
    y_pos = 55
    size = 15
    fps = 45
    v_x = 0
    v_y = 0
    width = 900
    height = 600
    init_velocity = 5
    food_x = random.randint(20, width // 2)
    food_y = random.randint(20, height // 2)
    score = 0
    snake_list = []
    snake_len = 1
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt","w") as f:
            f.write(str(0))

    with open("highscore.txt", "r") as f:
        high_score = f.read()

    # Game Loop
    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(high_score))
            window.fill(white)
            window.blit(game_o,[0,0])
            text_screen("Score: " + str(score), (233,134,88), 365, 200)
            text_screen("Press Enter to Continue!", red, 250, 350)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        v_x = init_velocity
                        v_y = 0
                    if event.key == pygame.K_LEFT:
                        v_x = -init_velocity
                        v_y = 0
                    if event.key == pygame.K_UP:
                        v_y = -init_velocity
                        v_x = 0
                    if event.key == pygame.K_DOWN:
                        v_y = init_velocity
                        v_x = 0
            x_pos += v_x
            y_pos += v_y
            if abs(x_pos - food_x) < 8 and abs(y_pos - food_y) < 8:
                score += 10
                food_x = random.randint(20, width // 2)
                food_y = random.randint(20, height // 2)
                snake_len += 5
                if int(score) > int(high_score):
                    high_score = str(score)

            window.fill(white)
            window.blit(bgimg, [0, 0])
            text_screen("Score: " + str(score) + "    Hiscore: " + str(high_score), (120,87,241), 5, 5)
            pygame.draw.rect(window, red, [food_x, food_y, size, size])
            head = []
            head.append(x_pos)
            head.append(y_pos)
            snake_list.append(head)

            if len(snake_list) > snake_len:
                del snake_list[0]

            if head in snake_list[:-1]:
                pygame.mixer.music.load("over.wav")
                pygame.mixer.music.play()
                game_over = True

            if x_pos < 0 or x_pos > width or y_pos < 0 or y_pos > height:
                pygame.mixer.music.load("over.wav")
                pygame.mixer.music.play()
                game_over = True
            plot_snake(window, black, snake_list, size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()
