import time
from sprite import *


def dialogue_mode(sprite, text):
    sprite.update()
    screen.blit(background, (0, 0))
    screen.blit(sprite.image, sprite.rect)
    text1 = font1.render(text[text_number], True, pg.Color("White"))
    screen.blit(text1, (280, 450))
    if text_number < len(text) - 1:
        text2 = font1.render(text[text_number + 1], True, pg.Color("White"))
        screen.blit(text2, (280, 480))


pg.init()
pg.mixer.init()

size = (800, 600)
screen = pg.display.set_mode(size)
pg.display.set_caption("Космические коты")

FPS = 120
clock = pg.time.Clock()

background = pg.image.load("images/space.png").convert()
background = pg.transform.scale(background, size)

health = pg.image.load("images/сердце.png")
health = pg.transform.scale(health, (40, 40))

is_running = True
mode = "start_scene"

meteorites = pg.sprite.Group()
mice = pg.sprite.Group()
lasers = pg.sprite.Group()

captain = Captain()
alien = Alien()

catship = Starship()

start_text = ["Мы засекли сигнал с планеты Мур.",
              "",
              "Наши друзья, инопланетные коты,",
              "нуждаются в помощи.",
              "Космические мыши хотят съесть их луну,",
              "потому что она похожа на сыр.",
              "Как долго наш народ страдал от них, ",
              "теперь и муряне в беде...",
              "Мы должны помочь им.",
              "Вылетаем прямо сейчас.",
              "Спасибо, что починил звездолёт, штурман. ",
              "Наконец-то функция автопилота работает.",
              "Поехали!"]

alien_text = ["СПАСИТЕ! МЫ ЕЛЕ ДЕРЖИМСЯ!",
              "",
              "Мыши уже начали грызть луну...",
              "Скоро куски луны будут падать на нас.",
              "Спасите муриан!", ]

final_text = ["Огромное вам спасибо,",
              "друзья с планеты Мяу!",
              "Как вас называть? Мяуанцы? Мяуриане?",
              "В любом случае, ",
              "теперь наша планета спасена!",
              "Мы хотим отблагодарить вас.",
              "Капитан Василий и его штурман получают",
              "орден SKYSMART.",
              "А также несколько бутылок нашей",
              "лучшей валерьянки.",
              "",
              ""]

text_number = 0
font1 = pg.font.Font("font.otf", 25)
pg.mixer.music.load("sounds/музыка.wav")
pg.mixer.music.set_volume(0.2)
pg.mixer.music.play()

laser_sound = pg.mixer.Sound("sounds/звук лазера.wav")
laser_sound.set_volume(0.3)
win_sound = pg.mixer.Sound("sounds/звук победы.wav")
win_sound.set_volume(0.3)
while is_running:

    # СОБЫТИЯ
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False

        if event.type == pg.KEYDOWN:
            if mode == "start_scene":
                text_number += 2
                if text_number > len(start_text):
                    text_number = 0
                    mode = "meteorites"
                    time = pg.time.get_ticks()
                    catship.hp = 3

            if mode == "alien_scene":
                text_number += 2
                if text_number > len(alien_text):
                    text_number = 0
                    alien.rect.topleft = (-30, 600)
                    alien.mode = "up"
                    mode = "moon"
                    time = pg.time.get_ticks()
                    catship.hp = 3
                    catship.switch_mode()

            if mode == "moon":
                if event.key == pg.K_SPACE:
                    lasers.add(Laser(catship.rect.midtop))
                    laser_sound.play()

            if mode == "final_scene":
                if text_number < len(final_text) - 2:
                    text_number += 2
                else:
                    text_number = 11

    # ОБНОВЛЕНИЯ
    if mode == "start_scene":
        dialogue_mode(captain, start_text)

    if mode == "meteorites":
        pg.mixer.music.fadeout(2)
        if pg.time.get_ticks() - 2000 >= time:
            mode = "alien_scene"
            win_sound.play()
            pg.mixer.music.play()

        if random.randint(1, 80) == 1:
            meteorites.add(Meteorite())

        meteorites.update()
        catship.update()

        hits = pg.sprite.spritecollide(catship, meteorites, True)
        for hit in hits:
            catship.hp -= 1
            if catship.hp == 0:
                mode = "start_scene"
                pg.mixer.music.play()

        screen.blit(background, (0, 0))
        screen.blit(catship.image, catship.rect)
        meteorites.draw(screen)
        for i in range(catship.hp):
            screen.blit(health, (i * 37, 5))

    if mode == "alien_scene":
        dialogue_mode(alien, alien_text)

    if mode == "moon":
        pg.mixer.music.fadeout(2)
        if pg.time.get_ticks() - 30000 >= time:
            mode = "final_scene"
            win_sound.play()
            pg.mixer.music.play()

        if random.randint(1, 80) == 1:
            mice.add(Mouse_starship())

        catship.update()
        mice.update()
        lasers.update()

        hits = pg.sprite.spritecollide(catship, mice, dokill=True)
        for hit in hits:
            catship.hp -= 1
            if catship.hp == 0:
                mode = "alien_scene"
                pg.mixer.music.play()

        pg.sprite.groupcollide(lasers, mice, True, True)

        screen.blit(background, (0, 0))
        screen.blit(catship.image, catship.rect)
        mice.draw(screen)
        lasers.draw(screen)
        for i in range(catship.hp):
            screen.blit(health, (i * 37, 5))

    if mode == "final_scene":
        dialogue_mode(alien, final_text)

    pg.display.flip()
    clock.tick(FPS)
