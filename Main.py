from pygame import *
import random

from pygame.examples.music_drop_fade import starting_pos

width , height =  720 , 1080
screen = display.set_mode((width , height))
colourcliff =  (20, 80, 20)

tilewidth , tilelength = 80 , 64


c = time.Clock()
FPS = 60


#make the actual object which handles the plaer as well as trees:
class treeorplayer:
    def __init__(self , x , y , image , base , length ):
        self.x = x
        self.y = y
        image = transform.scale(image, (base, length))
        colourremoval = image.get_at((0, 0))
        image.set_colorkey(colourremoval)

        self.img = Surface((base , length) , SRCALPHA)
        self.img.blit(image , (0,0))
        self.rect = Rect(x , y , base , length )#make a rectangle for the shadow to attach to


    def playerdead(self):
        #need to make it go back to the start
        self.rect.x = self.x
        self.rect.y = self.y


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

        self.playerhitbox = self.rect.inflate(-20, -15)
        draw.rect(screen, (255, 0, 0), self.playerhitbox, 2)
        playerhitbox = self.playerhitbox

        return playerhitbox , self.rect

pic = image.load(r"C:\Users\aliff\Downloads\frog.png")
player = treeorplayer( (width / 2) , height , pic ,  60, 60  )



class log:
    def __init__(self , x , y , image , base, length , opposite ):
        self.opposite = opposite
        image = transform.scale(image, (base, length))
        self.img = Surface((80, 50), SRCALPHA)
        self.img.blit(image, (0, 0))
        self.rect = Rect(x, y, base, length)
        self.speed = 1.5

    def draw(self , screen):
        screen.blit(self.img , self.rect)

    def movement(self):
        #print("so it is being referrred to ")
        if self.opposite:
            #print("so the apramters did pass in")
            self.rect.x -= self.speed
        elif not self.opposite:
            self.rect.x += self.speed

        return self.rect

    def collision(self):
        hitbox  = self.rect.inflate(-20, -30)
        playerhitbox , xpos = player.playermovement()
        if hitbox.colliderect(playerhitbox):
            xpos.x = self.rect.x
            return True



class tile:
    def __init__(self , x , y , image ,extraheight = 0 , flip = False , overlay = False , water = False):
        if water:
            self.water = water
            image = transform.scale(image, (tilewidth, tilelength + extraheight))
            image = transform.flip(image, False, True)
            self.img = Surface((tilewidth, tilelength + extraheight))
            self.img.blit(image, (0, 0))
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

    def watercollision(self , loglist):
        waterhitbox = self.rect.inflate(0, -5)
        playerhitbox, xpos = player.playermovement()
        if loglist != []:
            if waterhitbox.colliderect(playerhitbox):
                onlog = False
                # Loop through the list we just "passed in"
                for log in loglist:
                    if log.collision():
                        onlog = True

                if not onlog:
                    player.playerdead()
        else:
            pass




class car:
    def __init__(self , x,y , image , base , length , opposite):
        self.opposite = opposite
        if not self.opposite:
            image = transform.scale(image, (base, length)).convert()
            image = transform.flip(image, True, False)
            self.img = Surface((80, 50), SRCALPHA)
            self.img.blit(image, (0, 0))
            self.rect = Rect(x, y, base, length)
            self.speed = 1.5
        else:
            image = transform.scale(image, (base, length)).convert()
            self.img = Surface((80, 50), SRCALPHA)
            self.img.blit(image, (0, 0))
            self.rect = Rect(x, y, base, length)
            self.speed = 1.5

    def draw(self , screen):
        screen.blit(self.img , self.rect)

    def movement(self):
        if self.opposite:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

    def collision(self):
        hitbox = self.rect.inflate(-20, -30)
        playerhitbox, xpos = player.playermovement()
        if hitbox.colliderect(playerhitbox):

            print("should return to spawn")
            player.playerdead()


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
            print(xpos , ypos)
            groundlayer.append(tile(xpos, ypos, pic))
        elif col == "W":
            pic = image.load(r"C:\Users\aliff\Downloads\water.png")
            waterlayer.append(tile(xpos, ypos, pic , 0  , False , False , True))

        elif col == "C":
            if index == 10:
                pic = image.load(r"C:\Users\aliff\Downloads\cliff.png")
                groundlayer.append(tile(xpos, ypos, pic, 25 , True))
            else:
                pic = image.load(r"C:\Users\aliff\Downloads\cliff.png")
                groundlayer.append(tile(xpos , ypos , pic , 25))


