import numpy as np
import p5
from p5 import setup, draw, size, background, background, Vector, color, stroke, circle
import random
# from main import *

class Food():

    def __init__(self, x, y, Size, heal):
        self.position = Vector(x,y)
        self.Size = Size
        self.healAmmount = heal

    def show(self):
        stroke(255)
        p5.fill(255,140,165)
        p5.circle(self.position.x, self.position.y, self.Size)

    def move(self,buffer):
        self.position = Vector(random.randrange(buffer,width-buffer), random.randrange(buffer,height-buffer))

class EnemyKiller():

    def __init__(self, x, y, Size):
        self.position = Vector(x,y)
        self.Size = Size

    def show(self):
        stroke(255)
        p5.fill(50,50,250)
        p5.circle(self.position.x, self.position.y, self.Size)

    def move(self,buffer):
        self.position = Vector(random.randrange(buffer,width-buffer), random.randrange(buffer,height-buffer))

class WallTeleport():

    def __init__(self, x, y, Size):
        self.position = Vector(x,y)
        self.Size = Size

    def show(self):
        stroke(255)
        p5.fill(255,255,0)
        p5.circle(self.position.x, self.position.y, self.Size)

    def move(self,buffer):
        self.position = Vector(random.randrange(buffer,width-buffer), random.randrange(buffer,height-buffer))

class GetShield():

    def __init__(self, x, y, Size):
        self.position = Vector(x,y)
        self.Size = Size

    def show(self):
        stroke(255)
        p5.no_fill()
        p5.circle(self.position.x, self.position.y, self.Size)

    def move(self,buffer):
        self.position = Vector(random.randrange(buffer,width-buffer), random.randrange(buffer,height-buffer))

class Snake():

    def __init__(self, x, y, length, vx, vy, speed, Size, cooldown, health, shield, alive, teleport, scale):
        self.scale = scale
        self.length = length
        self.speed = speed
        self.Size = Size
        self.position = Vector(x, y)
        self.velocity = Vector(vx * self.speed, vy * self.speed)*self.scale
        self.cooldown = cooldown
        self.cooldownMax = cooldown
        self.health = health
        self.shield = shield
        self.alive = alive
        self.teleport = teleport
        self.teleportCount = teleport


        Size = 10

    def show(self):
        stroke(255)
        for i in range(self.shield):
            n = i+1
            p5.no_fill()
            p5.circle(self.position.x, self.position.y, self.Size*np.sqrt(n)*1.5)

        p5.fill(0,0,0)
        p5.circle(self.position.x, self.position.y, self.Size)

        p5.text_align(align_x = "CENTER", align_y = "TOP")
        p5.text(str(self.health), self.position.x, self.position.y -20)


    def update(self):
        self.position += self.velocity

        if self.teleportCount <= 0 and self.teleport <= 0:
            if self.position.x > width or self.position.x < 0 or self.position.y > height or self.position.y < 0:
                self.death()
        if self.teleportCount > 0 or self.teleport > 0:
            if self.position.x > width or self.position.x < 0:
                self.position.x = np.abs(self.position.x - width)
                self.teleportCount = max(self.teleportCount - 1, 0)
                if self.teleport > 100:
                    self.teleport -= 1
            if self.position.y > height or self.position.y < 0:
                self.position.y = np.abs(self.position.y - height)
                self.teleportCount = max(self.teleportCount - 1, 0)
                if self.teleport > 100:
                    self.teleport -= 1

        if self.teleport <= 100:
            self.teleport -= 1


        if self.health <= 0:
            self.death()

        if key_is_pressed:
            if key == "UP" and self.velocity.y == 0:
                self.velocity = Vector(0,-1 * self.speed*self.scale)
            if key == "DOWN" and self.velocity.y == 0:
                self.velocity = Vector(0, 1 * self.speed*self.scale)
            if key == "LEFT" and self.velocity.x == 0:
                self.velocity = Vector(-1 * self.speed*self.scale, 0)
            if key == "RIGHT" and self.velocity.x == 0:
                self.velocity = Vector(1 * self.speed*self.scale, 0)


        if self.cooldown < 0:
            self.cooldown = self.cooldownMax
        if self.cooldown != self.cooldownMax:
            self.cooldown -= 1

    def death(self):
        self.alive = False

    def reset(self):
        self.position = Vector(50,80)
        self.velocity = Vector(self.speed,0)
        self.alive = True
        self.health = 100
        self.shield = 1
        self.teleport = 0
        self.alive = True

class Enemy():
    def __init__(self, x, y, redness, shape, size, range, damage, meleecooldown, rangecooldown, speed, scale):
        self.position = Vector(x,y)
        self.redness = redness
        self.range = range
        self.scale = scale
        self.damage = damage
        self.size = size
        self.shape = shape
        self.speed = speed*self.scale
        self.meleecooldown = meleecooldown - 1
        self.meleecooldownMax = meleecooldown
        self.rangecooldown = rangecooldown - 1
        self.rangecooldownMax = rangecooldown
        self.velocity = Vector(self.speed, self.speed)

        self.randx = np.random.random() - 0.5
        self.randy = np.random.random() - 0.5

    def show(self,difficulty):
        stroke(255)
        p5.fill(int(self.redness),0,0)
        if self.shape == 'tri':
            x = self.position.x
            y = self.position.y
            p5.circle(x,y,10*self.scale)
            

    def update(self,player,enemies):

        toPlayer = (player.position - self.position) / np.linalg.norm(self.position - player.position)
        awayEnemy = Vector(0,0)
        newVelocity = Vector(0,0)
        for badguy in enemies:
            if (badguy.position != self.position):
                if (np.linalg.norm(badguy.position - self.position)) < 15:
                    awayEnemy += self.position - badguy.position

        if np.linalg.norm(awayEnemy) != 0:
            newVelocity = awayEnemy / np.linalg.norm(awayEnemy)

        newVelocity += (toPlayer + Vector(self.randx,self.randy))
        newVelocity /= np.linalg.norm(self.velocity)
        newVelocity *= self.scale

        self.position += newVelocity * self.speed




        if self.meleecooldown < 0:
            self.meleecooldown = self.meleecooldownMax
        if self.meleecooldown != self.meleecooldownMax:
            self.meleecooldown -= 1

        if self.rangecooldown < 0:
            self.rangecooldown = self.rangecooldownMax
        if self.rangecooldown != self.rangecooldownMax:
            self.rangecooldown -= 1

    def attack(self,victim):
        self.cooldown -= 1

class Projectile():
    def __init__(self, x, y, vx, vy, speed, damage, scale):
        self.scale = scale
        self.position = Vector(x,y)
        self.velocity = Vector(vx,vy) / np.linalg.norm(Vector(vx,vy)) * 5
        self.speed = speed
        self.damage = damage

    def show(self):
        stroke(255)
        p5.fill(100,0,0)
        p5.circle(self.position.x, self.position.y, 5*self.scale)

    def update(self, player):

        toPlayer = (player.position + player.velocity*3) - self.position

        toPlayer /= np.linalg.norm(toPlayer) * 5
        self.velocity += toPlayer
        self.position += self.velocity*self.scale



    def __del__(self):
        pass

class Statistics():
    def __init__(self):
        self.distanceTravelled = 0
        self.damageTaken = 0
        self.healthRegained = 0
        self.enemiesKilled = 0
