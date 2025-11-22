# setup_assets.py (High Quality Design)
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav

# --- 設定 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, 'assets', 'images')
SND_DIR = os.path.join(BASE_DIR, 'assets', 'sounds')

# フォント設定: 立体をサンセリフ体っぽくしてモダンに
plt.rcParams['mathtext.fontset'] = 'cm' # Computer Modern (標準的で美しい)

# --- 問題データ (内容は同じ) ---
QUESTIONS_LIST = [
    { "id": "q1", "category": "Definition", "hint": "Sum of squared deviations", "q": r"\hat{\beta} = \frac{S_{xy}}{\mathbf{?}}", "opts": [r"S_{xx}", r"S_{yy}", r"\sqrt{S_{xx}}"], "ans": 0 },
    { "id": "q2", "category": "Sigma Notation", "hint": "Variance part", "q": r"\hat{\beta} = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\mathbf{?}}", "opts": [r"\sum (x_i - \bar{x})^2", r"\sum (y_i - \bar{y})^2", r"\sum (x_i - \bar{x})"], "ans": 0 },
    { "id": "q3", "category": "Numerator", "hint": "Expansion of covariance", "q": r"\sum (x_i - \bar{x})(y_i - \bar{y}) = \sum x_i y_i - \mathbf{?}", "opts": [r"n \bar{x} \bar{y}", r"\bar{x} \bar{y}", r"\sum x_i \sum y_i"], "ans": 0 },
    { "id": "q4", "category": "Denominator", "hint": "Expansion of variance", "q": r"S_{xx} = \sum x_i^2 - \mathbf{?}", "opts": [r"n \bar{x}^2", r"(\sum x_i)^2", r"\bar{x}^2"], "ans": 0 },
    { "id": "q5", "category": "Computational", "hint": "Calculation formula", "q": r"\hat{\beta} = \frac{\sum x_i y_i - n\bar{x}\bar{y}}{\mathbf{?}}", "opts": [r"\sum x_i^2 - n\bar{x}^2", r"\sum y_i^2 - n\bar{y}^2", r"S_{xy}^2"], "ans": 0 },
    { "id": "q6", "category": "Correlation", "hint": "Relation to r", "q": r"\hat{\beta} = r_{xy} \cdot \frac{\mathbf{?}}{S_x}", "opts": [r"S_y", r"S_x", r"\sigma_y"], "ans": 0 },
    { "id": "q7", "category": "Intercept", "hint": "Passing through means", "q": r"\hat{\alpha} = \bar{y} - \mathbf{?}", "opts": [r"\hat{\beta} \bar{x}", r"\bar{x}", r"\beta_0"], "ans": 0 },
    { "id": "q8", "category": "Normal Eq.", "hint": "Matrix form", "q": r"(\mathbf{X}^T \mathbf{X}) \hat{\beta} = \mathbf{?}", "opts": [r"\mathbf{X}^T \mathbf{y}", r"\mathbf{y}^T \mathbf{X}", r"\mathbf{X}^{-1} \mathbf{y}"], "ans": 0 },
    { "id": "q9", "category": "Solution", "hint": "Beta vector", "q": r"\hat{\beta} = (\mathbf{?})^{-1} \mathbf{X}^T \mathbf{y}", "opts": [r"\mathbf{X}^T \mathbf{X}", r"\mathbf{X} \mathbf{X}^T", r"\mathbf{X}^T \mathbf{y}"], "ans": 0 },
    { "id": "q10", "category": "Residuals", "hint": "Orthogonality", "q": r"\sum x_i \hat{e}_i = \mathbf{?}", "opts": [r"0", r"1", r"\sigma^2"], "ans": 0 },
    { "id": "q11", "category": "Variance", "hint": "Accuracy", "q": r"V(\hat{\beta}) = \frac{\sigma^2}{\mathbf{?}}", "opts": [r"S_{xx}", r"S_{xy}", r"n"], "ans": 0 },
    { "id": "q12", "category": "Gauss-Markov", "hint": "BLUE property", "q": r"\mathrm{Var}(\hat{\beta}_{OLS}) \leq \mathrm{Var}(\tilde{\beta}_{\mathrm{other}})", "opts": [r"\mathrm{Estimator}", r"\mathrm{Model}", r"\mathrm{Error}"], "ans": 0 }
]

def ensure_dir(path):
    if not os.path.exists(path): os.makedirs(path)

def save_latex_img(text, filename, fontsize=28, color="white"): # フォントサイズUP
    path = os.path.join(IMG_DIR, filename)
    # DPIを上げてくっきりと
    dpi = 150 
    fig = plt.figure(figsize=(8, 2.2), dpi=dpi)
    fig.patch.set_alpha(0)
    plt.text(0.5, 0.5, f"${text}$", fontsize=fontsize, ha='center', va='center', color=color)
    plt.axis('off')
    plt.savefig(path, format="png", bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)
    print(f"Saved (HQ): {filename}")

def save_wave(filename, type):
    rate = 44100
    if type == "GABIN": duration = 1.5 # 少し長く
    else: duration = 0.2
    t = np.linspace(0, duration, int(rate * duration), False)
    
    if type == "PIKON": 
        # 柔らかい音に
        wave = np.sin(2 * np.pi * 880 * t) * np.exp(-5 * t)
        wave += np.sin(2 * np.pi * 1320 * t) * 0.3 * np.exp(-5 * t)
    elif type == "SHOBON": 
        freqs = np.linspace(300, 100, len(t))
        wave = (np.sin(2 * np.pi * freqs * t)) * 0.5
    elif type == "GABIN": 
        # 少しマイルドだが壮大なノイズ
        noise = np.random.uniform(-0.5, 0.5, len(t))
        bass = np.sin(2 * np.pi * 60 * t)
        mod = np.sin(2 * np.pi * 10 * t) # うねり
        wave = (noise * 0.6 + bass * 0.4) * mod * np.exp(-2 * t)
    
    audio = (wave * 32767).astype(np.int16)
    wav.write(os.path.join(SND_DIR, filename), rate, audio)
    print(f"Saved Sound: {filename}")

def main():
    print("--- Generating Assets (High Quality) ---")
    ensure_dir(IMG_DIR)
    ensure_dir(SND_DIR)
    
    save_latex_img(r"\beta", "beta_large.png", fontsize=150, color="#58cc02")
    for q in QUESTIONS_LIST:
        save_latex_img(q["q"], f"{q['id']}_q.png", fontsize=30, color="white")
        for i, opt in enumerate(q["opts"]):
            save_latex_img(opt, f"{q['id']}_opt_{i}.png", fontsize=24, color="black")
            
    save_wave("PIKON.wav", "PIKON")
    save_wave("SHOBON.wav", "SHOBON")
    save_wave("GABIN.wav", "GABIN")
    print("\n[Done] High quality assets ready.")

if __name__ == "__main__":
    main()