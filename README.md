
Title: Chessboard & Rice Challenge


Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# ♟️ Chess & Rice — Gradio App

[![Gradio](https://img.shields.io/badge/Gradio-%E2%9C%85-1f8feb)](#)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](#)

An interactive visualization of the **classic “chessboard and rice grains” exponential growth problem**,  
built with **Gradio** and **Plotly**, and ready for deployment on **Hugging Face Spaces** 🚀

---

## 🎯 What It Does

- Visualizes how rice grains double on each chess square (1 → 64).  
- Interactive **chessboard heatmap** of grains (log scale).  
- **Exponential growth** and **cumulative total** line charts.  
- Real-world **comparisons** (vs. world population, sand grains, etc.).  
- Dynamic **stats panel** that updates as you move the slider.

---

## 📂 Project Structure


---

## ⚙️ Run Locally

```bash
# 1️⃣ Create virtual environment
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows

# 2️⃣ Install dependencies
pip install -r requirements.txt

# 3️⃣ Run the app
python app.py
