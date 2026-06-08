from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

QUIZ_DATA = [
    {
        "question": "Millions of people message every second, but there are no clashes. What handles this?",
        "options": ["Load balancer", "Big database", "Fast CPU", "Cache only"],
        "correct": 0,
        "explanation": "Load balancers distribute traffic across many servers, preventing clashes."
    },
    {
        "question": "What happens if two people book the same seat at the same millisecond?",
        "options": ["Both get it", "First wins", "System crashes", "Random remove"],
        "correct": 1,
        "explanation": "Concurrency control (locks/transactions) ensures the first request succeeds."
    },
    {
        "question": "Chatbots answer instantly for millions, yet don't slow down. What's the key?",
        "options": ["One GPU", "Model caching", "Queue all", "Human help"],
        "correct": 1,
        "explanation": "Cached responses and shared model instances reduce repeated computation."
    },
    {
        "question": "AI models train on huge data, but stay fast. What helps most?",
        "options": ["More RAM", "Distributed training", "Faster disk", "Manual sorting"],
        "correct": 1,
        "explanation": "Training splits across many machines/GPUs for speed and scale."
    },
    {
        "question": "Two users edit the same file at once; no corruption. How?",
        "options": ["Lock file", "Nightly merge", "Delete later", "Email copy"],
        "correct": 0,
        "explanation": "File locks or atomic operations prevent concurrent corruption."
    },
    {
        "question": "Millions upload photos daily, yet search stays fast. Why?",
        "options": ["Full scan", "Index + cache", "One server", "Manual tags"],
        "correct": 1,
        "explanation": "Indexes and cached results enable quick photo search."
    },
    {
        "question": "AI chatbots avoid 'hallucinations' in 2025–2026 more than before. Main reason?",
        "options": ["True–False training", "Better RLHF", "More words", "Human chat"],
        "correct": 1,
        "explanation": "Improved Reinforcement Learning from Human Feedback reduces false outputs."
    },
    {
        "question": "Real-time video calls for millions don't drop frames. What's critical?",
        "options": ["Big buffer", "Edge streaming", "Slow encode", "One CDN"],
        "correct": 1,
        "explanation": "Edge servers reduce latency and prevent frame drops."
    },
    {
        "question": "Two apps update a user's balance at once; no errors. How?",
        "options": ["Async only", "ACID transaction", "Night backup", "File lock"],
        "correct": 1,
        "explanation": "ACID guarantees safety and consistency for concurrent updates."
    },
    {
        "question": "Generative AI models scale up but stay affordable in 2024–2026. Key factor?",
        "options": ["More servers", "Efficient inference", "Manual tuning", "Copy prompts"],
        "correct": 1,
        "explanation": "Optimized inference (quantization, pruning, batching) cuts costs."
    }
]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/quiz")
def quiz():
    # We pass the quiz data, but the HTML uses hardcoded JS now – still fine
    return render_template("quiz.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    answers = data.get("answers", {})

    score = 0
    results = []

    for i, question in enumerate(QUIZ_DATA):
        # answers keys come as strings from JS, e.g., "0", "1", ...
        user_answer = int(answers.get(str(i), -1))
        correct = question["correct"]
        is_correct = (user_answer == correct)

        if is_correct:
            score += 1

        results.append({
            "question": question["question"],
            "user_answer": (
                question["options"][user_answer]
                if 0 <= user_answer < len(question["options"])
                else "Not answered"
            ),
            "correct_answer": question["options"][correct],
            "explanation": question["explanation"],
            "is_correct": is_correct,
        })

    return jsonify({
        "score": score,
        "total": len(QUIZ_DATA),
        "results": results,
        "percentage": (score / len(QUIZ_DATA)) * 100
    })

if __name__ == "__main__":
    os.makedirs("templates", exist_ok=True)
    app.run(debug=True, port=5000)