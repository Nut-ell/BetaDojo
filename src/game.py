# src/game.py
import pygame
import os
import random
import math
from src.config import *
from src.questions_data import QUESTIONS_LIST

# --- 色設定 (Web風モダンパレット) ---
C_BG = (30, 30, 40)       # 落ち着いたダークネイビー
C_CARD = (255, 255, 255)  # カード背景
C_SHADOW = (200, 200, 200) # カードの影（厚み）
C_BTN_BASE = (240, 240, 245) # ボタン色
C_BTN_SHADOW = (180, 180, 190) # ボタンの厚み
C_ACCENT = (88, 204, 2)   # 正解グリーン
C_ACCENT_S = (60, 160, 0) # 正解の厚み
C_FAIL = (255, 80, 80)    # 不正解レッド
C_FAIL_S = (180, 50, 50)  # 不正解の厚み
C_TEXT = (50, 50, 60)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Beta Blitz - Stylish Edition")
        self.clock = pygame.time.Clock()
        
        # フォント: システムのサンセリフ体を探す
        self.font_cat = pygame.font.SysFont("arial", 30, bold=True)
        self.font_hint = pygame.font.SysFont("arial", 20, italic=True)

        self.load_assets()
        self.reset_quiz()

    def load_assets(self):
        def load_img(name):
            path = os.path.join(IMG_DIR, name)
            if not os.path.exists(path): return pygame.Surface((100, 50))
            # スムーススケーリング用に変換
            return pygame.image.load(path).convert_alpha()

        self.img_beta = load_img("beta_large.png")
        self.q_assets = {}
        for q in QUESTIONS_LIST:
            self.q_assets[q["id"]] = {
                "q": load_img(f"{q['id']}_q.png"),
                "opts": [load_img(f"{q['id']}_opt_{i}.png") for i in range(3)]
            }
        
        pygame.mixer.init()
        self.sounds = {}
        for name in ["PIKON", "SHOBON", "GABIN"]:
            path = os.path.join(SND_DIR, f"{name}.wav")
            if os.path.exists(path): self.sounds[name] = pygame.mixer.Sound(path)

    def reset_quiz(self):
        self.state = "INTRO"
        self.spin = 0
        self.scale = 1.0
        self.q_list = list(QUESTIONS_LIST)
        random.shuffle(self.q_list)
        self.q_idx = 0
        self.streak = 0
        
        # 演出用変数
        self.shake = 0
        self.flash_alpha = 0
        self.flash_color = (255, 255, 255)
        
        self.msg_timer = 0
        self.msg_type = None
        self.clicked_btn = -1 # どのボタンを押したか（沈む演出用）

    def play_sound(self, name):
        if name in self.sounds: self.sounds[name].play()

    # --- お洒落な角丸ボタン描画 ---
    def draw_btn(self, rect, color_top, color_side, is_pressed=False):
        r = 15 # 角丸の半径
        off = 4 if not is_pressed else 0 # 押していない時の浮き上がり量
        
        # 下の厚み部分 (Side)
        if not is_pressed:
            shadow_rect = pygame.Rect(rect.x, rect.y + off, rect.width, rect.height)
            pygame.draw.rect(self.screen, color_side, shadow_rect, border_radius=r)
        
        # 上の面 (Top)
        top_rect = pygame.Rect(rect.x, rect.y + (0 if not is_pressed else 4), rect.width, rect.height)
        pygame.draw.rect(self.screen, color_top, top_rect, border_radius=r)
        return top_rect # テキスト描画用の中心を返す

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            self.update()
            self.draw(mouse_pos)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def update(self):
        # シェイク減衰
        if self.shake > 0: self.shake -= 2
        if self.shake < 0: self.shake = 0
        
        # フラッシュ減衰
        if self.flash_alpha > 0: self.flash_alpha -= 5
        if self.flash_alpha < 0: self.flash_alpha = 0

        # 次の問題へ
        if self.msg_timer > 0:
            self.msg_timer -= 1
            if self.msg_timer == 0 and self.state == "QUIZ":
                self.q_idx += 1
                self.msg_type = None
                self.clicked_btn = -1

        if self.state == "SPIN":
            self.spin += 20 # 回転を少し滑らかに
            self.scale -= 0.02
            if self.scale <= 0:
                self.state = "QUIZ"
                self.scale = 0

    def draw(self, mouse_pos):
        # 画面揺れ
        ox = random.randint(-self.shake, self.shake) if self.shake > 0 else 0
        oy = random.randint(-self.shake, self.shake) if self.shake > 0 else 0
        
        # 背景
        self.screen.fill(C_BG)

        # コンテンツ描画用オフセット
        draw_surf = self.screen.copy() # 一旦別サーフェスにはしないが、座標計算用

        if self.state == "INTRO":
            # タイトル
            rect = self.img_beta.get_rect(center=(SCREEN_WIDTH//2 + ox, SCREEN_HEIGHT//2 + oy))
            self.screen.blit(self.img_beta, rect)
            
            # 点滅テキスト
            if pygame.time.get_ticks() % 1500 < 800:
                t = self.font_cat.render("CLICK TO START", True, (150, 150, 180))
                self.screen.blit(t, (SCREEN_WIDTH//2 - t.get_width()//2, SCREEN_HEIGHT - 100))

        elif self.state == "SPIN":
            w, h = int(self.img_beta.get_width()*self.scale), int(self.img_beta.get_height()*self.scale)
            if w > 0:
                scaled = pygame.transform.scale(self.img_beta, (w, h))
                rot = pygame.transform.rotate(scaled, self.spin)
                self.screen.blit(rot, rot.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))

        elif self.state == "QUIZ":
            if self.q_idx >= len(self.q_list):
                t = self.font_cat.render("COMPLETE!", True, C_ACCENT)
                self.screen.blit(t, (SCREEN_WIDTH//2 - t.get_width()//2, SCREEN_HEIGHT//2))
            else:
                q = self.q_list[self.q_idx]
                assets = self.q_assets[q["id"]]
                
                # カテゴリ
                cat_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, 30, 400, 40)
                pygame.draw.rect(self.screen, (40, 40, 55), cat_rect, border_radius=20)
                t_cat = self.font_cat.render(q["category"], True, C_ACCENT)
                self.screen.blit(t_cat, (SCREEN_WIDTH//2 - t_cat.get_width()//2, 35))
                
                # 問題画像
                q_rect = assets["q"].get_rect(center=(SCREEN_WIDTH//2, 160))
                self.screen.blit(assets["q"], q_rect)
                
                # ヒント
                t_hint = self.font_hint.render(f"{q['hint']}", True, (150, 150, 170))
                self.screen.blit(t_hint, (SCREEN_WIDTH//2 - t_hint.get_width()//2, 240))

                # ボタンエリア
                base_y = 320
                for i in range(3):
                    btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, base_y + i*90, 400, 70)
                    
                    # 状態判定
                    is_hover = btn_rect.collidepoint(mouse_pos)
                    is_pressed = (self.clicked_btn == i)
                    
                    # 色決定
                    c_top, c_side = C_BTN_BASE, C_BTN_SHADOW
                    
                    # 正解・不正解のフィードバック色
                    if self.msg_type:
                        if i == q["ans"] and (self.msg_type == "PIKON" or self.msg_type == "GABIN"):
                            c_top, c_side = C_ACCENT, C_ACCENT_S # 緑
                            is_pressed = True # 正解はずっと沈ませる
                        elif i == self.clicked_btn and self.msg_type == "SHOBON":
                            c_top, c_side = C_FAIL, C_FAIL_S   # 赤
                            is_pressed = True
                    elif is_hover and not is_pressed:
                        c_top = (255, 255, 255) # ホバーで少し明るく

                    # 描画
                    top_area = self.draw_btn(btn_rect, c_top, c_side, is_pressed)
                    
                    # 選択肢画像
                    img = assets["opts"][i]
                    img_rect = img.get_rect(center=top_area.center)
                    self.screen.blit(img, img_rect)

        # フラッシュ効果 (オーバーレイ)
        if self.flash_alpha > 0:
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            s.set_alpha(self.flash_alpha)
            s.fill(self.flash_color)
            self.screen.blit(s, (0,0))

        # GABIN演出（文字だけ）
        if self.msg_type == "GABIN":
            f = pygame.font.SysFont("arial", 100, bold=True)
            t = f.render("GABIN!!", True, (255, 220, 0))
            self.screen.blit(t, (SCREEN_WIDTH//2 - t.get_width()//2 + ox, 300 + oy))

    def handle_click(self, pos):
        if self.state == "INTRO":
            self.play_sound("PIKON")
            self.state = "SPIN"
        
        elif self.state == "QUIZ" and self.msg_timer == 0 and self.q_idx < len(self.q_list):
            base_y = 320
            for i in range(3):
                rect = pygame.Rect(SCREEN_WIDTH//2 - 200, base_y + i*90, 400, 70)
                if rect.collidepoint(pos):
                    self.clicked_btn = i
                    if i == self.q_list[self.q_idx]["ans"]:
                        self.correct_answer()
                    else:
                        self.wrong_answer()

    def correct_answer(self):
        self.streak += 1
        if self.streak >= 3:
            # GABIN! (派手)
            self.msg_type = "GABIN"
            self.play_sound("GABIN")
            self.shake = 20       # 揺れ
            self.flash_alpha = 150
            self.flash_color = (255, 255, 0) # 黄色フラッシュ
            self.msg_timer = 90
        else:
            # 通常正解 (上品)
            self.msg_type = "PIKON"
            self.play_sound("PIKON")
            self.shake = 0        # 揺らさない
            self.flash_alpha = 0  # 光らせない
            self.msg_timer = 40   # サクサク次へ

    def wrong_answer(self):
        self.streak = 0
        self.msg_type = "SHOBON"
        self.play_sound("SHOBON")
        self.shake = 10       # 少しだけ揺れる
        self.flash_alpha = 100
        self.flash_color = (255, 0, 0) # 赤フラッシュ
        self.msg_timer = 60