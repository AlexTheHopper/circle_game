import numpy as np
import random
import p5
import math
from p5 import *
from snakes import *
import os
width = 1250
height = 1250
scale = height / 500
buffer = 20
speed = 3
Size = 10 * scale
score = 0
difficulty = 1
maxHealth = 100
maxShields = 1
maxTeleports = 1
endGame = False
readyToReset = False
scoreSent = False
preGame = True
showStats = False
badGuyCooldown = 200
badGuySpeed = 1
delay = 5
score_list = []
name = ''

#Initialising Scoreboard
dir_path = os.path.dirname(os.path.realpath(__file__))


os.chdir(dir_path)
scoreboard = open('leaderboard.txt', 'r')
data = scoreboard.read()
data_list = data.split('\n')
scoreboard.close()

for i in range(int((len(data_list)-1)/2)):
    score_list.append((int(data_list[i*2+1]),data_list[i*2]))

score_list.sort(key=lambda y: y[0])
score_list.reverse()



def preload():
    pass

def setup():
    size(width, height)



def createFood(x,y):
    apple = Food(x,y)
def createEnemyKiller(x,y):
    killer = EnemyKiller(x,y)
def createShield(x,y):
    Shield = GetShield(x,y)

def createProjectile(start,destination,player):
    global scale
    trajectory = destination - start
    projectiles.append(Projectile(start.x,start.y, trajectory.x, trajectory.y, 2, 10,scale))

def check_near(dist,enemies, statistics):
    global score, maxShields, maxTeleports, scale

    if p5.dist(animal.position,apple.position) < dist:
        score += 1
        apple.move(buffer)
        updateDifficulty()
        if animal.health < 100:
            animal.health += apple.healAmmount
            statistics.healthRegained += apple.healAmmount

    if p5.dist(animal.position,killer.position) < dist:
        killer.move(buffer)
        for badguys in enemies:
            if random.randint(0,3) == 0:
                enemies.remove(badguys)
                statistics.enemiesKilled += 1

    if p5.dist(animal.position,Shield.position) < dist:
        Shield.move(buffer)

        if animal.shield < maxShields:
            animal.shield += 1

    if p5.dist(animal.position,wallTeleport.position) < dist:
        wallTeleport.move(buffer)

        if animal.teleportCount < maxTeleports:
            animal.teleportCount += 1
            animal.teleport = 101


    for badguy in enemies:
        if np.linalg.norm(animal.position - badguy.position) < badguy.range*scale and badguy.rangecooldown == badguy.rangecooldownMax:
            badguy.rangecooldown -= 1
            createProjectile(badguy.position,animal.position+animal.velocity*20,animal)
        if np.linalg.norm(animal.position - badguy.position) < 10 and badguy.meleecooldown == badguy.meleecooldownMax:
            if animal.shield == 0:
                damageAnimal(50,animal,statistics)

            animal.shield = max(animal.shield - 1, 0)
            badguy.meleecooldown -= 1


    for bullet in projectiles:
        if np.linalg.norm(animal.position - bullet.position) < 10:
            projectiles.remove(bullet)
            if animal.shield == 0:
                damageAnimal(bullet.damage, animal, statistics)

            animal.shield = max(animal.shield - 1, 0)

def updateDifficulty():
    global difficulty, badGuyCooldown, badGuySpeed, maxShields, maxTeleports
    difficulty = int(np.ceil(score / 5))
    maxShields = difficulty
    maxTeleports = difficulty

    if difficulty > 0:
        badGuySpeed = (math.log(difficulty) / 2) + 2
        badGuyCooldown = (200 - 75*math.log(difficulty))




def damageAnimal(damage,animal,statistics):
    animal.health -= damage
    statistics.damageTaken += damage

def createEnemy(animal):
    global badGuyCooldown, buffer, scale
    x = random.randrange(buffer,width-buffer)
    y = random.randrange(buffer,height-buffer)
    enemies.append(Enemy(x,y,max(100,255-difficulty*25),'tri',10,(width + height)/4,250*scale,60,badGuyCooldown,badGuySpeed,scale))
