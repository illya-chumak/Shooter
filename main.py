from pygame import *
from random import randint


class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, player_speed, width=65, height=65):
        super().__init__()
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed # швидкість переміщення спрайту
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x # координата x спрайту
        self.rect.y = player_y # координата y спрайту

    # метод для відображення спрайту у точці з координатами (x, y)
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# клас головного гравця
class Player(GameSprite):
    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 85:
            self.rect.x += self.speed

    # метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


# клас спрайта-ворога
class Enemy(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


# клас спрайта-кулі
class Bullet(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.y < 0:
            self.kill()

# ігрова сцена
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

# персонажі гри
ship = Player('rocket.png', 5, win_height - 100, 80, 100, 20)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

# шрифти й написи
font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 80)
win = font2.render('YOU WIN!', True, (255, 255, 255))
lose = font2.render('YOU LOSE!', True, (180, 0, 0))

score = 0  # збито кораблів
lost = 0  # пропущено кораблів
goal = 10  # стільки кораблів потрібно збити для перемоги
max_lost = 3  # програли, якщо пропустили стільки

game = True  # прапорець скидається кнопкою закриття вікна
finish = False  # змінна "гра закінчилася"

clock = time.Clock()
FPS = 20

while game:
    # подія натискання на кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            game = False
        # подія натискання на пробіл - спрайт стріляє
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                # fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(background, (0, 0))  # оновлюємо фон

        # пишемо текст на екрані
        text = font1.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # рух спрайтів
        ship.update()
        monsters.update()
        bullets.update()

        # оновлюємо їх у новому місці при кожній ітерації циклу
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        # перевірка зіткнення кулі та монстрів (і монстр, і куля при зіткненні зникають)
        if sprite.groupcollide(monsters, bullets, True, True):
            score = score + 1
            monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        # можливий програш: пропустили занадто багато або герой зіткнувся з ворогом
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        # перевірка виграшу: скільки очок набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()

    clock.tick(FPS)