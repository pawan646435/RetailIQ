import matplotlib.pyplot as plt
import pandas as pd


def save_eda_charts(df: pd.DataFrame, output_dir: str = "reports/figures") -> list[str]:
    """Save a small set of static EDA charts for documentation and notebook use."""
    from pathlib import Path
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    saved = []
    monthly = df.groupby("month_year", as_index=False).sales.sum()
    fig, ax = plt.subplots(figsize=(11, 4)); ax.plot(monthly.month_year, monthly.sales, linewidth=2)
    ax.set(title="Monthly Revenue", xlabel="Month", ylabel="Sales"); ax.grid(alpha=.2); fig.tight_layout()
    p = out / "monthly_revenue.png"; fig.savefig(p, dpi=160); plt.close(fig); saved.append(str(p))
    cats = df.groupby("category").profit.sum().sort_values()
    fig, ax = plt.subplots(figsize=(8, 4)); cats.plot(kind="barh", ax=ax)
    ax.set(title="Profit by Category", xlabel="Profit", ylabel="Category"); fig.tight_layout()
    p = out / "profit_by_category.png"; fig.savefig(p, dpi=160); plt.close(fig); saved.append(str(p))
    return saved
