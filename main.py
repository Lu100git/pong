import pygame, time, random
# WINDOW SIZE AND COLOR FLAGS
WINDOW_WIDHT = 640
WINDOW_HEIGHT = 480
VIOLET = (148, 0, 211)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 127, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

pygame.init()

# prints  available fonts in the console
# print('\n')
# print("Available fonts:")
# print(pygame.font.get_fonts())


class Ball(object):
    speedX = 8
    speedY = 8
    score1 = 0
    score2 = 0

    def __init__(self, color, x, y, w, h):
        self.initialX = x
        self.initialY = y
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.ball = pygame.Surface((self.w, self.h))
        self.ball.fill(color)

    # FUNCTION TO MOVE THE BALL
    def update(self, lowEdge, rightEdge):

        #MOVING THE BALL
        self.x += self.speedX
        self.y += self.speedY

        #preventing from going out of screen up and down
        if self.y >= lowEdge - self.w:
            self.speedY = -abs(self.speedY)
        elif self.y <= 0:
            self.speedY = abs(self.speedY)

        #reset the position of the ball if one player scores
        if self.x > rightEdge + self.w:
            self.x = self.initialX
            self.y = self.initialY
            self.speedX = -abs(self.speedX)
            time.sleep(1)
            self.score1 += 1
        elif self.x < -self.w:
            self.x = self.initialX
            self.y = self.initialY
            self.speedX = abs(self.speedX)
            time.sleep(1)
            self.score2 += 1

    #function used to colide with the paddles
    def colides(self, paddle):
        if self.x + self.w < paddle.x or self.x > paddle.x + paddle.w:
            return False
        elif self.y + self.h < paddle.y or self.y > paddle.y + paddle.h:
            return False
        else:
            return True

    #changes the direction of the ball when they colide with the paddles
    def changeRight(self):
        self.speedX = abs(self.speedX)

    def changeLeft(self):
        self.speedX = -abs(self.speedX)

    #IT DRAWS IT TO THE SCREEN
    def draw(self, window):
        window.blit(self.ball, (self.x, self.y))


class Player(object):
    speed = 6

    def __init__(self, color, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.paddle = pygame.Surface((self.w, self.h)).convert_alpha()
        self.paddle.fill(color)

    def update(self, value, lowEdge):
        #control movement
        if value < 0:
            self.y -= self.speed
        elif value > 0:
            self.y += self.speed

        #preventing out of bounds
        if self.y >= lowEdge - self.h:
            self.y = lowEdge - self.h
        elif self.y <= 0:
            self.y = 0

    def draw(self, window):
        window.blit(self.paddle, (self.x, self.y))


# creating th window
window = pygame.display.set_mode((WINDOW_WIDHT, WINDOW_HEIGHT))

# creating the main player
moveSwitch = 0
player = Player(VIOLET, 0, 300, 25, 100)
player2 = Player(RED, WINDOW_WIDHT - 25, 300, 25, 100)
player2.speed = 8

#creating the ball
ball = Ball(WHITE, (WINDOW_WIDHT / 2) - 20, (WINDOW_HEIGHT / 2) - 20, 20, 20)

# values for computer player
choices = ["y", "n", "y", "n", "y", "y", "y", "n", "y", "y"]
speedControl = 0

executing = True
while executing:
    # displays the score
    p1 = ball.score1
    p2 = ball.score2
    score = pygame.font.SysFont("dejavusans", 50, bold=True)
    score = score.render("P1: " + str(p1) + " - P2: " + str(p2), True,
                         (255, 255, 255))

    for event in pygame.event.get():

        # quiting the game with [X] and escape key
        if event.type == pygame.QUIT:
            executing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                executing = False

            #controls
            if event.key == pygame.K_UP:
                moveSwitch = -10
            if event.key == pygame.K_DOWN:
                moveSwitch = 10
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                moveSwitch = 0
        # for AI
    randomChoice = random.choice(choices)
    if randomChoice == "y":
        if ball.speedY < 0:
            speedControl = -6
        elif ball.speedY > 0:
            speedControl = 6
    else:
        speedControl = 0

    #moving the paddles and the ball
    player.update(moveSwitch, WINDOW_HEIGHT)
    player2.update(speedControl, WINDOW_HEIGHT)
    ball.update(WINDOW_HEIGHT, WINDOW_WIDHT)

    #bounce off paddles
    if ball.colides(player):
        if ball.x > player.x:
            ball.changeRight()
    elif ball.colides(player2):
        if ball.x < player2.x:
            ball.changeLeft()

    #render
    window.fill((0, 0, 0))

    player.draw(window)
    player2.draw(window)
    ball.draw(window)
    window.blit(score, (150, 0))
    pygame.display.update()
    time.sleep(10 / 1000)
