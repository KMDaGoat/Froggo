from pygame import *
import random

from pygame.examples.music_drop_fade import starting_pos

width , height =  720 , 1080
screen = display.set_mode((width , height))
colourcliff =  (20, 80, 20)

tilewidth , tilelength = 80 , 64
class tile:
    def __init__(self , x , y , image ,extraheight = 0 , flip = False , overlay = False):
        if flip:
            image = transform.scale(image, (tilewidth, tilelength + extraheight))
            image = transform.flip(image , False , True)
            self.img = Surface((tilewidth, tilelength + extraheight))
            self.img.blit(image, (0, 0))
        else :
            self.img = Surface((tilewidth, tilelength + extraheight))
            image = transform.scale(image , (tilewidth, tilelength + extraheight))#this makes the current tile bigger in which the extra spacd would represent a wall or cliff side
            self.img.blit(image , (0,0))
            # Add a small highlight on top of cliffs to show the edge
            if extraheight > 0:
                draw.rect(self.img, (105, 138, 0), (0, 0, tilewidth, 5))
            elif overlay:
                draw.rect(self.img, (105, 138, 0), (0, 0, tilewidth, 5))

        self.rect = self.img.get_rect(topleft=(x, y))
        if y == 448 or y == 512 or y == 576 :
            #print(self.rect.center)
            pass

c = time.Clock()
FPS = 60



#make the actual object which handles the plaer as well as trees:
class treeorplayer:
    def __init__(self , x , y , image , base , length ):
        image = transform.scale(image, (base, length))
        colourremoval = image.get_at((0, 0))
        image.set_colorkey(colourremoval)

        self.img = Surface((base , length) , SRCALPHA)
        self.img.blit(image , (0,0))
        self.rect = Rect(x , y , base , length )#make a rectangle for the shadow to attach to
        self.randomint = random.randint(1, 5)
        self.speed = self.randomint


    def shadow(self , screen):
        shadowappearance = Surface((self.rect.width , 14) ,SRCALPHA)
        draw.ellipse(shadowappearance , (0,0,0,90) , [0,0,self.rect.width , 14 ])
        screen.blit(shadowappearance , (self.rect.x , self.rect.bottom - 7))

    def playermovement(self):

        movement = 64
        lowerlim = -64
        for e in event.get():
            if e.type == KEYDOWN:
                if e.key == K_w:
                    self.rect.y -= movement
                    if self.rect.y < lowerlim:
                        self.rect.y += movement
                if e.key == K_a:
                    self.rect.x -= movement
                    if self.rect.x < lowerlim:
                        self.rect.x += movement
                if e.key == K_s:
                    self.rect.y += movement
                    if self.rect.y > height:
                        self.rect.y -= movement
                if e.key == K_d:
                    self.rect.x += movement
                    if self.rect.x >= width:
                        self.rect.x -= movement


class log:
    def __init__(self , x , y , image , base, length , opposite ):
        self.opposite = opposite
        image = transform.scale(image, (base, length))
        self.img = Surface((80, 50), SRCALPHA)
        self.img.blit(image, (0, 0))
        self.rect = Rect(x, y, base, length)
        randomnum = random.uniform(0.25,2.0)
        self.speed = randomnum

    def draw(self , screen):
        screen.blit(self.img , self.rect)

    def movement(self):
        #print("so it is being referrred to ")
        if self.opposite:
            #print("so the apramters did pass in")
            self.rect.x -= self.speed
        elif not self.opposite:
            self.rect.x += self.speed











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
    ["G"] * colwise,


]

waterlayer =[]
groundlayer = []


for index , item in enumerate(tilemap):
    for multiplier , col in enumerate(item):
        xpos , ypos = multiplier * 64 , index * 64
        if col == "G":
            #refer to the object and put in thr paramters into the object
            pic = image.load(r"C:\Users\aliff\Downloads\grassone.png")
            groundlayer.append(tile(xpos , ypos , pic))
            if index == 11:
                # refer to the object and put in thr paramters into the object
                pic = image.load(r"C:\Users\aliff\Downloads\grassone.png")
                groundlayer.append(tile(xpos, ypos, pic , 0 , False , True))

        if col == "R":
            pic = image.load(r"C:\Users\aliff\OneDrive\Desktop\froggoassets\PNG\Default\roadTexture_13.png")
            groundlayer.append(tile(xpos, ypos, pic))
        elif col == "W":
            pic = image.load(r"C:\Users\aliff\Downloads\water.png")
            waterlayer.append(tile(xpos, ypos, pic))

        elif col == "C":
            if index == 10:
                pic = image.load(r"C:\Users\aliff\Downloads\cliff.png")
                groundlayer.append(tile(xpos, ypos, pic, 25 , True))
            else:
                pic = image.load(r"C:\Users\aliff\Downloads\cliff.png")
                groundlayer.append(tile(xpos , ypos , pic , 25))

pic = image.load(r"C:\Users\aliff\Downloads\frog.png")
player = treeorplayer( (width / 2) , height , pic ,  64, 64  )

pic = image.load(r"C:\Users\aliff\Downloads\tree.png")
trees = []


#with the logs i could make them into a logs group
#and then pass in a paramter in which determines what direction it starst mvoing in

class loggroup:
    def __init__(self):
        #acc adds all the log objects into a single list
        self.tableofxpos = [-80, 800]
        self.tableofypos = [455 , 520 , 585]
        self.pic = image.load(r"C:\Users\aliff\Downloads\log.png")
        for i in range(len(self.tableofxpos)):
            if i == 0:
                x = self.tableofxpos[i]
                y1, y2 = self.tableofypos[0], self.tableofypos[2]
                self.logs = [log(x, y1, self.pic, 70, 40 , False),
                        log(x, y2, self.pic, 70, 40 , False )]
            if i == 1:
                x = self.tableofxpos[i]
                y = self.tableofypos[1]
                self.logs.append(log(x, y, self.pic, 80, 50 , True))

        self.logs =[]

    def spawn(self):
        y = random.choice(self.tableofypos)
        x = random.choice(self.tableofxpos)
        if x == -80:
            self.logs.append(log(x, y, self.pic, 80, 50, False))
        if x == 800:
            self.logs.append(log(x, y, self.pic, 80, 50, True))

    def drawlogs(self):
        for log in self.logs:
            log.movement()
            log.draw(screen)
            log.movement()
            
        self.logs = [l for l in self.logs if -100 < l.rect.x < width + 100]


logs = loggroup()

numberoftrees = 15
for i in range(numberoftrees):
    xpos = random.randint(1,720)
    xpos = (xpos // 64) * 64
    ypos = random.randint(1, 1080)
    ypos = (ypos // 64) * 64
    trees.append(treeorplayer(xpos, ypos, pic, 40, 45))

endgame = False

starttime = time.get_ticks()
delay = 1000
while not endgame:
    player.playermovement()
    for e in event.get():
        if e.type == QUIT:
            endgame = True

    for tile in waterlayer:screen.blit(tile.img , tile.rect)

    logs.drawlogs()

    currenttime = time.get_ticks()
    if currenttime - starttime > delay:
        logs.spawn()
        starttime = currenttime
        currenttime = time.get_ticks()


    for tile in groundlayer:screen.blit(tile.img , tile.rect)

    depth_elements = [player] + trees
        # sorts the list out in order of lowest to highest yaxis vals
    depth_elements.sort(key=lambda obj: obj.rect.bottom)


    for obj in depth_elements:
        obj.shadow(screen)
        screen.blit(obj.img ,  obj.rect)


    c.tick(FPS)
    display.update()
