import pygame, sys, random

pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)

#Game Settings
birdMovement = 0
flapForce = 12
gravity = 0.25
gameActive = False
score = 0
highscore = 0
canScore = True

def draw_Floor():
    screen.blit(floorSurface,(floorXpos,900))
    screen.blit(floorSurface,(floorXpos+576,900))
def createPipe():
    randomPipePos = random.choice(pipeHeight)
    bottomPipe = pipeSurface.get_rect(midtop = (700,randomPipePos))
    topPipe = pipeSurface.get_rect(midbottom = (700,randomPipePos- 300))
    return bottomPipe, topPipe
def movePipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visibilePipes = [pipe for pipe in pipes if pipe.right >= -50]
    return visibilePipes
def drawPipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipeSurface,pipe)
        else:
            flippedPipe = pygame.transform.flip(pipeSurface, False, True)
            screen.blit(flippedPipe, pipe)
def checkCollisions(pipes):
    global canScore

    for pipe in pipes:
        if birdRect.colliderect(pipe):
            deathSound.play()
            canScore = True
            return False
    if birdRect.top <= -100 or birdRect.bottom >= 900:
        canScore = True
        deathSound.play()
        return False
    return True
def rotateBird(bird):
    newBird = pygame.transform.rotozoom(bird, - birdMovement * 3,1)
    return newBird
def birdAnimation():
    newBird = birdFrames[birdIndex]
    newbirdRect = newBird.get_rect(center = (100,birdRect.centery))
    return newBird, newbirdRect
def scoreDisplay(gameState):
    if gameState == "MainGame":
        scoreSurface = game_font.render(str(int(score)), True,(255,255,255))
        scoreRect = scoreSurface.get_rect(center = (288, 100))
        screen.blit(scoreSurface,scoreRect)
    if gameState == "GameOver":
        scoreSurface = game_font.render(f'Score: {int(score)}', True,(255,255,255))
        scoreRect = scoreSurface.get_rect(center = (288, 100))
        screen.blit(scoreSurface,scoreRect)

        highScoreSurface = game_font.render(f'Highscore: {int(highscore)}', True,(255,255,255))
        highScoreRect = highScoreSurface.get_rect(center = (288, 850))
        screen.blit(highScoreSurface,highScoreRect)        
def updateScore(score, highscore):
    if score > highscore:
        highscore = score
    return highscore
def pipeScoreCheck():
    global score, canScore

    if pipeList:
        for pipe in pipeList:
            if 95 < pipe.centerx < 105 and canScore:
                score += 1
                scoreSound.play()
                canScore = False
            if pipe.centerx < 0:
                canScore = True

#GAMEOVER AND START
gameStartSurface = pygame.transform.scale2x(pygame.image.load("assets/message.png").convert_alpha())
gameStartRect = gameStartSurface.get_rect(center= (288,512))

#BACKGROUND
bgSurface = pygame.transform.scale2x(pygame.image.load('assets/background-day.png').convert()) 

#FLOOR
floorSurface = pygame.image.load('assets/base.png').convert()
floorSurface = pygame.transform.scale2x(floorSurface)
floorXpos = 0

#PIPES
pipeSurface = pygame.transform.scale2x(pygame.image.load('assets/pipe-green.png').convert()) 

pipeList = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipeHeight = [400,500,600,700,800]

#BIRD
birdDownflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
birdMidFlap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
birdUpFlap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())

birdFrames = [birdDownflap, birdMidFlap, birdUpFlap]
birdIndex = 0
birdSurface = birdFrames[birdIndex]
birdRect = birdSurface.get_rect(center= (100,512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

#SOUND
scoresoundCountdown = 100

deathSound = pygame.mixer.Sound("sound/sfx_hit.wav")
scoreSound = pygame.mixer.Sound("sound/sfx_point.wav")
flapSound = pygame.mixer.Sound("sound/sfx_wing.wav")



while True:
    screen.blit(bgSurface,(0,0))  
    floorXpos -= 1
    draw_Floor()
    if floorXpos <= -576:
        floorXpos = 0
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and gameActive or event.key == pygame.K_SPACE and gameActive:
                birdMovement = 0
                birdMovement -= flapForce
                flapSound.play()
            if event.key == pygame.K_UP and gameActive == False or event.key == pygame.K_SPACE and gameActive == False:
                score = 0 
                gameActive = True
                pipeList.clear()
                birdRect.center = (100,512)
                birdMovement = 0
        if event.type == SPAWNPIPE:
            pipeList.extend(createPipe())
        if event.type == BIRDFLAP:
            if birdIndex < 2:
                birdIndex += 1
            else:
                birdIndex = 0
            birdSurface,birdRect = birdAnimation()
    
    if gameActive: 
        birdMovement += gravity
        rotatedBird = rotateBird(birdSurface)
        birdRect.centery += birdMovement
        screen.blit(rotatedBird, birdRect)
        
        pipeList = movePipes(pipeList)
        drawPipes(pipeList)
        gameActive = checkCollisions(pipeList)
 
        scoreDisplay("MainGame")
        pipeScoreCheck()
    else:
        screen.blit(gameStartSurface,gameStartRect)
        highscore = updateScore(score, highscore)
        scoreDisplay("GameOver")
    pygame.display.update()
    clock.tick(120)