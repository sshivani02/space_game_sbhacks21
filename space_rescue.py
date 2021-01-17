import pygame, random, sys
from pygame.locals import *

# graphics/background
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 50)
FPS = 40
MINSIZE = 30
MAXSIZE = 40
MINSPEED = 1
MAXSPEED = 8
ADDNEWRATE = 6
PLAYERMOVERATE = 5

def terminate(): # for ending/exiting the game
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey(): # press key to begin game
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate() # end
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return

def playerHasHitObstacle(playerRect, obstacles): # if it collides with an obstacle return true
    for o in obstacles:
        if playerRect.colliderect(o['rect']):
            return True
    return False

def drawText(text, font, surface, x, y): # text/graphic stuff
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def obstacle_choose(): # randomly generate obstacle type: either asteroid or meteor
    num = random.randint(0,1)
    if num == 0:
        return pygame.image.load('asteroid.png')
    elif num == 1:
        return pygame.image.load('meteor.png')

def alien_choose(): # randomly generate aliens: 3 alien type
    num = random.randint(0,2)
    if num == 0:
        return pygame.image.load('alien1.png')
    elif num == 1:
        return pygame.image.load('alien2.png')
    elif num == 2:
        return pygame.image.load('alien3.png')


def ifPlayerHitsAlien(playerRect, aliens): # if player encounters alien
    for a in aliens:
        if playerRect.colliderect(a['rect']):
            return True
    return False


# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Space Rescue')
pygame.mouse.set_visible(False)

# set up fonts
font = pygame.font.SysFont('cambria', 23)
title_font = pygame.font.SysFont('impact', 50)

# set up sounds
gameOverSound = pygame.mixer.Sound('gameover.wav') # sets the sound effect for game ending

# set up images
playerImage = pygame.image.load('rocket.png')
playerRect = playerImage.get_rect()

# show the "Start" screen
drawText('Space Rescue!', title_font, windowSurface, (WINDOWWIDTH / 3 - 150), (WINDOWHEIGHT / 3 - 150))
drawText('Your job is to rescue the stranded aliens...', font, windowSurface, (WINDOWWIDTH / 3 - 150), (WINDOWHEIGHT / 3))
drawText('But avoid the asteroids and fiery meteors!', font, windowSurface, (WINDOWWIDTH / 3 - 150), (WINDOWHEIGHT / 3) + 50)
drawText('Use the arrow keys to navigate.', font, windowSurface, (WINDOWWIDTH / 3 - 150), (WINDOWHEIGHT / 3) + 100)
drawText('Good luck! The galaxy is counting on you!', font, windowSurface, (WINDOWWIDTH / 3 - 150), (WINDOWHEIGHT / 3) + 150)
drawText('Press any key to begin:', font, windowSurface, (WINDOWWIDTH / 3 - 150), (WINDOWHEIGHT / 3) + 200)


pygame.display.update()
waitForPlayerToPressKey()


topScore = 0 # initialize top score to 0
while True:
    # set up the start of the game
    obstacles = []
    aliens = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    obstacleAddCounter = 0
    alienAddCounter = 0

    while True: # the game loop runs while the game part is playing

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN: # Key commands
                if event.key == ord('z'):
                    reverseCheat = True # make it go in reverse
                if event.key == ord('x'):
                    slowCheat = True # make everything go slow motion
                if event.key == K_LEFT: # left arrow
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT: # right arrow
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP: # up arrow
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN: # down arrow
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP: # if key is not being pressed anymore
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_LEFT:
                    moveLeft = False
                if event.key == K_RIGHT:
                    moveRight = False
                if event.key == K_UP:
                    moveUp = False
                if event.key == K_DOWN:
                    moveDown = False

        # Add new obstacles at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            obstacleAddCounter += 1
        if obstacleAddCounter == ADDNEWRATE:
            obstacleAddCounter = 0
            obstacleSize = random.randint(MINSIZE, MAXSIZE)
            newobstacle = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-obstacleSize), 0 - obstacleSize, obstacleSize, obstacleSize),
                        'speed': random.randint(MINSPEED, MAXSPEED),
                        'surface':pygame.transform.scale(obstacle_choose(), (obstacleSize, obstacleSize)),
                        }

            obstacles.append(newobstacle)
        # Add new aliens to the top of the screen
        if not reverseCheat and not slowCheat:
            alienAddCounter += 1
        if alienAddCounter == ADDNEWRATE:
            alienAddCounter = 0
            alienSize = random.randint(MINSIZE, MAXSIZE)
            newAlien = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-alienSize), 0 - alienSize, alienSize, alienSize),
                        'speed': random.randint(MINSPEED, MAXSPEED),
                        'surface':pygame.transform.scale(alien_choose(), (alienSize, alienSize)),
                        }

            aliens.append(newAlien)
        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the mouse cursor to match the player.
        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        # Move the obstacles down.
        for o in obstacles:
            if not reverseCheat and not slowCheat:
                o['rect'].move_ip(0, o['speed'])
            elif reverseCheat:
                o['rect'].move_ip(0, -5)
            elif slowCheat:
                o['rect'].move_ip(0, 1)

         # Delete obstacles that have fallen past the bottom.
        for o in obstacles[:]:
            if o['rect'].top > WINDOWHEIGHT:
                obstacles.remove(o)

         # Move the aliens down.
        for a in aliens:
            if not reverseCheat and not slowCheat:
                a['rect'].move_ip(0, a['speed'])
            elif reverseCheat:
                a['rect'].move_ip(0, -5)
            elif slowCheat:
                a['rect'].move_ip(0, 1)

         # Delete aliens that have fallen past the bottom.
        for a in aliens[:]:
            if a['rect'].top > WINDOWHEIGHT:
                aliens.remove(a)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Draw the player's rectangle
        windowSurface.blit(playerImage, playerRect)

        # Draw each obstacle
        for o in obstacles:
            windowSurface.blit(o['surface'], o['rect'])
        
        # draw aliens
        for a in aliens:
            windowSurface.blit(a['surface'], a['rect'])

        pygame.display.update()

        # Check if any of the obstacles have hit the player.
        if playerHasHitObstacle(playerRect, obstacles):
            if score > topScore:
                topScore = score # set new top score
            break # immediately end game

        # Check if player has encountered any aliens.
        if ifPlayerHitsAlien(playerRect, aliens):
            score += 10
            for a in aliens[:]:
                aliens.remove(a) # remove all aliens for a moment

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    gameOverSound.play() # play end of game music

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 2 - 65), (WINDOWHEIGHT / 3 + 50))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 2 - 130), (WINDOWHEIGHT / 3) + 100)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
