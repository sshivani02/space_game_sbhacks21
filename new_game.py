import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 50)
FPS = 40
BADDIEMINSIZE = 30
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def obstacles():
    num = random.randint(0,1)
    if num == 0:
        return pygame.image.load('asteroid.png')
    elif num == 1:
        return pygame.image.load('meteor.png')

def aliens():
    num = random.randint(0,2)
    if num == 0:
        return pygame.image.load('alien1.png')
    elif num == 1:
        return pygame.image.load('alien2.png')
    elif num == 2:
        return pygame.image.load('alien3.png')


def ifPlayerHitsGood(playerRect, healthy):
    # check if it hit
    for h in healthy:
        if playerRect.colliderect(h['rect']):
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
gameOverSound = pygame.mixer.Sound('gameover.wav')

# set up images
playerImage = pygame.image.load('rocket.png')
playerRect = playerImage.get_rect()

# show the "Start" screen
drawText('Space Rescue!', title_font, windowSurface, (WINDOWWIDTH / 3 - 150), (WINDOWHEIGHT / 3 - 150))
drawText('Your job is to rescue the stranded aliens...', font, windowSurface, (WINDOWWIDTH / 3 - 150), (WINDOWHEIGHT / 3) + 100)
drawText('But avoid the asteroids and fiery meteors!', font, windowSurface, (WINDOWWIDTH / 3 - 150), (WINDOWHEIGHT / 3) + 150)
drawText('Good luck! The galaxy is counting on you!', font, windowSurface, (WINDOWWIDTH / 3 - 150), (WINDOWHEIGHT / 3) + 200)
drawText('Press any key to begin:', font, windowSurface, (WINDOWWIDTH / 3 - 150), (WINDOWHEIGHT / 3) + 250)

pygame.display.update()
waitForPlayerToPressKey()


topScore = 0
while True:
    # set up the start of the game
    baddies = []
    healthy = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    goodAddCounter = 0

    while True: # the game loop runs while the game part is playing

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True # make it go in reverse
                if event.key == ord('x'):
                    slowCheat = True # make everything go slow motion
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where the cursor is.
                playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)

        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(obstacles(), (baddieSize, baddieSize)),
                        }

            baddies.append(newBaddie)
        # good healthy food
        if not reverseCheat and not slowCheat:
            goodAddCounter += 1
        if goodAddCounter == ADDNEWBADDIERATE:
            goodAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newGood = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(aliens(), (baddieSize, baddieSize)),
                        }

            healthy.append(newGood)
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

        # Move the baddies down.
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

         # Delete baddies that have fallen past the bottom.
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # GOODIES

         # Move the goodies down.
        for h in healthy:
            if not reverseCheat and not slowCheat:
                h['rect'].move_ip(0, h['speed'])
            elif reverseCheat:
                h['rect'].move_ip(0, -5)
            elif slowCheat:
                h['rect'].move_ip(0, 1)

         # Delete baddies that have fallen past the bottom.
        for h in healthy[:]:
            if h['rect'].top > WINDOWHEIGHT:
                healthy.remove(h)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Draw the player's rectangle
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])
        
        # draw goodies
        for h in healthy:
            windowSurface.blit(h['surface'], h['rect'])

        pygame.display.update()

        # Check if any of the baddies have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score # set new top score
            break
        if ifPlayerHitsGood(playerRect, healthy):
            score += 10
            for h in healthy[:]:
                healthy.remove(h)

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 2 - 65), (WINDOWHEIGHT / 3 + 50))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 2 - 130), (WINDOWHEIGHT / 3) + 100)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
