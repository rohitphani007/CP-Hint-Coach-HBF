# CP Hint Coach

A local, open-source Socratic coding coach for competitive programmers and software engineers practicing algorithmic problem solving.

Instead of spoiling full solutions or leaving you completely stuck, **CP Hint Coach** provides a graduated 4-tier hint ladder that gives just enough guidance to get you unstuck.

---

## The Problem

When practicing on platforms like LeetCode, Codeforces, or CodeChef, developers usually face two extremes when stuck:
1. **Stay stuck** for hours and lose momentum.
2. **Read the editorial or paste into ChatGPT**, getting the full solution immediately—which defeats the purpose of practice and hurts retention.

CP Hint Coach solves this with progressive hint revelation.

---

## The 4-Tier Hint Ladder

1. **Hint 1 — Nudge**: A single focused question prompting you what to think about without mentioning any algorithms or data structures.
2. **Hint 2 — Key Observation**: The underlying structural or mathematical insight of the problem.
3. **Hint 3 — Approach**: The strategy and data structures described in plain English (no code).
4. **Hint 4 — Code Skeleton**: A scaffold/pseudocode in your preferred programming language with key logic left as blanks.

---

## Why Open-Source AI Matters

This project was built for the **Hacktoberfest Week 2 Dev Challenge ("Side Hustle")**. Here is why open innovation and local models are the core reason this product works:

### 1. Zero-Cost Unit Economics
A typical 45-minute practice session involves dozens of micro-interactions ("Is this edge case covered?", "What if I sort?", "Unlock Hint 1", "Unlock Hint 2"). On commercial cloud APIs (like GPT-4o), this burns tokens rapidly, making an affordable subscription model financially unviable. With local open-weight models (`qwen2.5-coder:3b`), inference costs **$0.00**.

### 2. 100% Offline & Private
Contest preparation and coding interviews often happen in classrooms, during transit, or offline. CP Hint Coach runs completely on-device via Ollama, requiring zero internet connectivity once the model weights are downloaded.

### 3. Open Model Specialization
Rather than using generic closed models that are prone to immediately revealing answers, we utilize `qwen2.5-coder:3b`, an open-weight model specialized in code and algorithmic reasoning, guided by strict JSON-constrained decoding.

---

## Features

- **Progressive Hint Revelation**: Hints are unlocked sequentially—you only see the next hint when you explicitly choose to go deeper.
- **Language Support**: Tailor Hint 4's skeleton to Python, C++, Java, JavaScript, Go, Rust, or Kotlin.
- **Codeforces Integration**: Enter any Codeforces handle to automatically fetch problems you recently submitted with non-accepted verdicts (Wrong Answer, Time Limit Exceeded, etc.).
- **Minimal, Distraction-Free UI**: Clean interface built with Streamlit.

---

## Getting Started

### Prerequisites

1. **Install Ollama**: Download from [ollama.com](https://ollama.com).
2. **Pull the Model**:
   ```bash
   ollama pull qwen2.5-coder:3b
   ```

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/cp-hint-coach.git
   cd cp-hint-coach
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

---

## Tech Stack

- **Inference Engine**: [Ollama](https://ollama.com)
- **Model**: `qwen2.5-coder:3b` (Open-weight, Apache 2.0)
- **Frontend / App Framework**: [Streamlit](https://streamlit.io)
- **Platform Integration**: Codeforces Public REST API

---

## License

MIT License.
