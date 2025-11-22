# src/game.py
import pygame
import os
import random
from .config import *
from .questions_data import QUESTIONS_LIST

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Beta Blitz")
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.SysFont("arial", 40, bold=True)
        self.font_hint = pygame.font.SysFont("arial", 24, italic=True)

        # アセット読み込み
        self.load_assets()
        
        # ゲーム状態
        self.state = "INTRO"
        self.reset_quiz()

    def load_assets(self):
        # 画像ローダーヘルパー
        def load_img(name):
            path = os.path.join(IMG_DIR, name)
            if not os.path.exists(path):
                print(f"Error: {path} not found. Run setup_assets.py first!")
                return pygame.Surface((100, 100)) # fallback
            return pygame.image.load(path)

        self.img_beta = load_img("beta_large.png")
        self.q_assets = {}
        for q in QUESTIONS_LIST:
            self.q_assets[q["id"]] = {
                "q": load_img(f"{q['id']}_q.png"),
                "opts": [load_img(f"{q['id']}_opt_{i}.png") for i in range(3)]
            }
        
        # 音声
        pygame.mixer.init()
        self.sounds = {}
        for name in ["PIKON", "SHOBON", "GABIN"]:
            path = os.path.join(SND_DIR, f"{name}.wav")
            if os.path.exists(path):
                self.sounds[name] = pygame.mixer.Sound(path)
            else:
                self.sounds[name] = None

    def reset_quiz(self):
        self.spin = 0
        self.scale = 1.0
        self.q_list = list(QUESTIONS_LIST)
        random.shuffle(self.q_list)
        self.q_idx = 0
        self.streak = 0
        self.shake = 0
        self.flash = 0
        self.msg_timer = 0
        self.msg_type = None

    def play_sound(self, name):
        if self.sounds.get(name):
            self.sounds[name].play()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
            
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

    def update(self):
        if self.shake > 0: self.shake -= 1
        if self.flash > 0: self.flash -= 1
        if self.msg_timer > 0:
            self.msg_timer -= 1
            if self.msg_timer == 0 and self.state == "QUIZ":
                self.q_idx += 1
                self.msg_type = None

        if self.state == "SPIN":
            self.spin += 40
            self.scale -= 0.02
            if self.scale <= 0:
                self.state = "QUIZ"
                self.scale = 0

    def draw(self):
        ox = random.randint(-self.shake, self.shake) if self.shake else 0
        oy = random.randint(-self.shake, self.shake) if self.shake else 0
        
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        surf.fill(BG_COLOR)

        if self.state == "INTRO":
            rect = self.img_beta.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            surf.blit(self.img_beta, rect)
            if pygame.time.get_ticks() % 1000 < 500:
                txt = self.font_title.render("CLICK TO START", True, (100, 100, 100))
                surf.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, SCREEN_HEIGHT - 100))

        elif self.state == "SPIN":
            w, h = int(self.img_beta.get_width()*self.scale), int(self.img_beta.get_height()*self.scale)
            if w > 0:
                scaled = pygame.transform.scale(self.img_beta, (w, h))
                rot = pygame.transform.rotate(scaled, self.spin)
                surf.blit(rot, rot.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))

        elif self.state == "QUIZ":
            if self.q_idx >= len(self.q_list):
                txt = self.font_title.render("ALL CLEARED!", True, LIGHTNING_COLOR)
                surf.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, SCREEN_HEIGHT//2))
            else:
                q_data = self.q_list[self.q_idx]
                assets = self.q_assets[q_data["id"]]
                
                # タイトル
                t_txt = self.font_title.render(q_data["category"], True, ACCENT_COLOR)
                surf.blit(t_txt, (SCREEN_WIDTH//2 - t_txt.get_width()//2, 50))
                
                # 問題画像
                q_rect = assets["q"].get_rect(center=(SCREEN_WIDTH//2, 180))
                surf.blit(assets["q"], q_rect)

                # ヒント
                h_txt = self.font_hint.render(f"Hint: {q_data['hint']}", True, HINT_COLOR)
                surf.blit(h_txt, (SCREEN_WIDTH//2 - h_txt.get_width()//2, 250))

                # 選択肢
                mouse = pygame.mouse.get_pos()
                base_y = 340
                for i in range(3):
                    rect = pygame.Rect(SCREEN_WIDTH//2 - 200, base_y + i*85, 400, 70)
                    col = (230, 230, 230)
                    if rect.collidepoint((mouse[0]-ox, mouse[1]-oy)): col = (255, 255, 255)
                    
                    pygame.draw.rect(surf, col, rect, border_radius=15)
                    pygame.draw.rect(surf, (100,100,120), rect, 4, border_radius=15)
                    
                    opt_img = assets["opts"][i]
                    surf.blit(opt_img, opt_img.get_rect(center=rect.center))

        # フィードバック
        if self.msg_type == "GABIN":
            if self.flash % 4 < 2: surf.fill(LIGHTNING_COLOR, special_flags=pygame.BLEND_ADD)
            f = pygame.font.SysFont("arial", 120, bold=True)
            t = f.render("GABIN!!!", True, (255, 50, 50))
            surf.blit(t, (SCREEN_WIDTH//2 - t.get_width()//2 + ox*2, 300 + oy*2))
        elif self.msg_type == "PIKON":
            pygame.draw.rect(surf, ACCENT_COLOR, (0,0,SCREEN_WIDTH,SCREEN_HEIGHT), 15)
        elif self.msg_type == "SHOBON":
            t = self.font_title.render("NO...", True, FAIL_COLOR)
            surf.blit(t, (SCREEN_WIDTH//2 - t.get_width()//2 + ox, 550 + oy))

        self.screen.blit(surf, (ox, oy))

    def handle_click(self, pos):
        if self.state == "INTRO":
            self.play_sound("PIKON")
            self.state = "SPIN"
        elif self.state == "QUIZ" and self.msg_timer == 0 and self.q_idx < len(self.q_list):
            base_y = 340
            for i in range(3):
                rect = pygame.Rect(SCREEN_WIDTH//2 - 200, base_y + i*85, 400, 70)
                if rect.collidepoint(pos):
                    if i == self.q_list[self.q_idx]["ans"]:
                        self.streak += 1
                        if self.streak >= 3:
                            self.msg_type = "GABIN"
                            self.play_sound("GABIN")
                            self.shake, self.flash, self.msg_timer = 40, 60, 120
                        else:
                            self.msg_type = "PIKON"
                            self.play_sound("PIKON")
                            self.msg_timer = 45
                    else:
                        self.streak = 0
                        self.msg_type = "SHOBON"
                        self.play_sound("SHOBON")
                        self.shake, self.msg_timer = 15, 45