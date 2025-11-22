# src/config.py
import os

# 画面設定
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650
FPS = 60

# パス設定（assetsフォルダの場所）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMG_DIR = os.path.join(ASSETS_DIR, 'images')
SND_DIR = os.path.join(ASSETS_DIR, 'sounds')

# 色設定
BG_COLOR = (20, 20, 35)
ACCENT_COLOR = (88, 204, 2)    # Duolingo Green
FAIL_COLOR = (235, 75, 75)
LIGHTNING_COLOR = (255, 255, 0)
TEXT_COLOR = (220, 220, 220)
HINT_COLOR = (150, 150, 170)