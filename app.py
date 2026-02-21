from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import random

app = Flask(__name__)
app.secret_key = "smart_learner_secret_key"


# =========================================================
# QUESTIONS (30 QUESTIONS – CSE 2nd & 3rd Year Topics)
# =========================================================

QUESTIONS = [

# ================= DATA STRUCTURES =================

{"id": 1, "topic": "Data Structures",
"text": "How do you prefer learning Linked Lists?",
"options": {"V": "Watch pointer diagrams",
"A": "Listen lecture",
"R": "Read textbook",
"K": "Write implementation"}},

{"id": 2, "topic": "Data Structures",
"text": "How do you understand Stack and Queue?",
"options": {"V": "Watch animation",
"A": "Listen explanation",
"R": "Read theory",
"K": "Practice coding"}},

{"id": 3, "topic": "Data Structures",
"text": "How do you learn Trees?",
"options": {"V": "Watch diagrams",
"A": "Listen lecture",
"R": "Read notes",
"K": "Code tree traversal"}},

{"id": 4, "topic": "Data Structures",
"text": "How do you learn Graph Algorithms?",
"options": {"V": "Watch visualization",
"A": "Listen explanation",
"R": "Read algorithms",
"K": "Code BFS/DFS"}},


# ================= OPERATING SYSTEM =================

{"id": 5, "topic": "Operating Systems",
"text": "How do you learn Process Scheduling?",
"options": {"V": "Watch diagrams",
"A": "Listen lecture",
"R": "Read notes",
"K": "Use simulator"}},

{"id": 6, "topic": "Operating Systems",
"text": "How do you learn Memory Management?",
"options": {"V": "Watch paging diagrams",
"A": "Listen lecture",
"R": "Read theory",
"K": "Practice implementation"}},

{"id": 7, "topic": "Operating Systems",
"text": "How do you understand Deadlocks?",
"options": {"V": "Watch diagrams",
"A": "Listen explanation",
"R": "Read theory",
"K": "Simulate deadlock"}},


# ================= DBMS =================

{"id": 8, "topic": "DBMS",
"text": "How do you learn SQL?",
"options": {"V": "Watch schema diagrams",
"A": "Listen lecture",
"R": "Read SQL syntax",
"K": "Practice SQL"}},

{"id": 9, "topic": "DBMS",
"text": "How do you learn Normalization?",
"options": {"V": "Watch diagrams",
"A": "Listen lecture",
"R": "Read theory",
"K": "Solve problems"}},

{"id": 10, "topic": "DBMS",
"text": "How do you learn ER Diagrams?",
"options": {"V": "Draw diagrams",
"A": "Listen lecture",
"R": "Read textbook",
"K": "Create ER models"}},


# ================= COMPUTER NETWORKS =================

{"id": 11, "topic": "Computer Networks",
"text": "How do you learn OSI Model?",
"options": {"V": "Watch diagrams",
"A": "Listen lecture",
"R": "Read theory",
"K": "Practice tools"}},

{"id": 12, "topic": "Computer Networks",
"text": "How do you learn TCP/IP?",
"options": {"V": "Watch diagrams",
"A": "Listen explanation",
"R": "Read notes",
"K": "Use packet tracer"}},

{"id": 13, "topic": "Computer Networks",
"text": "How do you learn Network Topology?",
"options": {"V": "Watch diagrams",
"A": "Listen lecture",
"R": "Read theory",
"K": "Configure networks"}},


# ================= THEORY OF COMPUTATION =================

{"id": 14, "topic": "Theory of Computation",
"text": "How do you learn Finite Automata?",
"options": {"V": "Watch state diagrams",
"A": "Listen lecture",
"R": "Read notes",
"K": "Design automata"}},

{"id": 15, "topic": "Theory of Computation",
"text": "How do you learn Regular Expressions?",
"options": {"V": "Watch diagrams",
"A": "Listen explanation",
"R": "Read theory",
"K": "Practice problems"}},


# ================= SOFTWARE ENGINEERING =================

{"id": 16, "topic": "Software Engineering",
"text": "How do you learn SDLC?",
"options": {"V": "Watch diagrams",
"A": "Listen lecture",
"R": "Read documentation",
"K": "Work on project"}},

{"id": 17, "topic": "Software Engineering",
"text": "How do you learn UML?",
"options": {"V": "Draw diagrams",
"A": "Listen lecture",
"R": "Read notes",
"K": "Design system"}},


# ================= COMPILER DESIGN =================

{"id": 18, "topic": "Compiler Design",
"text": "How do you learn Lexical Analysis?",
"options": {"V": "Watch DFA diagrams",
"A": "Listen lecture",
"R": "Read theory",
"K": "Write lexer"}},

{"id": 19, "topic": "Compiler Design",
"text": "How do you learn Parsing?",
"options": {"V": "Watch parse trees",
"A": "Listen lecture",
"R": "Read notes",
"K": "Write parser"}},


# ================= MODERN TOPICS =================

{"id": 20, "topic": "Machine Learning",
"text": "How do you learn ML algorithms?",
"options": {"V": "Watch diagrams",
"A": "Listen lecture",
"R": "Read theory",
"K": "Train model"}},

{"id": 21, "topic": "Cloud Computing",
"text": "How do you learn Cloud?",
"options": {"V": "Watch architecture",
"A": "Listen lecture",
"R": "Read docs",
"K": "Deploy apps"}},

{"id": 22, "topic": "Cyber Security",
"text": "How do you learn Security?",
"options": {"V": "Watch attack diagrams",
"A": "Listen lecture",
"R": "Read theory",
"K": "Use tools"}},

{"id": 23, "topic": "Artificial Intelligence",
"text": "How do you learn AI?",
"options": {"V": "Watch diagrams",
"A": "Listen lecture",
"R": "Read papers",
"K": "Build model"}},

{"id": 24, "topic": "Web Development",
"text": "How do you learn Web Dev?",
"options": {"V": "Watch UI diagrams",
"A": "Listen tutorial",
"R": "Read docs",
"K": "Build website"}},

{"id": 25, "topic": "Computer Graphics",
"text": "How do you learn Graphics?",
"options": {"V": "Watch rendering",
"A": "Listen lecture",
"R": "Read theory",
"K": "Write code"}},

{"id": 26, "topic": "Parallel Computing",
"text": "How do you learn Parallel Computing?",
"options": {"V": "Watch diagrams",
"A": "Listen lecture",
"R": "Read theory",
"K": "Write programs"}},

{"id": 27, "topic": "Big Data",
"text": "How do you learn Big Data?",
"options": {"V": "Watch architecture",
"A": "Listen lecture",
"R": "Read docs",
"K": "Use tools"}},

{"id": 28, "topic": "IoT",
"text": "How do you learn IoT?",
"options": {"V": "Watch diagrams",
"A": "Listen lecture",
"R": "Read theory",
"K": "Build project"}},

{"id": 29, "topic": "Blockchain",
"text": "How do you learn Blockchain?",
"options": {"V": "Watch diagrams",
"A": "Listen lecture",
"R": "Read whitepaper",
"K": "Build project"}},

{"id": 30, "topic": "Competitive Programming",
"text": "How do you learn Competitive Programming?",
"options": {"V": "Watch solutions",
"A": "Listen explanation",
"R": "Read editorial",
"K": "Solve problems"}}

]