def draw():
    global name, readyToReset, scoreSent, preGame, showStats, Size, difficulty, maxShields, maxTeleports

    if preGame == True:
        background(100,200,100)
        stroke(255)

        p5.fill(130,0,130)
        p5.text_align(align_x = "CENTER", align_y = "TOP")
        # p5.text_font(scale)
        p5.text("Welcome to Game!",width / 2, 20*scale)
        p5.text("Press ENTER to begin!",width / 2, 420*scale)

        p5.fill(0,0,0)
        p5.text("This is you!",width / 2, 100*scale)
        p5.text("These are the bad guys, watch out for them!",width / 2, 150*scale)
        p5.text("They will get more aggressive and red the further you get!",width / 2, 170*scale)
        p5.text("This is an apple! These get you points and a bit of health if you're injured!",width / 2, 200*scale)
        p5.text("This will get you a shield, which will block one attack!",width / 2, 250*scale)
        p5.text("This is an exterminator! It gives each enemy a 25% chance to die!",width / 2, 300*scale)
        p5.text("This will allow you to move from one side of the field to the other!",width / 2, 350*scale)
        p5.text("But only once! This can be seen by the field's border!",width / 2, 370*scale)

        #Player
        p5.fill(0,0,0)
        p5.circle(width / 2, 90*scale, Size)
        #Enemy
        p5.fill(200,0,0)
        p5.circle(width / 2, 140*scale, Size)
        #Apple
        p5.fill(255,140,165)
        p5.circle(width / 2, 190*scale, Size)
        #Shield
        p5.no_fill()
        p5.circle(width / 2, 240*scale, Size)
        #Exterminator
        p5.fill(50,50,250)
        p5.circle(width / 2, 290*scale, Size)
        #Teleport
        p5.fill(255,255,0)
        p5.circle(width / 2, 340*scale, Size)


        if key_is_pressed:
            if key == "ENTER":
                preGame = False



    if animal.alive == True and preGame == False:
        background(100,200,100)
        animal.show()
        apple.show()
        killer.show()
        Shield.show()
        wallTeleport.show()
        for badguy in enemies:
            badguy.show(difficulty)
            badguy.update(animal,enemies)
        for bullet in projectiles:
            bullet.show()
            bullet.update(animal)
            if bullet.position.x > width or bullet.position.x < 0 or bullet.position.y > height or bullet.position.y < 0:
                projectiles.remove(bullet)

        animal.update()
        statistics.distanceTravelled += (np.abs(animal.velocity.x) + np.abs(animal.velocity.y))

        check_near(10*scale,enemies, statistics)
        if frame_count % 150 == 0 and len(enemies) < min(8,difficulty):
            createEnemy(animal)

        if animal.teleport <= 0:
            stroke(0,0,0)
            p5.no_fill()
            p5.rect(2,2,width-4,height-4)

        if animal.teleport <= 100 and animal.teleport > 0 and animal.teleportCount <= 0:
            if frame_count % 10 < 5:
                stroke(0)
                p5.no_fill()
                p5.rect(2,2,width-4,height-4)

        p5.fill(0,0,0)
        p5.text_align(align_x = "LEFT", align_y = "TOP")
        p5.text("Score:" + str(score),5, 5*scale)
        p5.text("Teleport Count:" + str(animal.teleportCount) + "/" + str(maxTeleports),5, 15*scale)
        p5.text("Shield Count:" + str(animal.shield) + "/" + str(maxShields),5, 25*scale)
        p5.text_align(align_x = "RIGHT", align_y = "TOP")
        p5.text("Difficulty:" + str(difficulty),width-5, 5*scale)

    if animal.alive == False and preGame == False and showStats == False:
        background(100,200,100)

        p5.fill(150,0,0)
        p5.text_align(align_x = "CENTER", align_y = "TOP")
        p5.text("YOU ARE DEAD",width / 2, 50*scale)
        p5.text("Your score was:{}".format(score), width/2, 70*scale)

        p5.fill(0,0,0)
        for i in range(min(len(score_list),10)):
            p5.text(str(str(score_list[i][0]) + ' -- ' + score_list[i][1]),width/2, height/2 + 25 + 20*i)

        p5.text("Enter Username then press ENTER:", width / 2, 100*scale)
        p5.text(name, width/2, 150)

        p5.fill(150,0,0)
        p5.text('Scoreboard:',width/2, height/2)

        if scoreSent == True:
            p5.fill(0,0,200)
            p5.text('Press r to try again!',width/2, (height/2 - 20)*scale)
            p5.text('Press s to show stats!',width/2, (height/2 - 30)*scale)

        if key_is_pressed:
            if key == "BACKSPACE":
                name = name[:-1]
            elif key == "ENTER":
                if scoreSent == False:
                    sendScore(name,score,score_list)
                    readyToReset = True
                    scoreSent = True
                    score_list.append((score,name))
                    score_list.sort(key=lambda y: y[0])
                    score_list.reverse()

            elif readyToReset == True:
                if key == "r":
                    restart()
                if key == 's':
                    showStats = True

            else:
                name += str(key)

    if animal.alive == False and preGame == False and showStats == True:
        background(100,200,100)
        p5.fill(0,0,200)
        p5.text("Press ENTER to return to leaderboard!",width/2, 10*scale)
        p5.fill(0,0,0)
        p5.text_align(align_x = "CENTER", align_y = "TOP")
        p5.text("Stats:",width/2, 50*scale)
        p5.text("Total distance travelled: " + str(statistics.distanceTravelled),width / 2, 100*scale)
        p5.text("Total damage taken: " + str(statistics.damageTaken),width / 2, 120*scale)
        p5.text("Total health regained: " + str(statistics.healthRegained),width / 2, 140*scale)
        p5.text("Total enemies exterminated: " + str(statistics.enemiesKilled),width / 2, 160*scale)

        if key_is_pressed:
            if key == 'ENTER':
                showStats = False




def sendScore(name,score,score_list):
    print("Your name is",name)
    print("Your score was",score)

    with open('leaderboard.txt', 'a') as f:
        f.write(name)
        f.write('\n')
        f.write(str(score))
        f.write('\n')
    scoreboard.close()

    score_list.sort(key=lambda y: y[0])
    score_list.reverse()

def restart():
    global animal,apple,killer,Shield,wallTeleport,enemies,statistics,projectiles,property,preGame,scoreSent,readyToReset,score,difficulty,scale
    animal = Snake(50, 80, 1, 1, 0, speed, Size, 100, maxHealth, 1, True, 0,scale)
    apple = Food(random.randrange(width/2,width-buffer), random.randrange(height/2,height-buffer), Size, 10)
    killer = EnemyKiller(random.randrange(buffer,width-buffer), random.randrange(buffer,height-buffer), Size)
    Shield = GetShield(random.randrange(buffer,width-buffer), random.randrange(buffer,height-buffer), Size)
    wallTeleport = WallTeleport(random.randrange(buffer,width-buffer), random.randrange(buffer,height-buffer), Size)
    enemies = [Enemy(random.randrange(width/2,width-buffer),random.randrange(height/2,height-buffer),255,'tri',10,250*scale,10,60,badGuyCooldown,badGuySpeed, scale)]
    statistics = Statistics()
    statistics.__init__()
    projectiles = []
    preGame = True
    scoreSent = False
    readyToReset = False
    score = 0
    difficulty = 1

restart()
run()
