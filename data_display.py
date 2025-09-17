import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, AutoMinorLocator, FuncFormatter


class DataDisplay:
    def get_grades_df(self, db_path: str = "etrog_grades.db") -> pd.DataFrame:
        """Return the whole 'grades' table as a pandas DataFrame (ordered by variety)."""
        with sqlite3.connect(db_path) as conn:
            exists = conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name='grades'"
            ).fetchone()
            if not exists:
                return pd.DataFrame(columns=["variety", "A", "B", "C", "D", "E", "updated_at"])

            return pd.read_sql_query(
                """
                SELECT variety, A, B, C, D, E, updated_at
                FROM grades
                ORDER BY variety COLLATE NOCASE
                """,
                conn,
            )


    def plot_variety_grade_groups(self, df):
        """
        Draws a clustered column graph: For each variety, A..E are displayed side by side.
        Expects columns: variety, A, B, C, D, E
        """
        if df is None or df.empty:
            print("Empty DataFrame")
            return

        for col in ["variety", "A", "B", "C", "D", "E"]:
            if col not in df.columns:
                raise ValueError(f"Missing column: {col}")

        data = df.copy()
        data["total"] = data[["A", "B", "C", "D", "E"]].sum(axis=1)
        data = data.sort_values("total", ascending=False)

        grades = ["A", "B", "C", "D", "E"]
        x = np.arange(len(data))
        width = 0.12

        plt.figure(figsize=(12, 7))
        for i, g in enumerate(grades):
            plt.bar(x + i * width - 2 * width, data[g].to_numpy(), width, label=g)

        plt.xticks(x, data["variety"], rotation=45, ha="right")
        plt.xlabel("variety")
        plt.ylabel("Number of shows")
        plt.title("Occurrences in each grade (A..E) — grouped columns")
        plt.legend(title="score")
        plt.tight_layout()
        plt.show()


    def plot_variety_grade_pies(self, df, top_n=9, ncols=3, donut=False, show_legend=True):
        """
        Pie/donut charts for each variety (A..E) + side legend for colors.
        Expect columns: variety, A, B, C, D, E
        """
        if df is None or df.empty:
            print("Empty DataFrame");
            return
        for col in ["variety", "A", "B", "C", "D", "E"]:
            if col not in df.columns:
                raise ValueError(f"Missing column: {col}")

        data = df.copy()
        data["total"] = data[["A", "B", "C", "D", "E"]].sum(axis=1)
        data = data.sort_values("total", ascending=False).head(top_n)

        grades = ["A", "B", "C", "D", "E"]
        k = len(data)
        nrows = (k + ncols - 1) // ncols
        fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols + (2 if show_legend else 0), 3 * nrows))
        axes = (axes.ravel() if hasattr(axes, "ravel") else [axes])

        wedgeprops = {"width": 0.5} if donut else None
        fmt = lambda p: f"{p:.0f}%" if p > 0 else ""

        legend_handles = None
        for idx, (ax, (_, row)) in enumerate(zip(axes, data.iterrows())):
            vals = [float(row[g]) for g in grades]
            if sum(vals) == 0:
                ax.text(0.5, 0.5, "No data", ha="center", va="center");
                ax.axis("off");
                continue
            wedges, _, _ = ax.pie(vals, labels=grades, startangle=90, autopct=fmt, wedgeprops=wedgeprops)
            if idx == 0 and show_legend:
                legend_handles = wedges
            ax.set_title(str(row["variety"]));
            ax.axis("equal")

        for ax in axes[k:]:
            ax.axis("off")

        if show_legend and legend_handles:
            fig.legend(legend_handles, grades, title="score", loc="center left", bbox_to_anchor=(1.02, 0.5))
            fig.subplots_adjust(right=0.85)

        plt.tight_layout()
        plt.show()

    def plot_variety_grade_stacked(self, df):
        """Stacked bars: For each strain, A..E are shown as stacked segments."""
        if df is None or df.empty:
            print("Empty DataFrame");
            return
        for c in ["variety", "A", "B", "C", "D", "E"]:
            if c not in df.columns:
                raise ValueError(f"Missing column: {c}")

        data = df.copy()
        grades = ["A", "B", "C", "D", "E"]

        plt.figure(figsize=(12, 7))
        bottom = np.zeros(len(data))
        for g in grades:
            vals = data[g].to_numpy()
            plt.bar(data["variety"], vals, bottom=bottom, label=g)
            bottom += vals

        plt.xticks(rotation=45, ha="right")
        plt.xlabel("variety")
        plt.ylabel("count")
        plt.title("Counts in each grade (A..E) by variety — stacked")
        plt.legend(title="grade")
        plt.tight_layout()
        plt.show()


    def plot_variety_totals(self, df):
        """
        A vertical bar chart summarizing how many etrogs there are of each variety (sum of A..E),
        with denser Y-axis ticks and diagonal X labels to avoid overlap.
        Expects columns: variety, A, B, C, D, E
        """
        if df is None or df.empty:
            print("Empty DataFrame");
            return
        for c in ["variety", "A", "B", "C", "D", "E"]:
            if c not in df.columns:
                raise ValueError(f"Missing column: {c}")

        data = df.copy()
        data["total"] = data[["A", "B", "C", "D", "E"]].sum(axis=1)
        data = data.sort_values("total", ascending=False)

        fig_h = 6
        fig_w = max(8, 0.5 * len(data) + 4)
        fig, ax = plt.subplots(figsize=(fig_w, fig_h))

        ax.bar(data["variety"], data["total"])

        # Y-axis ticks (more numbers)
        ax.set_ylim(0, max(1, data["total"].max() * 1.10))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=12, integer=True))
        ax.yaxis.set_minor_locator(AutoMinorLocator(2))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))

        # Diagonal X labels + spacing so they don't collide or get cut off
        angle = 60
        ax.set_xticks(range(len(data)))
        ax.set_xticklabels(list(data["variety"]), rotation=angle, ha="right", rotation_mode="anchor")
        ax.tick_params(axis="x", which="major", pad=8)
        ax.margins(x=0.02)

        # Styling
        ax.grid(True, axis="y", which="major", linestyle=":", alpha=0.6)
        ax.grid(True, axis="y", which="minor", linestyle=":", alpha=0.3)
        ax.set_xlabel("זן")
        ax.set_ylabel("סה\"כ אתרוגים")
        ax.set_title("סה״כ אתרוגים לכל זן")

        # Extra bottom margin so long labels aren't clipped
        plt.subplots_adjust(bottom=0.28)
        plt.tight_layout()
        plt.show()
