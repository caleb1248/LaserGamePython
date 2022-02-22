import pygame, time, os

pygame.init()
win = pygame.display.set_mode((700, 400))
win.fill((225, 225, 225))


class Variables():
    def __init__(self):
        pass

    def values(self):
        self.running = True

    def brake(self):
        self.running = False


def rewrite(original_file, text):
    dummy_file = original_file + '.bak'
    open(original_file, 'r')
    open(dummy_file, 'w')
    os.remove(original_file)
    os.rename(dummy_file, original_file)
    write_obj = open(original_file, 'w')
    write_obj.write(text)


def align_center(surface):
    return 350 - (surface.get_width() / 2)


class Everything():
    def __init__(self):
        self.ground = pygame.image.load("ground.png")
        self.celing = pygame.image.load("celing.png")
        self.waveup = pygame.image.load("wave.png")
        self.waveup = pygame.transform.scale(self.waveup, (30, 30))
        self.wavedown = pygame.image.load("wave1.png")
        self.wavedown = pygame.transform.scale(self.wavedown, (30, 30))
        self.upordown = False

    def movegroundceling(self):
        global spikesx
        spikesx -= 1
        if spikesx == -20:
            spikesx = 0
        win.blit(self.ground, (spikesx, 380))
        win.blit(self.celing, (spikesx, 0))

    def moveplayer(self):
        global player_y
        global actual_running
        for eve in pygame.event.get():
            if eve.type == pygame.QUIT:
                Vars.brake()
                actual_running = False
                break
            elif eve.type == pygame.KEYDOWN or eve.type == pygame.MOUSEBUTTONDOWN:
                self.upordown = True
            elif eve.type == pygame.KEYUP or eve.type == pygame.MOUSEBUTTONUP:
                self.upordown = False
        if self.upordown == True:
            self.image = self.waveup
            player_y -= 1
        elif self.upordown == False:
            self.image = self.wavedown
            player_y += 1
        win.blit(self.image, (200, player_y))
        if player_y <= 20:
            Vars.brake()
        elif player_y + 30 >= 380:
            Vars.brake()


class Enemy():
    def __init__(self):
        #draws the enemy and does other stuff like shoot
        global enemy_y
        self.enemy = pygame.Rect(500, enemy_y, 50, 40)
        self.laser = pygame.Rect(0, enemy_y + 10, 500, 20)
        pygame.draw.rect(win, (225, 0, 0), self.enemy)

    def set_target(self):
        global player_y
        self.target = player_y

    def shoot(self):
        global player_y
        global enemy_y
        pygame.draw.rect(win, (225, 225, 0), self.laser)
        if player_y <= enemy_y + 30 and player_y + 30 >= enemy_y + 10:
            Vars.brake()

    def gototarget(self):
        global enemy_y
        if self.target > enemy_y:
            enemy_y += 1
        elif self.target < enemy_y:
            enemy_y -= 1


font = pygame.font.SysFont('arial', 40)
smallFont = pygame.font.SysFont('arial', 20)
shoots = 0
Vars = Variables()
Vars.values()
actual_running = True
timy = time.time()

while actual_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        elif (event.type == pygame.KEYDOWN) and time.time() - timy >= 1:
            if (event.key == pygame.K_SPACE):
                # starting up the game
                rruning = True
                Vars.values()
                global enemy_y
                global player_y
                global spikesx
                spikesx = 0
                clock = pygame.time.Clock()
                player_y = 185
                enemy_y = 185
                shooting = False
                start = time.time()
                everything = Everything()
                enemy = Enemy()
                enemy.set_target()
                shoots = 0
                while True:
                    win.fill((225, 225, 225))
                    everything.moveplayer()
                    everything.movegroundceling()
                    if time.time() - start >= 1:
                        if not shooting:
                            shooting = True
                            shoots += 1
                        elif shooting:
                            shooting = False
                            enemy.set_target()
                        start = time.time()
                    if shooting == True:
                        enemy.shoot()

                    enemy.__init__()
                    enemy.gototarget()
                    text = font.render(str(shoots), True, (0, 0, 0))
                    win.blit(text, (350 - (text.get_width() / 2), 100))
                    pygame.display.update()

                    if not Vars.running:
                        break
                time.sleep(1)

                if shoots > int(open('High Score.txt').read()):
                    rewrite('High Score.txt', str(shoots))

                timy = time.time()
    win.fill((225, 225, 225))
    # rendering the score
    previous_score = font.render('your score' + ' ' + str(shoots), True,
                                 (0, 0, 0))
    win.blit(previous_score, (align_center(previous_score), 100))
    highscore = open('High Score.txt')

    #rendering the high score
    high_score = font.render('high score' + ' ' + highscore.read(), True,
                             (0, 0, 0))
    win.blit(high_score,
             (align_center(high_score), 100 + high_score.get_height() + 20))
    pressSpace = smallFont.render('press the space bar to play', True,
                                  (0, 0, 0))

    #rendering the press space bar to play
    win.blit(pressSpace, (align_center(pressSpace), 250))
    pygame.display.update()
    highscore.close()
