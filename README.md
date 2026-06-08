# 🧠 AI & CS Quiz (Flask + Vanilla JS)

An AI & computer science multiple-choice quiz built with **Python + Flask** on the backend and **plain HTML/CSS/JavaScript** on the frontend.

---

## 🏗 Project Structure

```text
quiz_app/
├── app.py            # Flask backend (routes + scoring logic)
└── templates/
    ├── home.html     # Landing page (Start Quiz)
    └── quiz.html     # Quiz UI + JavaScript logic
```

---

<details>
<summary><strong>⚙ Backend: Flask logic (app.py)</strong></summary>

### Key ideas

- Imports:
  - `Flask` to create the app
  - `render_template` to serve HTML files from `templates/`
  - `request` + `jsonify` to receive JSON from JavaScript and send JSON back.[web:30][web:39]

- Data:
  - `QUIZ_DATA` is a Python list of dictionaries.
  - Each question has: `question`, `options`, `correct` (index), and `explanation`.

- Routes:
  - `@app.route("/")`  
    Returns `home.html` – a simple landing page with a “Start Quiz” button.

  - `@app.route("/quiz")`  
    Returns `quiz.html`, which renders the main quiz UI.

  - `@app.route("/submit", methods=["POST"])`  
    - Reads JSON from `request.get_json()`.
    - `answers` is a dict like `{"0": 1, "1": 0, ...}` sent from JavaScript.
    - Loops over `QUIZ_DATA`, compares user answer vs `correct` index.
    - Calculates:
      - `score`
      - `results` list (per-question correctness and explanation)
      - `percentage`
    - Returns all of this as JSON using `jsonify(...)` so the frontend can render results.[web:39][web:42]

This separation means: Flask only handles **data + scoring**, and the browser handles the **UI**.
</details>

---

<details>
<summary><strong>🖥 Frontend: Templates & Styling</strong></summary>

### `home.html`

- Pure HTML + CSS (no JavaScript) for a clean landing page.
- Uses:
  - A gradient background
  - Centered card layout
  - A single link: `<a href="/quiz">Start Quiz →</a>`

### `quiz.html`

- Layout:
  - A container with:
    - Header (`AI & Computer Science Quiz`)
    - Dynamic questions area
    - Submit button
    - Results section (hidden initially)

- Styling:
  - Modern card UI using pure CSS
  - `.question-card` blocks each question
  - `.option` elements act like buttons with hover + selected states

No frontend frameworks, just HTML + CSS so you can fully understand each part.
</details>

---

<details>
<summary><strong>🧮 Frontend Logic: JavaScript Flow</strong></summary>

### How questions are rendered

- `quizData` is a JavaScript array copied from the Python `QUIZ_DATA`.
- On page load:
  - `loadQuestions()`:
    - Loops through `quizData`
    - Builds HTML for each question and its options
    - Inserts it into `#questions-container`
    - Attaches click handlers to `.option` elements

### Answer selection

- When you click an option:
  - All options for that question remove `.selected`
  - The clicked one adds `.selected`
  - The selected option index is stored in an `answers` object:
    ```js
    answers[questionIndex] = optionIndex;
    ```
- This `answers` object is what gets sent to Flask.

### Sending data to Flask

- On “Submit Quiz”:
  - If not all questions are answered, an alert is shown.
  - Otherwise:
    ```js
    fetch('/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ answers })
    })
    .then(res => res.json())
    .then(data => showResults(data));
    ```
- Flask receives this JSON via `request.get_json()` and responds with scoring data.[web:39][web:42]

### Showing results

- `showResults(data)`:
  - Hides the quiz form (`#quiz-form`)
  - Shows the results section (`#results`)
  - Displays:
    - Total score (`score/total`)
    - A message based on percentage
    - Per-question:
      - Your answer
      - Correct answer (if wrong)
      - Explanation

This pattern demonstrates a classic **JSON API** flow: JS ➜ Flask ➜ JS.
</details>

---

<details>
<summary><strong>▶️ Running the Project</strong></summary>

1. Install dependencies (Flask):
   ```bash
   python -m pip install flask
   ```

2. Run the app:
   ```bash
   python app.py
   ```

3. Open in browser:
   ```text
   http://127.0.0.1:5000
   ```

4. To stop:
   - Press `Ctrl + C` in the terminal.
</details>

---

## 🧩 What You Learn From This Code

- How to structure a **minimal Flask app** with routes and templates.[web:55][web:58]
- How to send and receive **JSON** between JavaScript and Flask using `fetch` and `request.get_json()`.[web:39][web:42]
- How to keep logic separated:
  - Python handles **data and correctness**
  - JavaScript handles **UI interactions and rendering**

This makes it a good starter project if you’re moving from basic Python scripts to full web apps.
