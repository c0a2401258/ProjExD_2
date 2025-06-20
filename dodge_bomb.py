import os
import sys
import time
import random
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {  # 移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct:pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectか爆弾Rect
    戻り値：タプル（横方向判定結果、縦方向判定結果）
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True, True  # 初期値:画面内
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate  # 横方向、縦方向の画面内判定を返す

def gameover(screen: pg.Surface) -> None:
    bk_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bk_img, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    bk_img.set_alpha(200)  # 半透明化
    screen.blit(bk_img, [0, 0])
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over",
                      True, (255, 255, 255))
    screen.blit(txt, [WIDTH/2-150, HEIGHT/2-20])
    bg1_img = pg.image.load("fig/8.png")
    bg2_img = pg.image.load("fig/8.png")
    screen.blit(bg1_img, [WIDTH/2-210, HEIGHT/2-20])
    screen.blit(bg2_img, [WIDTH/2+170, HEIGHT/2-20])
    pg.display.update()
    time.sleep(5)
    
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_accs = [a for a in range(1, 11)]
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))  # 大きさ更新
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs  # リストを返す

def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    ZISYO = {
        (-5, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),
        (-5, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 315, 0.9),
        (0, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 270, 0.9),
        (+5, -5): pg.transform.flip(pg.image.load("fig/3.png"), True, False),
        (+5, 0): pg.transform.flip(pg.image.load("fig/3.png"), True, False),
        (+5, +5): pg.transform.flip(pg.image.load("fig/3.png"), True, False),
        (0, +5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 0.9),
        (-5, +5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 0.9),
    } 
    if sum_mv == (0, 0):
        return pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    if sum_mv[0] == +5:
        a = ZISYO[sum_mv]
        if sum_mv[1] == -5:
            a = pg.transform.rotozoom(a, 45, 0.9)
        elif sum_mv[1] == +5:
            a = pg.transform.rotozoom(a, -45, 0.9)
        return a
    elif sum_mv[0] == 0:
        a = ZISYO[sum_mv]
        a = pg.transform.flip(a, True, False)
        return a
    else:
        return ZISYO[sum_mv]

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 空のSurfaceを作る（爆弾用）
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い円を描く
    bb_img.set_colorkey((0, 0, 0))  # 黒を透明色に設定
    bb_rct = bb_img.get_rect()  # 爆弾Rectを取得
    bb_rct.centerx = random.randint(0, WIDTH)  # 横座標の乱数
    bb_rct.centery = random.randint(0, HEIGHT)  # 縦座標の乱数
    vx, vy = +5, +5  # 爆弾の移動速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):  # こうかとんRectと爆弾Rectの衝突
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 移動をなかったことにする
        
        kk_img = get_kk_img((0, 0))
        kk_img = get_kk_img(tuple(sum_mv))
        screen.blit(kk_img, kk_rct)

        bb_imgs, bb_accs = init_bb_imgs()
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]

        bb_rct.move_ip(avx, avy)  # 爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1 
        screen.blit(bb_img, bb_rct)  # 爆弾の描画
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
