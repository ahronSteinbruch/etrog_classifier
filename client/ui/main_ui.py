from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, StreamingResponse
import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from data_display import DataDisplay

DB_PATH = "etrog_grades.db"
display = DataDisplay()

app = FastAPI()

def make_chart(kind: str = "totals"):
    df = display.get_grades_df(DB_PATH)
    if df is None or df.empty:
        raise ValueError("DB is empty or missing 'grades' table.")

    plt.clf()
    if kind == "totals":
        display.plot_variety_totals(df)
    elif kind == "grouped":
        display.plot_variety_grade_groups(df)
    elif kind == "stacked":
        display.plot_variety_grade_stacked(df)
    elif kind == "pies":
        display.plot_variety_grade_pies(df, top_n=9, ncols=3, donut=False, show_legend=True)
    else:
        display.plot_variety_totals(df)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return buf

@app.get("/", response_class=HTMLResponse)
def home():
    # טופס בחירה + כפתור
    return """
    <html>
      <head><title>Etrog Graph UI</title></head>
      <body style="font-family: Arial; text-align:center; margin:40px;">
        <h1>📊 Etrog Graph UI</h1>
        <form action="/display" method="post">
          <label>בחר גרף:</label>
          <select name="kind">
            <option value="totals">Totals (bar)</option>
            <option value="grouped">Grouped (A..E)</option>
            <option value="stacked">Stacked (A..E)</option>
            <option value="pies">Pies</option>
          </select>
          <button type="submit">DISPLAY</button>
        </form>
      </body>
    </html>
    """

@app.post("/display")
def display_chart(kind: str = Form("totals")):
    buf = make_chart(kind)
    return StreamingResponse(buf, media_type="image/png")

# להרצה ישירה ב-PyCharm
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_ui:app", host="127.0.0.1", port=8000, reload=False)
