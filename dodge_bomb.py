import math
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

def show_game_over(screen):
    # 黒の半透明の四角を画面全体に描画
    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)  # 半透明度設定
    screen.blit(overlay, (0, 0))

    # Game Over のテキスト
    font = pg.font.Font(None, 100)
    text = font.render('Game Over', True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    screen.blit(text, text_rect)

    
    crying_img = pg.image.load("fig/8.png")
    crying_rect1 = crying_img.get_rect(center=(WIDTH / 2 - 270, HEIGHT / 2))
    crying_rect2 = crying_img.get_rect(center=(WIDTH / 2 + 270, HEIGHT / 2))
    screen.blit(crying_img, crying_rect1)
    screen.blit(crying_img, crying_rect2)
    pg.display.update()
    pg.time.delay(5000)  # 5秒間表示

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

def calc_bb_speed(current_pos, target_pos, prev_vx, prev_vy, inertia_distance=300, speed=5):
    # 差分ベクトル
    dx, dy = target_pos[0] - current_pos[0], target_pos[1] - current_pos[1]
    distance = math.sqrt(dx**2 + dy**2)
    
    if distance < inertia_distance:
        return prev_vx, prev_vy
    
    norm = math.sqrt(dx**2 + dy**2)
    normalized_vx = (dx / norm) * speed
    normalized_vy = (dy / norm) * speed
    
    return normalized_vx, normalized_vy

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
            show_game_over(screen)
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

        # 爆弾の速度
        vx, vy = calc_bb_speed((bd_rct.centerx, bd_rct.centery), (kk_rct.centerx, kk_rct.centery), vx, vy)
        bd_rct.move_ip(vx, vy)
        
        screen.blit(bd_img, bd_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()