pic = image.load(r"C:\Users\aliff\Downloads\tree.png")
trees = []
numberoftrees = 15
for i in range(numberoftrees):
    xpos = random.randint(1,720)
    xpos = (xpos // 64) * 64
    ypos = random.randint(1, 1080)
    ypos = (ypos // 64) * 64
    trees.append(treeorplayer(xpos, ypos, pic, 40, 45))

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
                self.logs = [log(x, y1, self.pic, 80, 50 , False),
                        log(x, y2, self.pic, 80, 50 , False )]
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
        self.tableofypos = [64, 128 , 192 , 256]
        self.pic = image.load(r"C:\Users\aliff\Downloads\car.png").convert_alpha()
        for i in range(len(self.tableofxpos)):
            if i == 0:
                x = self.tableofxpos[i]
                y1, y2 = self.tableofypos[0], self.tableofypos[2]
                self.cars = [car(x, y1, self.pic, 80, 50, False),
                             car(x, y2, self.pic, 80, 50, False)]
            if i == 1 :
                x = self.tableofxpos[i]
                y1 , y2 = self.tableofypos[1] , self.tableofypos[3]
                self.cars.append(car(x, y1, self.pic, 80, 50, True))
                self.cars.append(car(x, y2, self.pic, 80, 50, True))

        self.cars = []

    def spawn(self):
        #with this i want to have it so that there is onyl cars going on each lines
        yrandomone = random.choice([64 , 192])
        yrandomtwo = random.choice([128 , 256])
        x = random.choice(self.tableofxpos)

        if x <= 0 :
            self.cars.append(car(x, yrandomone, self.pic, 80, 50, False))
        elif x >= 720:
            self.cars.append(car(x, yrandomtwo, self.pic, 80, 50, True))

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
        self.tableofxpos = [-80, 800]
        self.tableofypos = [768, 832, 896, 960]
        self.pic = image.load(r"C:\Users\aliff\Downloads\car.png").convert_alpha()
        for i in range(len(self.tableofxpos)):
            if i == 0:
                x = self.tableofxpos[i]
                y1, y2 = self.tableofypos[0], self.tableofypos[2]
                self.cars = [car(x, y1, self.pic, 80, 50, False),
                             car(x, y2, self.pic, 80, 50, False)]
            if i == 1:
                x = self.tableofxpos[i]
                y1, y2 = self.tableofypos[1], self.tableofypos[3]
                self.cars.append(car(x, y1, self.pic, 80, 50, True))
                self.cars.append(car(x, y2, self.pic, 80, 50, True))

        self.cars = []

    def spawn(self):
        # with this i want to have it so that there is onyl cars going on each lines
        yrandomone = random.choice([768, 896])
        yrandomtwo = random.choice([832, 960])
        x = random.choice(self.tableofxpos)

        if x <= 0:
            self.cars.append(car(x, yrandomone, self.pic, 80, 50, False))
        elif x >= 720:
            self.cars.append(car(x, yrandomtwo, self.pic, 80, 50, True))

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

starttime = time.get_ticks()
delay = 1000
loglist = []

while not endgame:
    player.playermovement()
    for e in event.get():
        if e.type == QUIT:
            endgame = True

    for tile in waterlayer:
        screen.blit(tile.img , tile.rect)
        tile.watercollision(loglist)


    loglist = logs.drawlogs()

    currenttime = time.get_ticks()
    if currenttime - starttime > delay:
        logs.spawn()
        carsfirstlane.spawn()
        carsecondlane.spawn()
        starttime = currenttime
        currenttime = time.get_ticks()

    for tile in groundlayer:screen.blit(tile.img , tile.rect)

    carsfirstlane.drawcars()
    carsecondlane.drawcars()

    depth_elements = [player] + trees
    # sorts the list out in order of lowest to highest yaxis vals
    depth_elements.sort(key=lambda obj: obj.rect.bottom)

    for obj in depth_elements:
        obj.shadow(screen)
        screen.blit(obj.img ,  obj.rect)


    c.tick(FPS)
    display.update()

#btw u have to keep everythign contains wiithin the class when trying to maniupkate any oroperites of the object
#the only thing u fo outside the code in regards to objects is referring to a function of the class or actually intialisaing it
#as well as this what i figured out is during the spaning of multiple logs i was lookign at it the wrong way
#i looked at it from the persepctive of looking outside the object ans then addiang it in
#the proper way was to actually make a new log object within the group and then add it into the list
#in which all the logs were made intially
#an exmaple of this was that i made a function in the log group which adds a new log into the list to then be drawn in
#this function was only invioled and called upon after the delay in whcih a new log was then added to the list of logs and then with that lsit of logs
#the draw function in the log group class then goes through all of logs list and draws them
#so in escense the group handles and treats all the log objects as one meaning they all do one thing in which the loggroup is only used to to control the singular objects
#the behhaviors of thsoe singular objects ids all determined by the singular object which in thsi case was logs


#i need a way to refer to the characters rectangle as well as the logs rectangle
#with that i need to have ti so that when they two rectabgles touch each other and collide
#the rect of the froggo follows the rect of the log it is currently obn
#i need this to run oin the mainloop onbe way or another


#one way is to create a new part with the collisoon
#and woitht eh collision refer to both thge character and the logs using the objecbts alkready created before hand
