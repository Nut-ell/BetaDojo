# src/questions_data.py (エラー原因の構文を\Boxに完全に置き換えたもの)
# Raw strings (r"...") for LaTeX

QUESTIONS_LIST = [
    {
        "id": "q1",
        "category": "Definition (Deviation)",
        "hint": "Sum of squared deviations of x",
        "q": r"\hat{\beta} = \frac{S_{xy}}{\Box}", 
        "opts": [r"S_{xx}", r"S_{yy}", r"\sqrt{S_{xx}}"], 
        "ans": 0
    },
    {
        "id": "q2",
        "category": "Definition (Sigma Notation)",
        "hint": "Variance part (Denominator)",
        "q": r"\hat{\beta} = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\Box}", 
        "opts": [r"\sum (x_i - \bar{x})^2", r"\sum (y_i - \bar{y})^2", r"\sum (x_i - \bar{x})"], 
        "ans": 0
    },
    {
        "id": "q3",
        "category": "Expansion: Numerator",
        "hint": "Sum of products minus correction term",
        "q": r"\sum (x_i - \bar{x})(y_i - \bar{y}) = \sum x_i y_i - \Box", 
        "opts": [r"n \bar{x} \bar{y}", r"\bar{x} \bar{y}", r"\sum x_i \sum y_i"], 
        "ans": 0
    },
    {
        "id": "q4",
        "category": "Expansion: Denominator",
        "hint": "Sum of squares minus correction term",
        "q": r"S_{xx} = \sum x_i^2 - \Box", 
        "opts": [r"n \bar{x}^2", r"(\sum x_i)^2", r"\bar{x}^2"], 
        "ans": 0
    },
    {
        "id": "q5",
        "category": "Computational Form",
        "hint": "Final formula for calculation",
        "q": r"\hat{\beta} = \frac{\sum x_i y_i - n\bar{x}\bar{y}}{\Box}", 
        "opts": [r"\sum x_i^2 - n\bar{x}^2", r"\sum y_i^2 - n\bar{y}^2", r"S_{xy}^2"], 
        "ans": 0
    },
    {
        "id": "q6",
        "category": "Relation to Correlation",
        "hint": "Ratio of standard deviations",
        "q": r"\hat{\beta} = r_{xy} \cdot \frac{\Box}{S_x}", 
        "opts": [r"S_y", r"S_x", r"\sigma_y"], 
        "ans": 0
    },
    {
        "id": "q7",
        "category": "Intercept",
        "hint": "Regression line passes through means",
        "q": r"\hat{\alpha} = \bar{y} - \Box", 
        "opts": [r"\hat{\beta} \bar{x}", r"\bar{x}", r"\beta_0"], 
        "ans": 0
    },
    {
        "id": "q8",
        "category": "Matrix: Normal Equation",
        "hint": "Before inverting the matrix",
        "q": r"(\mathbf{X}^T \mathbf{X}) \hat{\beta} = \Box", 
        "opts": [r"\mathbf{X}^T \mathbf{y}", r"\mathbf{y}^T \mathbf{X}", r"\mathbf{X}^{-1} \mathbf{y}"], 
        "ans": 0
    },
    {
        "id": "q9",
        "category": "Matrix: Solution",
        "hint": "The 'Variance' part in matrix form",
        "q": r"\hat{\beta} = (\Box)^{-1} \mathbf{X}^T \mathbf{y}", 
        "opts": [r"\mathbf{X}^T \mathbf{X}", r"\mathbf{X} \mathbf{X}^T", r"\mathbf{X}^T \mathbf{y}"], 
        "ans": 0
    },
    {
        "id": "q10",
        "category": "Residual Property",
        "hint": "Orthogonality: x and e are uncorrelated",
        "q": r"\sum_{i=1}^n x_i \hat{e}_i = \Box", 
        "opts": [r"0", r"1", r"\sigma^2"], 
        "ans": 0
    },
    {
        "id": "q11",
        "category": "Variance of Beta",
        "hint": "Wider x range reduces error",
        "q": r"V(\hat{\beta}) = \frac{\sigma^2}{\Box}", 
        "opts": [r"S_{xx}", r"S_{xy}", r"n"], 
        "ans": 0
    },
    {
        "id": "q12",
        "category": "Gauss-Markov Theorem",
        "hint": "BLUE: Best Linear Unbiased ...",
        "q": r"\text{Var}(\hat{\beta}_{OLS}) \le \text{Var}(\tilde{\beta}_{\text{other}})", 
        "opts": [r"\text{Estimator}", r"\text{Model}", r"\text{Error}"], 
        "ans": 0
    }
]