# =========================================================
# AI RESOURCE GENERATOR
# =========================================================

def get_ai_resources(preference):

    topics = list(set(q["topic"] for q in QUESTIONS))

    resources = []

    for topic in topics:

        youtube = f"https://www.youtube.com/results?search_query={topic}+tutorial"
        google = f"https://www.google.com/search?q={topic}+notes+pdf"
        practice = f"https://www.google.com/search?q={topic}+practice+problems+leetcode+geeksforgeeks"

        resources.append({"title": f"YouTube Tutorial: {topic}", "url": youtube})
        resources.append({"title": f"Google Learning: {topic}", "url": google})
        resources.append({"title": f"Practice Problems: {topic}", "url": practice})

    return resources


# =========================================================
# ROUTES
# =========================================================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")

        session["username"] = username

        return redirect(url_for("home"))

    return render_template("login.html")


@app.route("/home")
def home():
    return render_template("home.html", name=session.get("username", "Student"))

@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    if request.method == "POST":

        scores = {"Visual": 0, "Auditory": 0, "Reading": 0, "Kinesthetic": 0}

        for q in QUESTIONS:

            ans = request.form.get(f"q{q['id']}")

            if ans == "V":
                scores["Visual"] += 1
            elif ans == "A":
                scores["Auditory"] += 1
            elif ans == "R":
                scores["Reading"] += 1
            elif ans == "K":
                scores["Kinesthetic"] += 1


        max_score = max(scores.values())

        dominant = [k for k, v in scores.items() if v == max_score]

        learner_type = "Multimodal Learner" if len(dominant) > 1 else "Unimodal Learner"

        dominant_str = ", ".join(dominant)


        if "Kinesthetic" in dominant:
            recommended = "Practical Courses"
        elif "Visual" in dominant or "Reading" in dominant:
            recommended = "Theory Courses"
        else:
            recommended = "Balanced Courses"


        resources = get_ai_resources(dominant)


        return render_template(
            "result.html",
            name="Student",
            learner_type=learner_type,
            dominant=dominant_str,
            scores=scores,
            recommended=recommended,
            resources=resources
        )


    return render_template("quiz.html", questions=QUESTIONS)


# =========================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

