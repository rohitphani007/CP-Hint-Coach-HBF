# CP Hint Coach

A hint coach for competitive programming that runs on your own computer. You paste a problem and whatever you have tried so far, and it gives you four hints that get more revealing one step at a time. The idea is to get you unstuck without handing you the solution.

It uses an open-weight model through Ollama, so hint generation does not need a cloud API or an account.

Built for the Hacktoberfest Week 2 Dev challenge (theme: Side Hustle).

---

## The problem

When you are stuck on a Codeforces, LeetCode or CodeChef problem, there are usually only two options. You stay stuck for an hour, or you open the editorial (or paste the problem into a chatbot) and see the whole solution. The first costs you momentum and the second costs you the practice, because the part where you work out the idea is the part that makes you better.

CP Hint Coach sits in between. It gives you the smallest nudge first and only goes deeper when you ask.

---

## How it works

1. You paste the problem statement, optionally describe your approach or paste your code, and pick a language.
2. The app sends this to a local model through Ollama in a single request.
3. The model returns four hints as JSON.
4. The app hides all four. You reveal them one at a time, and each button only appears after the previous hint.

The four levels:

| Level | Name | What it gives you |
|-------|------|-------------------|
| 1 | Nudge | One question about a property of the problem, with no algorithm or data structure named |
| 2 | Key observation | The core insight, without saying how to implement it |
| 3 | Approach | The strategy in plain English, now allowed to name the data structure, with no code |
| 4 | Code skeleton | Function signatures and loop structure in your chosen language, with the main logic left blank |

---

## Why an open model

**Many small requests.** A practice session is not one question. You ask, unlock a hint, try something, ask again. Running the model locally means there is no per-request fee, so this kind of heavy back-and-forth costs nothing beyond your own computer's time and power.

**Your code stays on your machine.** After the model is downloaded, hint generation works with no internet connection, and your attempts are not sent to any server. The one exception is the optional Codeforces lookup, which needs the internet and sends only the handle you type.

**You control the behavior.** How the coach behaves lives in `prompts.py`, and the model is one line in `coach.py`. You can change how much each hint reveals, or swap in a different model and compare, without touching anything else.

---

## Features

- Four-level hint ladder, revealed one level at a time
- Code skeleton in Python, C++, Java, JavaScript, Go, Rust or Kotlin
- Optional Codeforces lookup: enter a handle to list problems you recently submitted with a non-accepted verdict (wrong answer, time limit exceeded, memory limit exceeded, runtime error or compilation error)
- Simple Streamlit interface

---

## Getting started

### What you need

- Python 3.10 or newer
- [Ollama](https://ollama.com), installed and running
- A couple of GB of free disk space for the model

### Setup

1. Pull the model:

   ```
   ollama pull qwen2.5-coder:3b
   ```

2. Clone this repository:

   ```
   git clone https://github.com/rohitphani007/CP-Hint-Coach-HBF.git
   cd CP-Hint-Coach-HBF
   ```

3. Create and activate a virtual environment:

   ```
   python -m venv venv
   ```

   On Windows:

   ```
   venv\Scripts\activate
   ```

   On macOS or Linux:

   ```
   source venv/bin/activate
   ```

4. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

5. Start the app:

   ```
   streamlit run app.py
   ```

It opens in your browser. The first hint request can take a while because the model has to load, and generation on a CPU takes tens of seconds.

### Using a different model

Open `coach.py` and change the `MODEL` line at the top, then pull that model with `ollama pull <name>`. Larger models usually give more reliable hints but are slower.

---

## Known limitations

- **Nothing checks that a hint stays within its level.** The rules (no code before level 4, no algorithm name in level 1) are instructions in the prompt, and a small model sometimes ignores them, most often at level 4. The JSON output format only guarantees the structure of the reply, not what the hints say.
- **Hints can be wrong.** A 3B model can sound confident and still point the wrong way, especially on harder problems. Treat the hints as suggestions and not as truth.
- **All four hints are generated at once**, even though you only see them one at a time.
- **The coach does not judge your approach.** Your attempt is passed to the model as context, but the app does not tell you whether you are on the right track.
- **The Codeforces lookup only lists problems.** It checks your latest 40 submissions, shows up to 10 different problems, and you still paste the statement yourself.

---

## Tech stack

- Inference: [Ollama](https://ollama.com)
- Model: `qwen2.5-coder:3b`, an open-weight model. Ollama lists it under the Qwen Research License, so read those terms before using it commercially.
- Interface: [Streamlit](https://streamlit.io)
- Codeforces data: the public Codeforces API

## Project files

| File | Purpose |
|------|---------|
| `app.py` | Streamlit interface and hint unlocking |
| `coach.py` | Sends the request to Ollama and parses the reply |
| `prompts.py` | The system prompt that defines the coach and the four levels |
| `codeforces.py` | Fetches recent non-accepted submissions for a handle |

---

## License

MIT