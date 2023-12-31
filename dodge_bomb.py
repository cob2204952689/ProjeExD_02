import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900


delta = {#練習３:移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}



def check_bound(obj_rct: pg.Rect):
    """
    引数：こうかとんRectか爆弾Rect
    戻り値：タプル（横判定結果、縦判定結果）
    画面内ならTrue,画面外ならFalse
    """
    yoko,tate = True,True
    if obj_rct.left < 0 or WIDTH <obj_rct.right:#横方向判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT <obj_rct.bottom:#縦方向判定
        tate = False
    return yoko,tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    """こうかとん"""
    kk_img = pg.image.load("ex02/fig/3.png")
    key_lst = pg.key.get_pressed()
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = (900,400)
    kk_img2 = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct2 = kk_img2.get_rect()
    kk_rct2.center = (900,400)
    """爆弾"""
    bd_img = pg.Surface((20, 20))#爆弾surfaceの作成
    bd_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct = bd_img.get_rect()#surfaceからRectを抽出
    x, y = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    bd_rct.center = (x, y)#練習1　Rectにランダムな座標を設定する
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bd_rct):

            print("Game Over")
            return

        screen.blit(bg_img, [0, 0])

        """こうかとん"""
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        muki = {
            (-5,0):pg.transform.rotozoom(kk_img, 0, 1.0),
            (-5,-5):pg.transform.rotozoom(kk_img, 45, 1.0),
            (0,-5):pg.transform.rotozoom(kk_img2, 90, 1.0),
            (+5,-5):pg.transform.rotozoom(kk_img2, 45, 1.0),
            (+5,0):pg.transform.rotozoom(kk_img2, 0, 1.0),
            (+5,+5):pg.transform.rotozoom(kk_img2, -45, 1.0),
            (0,+5):pg.transform.rotozoom(kk_img2, -90, 1.0),
            (-5,+5):pg.transform.rotozoom(kk_img, -45, 1.0)
        }
        for key ,mv in delta.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
            screen.blit(muki(sum_mv),kk_rct) 
            
        kk_rct.move_ip(sum_mv[0],sum_mv[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        """爆弾"""
        bd_rct.move_ip(vx,vy)
        yoko, tate = check_bound(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bd_img,bd_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()