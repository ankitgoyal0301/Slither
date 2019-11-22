import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600

# here we pass a tuple of pixels
gameDisplay = pygame.display.set_mode((display_width,display_height))

# Name of the game or caption
pygame.display.set_caption("Slither")
icon = pygame.image.load("C:/Users/Admin/PycharmProjects/Pygame/Apple.png")
pygame.display.set_icon(icon)

# pygame.display.flip()
# This is something which helps in the motion during games
# pygame.display.update()

# Lets fill color RGB format
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (137,194,61)

# Setting Frame rate
clock = pygame.time.Clock()
FPS = 10   # making a frame per second variable

block_size = 20
# Draw apple before snake so that apple does not fall on snake
appleThickness = 30

# Initialising a font object to print text on screen. Here 25 is the font size
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

img = pygame.image.load("C:/Users/Admin/PycharmProjects/Pygame/SnakeFin20.png")
appleImg = pygame.image.load("C:/Users/Admin/PycharmProjects/Pygame/Apple.png")

direction = "right"

def pause():

    paused = True
    # gameDisplay.fill(white)
    message_to_screen("Paused", black, -100, "large")
    message_to_screen("Press C to continue or Q to quit.", black, 25)
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()


def score(score):
    text = smallfont.render("Score: "+str(score),True,black)
    gameDisplay.blit(text, [0,0])

def randAppleGen():
    randAppleX = random.randrange(0, display_width - appleThickness)
    randAppleY = random.randrange(0, display_height - appleThickness)

    return randAppleX,randAppleY

def game_intro():
    intro = True

    while intro==True:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen("Welcome to Slither",(0,155,0),-100,"large")
        message_to_screen("The Objective of this game is to eat apple.", black, -30)
        message_to_screen("The more apples you eat the longer you get.", black, 10)
        message_to_screen("If you run into yourself or edges you die.", black, 50)

        message_to_screen("Press C to continue,P to pause or Q to quit.", black, 180)
        pygame.display.update();
        clock.tick(15)


def snake(block_size, snakeList):

    if direction == "right":
        head = pygame.transform.rotate(img,90)
    if direction == "left":
        head = pygame.transform.rotate(img,270)
    if direction == "top":
        head = pygame.transform.rotate(img,180)
    if direction == "down":
        head = pygame.transform.rotate(img,0)


    # last element of snakelist is the head of the snake
    gameDisplay.blit(head,(snakeList[-1][0],snakeList[-1][1]))

    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])


def text_objects(msg,color,size="small"):

    # the below statement added just to prevent error local variable used before refernce
    textSurface = smallfont.render(msg, True, color)

    if size=="small":
        textSurface = smallfont.render(msg,True,color)
    elif size=="meduim":
        textSurface = medfont.render(msg,True,color)
    elif size=="large":
        textSurface = largefont.render(msg,True,color)
    return textSurface,textSurface.get_rect()

def message_to_screen(msg, color, y_displace,size="small"):

    textSurface, text_rect = text_objects(msg,color,size)
    text_rect.center = (display_width/2),(display_height/2)+y_displace
    gameDisplay.blit(textSurface,text_rect)
    # screen_text = font.render(msg, True, color)
    # gameDisplay.blit(screen_text, [display_width/2 , display_height/2])


def gameLoop():

    # to be able to modify direction
    global direction
    direction="right"

    # Event Handling
    gameExit = False
    gameOver = False

    lead_x = display_width / 2
    lead_y = display_height / 2
    lead_x_change = 10
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    # Generating coordinates of apple randomly
    randAppleX,randAppleY = randAppleGen()

    while not gameExit:

        if gameOver == True:
            # gameDisplay.fill(white)
            message_to_screen("Game Over", red, y_displace=-50, size="large")
            message_to_screen("Press C to play again and Q to quit.", black, y_displace=50, size="medium")
            pygame.display.update()

        while gameOver == True:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameOver = False
                        gameExit = True
                    if event.key == pygame.K_c:
                        gameLoop()
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                    direction = "left"
                if event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                    direction = "right"

                if event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                    direction = "top"
                if event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0
                    direction = "down"

                if event.key == pygame.K_p:
                    pause()
            # ADDING THIS FEATURE WOULD make the movement only until key is pressed. When key is unpressed, it makes the variable 0, hence stops
            """
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    lead_x_change = 0
            """

        # Adding conditions of boundary
        # here using equal to because the rectangles top left corner is considered. We use it so that it is not able to go into the screen partially

        if lead_x>=display_width or lead_x<0 or lead_y>=display_height or lead_y<0:
            gameOver = True

        """
        FEATURE SUCH THAT SCREEN KI EK SIDE SE JAAYE TO DUSRE SE NIKAL AAYE
    
        if lead_x==800:
            lead_x = 0
        elif lead_x<0:
            lead_x=800
        elif lead_y == 600:
            lead_y = 0
        elif lead_y < 0:
            lead_y = 600
        """


        lead_x += lead_x_change
        lead_y += lead_y_change
        gameDisplay.fill(white)


        # pygame.draw.rect(gameDisplay,red,[randAppleX,randAppleY,appleThickness,appleThickness])
        gameDisplay.blit(appleImg,[randAppleX,randAppleY])

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        # When snake goes over itself
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(block_size, snakeList)

        # Scoring

        score(len(snakeList)-1)

        # Better method to print rectangle
        # gameDisplay.fill(red,rect=[200,200,50,50])
        pygame.display.update()

        clock.tick(FPS)

        # Changing location of apple if they snake its that
        if (lead_x >= randAppleX and lead_x < randAppleX + appleThickness) or (lead_x+ block_size> randAppleX and lead_x + block_size<= randAppleX + appleThickness):
            if (lead_y >= randAppleY and lead_y < randAppleY + appleThickness) or (lead_y+ block_size> randAppleY and lead_y + block_size<= randAppleY + appleThickness):
                randAppleX,randAppleY = randAppleGen()
                snakeLength += 1

    pygame.quit()
    quit()

game_intro()
gameLoop()