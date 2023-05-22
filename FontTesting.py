import pygame as pg

pg.init()
screen = pg.display.set_mode((720, 720))
pg.display.set_caption("Font Testing")


fonts = pg.font.get_fonts()
print(fonts[4])
i = -1

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        elif event.type == pg.KEYDOWN:
            key = pg.key.get_pressed()
            if key[pg.K_RIGHT]:
                screen.fill((255, 255, 255))
                font_str = pg.font.match_font(fonts[i])
                font = pg.font.Font(font_str, 36)
                for j in range(9):
                    text = font.render(str(j+1), True, (0, 0, 0))
                    textpos = text.get_rect(topleft=(100+j*45, 360))
                    screen.blit(text, textpos)

                text = font.render("You win!", True, (0, 0, 0))
                textpos = text.get_rect(
                    centerx=screen.get_width()/2, y=screen.get_height()-100)
                screen.blit(text, textpos)
                print(fonts[i])

                pg.display.flip()
                i += 1
            elif key[pg.K_LEFT]:
                i -= 1

'''
win:

menlo
noteworthy
savoyelet - cursive
bodoni72smallcapsbook
MAIN:
arialunicode
applesdgothicneo
** menlo **
stheitimedium
whatever 5 is
geneva
hiraginosansgb - softer look
** sfnsmono **
pingfang - minimalistic
newyork - fancy
** ヒラキノ明朝pron **
palatino
** times **
markerfelt - fun
keyboard
** zapfino ** - fancy cursive
timesnewroman
** silom ** - old timey video game text
** stixgeneral **
arial
** couriernew **
superclarendon
** wingdings3 ** - special version
** wingdings2 **
** webdings ** - special version


NOTES:

** noteworthy **
kohinoortelugu
ヒラキノ角コシックw0
** zapfino ** - fancy cursive
** bradleyhand **
** arialnarrow **
papyrus
** mishafi ** - small text
** diwankufi **
** partyletplain ** - ornamental text
** sana ** - simple small text
** raanana **

'''
