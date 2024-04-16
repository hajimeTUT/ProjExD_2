import os
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_img2 = pg.transform.flip(bg_img, True, False)
    kokaton_img = pg.image.load("fig/3.png")
    kokaton_img = pg.transform.flip(kokaton_img, True, False)
    kokaton_rct = kokaton_img.get_rect()
    kokaton_rct.center = 300, 200
    key_dict = {pg.K_UP: (0,-1), pg.K_DOWN: (0,1), pg.K_RIGHT: (2, 0), pg.K_LEFT: (-1, 0)}
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        
        for key, value in key_dict.items():
            if pg.key.get_pressed()[key]: kokaton_rct.move_ip(value)

        kokaton_rct.move_ip((-1,0))
        x = tmr%3200
    
        screen.blit(bg_img, [-x, 0])
        screen.blit(bg_img2, [-x + 1600, 0])
        screen.blit(bg_img, [-x + 1600 * 2, 0])
        screen.blit(bg_img2, [-x + 1600 * 3, 0])
        screen.blit(kokaton_img, kokaton_rct)

        pg.display.update()
        tmr += 1        
        clock.tick(200)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()