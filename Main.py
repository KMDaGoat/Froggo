from pygame import *
import random
from pygame.examples.music_drop_fade import starting_pos

font.init()
init()

lives = 3
score = 0
level = 1

width, height = 720, 1080
screen = display.set_mode((width, height))
colourcliff = (20, 80, 20)
tilewidth, tilelength = 80, 64
c = time.Clock()
FPS = 60

colwise = 11
tilemap = [
    ["G"] * colwise,
    ["R"] * colwise,
    ["R"] * colwise,
    ["R"] * colwise,
    ["R"] * colwise,
    ["G"] * colwise,
    ["C"] * colwise,
    ["W"] * colwise,
    ["W"] * colwise,
    ["W"] * colwise,
    ["C"] * colwise,
    ["G"] * colwise,
    ["R"] * colwise,
    ["R"] * colwise,
    ["R"] * colwise,
    ["R"] * colwise,
    ["G"] * colwise]
waterlayer = []
groundlayer = []

class treeorplayer:
    def __init__(self, x, y, image, base, length):
        self.x = x
        self.y = y
        image = transform.scale(image, (base, length))
        colourremoval = image.get_at((0, 0))
        image.set_colorkey(colourremoval)

        self.img = Surface((base, length), SRCALPHA)
        self.img.blit(image, (0, 0))
        self.rect = Rect(x, y, base, length)

    def playerdead(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def shadow(self, screen):
        shadowappearance = Surface((self.rect.width, 14), SRCALPHA)
        draw.ellipse(shadowappearance, (0, 0, 0, 90), [0, 0, self.rect.width, 14])
        screen.blit(shadowappearance, (self.rect.x, self.rect.bottom - 7))

    def playermovement(self):
        global score, level
        levelwon = False
        movement = 64
        lowerlim = -64
        for e in event.get():
            if e.type == KEYDOWN:
                if e.key == K_w:
                    self.rect.y -= movement
                    score += 50
                    if self.rect.y < lowerlim:
                        self.rect.y += movement
                    elif self.rect.y <= 0:
                        levelwon = True
                if e.key == K_a:
                    self.rect.x -= movement
                    if self.rect.x < lowerlim:
                        self.rect.x += movement
                if e.key == K_s:
                    self.rect.y += movement
                    score += 50
                    if self.rect.y > height:
                        self.rect.y -= movement
                if e.key == K_d:
                    self.rect.x += movement
                    if self.rect.x >= width:
                        self.rect.x -= movement

        self.playerhitbox = self.rect.inflate(-20, -15)
        draw.rect(screen, (255, 0, 0), self.playerhitbox, 2)
        playerhitbox = self.playerhitbox

        return playerhitbox, self.rect, levelwon

pic = image.load(r"C:\Users\aliff\Downloads\frog.png")
player = treeorplayer((width / 2), height, pic, 60, 60)

class log:
    def __init__(self, x, y, image, base, length, opposite):
        self.opposite = opposite
        image = transform.scale(image, (base, length))
        self.img = Surface((80, 50), SRCALPHA)
        self.img.blit(image, (0, 0))
        self.rect = Rect(x, y, base, length)
        self.speed = 1.5

    def draw(self, screen):
        screen.blit(self.img, self.rect)

    def movement(self):
        if self.opposite:
            self.rect.x -= self.speed
        elif not self.opposite:
            self.rect.x += self.speed

        return self.rect

    def collision(self):
        hitbox = self.rect.inflate(-20, -30)
        playerhitbox, xpos, levelwon = player.playermovement()
        if hitbox.colliderect(playerhitbox):
            xpos.x = self.rect.x
            return True

class tile:
    def __init__(self, x, y, image, extraheight=0, flip=False, overlay=False, water=False):
        if water:
            self.water = water
            image = transform.scale(image, (tilewidth, tilelength + extraheight))
            image = transform.flip(image, False, True)
            self.img = Surface((tilewidth, tilelength + extraheight))
            self.img.blit(image, (0, 0))
        if flip:
            image = transform.scale(image, (tilewidth, tilelength + extraheight))
            image = transform.flip(image, False, True)
            self.img = Surface((tilewidth, tilelength + extraheight))
            self.img.blit(image, (0, 0))
        else:
            self.img = Surface((tilewidth, tilelength + extraheight))
            image = transform.scale(image, (tilewidth, tilelength + extraheight))
            self.img.blit(image, (0, 0))
            if extraheight > 0:
                draw.rect(self.img, (105, 138, 0), (0, 0, tilewidth, 5))
            elif overlay:
                draw.rect(self.img, (105, 138, 0), (0, 0, tilewidth, 5))

        self.rect = self.img.get_rect(topleft=(x, y))

    def watercollision(self, loglist):
        waterhitbox = self.rect.inflate(0, -5)

        playerhitbox, xpos, levelwon = player.playermovement()
        if loglist != []:
            if waterhitbox.colliderect(playerhitbox):
                onlog = False
                for log in loglist:
                    if log.collision():
                        onlog = True

                if not onlog:
                    global lives, score
                    if lives > 0:
                        lives -= 1
                        score -= 200
                        player.playerdead()
        else:
            pass

class car:
    def __init__(self, x, y, image, base, length, opposite, level):
        self.level = level

        self.opposite = opposite
        if not self.opposite:
            image = transform.scale(image, (base, length)).convert()
            image = transform.flip(image, True, False)
            self.img = Surface((80, 50), SRCALPHA)
            self.img.blit(image, (0, 0))
            self.rect = Rect(x, y, base, length)
            self.speed = 1.5 * level
        else:
            image = transform.scale(image, (base, length)).convert()
            self.img = Surface((80, 50), SRCALPHA)
            self.img.blit(image, (0, 0))
            self.rect = Rect(x, y, base, length)
            self.speed = 1.5 * level

    def draw(self, screen):
        screen.blit(self.img, self.rect)

    def movement(self):
        if self.opposite:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

    def collision(self):
        hitbox = self.rect.inflate(-20, -30)
        playerhitbox, xpos, levelwon = player.playermovement()
        if hitbox.colliderect(playerhitbox):
            global lives, score
            if lives > 0:
                lives -= 1
                score -= 200
                player.playerdead()

for index, item in enumerate(tilemap):
    for multiplier, col in enumerate(item):
        xpos, ypos = multiplier * 64, index * 64
        if col == "G":
            pic = image.load(r"C:\Users\aliff\Downloads\grassone.png")
            groundlayer.append(tile(xpos, ypos, pic))
            if index == 11:
                pic = image.load(r"C:\Users\aliff\Downloads\grassone.png")
                groundlayer.append(tile(xpos, ypos, pic, 0, False, True))

        if col == "R":
            pic = image.load(r"C:\Users\aliff\OneDrive\Desktop\froggoassets\PNG\Default\roadTexture_13.png")
            groundlayer.append(tile(xpos, ypos, pic))
        elif col == "W":
            pic = image.load(r"C:\Users\aliff\Downloads\water.png")
            waterlayer.append(tile(xpos, ypos, pic, 0, False, False, True))

        elif col == "C":
            if index == 10:
                pic = image.load(r"C:\Users\aliff\Downloads\cliff.png")
                groundlayer.append(tile(xpos, ypos, pic, 25, True))
            else:
                pic = image.load(r"C:\Users\aliff\Downloads\cliff.png")
                groundlayer.append(tile(xpos, ypos, pic, 25))

pic = image.load(r"C:\Users\aliff\Downloads\tree.png")
trees = []
numberoftrees = 15
for i in range(numberoftrees):
    xpos = random.randint(1, 720)
    xpos = (xpos // 64) * 64
    ypos = random.randint(1, 1080)
    ypos = (ypos // 64) * 64
    trees.append(treeorplayer(xpos, ypos, pic, 40, 45))

class loggroup:
    def __init__(self):
        self.tableofxpos = [-80, 800]
        self.tableofypos = [455, 520, 585]
        self.pic = image.load(r"C:\Users\aliff\Downloads\log.png")
        for i in range(len(self.tableofxpos)):
            if i == 0:
                x = self.tableofxpos[i]
                y1, y2 = self.tableofypos[0], self.tableofypos[2]
                self.logs = [log(x, y1, self.pic, 80, 50, False),
                             log(x, y2, self.pic, 80, 50, False)]
            if i == 1:
                x = self.tableofxpos[i]
                y = self.tableofypos[1]
                self.logs.append(log(x, y, self.pic, 80, 50, True))

        self.logs = []

    def spawn(self):
        y = random.choice(self.tableofypos)
        x = random.choice(self.tableofxpos)
        if x == -80:
            self.logs.append(log(x, y, self.pic, 80, 50, False))
        if x == 800:
            self.logs.append(log(x, y, self.pic, 80, 50, True))

        return self.logs

    def drawlogs(self):
        for log in self.logs:
            log.collision()
            log.movement()
            log.draw(screen)
            log.movement()
            log.collision()

        self.logs = [l for l in self.logs if -100 < l.rect.x < width + 100]

        return self.logs

class groupcarsfirstlane:
    def __init__(self):
        self.tableofxpos = [-80, 800]
        self.tableofypos = [64, 128, 192, 256]
        self.pic = image.load(r"C:\Users\aliff\Downloads\car.png").convert_alpha()
        for i in range(len(self.tableofxpos)):
            if i == 0:
                x = self.tableofxpos[i]
                y1, y2 = self.tableofypos[0], self.tableofypos[2]
                self.cars = [car(x, y1, self.pic, 80, 50, False, level),
                             car(x, y2, self.pic, 80, 50, False, level)]
            if i == 1:
                x = self.tableofxpos[i]
                y1, y2 = self.tableofypos[1], self.tableofypos[3]
                self.cars.append(car(x, y1, self.pic, 80, 50, True, level))
                self.cars.append(car(x, y2, self.pic, 80, 50, True, level))

        self.cars = []

    def spawn(self):
        yrandomone = random.choice([64, 192])
        yrandomtwo = random.choice([128, 256])
        x = random.choice(self.tableofxpos)

        if x <= 0:
            self.cars.append(car(x, yrandomone, self.pic, 80, 50, False, level))
        elif x >= 720:
            self.cars.append(car(x, yrandomtwo, self.pic, 80, 50, True, level))

    def drawcars(self):
        for car in self.cars:
            car.collision()
            car.movement()
            car.draw(screen)
            car.movement()
            car.collision()

        self.cars = [c for c in self.cars if -100 < c.rect.x < width + 100]

class groupcarsecondlane:
    def __init__(self):
        global level
        self.tableofxpos = [-80, 800]
        self.tableofypos = [768, 832, 896, 960]
        self.pic = image.load(r"C:\Users\aliff\Downloads\car.png").convert_alpha()
        for i in range(len(self.tableofxpos)):
            if i == 0:
                x = self.tableofxpos[i]
                y1, y2 = self.tableofypos[0], self.tableofypos[2]
                self.cars = [car(x, y1, self.pic, 80, 50, False, level),
                             car(x, y2, self.pic, 80, 50, False, level)]
            if i == 1:
                x = self.tableofxpos[i]
                y1, y2 = self.tableofypos[1], self.tableofypos[3]
                self.cars.append(car(x, y1, self.pic, 80, 50, True, level))
                self.cars.append(car(x, y2, self.pic, 80, 50, True, level))

        self.cars = []

    def spawn(self):
        yrandomone = random.choice([768, 896])
        yrandomtwo = random.choice([832, 960])
        x = random.choice(self.tableofxpos)

        if x <= 0:
            self.cars.append(car(x, yrandomone, self.pic, 80, 50, False, level))
        elif x >= 720:
            self.cars.append(car(x, yrandomtwo, self.pic, 80, 50, True, level))

    def drawcars(self):
        for car in self.cars:
            car.collision()
            car.movement()
            car.draw(screen)
            car.movement()
            car.collision()

        self.cars = [c for c in self.cars if -100 < c.rect.x < width + 100]

logs = loggroup()
logs.drawlogs()
carsfirstlane = groupcarsfirstlane()
carsecondlane = groupcarsecondlane()

endgame = False
global start
start = False
starttime = time.get_ticks()
delay = 1000
loglist = []

def startingscreen(screen):
    gamestart = False
    global lives
    global score
    surface = screen.convert()
    width, height = surface.get_size()
    while not gamestart:
        for e in event.get():
            xpos, ypos = mouse.get_pos()
            if e.type == MOUSEBUTTONDOWN:
                if xpos >= 210 and xpos <= 510 and ypos >= 540 and ypos <= 640:
                    gamestart = True

        backgroundimg = image.load(r"C:\Users\aliff\Downloads\background.png")
        backgroundimg = transform.scale(backgroundimg, (720, 1080))
        backgroundrect = Rect(0, 0, width, height)
        screen.blit(backgroundimg, backgroundrect)

        titlepic = image.load(r"C:\Users\aliff\Downloads\titlepic.png").convert()
        bgcolor = titlepic.get_at((0, 0))
        titlepic.set_colorkey(bgcolor)
        titlepic = transform.scale(titlepic, (100 * 3, 100 * 3))
        xpostitle = (width / 2) - 150
        ypostitle = (height / 2) - 450
        imagerect = Rect(xpostitle, ypostitle, 300, 300)

        screen.blit(titlepic, imagerect)

        playimg = image.load(r"C:\Users\aliff\Downloads\play.png").convert()
        bgcolor = playimg.get_at((0, 0))
        playimg.set_colorkey(bgcolor)
        playimg = transform.scale(playimg, (300, 100))
        playrect = Rect(xpostitle, (ypostitle + 450), 300, 100)
        screen.blit(playimg, playrect)
        display.update()

    return gamestart

def scoredisplay(screen):
    fontscore = font.Font(r"C:\Users\aliff\PycharmProjects\tictactoe\Recources\SamuraiBlast-YznGj.ttf", 30)
    textsurface = fontscore.render(f"score :{score}", True, (255, 255, 255))
    livessurface = fontscore.render(f"lives :{lives}", True, (255, 255, 255))
    levelsurface = fontscore.render(f"level :{level}", True, (255, 255, 255))
    screen.blit(textsurface, (20, 20))
    screen.blit(livessurface, (580, 20))
    screen.blit(levelsurface, (290, 20))

while not start:
    mixer.music.load(r"C:\Users\aliff\PycharmProjects\tictactoe/Recources\Color Your Night.mp3")
    mixer.music.set_volume(0.02)
    mixer.music.play(-1)
    start = startingscreen(screen)
else:
    while not endgame and start:
        playerhitbox, rect, levelwon = player.playermovement()
        if levelwon:
            level += 1
            player.playerdead()
            score = 0

        for e in event.get():
            if e.type == QUIT:
                endgame = True

        for tile in waterlayer:
            screen.blit(tile.img, tile.rect)
            tile.watercollision(loglist)

        loglist = logs.drawlogs()

        currenttime = time.get_ticks()
        if currenttime - starttime > delay:
            logs.spawn()
            carsfirstlane.spawn()
            carsecondlane.spawn()
            starttime = currenttime
            currenttime = time.get_ticks()

        for tile in groundlayer: screen.blit(tile.img, tile.rect)

        carsfirstlane.drawcars()
        carsecondlane.drawcars()

        depth_elements = [player] + trees
        depth_elements.sort(key=lambda obj: obj.rect.bottom)

        for obj in depth_elements:
            obj.shadow(screen)
            screen.blit(obj.img, obj.rect)

        if lives == 0:
            start = startingscreen(screen)
            lives = 3
            level = 0
            score = 0

        scoredisplay(screen)

        c.tick(FPS)
        display.update()
