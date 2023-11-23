import time
from random import randint

import pygame

pygame.init()
background = (204, 255, 51)
mw = pygame.display.set_mode((500, 500))
mw.fill(background)

clock = pygame.time.Clock()

VIOLET = (102, 51, 255)
CARD_COLOR = (51, 204, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 51)
LIGHT_RED = (250, 128, 114)
LIGHT_GREEN = (200, 255, 200)


class Rectangle():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)  # прямоугольник
        self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)


class Object(Rectangle):
    def set_text(self, text, fsize=12, text_color=(255, 51, 204)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


start_time = time.time()
cur_time = start_time

cards = []
num_cards = 4
x = 70

time_text = Object(0, 0, 50, 50, background)
time_text.set_text('Time:', 25, VIOLET)
time_text.draw(20, 20)

timer = Object(50, 55, 50, 40, background)
timer.set_text('0', 40, VIOLET)
timer.draw(0, 0)

score_text = Object(380, 0, 50, 50, background)
score_text.set_text('Score:', 25, VIOLET)
score_text.draw(20, 20)

score = Object(430, 55, 50, 40, background)
score.set_text('0', 40, VIOLET)
score.draw(0, 0)

for i in range(num_cards):
    new_card = Object(x, 170, 70, 100, CARD_COLOR)
    new_card.set_text('CLICK', 13)
    cards.append(new_card)
    x = x + 100

wait = 0
points = 0

while True:
    if wait == 0:
        wait = 20  # столько тиков надпись будет на одном месте
        click = randint(1, num_cards)
        for i in range(num_cards):
            cards[i].color(CARD_COLOR)
            if (i + 1) == click:
                cards[i].draw(10, 40)
            else:
                cards[i].fill()
    else:
        wait -= 1
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            for i in range(num_cards):
                # ищем, в какую карту попал клик
                if cards[i].collidepoint(x, y):
                    if i + 1 == click:  # если на карте есть надпись перекрашиваем в зелёный, плюс очко
                        cards[i].color(GREEN)
                        points += 1
                    else:  # иначе перекрашиваем в красный, минус очко
                        cards[i].color(RED)
                        points -= 1
                    cards[i].fill()
                    score.set_text(str(points), 40, VIOLET)
                    score.draw(0, 0)
    new_time = time.time()

    if int(new_time) - int(cur_time) == 1:  # проверяем, есть ли разница в 1 секунду между старым и новым временем
        timer.set_text(str(int(new_time - start_time)), 40, VIOLET)
        timer.draw(0, 0)
        cur_time = new_time

    if new_time - start_time >= 11:
        win = Object(0, 0, 500, 500, LIGHT_RED)
        win.set_text("Time is up!!!", 45, VIOLET)
        win.draw(110, 180)
        break

    if points >= 5:
        win = Object(0, 0, 500, 500, LIGHT_GREEN)
        win.set_text("You won!", 45, VIOLET)
        win.draw(140, 180)
        resul_time = Object(90, 230, 250, 250, LIGHT_GREEN)
        resul_time.set_text("Your time is: " + str(int(new_time - start_time)) + " sec", 20, VIOLET)
        resul_time.draw(0, 0)
        break

    pygame.display.update()
    clock.tick(40)
