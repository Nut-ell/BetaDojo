# fix_it.py (最終決戦版)
import os

# setup_assets.py の中身
# 修正点: Q12の \le -> \leq, \text{other} -> \mathrm{other}
new_code = r"""import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav

# --- 設定: パスを直接指定 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, 'assets', 'images')
SND_DIR = os.path.join(BASE_DIR, 'assets', 'sounds')

# --- 設定: 問題データをここに直接埋め込む ---
QUESTIONS_LIST = [
    {
        "id": "q1",
        "category": "Definition (Deviation)",
        "hint": "Sum of squared deviations of x",
        "q": r"\hat{\beta} = \frac{S_{xy}}{\mathbf{?}}", 
        "opts": [r"S_{xx}", r"S_{yy}", r"\sqrt{S_{xx}}"], 
        "ans": 0
    },
    {
        "id": "q2",
        "category": "Definition (Sigma Notation)",
        "hint": "Variance part (Denominator)",
        "q": r"\hat{\beta} = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\mathbf{?}}", 
        "opts": [r"\sum (x_i - \bar{x})^2", r"\sum (y_i - \bar{y})^2", r"\sum (x_i - \bar{x})"], 
        "ans": 0
    },
    {
        "id": "q3",
        "category": "Expansion: Numerator",
        "hint": "Sum of products minus correction term",
        "q": r"\sum (x_i - \bar{x})(y_i - \bar{y}) = \sum x_i y_i - \mathbf{?}", 
        "opts": [r"n \bar{x} \bar{y}", r"\bar{x} \bar{y}", r"\sum x_i \sum y_i"], 
        "ans": 0
    },
    {
        "id": "q4",
        "category": "Expansion: Denominator",
        "hint": "Sum of squares minus correction term",
        "q": r"S_{xx} = \sum x_i^2 - \mathbf{?}", 
        "opts": [r"n \bar{x}^2", r"(\sum x_i)^2", r"\bar{x}^2"], 
        "ans": 0
    },
    {
        "id": "q5",
        "category": "Computational Form",
        "hint": "Final formula for calculation",
        "q": r"\hat{\beta} = \frac{\sum x_i y_i - n\bar{x}\bar{y}}{\mathbf{?}}", 
        "opts": [r"\sum x_i^2 - n\bar{x}^2", r"\sum y_i^2 - n\bar{y}^2", r"S_{xy}^2"], 
        "ans": 0
    },
    {
        "id": "q6",
        "category": "Relation to Correlation",
        "hint": "Ratio of standard deviations",
        "q": r"\hat{\beta} = r_{xy} \cdot \frac{\mathbf{?}}{S_x}", 
        "opts": [r"S_y", r"S_x", r"\sigma_y"], 
        "ans": 0
    },
    {
        "id": "q7",
        "category": "Intercept",
        "hint": "Regression line passes through means",
        "q": r"\hat{\alpha} = \bar{y} - \mathbf{?}", 
        "opts": [r"\hat{\beta} \bar{x}", r"\bar{x}", r"\beta_0"], 
        "ans": 0
    },
    {
        "id": "q8",
        "category": "Matrix: Normal Equation",
        "hint": "Before inverting the matrix",
        "q": r"(\mathbf{X}^T \mathbf{X}) \hat{\beta} = \mathbf{?}", 
        "opts": [r"\mathbf{X}^T \mathbf{y}", r"\mathbf{y}^T \mathbf{X}", r"\mathbf{X}^{-1} \mathbf{y}"], 
        "ans": 0
    },
    {
        "id": "q9",
        "category": "Matrix: Solution",
        "hint": "The 'Variance' part in matrix form",
        "q": r"\hat{\beta} = (\mathbf{?})^{-1} \mathbf{X}^T \mathbf{y}", 
        "opts": [r"\mathbf{X}^T \mathbf{X}", r"\mathbf{X} \mathbf{X}^T", r"\mathbf{X}^T \mathbf{y}"], 
        "ans": 0
    },
    {
        "id": "q10",
        "category": "Residual Property",
        "hint": "Orthogonality: x and e are uncorrelated",
        "q": r"\sum_{i=1}^n x_i \hat{e}_i = \mathbf{?}", 
        "opts": [r"0", r"1", r"\sigma^2"], 
        "ans": 0
    },
    {
        "id": "q11",
        "category": "Variance of Beta",
        "hint": "Wider x range reduces error",
        "q": r"V(\hat{\beta}) = \frac{\sigma^2}{\mathbf{?}}", 
        "opts": [r"S_{xx}", r"S_{xy}", r"n"], 
        "ans": 0
    },
    {
        "id": "q12",
        "category": "Gauss-Markov Theorem",
        "hint": "BLUE: Best Linear Unbiased ...",
        # 修正: \le -> \leq, \text -> \mathrm
        "q": r"\mathrm{Var}(\hat{\beta}_{OLS}) \leq \mathrm{Var}(\tilde{\beta}_{\mathrm{other}})", 
        "opts": [r"\mathrm{Estimator}", r"\mathrm{Model}", r"\mathrm{Error}"], 
        "ans": 0
    }
]

# --- ヘルパー関数 ---
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# --- 画像生成 ---
def save_latex_img(text, filename, fontsize=24, color="white"):
    path = os.path.join(IMG_DIR, filename)
    dpi = 100
    fig = plt.figure(figsize=(8, 2.0), dpi=dpi)
    fig.patch.set_alpha(0)
    
    # 唯一の安全な数式描画
    plt.text(0.5, 0.5, f"${text}$", fontsize=fontsize, ha='center', va='center', color=color)
    
    plt.axis('off')
    plt.savefig(path, format="png", bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)
    print(f"Saved: {filename}")

# --- 音声生成 ---
def save_wave(filename, type):
    rate = 44100
    if type == "GABIN": duration = 1.0 
    else: duration = 0.2
    t = np.linspace(0, duration, int(rate * duration), False)
    
    if type == "PIKON": 
        wave = np.sin(2 * np.pi * 880 * t) * np.exp(-5 * t)
        wave += np.sin(2 * np.pi * 1760 * t) * 0.5 * np.exp(-5 * t)
    elif type == "SHOBON": 
        freqs = np.linspace(300, 50, len(t))
        wave = (2 * (t * freqs % 1) - 1) * 0.5
    elif type == "GABIN": 
        noise = np.random.uniform(-1, 1, len(t))
        bass = np.sin(2 * np.pi * 50 * t)
        wave = (noise * 0.8 + bass * 0.5) * np.exp(-3 * t)
    
    audio = (wave * 32767).astype(np.int16)
    path = os.path.join(SND_DIR, filename)
    wav.write(path, rate, audio)
    print(f"Saved Sound: {filename}")

def main():
    print("--- Generating Assets (Final Fix Mode) ---")
    ensure_dir(IMG_DIR)
    ensure_dir(SND_DIR)

    # 1. Betaタイトル
    save_latex_img(r"\beta", "beta_large.png", fontsize=120, color="#58cc02")

    # 2. 問題画像
    for q in QUESTIONS_LIST:
        save_latex_img(q["q"], f"{q['id']}_q.png", fontsize=26, color="white")
        for i, opt in enumerate(q["opts"]):
            save_latex_img(opt, f"{q['id']}_opt_{i}.png", fontsize=20, color="black")

    # 3. 効果音
    save_wave("PIKON.wav", "PIKON")
    save_wave("SHOBON.wav", "SHOBON")
    save_wave("GABIN.wav", "GABIN")

    print("\n[Done] Assets generated successfully!")
    print("Now run 'python src/main.py'")

if __name__ == "__main__":
    main()
"""

target_file = "setup_assets.py"
with open(target_file, "w", encoding="utf-8") as f:
    f.write(new_code)

print(f"SUCCESS: {target_file} updated. Fixed LaTeX symbols for Q12.")