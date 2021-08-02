import pygame
import random
import os

pygame.mixer.init()

pygame.init()


# Colors
White =(255, 255 ,255)
red = (255, 0, 0)
black = (0, 0, 0)


screen_width = 900
screen_height = 600
# creating window
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Backgroung image
bgimg = pygame.image.load("background/bg.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()


pygame.display.set_caption("Snake Game")
pygame.display.update()


clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
     pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(White)
        
        text_screen("Welcome to Snakes", black, 270, 180)
        text_screen("Press spacebar to play", black, 250, 220)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('Music/Music_bgm.mp3')
                    pygame.mixer.music.play()
                    gameloop()
            

        pygame.display.update()
        clock.tick(60)


# creating a game loop
def gameloop():

    
# game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 4
    velocity_y = 0
    food_x = random.randint(40, screen_width-80)
    food_y = random.randint(80, screen_height-80)
    score = 0
    init_velocity = 4
    snake_size = 10
    fps = 60
    snk_list = []
    snk_length = 1

    #check if high score file exists
    if(not os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))

            gameWindow.fill(White)
            text_screen("Game Over! Press Enter To Continue", red, screen_width/6, screen_height/2.5)
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

                if event.type ==pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_x = 0
                        velocity_y = -init_velocity

                    if event.key == pygame.K_DOWN:
                        velocity_x = 0
                        velocity_y = init_velocity

                    # Cheat
                    if event.key == pygame.K_q:
                        score +=10
                    
                


            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<6 and abs(snake_y - food_y)<6:
                score +=10
                
                food_x = random.randint(20, screen_width)
                food_y = random.randint(20, screen_height)
                snk_length +=5
                if score > int(hiscore):
                    hiscore = score

            gameWindow.fill(White)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score: "+ str(score) + " Hiscore: "+str(hiscore), red, 5, 5)
            # pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('Music/Music_bgm1.mp3')
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('Music/Music_bgm1.mp3')
                pygame.mixer.music.play()

            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()