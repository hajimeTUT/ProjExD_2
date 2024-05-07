import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = {  # 移動量辞書（押下キー：移動量タプル）
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    こうかとんRect，または，爆弾Rectの画面内外判定用の関数
    引数：こうかとんRect，または，爆弾Rect
    戻り値：横方向判定結果，縦方向判定結果（True：画面内／False：画面外）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: 
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

# 移動方向に基づいて画像を反転させ、適切な角度で回転させる設定
ROTATE_DICT = {
    (1, 0): (False, 0),     # 右
    (1, 1): (False, -45),   # 右下
    (1, -1): (False, 45),   # 右上
    (0, 1): (False, -90),   # 下
    (0, -1): (False, 90),   # 上
    (-1, 0): (True, 0),     # 左
    (-1, 1): (True, 45),   # 左下
    (-1, -1): (True, -45)    # 左上
}

def update_bb():
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs

def update_kk_image(original_img, last_direction):
    flip, angle = ROTATE_DICT.get(last_direction, (False, 0))
    new_img = pg.transform.flip(original_img, flip, False)
    new_img = pg.transform.rotate(new_img, angle)
    return new_img

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    # ここからこうかとんの設定
    bg_img = pg.image.load("fig/pg_bg.jpg")
    original_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    original_img = pg.transform.flip(original_img, True, False)  # 初期反転
    kk_img = original_img
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_imgs, bb_accs = update_bb()
    bd_img = bb_imgs[0]
    bd_rct = bd_img.get_rect()
    bd_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 横方向速度，縦方向速度
    last_direction = (0, 0)
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 
        if kk_rct.colliderect(bd_rct):  # こうかとんと爆弾がぶつかったら
            print("Game Over")
            return
        screen.blit(bg_img, [0, 0]) 

        # こうかとんの移動と表示
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]

        if sum_mv[0] != 0 or sum_mv[1] != 0:
            last_direction = (sum_mv[0] // abs(sum_mv[0]) if sum_mv[0] != 0 else 0,
                              sum_mv[1] // abs(sum_mv[1]) if sum_mv[1] != 0 else 0)
            kk_img = update_kk_image(original_img, last_direction)

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        # 爆弾の移動と表示
        bd_img = bb_imgs[min(tmr // 150, 9)]
        bd_rct.size = bd_img.get_size()
        # 爆弾の速度更新
        # 爆弾を移動させる
        bd_rct.move_ip(vx, vy)
        
        # 爆弾が画面端に達した場合の反転処理
        yoko, tate = check_bound(bd_rct)
        if not yoko:  # 横方向にはみ出てたら
            vx *= -1
        if not tate:  # 縦方向にはみ出てたら
            vy *= -1

        # 爆弾の速度を更新する
        vx = bb_accs[min(tmr // 150, 9)] * (5 if vx > 0 else -5)
        vy = bb_accs[min(tmr // 150, 9)] * (5 if vy > 0 else -5)

        screen.blit(bd_img, bd_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()