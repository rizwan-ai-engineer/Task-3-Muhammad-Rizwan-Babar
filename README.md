

https://github.com/user-attachments/assets/525ccbb4-9b26-4945-93a0-27901acc5d85



https://github.com/user-attachments/assets/aefba898-1d60-4e93-ae2d-fa781e70e3c3

# 🎯 Tech Stack Recommender
**DecodeLabs Industrial Training Kit · AI Project 3 · Batch 2026**

A content-based filtering recommendation engine that maps user skills to job roles using TF-IDF vectorization and Cosine Similarity — built with zero external ML libraries.

---

## 📁 Folder Structure

```
tech_stack_recommender/
│
├── data/
│   └── raw_skills.csv          # Dataset: 15 job roles × skill tags
│
├── core/
│   ├── __init__.py
│   └── recommender.py          # Engine: TF-IDF + Cosine Similarity
│
├── ui/
│   └── app.py                  # Streamlit web interface
│
├── main.py                     # CLI entry point
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

```bash
# 1. Navigate to project folder
cd tech_stack_recommender

# 2. (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Run

### Streamlit Web App (recommended)
```bash
streamlit run ui/app.py
```
Opens at `http://localhost:8501`

### CLI Mode
```bash
python main.py
```

---

## 🧠 How It Works

### Architecture: IPO Model
```
INPUT (User Skills) → PROCESS (TF-IDF + Cosine) → OUTPUT (Top-N Roles)
```

### 4-Step Pipeline
| Step | Name | Description |
|------|------|-------------|
| 1 | Ingestion | Capture ≥3 user skills; build shared vocabulary |
| 2 | Scoring | Compute TF-IDF vectors; calculate cosine similarity |
| 3 | Sorting | Rank all roles by similarity score (descending) |
| 4 | Filtering | Return only Top-N results |

### Key Algorithms

**TF-IDF Weighting**
```
TF(t,d)  = count(t in d) / total_terms(d)
IDF(t)   = log((N+1) / (df(t)+1)) + 1
TF-IDF   = TF × IDF
```

**Cosine Similarity**
```
cos(θ) = (A · B) / (‖A‖ × ‖B‖)
```
- Score 1.0 → perfect alignment
- Score 0.0 → no shared characteristics

---

## 📊 Dataset

`data/raw_skills.csv` — 15 job roles including:
Data Scientist, Backend Developer, Frontend Developer, DevOps Engineer,
Cloud Architect, ML Engineer, Cybersecurity Analyst, Full Stack Developer,
Data Engineer, Mobile Developer, Systems Administrator, AI Research Engineer,
Blockchain Developer, Game Developer, QA Engineer.

To add more roles, simply add rows to `raw_skills.csv`:
```
New Role Name,"skill1,skill2,skill3,skill4,skill5"
```

---

---

*Submitted By: Muhammad Rizwan Babar*
