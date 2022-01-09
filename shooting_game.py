"""
Hand Tracing Module
By: Murtaza Hassan
Youtube: http://www.youtube.com/c/MurtazasWorkshopRoboticsandAI
Website: https://www.computervision.zone
"""

import cv2
import mediapipe as mp
import time
import math
import numpy as np
import Hand_predict as Hp


# mediapipe part
def find_dist(a, b, h, w):
    return math.sqrt((a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) / (500)


class handDetector():
    def __init__(self, mode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon,
                                        self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy, lm.z])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        return lmList


RL_JUDGE_DISABLE_DEGREE = (0.45 * math.pi, 0.55 * math.pi)
FB_JUDGE_DISABLE_DEGREE = (-0.10 * math.pi, -0.05 * math.pi)
RL_JUDGE_DISABLE_ZONE = tuple(map(math.cos, RL_JUDGE_DISABLE_DEGREE))
FB_JUDGE_DISABLE_ZONE = tuple(map(math.sin, FB_JUDGE_DISABLE_DEGREE))

# ==========pygame part==========
import pygame
import random
import os
import sys

# ----- Fix Game screen size -----

win_posx = 700
win_posy = 500
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (win_posx, win_posy)

# ----- Global variable -----

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
FPS = 60

score = 0
high_score = 0
playtime = 1

background = pygame.image.load(os.path.join(os.path.abspath('Resources'), 'background.png'))
rocks = [pygame.image.load(os.path.join(os.path.abspath('Resources'), 'rock%02d.png' % (i))) for i in range(1, 31)]

# ----- Colors -----

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN1 = 25, 102, 25
GREEN2 = 51, 204, 51
GREEN3 = 233, 249, 185
BLUE = 17, 17, 212
BLUE2 = 0, 0, 255
YELLOW = 255, 255, 0
LIGHT_PINK1 = 255, 230, 255
LIGHT_PINK2 = 255, 204, 255


def initialize_game(width, height):
    pygame.init()
    surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Shooting game - JaeHyuk")
    return surface


def score_update(surface):
    font = pygame.font.SysFont('malgungothic', 35)
    image = font.render(f'  Score : {score}  HP: {player_health} ', True, WHITE)
    pos = image.get_rect()
    pos.move_ip(20, 20)
    pygame.draw.rect(image, BLACK, (pos.x - 20, pos.y - 20, pos.width, pos.height), 2)
    surface.blit(image, pos)


def gameover(surface):
    font = pygame.font.SysFont('malgungothic', 50)
    image = font.render('GAME OVER', True, BLACK)
    pos = image.get_rect()
    pos.move_ip(50, int(SCREEN_HEIGHT / 2))
    surface.blit(image, pos)
    pygame.display.update()
    time.sleep(2)


def close_game():
    pygame.quit()
    print('Game closed')


def restart():
    print("Restart")
    screen = initialize_game(SCREEN_WIDTH, SCREEN_HEIGHT)
    game_loop(screen)


class PlayerShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        """
        self.image = pygame.Surface((40,30))
        self.image.fill(RED)
        """
        self.image = pygame.image.load(os.path.join(os.path.abspath('Resources'), 'fighter.png'))
        self.rect = self.image.get_rect()
        self.rect.centerx = int(SCREEN_WIDTH / 2)
        self.rect.centery = SCREEN_HEIGHT - 20
        self.friction = 4
        self.speedx = 0
        self.speedy = 0
        self.accx = 0
        self.accy = 0
        self.posx = self.rect.centerx
        self.posy = self.rect.centery

    def update(self, x=0, y=0, dt=1 / 60):

        self.accx = 0
        self.accy = 0

        self.accx += 10000 * x

        self.accy += 10000 * y

        self.accx -= self.friction * self.speedx
        self.accy -= self.friction * self.speedy
        self.speedx += self.accx * dt
        self.speedy += self.accy * dt
        self.limit_vel(1000)

        self.posx += self.speedx * dt
        self.posy += self.speedy * dt

        self.rect.x = self.posx
        self.rect.y = self.posy
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.speedx = 0
            self.accx = 0
        if self.rect.left < 0:
            self.rect.left = 0
            self.speedx = 0
            self.accx = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.speedy = 0
            self.accy = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.speedy = 0
            self.accy = 0

    def limit_vel(self, max_vel):
        self.speedx = max(-max_vel, min(self.speedx, max_vel))
        self.speedy = max(-max_vel, min(self.speedy, max_vel))
        if abs(self.speedx) < 0.01: self.speedx = 0
        if abs(self.speedy) < 0.01: self.speedy = 0

    def shoot(self, all_sprites, bullets):
        bullet = Bullet(self.rect.centerx, self.rect.top, self.speedx, self.speedy)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        """
        self.image = pygame.Surface((30,30))
        self.color = random.choice([BLACK, BLUE, RED, GREEN1, YELLOW])
        self.image.fill(self.color)
        """
        self.image = rocks[random.randint(0, 29)]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.direction_change = False

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.top > SCREEN_HEIGHT + 10 or self.rect.left < -25 or self.rect.right > SCREEN_WIDTH + 20:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y, speed_x, speed_y):
        pygame.sprite.Sprite.__init__(self)
        """
        self.image = pygame.Surface((10,20))
        self.image.fill(GREEN1)
        """
        self.image = pygame.image.load(os.path.join(os.path.abspath('Resources'), 'bullet.png'))
        self.rect = self.image.get_rect()
        self.rect.bottom = player_y
        self.rect.centerx = player_x
        self.speedx = speed_x / 60
        self.speedy = - 10 + speed_y / 60

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom < 0:
            self.kill()


def game_loop(surface):
    running = True
    # mediapipe
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detector = handDetector()
    # 해상도 확인
    success, img = cap.read()
    h, w, c = img.shape
    # pygame
    clock = pygame.time.Clock()
    sprite_group = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = PlayerShip()
    global player_health
    player_health = 100
    global high_score
    score = 0

    sprite_group.add(player)  # not add the player
    for i in range(7):
        enemy = Mob()
        sprite_group.add(enemy)
        mobs.add(enemy)
    shooting = 0  # if %3 == 0 shoot

    while running:
        # pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_SPACE:
                    player.shoot(sprite_group, bullets)
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.shoot(sprite_group, bullets)

        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        if lmList:
            # print(lmList[9])
            # find distance between 5,13
            dist = find_dist(lmList[5], lmList[13], h, w)
            # print normalized z
            value = lmList[9][3] / max(dist, 0.0001) + 0.5
            # print(np.arcsin(min(max(value,-2),2)/2))
            front_back_value = min(max(value, -2), 2) / 2

            '''dist_0_9 = find_dist(lmList[0], lmList[9],h,w)
            if dist_0_9 < 10:
                print("forth")
            else:
                print("back")'''

            ##
            # figure out which direction hand is tilted
            ##
            r = find_dist(lmList[0], lmList[9], h, w)
            x = (lmList[9][1] - lmList[0][1]) / 500
            right_left_value = x / r
            player.update(-right_left_value, front_back_value)
            ans = Hp.define_hand(img, lmList)

        else:
            ans = False
            front_back_value = 0
            right_left_value = 0
            player.update(-right_left_value, front_back_value)

        if ans:
            if shooting % 10 == 0:
                player.shoot(sprite_group, bullets)
            shooting += 1
        else:
            shooting = 0

        sprite_group.update()

        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            mob = Mob()
            sprite_group.add(mobs)
            mobs.add(mob)
            score += 10

        hits = pygame.sprite.spritecollide(player, mobs, False)
        if hits:
            player_health -= 1
            if player_health <= 0:
                if high_score < score:
                    high_score = score
                running = False
                gameover(surface)
                restart()

        surface.fill(LIGHT_PINK1)
        surface.blit(background, (0, 0))
        sprite_group.draw(surface)
        score_update(surface)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    screen = initialize_game(SCREEN_WIDTH, SCREEN_HEIGHT)
    game_loop(screen)
    close_game()
    print('game played: ', playtime)
    print('high score: ', high_score)
    sys.exit()
