from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import joblib

app = Flask(__name__)
app.secret_key = "smartlearner_secret"


# ===============================
# LOAD AI MODEL
# ===============================

try:
    model = joblib.load("ai/model.pkl")
    encoder = joblib.load("ai/encoder.pkl")
except:
    model = None
    encoder = None


# ===============================
# CSE SUBJECT TOPICS
# ===============================

CSE_TOPICS = [
    "Data Structures",
    "Operating Systems",
    "DBMS",
    "Computer Networks",
    "Theory of Computation",
    "Software Engineering",
    "Compiler Design",
    "Machine Learning",
    "Cloud Computing",
    "Cyber Security",
    "Artificial Intelligence",
    "Web Development"
]


# ===============================
# AI RESOURCE GENERATOR
# ===============================

def get_ai_resources(preference, topics):

    resources = []

    for topic in topics:

        if preference == "Visual":

            yt_query = f"{topic} animation tutorial"
            google_query = f"{topic} visual explanation diagrams"

            resources.append({
                "topic": topic,
                "title": f"YouTube Visual: {topic}",
                "link": f"https://www.youtube.com/results?search_query={yt_query.replace(' ','+')}"
            })

            resources.append({
                "topic": topic,
                "title": f"Google Visual Notes: {topic}",
                "link": f"https://www.google.com/search?q={google_query.replace(' ','+')}"
            })


        elif preference == "Auditory":

            yt_query = f"{topic} lecture explanation"

            resources.append({
                "topic": topic,
                "title": f"YouTube Lecture: {topic}",
                "link": f"https://www.youtube.com/results?search_query={yt_query.replace(' ','+')}"
            })


        elif preference == "Reading":

            google_query = f"{topic} notes pdf tutorial"

            resources.append({
                "topic": topic,
                "title": f"Google Notes: {topic}",
                "link": f"https://www.google.com/search?q={google_query.replace(' ','+')}"
            })


        elif preference == "Kinesthetic":

            practice_query = f"{topic} coding practice problems"

            resources.append({
                "topic": topic,
                "title": f"Practice Problems: {topic}",
                "link": f"https://www.google.com/search?q={practice_query.replace(' ','+')}"
            })

    return resources


# ===============================
# QUESTIONS (30 REAL CSE QUESTIONS)
# ===============================

QUESTIONS = [

# =========================
# DATA STRUCTURES
# =========================

{"id": 1, "text": "How do you prefer learning Linked Lists in Data Structures?",
 "options": {"V": "Watch visual pointer diagrams",
             "A": "Listen to lecture explanation",
             "R": "Read textbook explanation",
             "K": "Implement linked list program"}},

{"id": 2, "text": "How do you understand Stack and Queue concepts?",
 "options": {"V": "Watch animation",
             "A": "Listen lecture",
             "R": "Read notes",
             "K": "Write code implementation"}},

{"id": 3, "text": "How do you learn Tree data structures?",
 "options": {"V": "View tree diagrams",
             "A": "Listen explanation",
             "R": "Read theory",
             "K": "Implement tree traversal"}},

{"id": 4, "text": "How do you study Graph algorithms?",
 "options": {"V": "Graph visualizations",
             "A": "Audio explanation",
             "R": "Read algorithms",
             "K": "Code BFS/DFS"}},


# =========================
# OPERATING SYSTEM
# =========================

{"id": 5, "text": "How do you understand Process Scheduling?",
 "options": {"V": "Watch scheduling diagrams",
             "A": "Listen lecture",
             "R": "Read scheduling theory",
             "K": "Use OS simulator"}},

{"id": 6, "text": "How do you learn Memory Management?",
 "options": {"V": "View paging diagrams",
             "A": "Listen lecture",
             "R": "Read OS book",
             "K": "Practice implementation"}},

{"id": 7, "text": "How do you understand Deadlocks?",
 "options": {"V": "Watch deadlock diagrams",
             "A": "Listen explanation",
             "R": "Read notes",
             "K": "Simulate deadlock"}},


# =========================
# DATABASE MANAGEMENT SYSTEM
# =========================

{"id": 8, "text": "How do you learn SQL Queries?",
 "options": {"V": "Watch schema diagrams",
             "A": "Listen explanation",
             "R": "Read SQL syntax",
             "K": "Practice SQL queries"}},

{"id": 9, "text": "How do you understand Normalization?",
 "options": {"V": "Watch normalization diagrams",
             "A": "Listen lecture",
             "R": "Read DBMS theory",
             "K": "Solve normalization problems"}},

{"id": 10, "text": "How do you learn ER Diagrams?",
 "options": {"V": "Draw diagrams",
             "A": "Listen lecture",
             "R": "Read textbook",
             "K": "Create ER models"}},


# =========================
# COMPUTER NETWORKS
# =========================

{"id": 11, "text": "How do you learn OSI Model?",
 "options": {"V": "Watch OSI diagrams",
             "A": "Listen explanation",
             "R": "Read networking book",
             "K": "Practice networking tools"}},

{"id": 12, "text": "How do you understand TCP/IP Protocol?",
 "options": {"V": "Watch packet flow diagrams",
             "A": "Listen lecture",
             "R": "Read protocol theory",
             "K": "Use packet tracer"}},

{"id": 13, "text": "How do you study Network Topologies?",
 "options": {"V": "Watch topology diagrams",
             "A": "Listen explanation",
             "R": "Read theory",
             "K": "Configure networks"}},


# =========================
# THEORY OF COMPUTATION
# =========================

{"id": 14, "text": "How do you learn Finite Automata?",
 "options": {"V": "Watch state diagrams",
             "A": "Listen explanation",
             "R": "Read theory",
             "K": "Design automata"}},

{"id": 15, "text": "How do you understand Regular Expressions?",
 "options": {"V": "Watch visual examples",
             "A": "Listen lecture",
             "R": "Read notes",
             "K": "Practice problems"}},


# =========================
# SOFTWARE ENGINEERING
# =========================

{"id": 16, "text": "How do you learn SDLC Models?",
 "options": {"V": "Watch SDLC diagrams",
             "A": "Listen lecture",
             "R": "Read documentation",
             "K": "Work on projects"}},

{"id": 17, "text": "How do you understand UML Diagrams?",
 "options": {"V": "Draw UML diagrams",
             "A": "Listen explanation",
             "R": "Read UML notes",
             "K": "Design software"}},


# =========================
# COMPILER DESIGN
# =========================

{"id": 18, "text": "How do you learn Lexical Analysis?",
 "options": {"V": "Watch DFA diagrams",
             "A": "Listen lecture",
             "R": "Read compiler book",
             "K": "Write lexer program"}},

{"id": 19, "text": "How do you understand Parsing?",
 "options": {"V": "Watch parse trees",
             "A": "Listen lecture",
             "R": "Read parsing theory",
             "K": "Write parser"}},


# =========================
# MACHINE LEARNING
# =========================

{"id": 20, "text": "How do you learn Machine Learning algorithms?",
 "options": {"V": "Watch model diagrams",
             "A": "Listen lecture",
             "R": "Read ML theory",
             "K": "Train ML models"}},


# =========================
# CLOUD COMPUTING
# =========================

{"id": 21, "text": "How do you learn Cloud Architecture?",
 "options": {"V": "Watch architecture diagrams",
             "A": "Listen lecture",
             "R": "Read documentation",
             "K": "Deploy applications"}},


# =========================
# CYBER SECURITY
# =========================

{"id": 22, "text": "How do you learn Network Security?",
 "options": {"V": "Watch attack diagrams",
             "A": "Listen lecture",
             "R": "Read security notes",
             "K": "Use security tools"}},


# =========================
# ARTIFICIAL INTELLIGENCE
# =========================

{"id": 23, "text": "How do you learn AI concepts?",
 "options": {"V": "Watch AI diagrams",
             "A": "Listen lecture",
             "R": "Read research papers",
             "K": "Build AI models"}},


# =========================
# WEB DEVELOPMENT
# =========================

{"id": 24, "text": "How do you learn Web Development?",
 "options": {"V": "Watch UI diagrams",
             "A": "Listen tutorial",
             "R": "Read documentation",
             "K": "Build websites"}},


# =========================
# COMPUTER GRAPHICS
# =========================

{"id": 25, "text": "How do you learn Computer Graphics?",
 "options": {"V": "Watch visual rendering",
             "A": "Listen lecture",
             "R": "Read graphics theory",
             "K": "Write graphics code"}},


# =========================
# PARALLEL COMPUTING
# =========================

{"id": 26, "text": "How do you learn Parallel Computing?",
 "options": {"V": "Watch thread diagrams",
             "A": "Listen lecture",
             "R": "Read notes",
             "K": "Write parallel programs"}},


# =========================
# BIG DATA
# =========================

{"id": 27, "text": "How do you learn Big Data concepts?",
 "options": {"V": "Watch architecture diagrams",
             "A": "Listen lecture",
             "R": "Read documentation",
             "K": "Run big data tools"}},


# =========================
# INTERNET OF THINGS
# =========================

{"id": 28, "text": "How do you learn IoT systems?",
 "options": {"V": "Watch IoT diagrams",
             "A": "Listen lecture",
             "R": "Read theory",
             "K": "Build IoT projects"}},


# =========================
# BLOCKCHAIN
# =========================

{"id": 29, "text": "How do you learn Blockchain?",
 "options": {"V": "Watch block diagrams",
             "A": "Listen lecture",
             "R": "Read whitepapers",
             "K": "Build blockchain project"}},


# =========================
# COMPETITIVE PROGRAMMING
# =========================

{"id": 30, "text": "How do you learn Competitive Programming?",
 "options": {"V": "Watch visual solutions",
             "A": "Listen explanation",
             "R": "Read editorial",
             "K": "Solve coding problems"}}

]


# ===============================
# LOGIN ROUTE
# ===============================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username and password:

            session["username"] = username

            return redirect(url_for("home"))

        else:

            return render_template("login.html", error="Invalid Login")

    return render_template("login.html")


# ===============================
# HOME ROUTE
# ===============================

@app.route("/home")
def home():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("home.html", name=session["username"])


# ===============================
# QUIZ ROUTE
# ===============================

@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        scores = {
            "Visual": 0,
            "Auditory": 0,
            "Reading": 0,
            "Kinesthetic": 0
        }

        answers = []

        for q in QUESTIONS:

            ans = request.form.get(f"q{q['id']}")

            answers.append(ans)

            if ans == "V":
                scores["Visual"] += 1

            elif ans == "A":
                scores["Auditory"] += 1

            elif ans == "R":
                scores["Reading"] += 1

            elif ans == "K":
                scores["Kinesthetic"] += 1


        # ===============================
        # AI PREDICTION
        # ===============================

        try:

            if model and encoder:

                encoded = encoder.transform(np.array(answers))

                encoded = encoded.reshape(1, -1)

                prediction = model.predict(encoded)[0]

            else:

                prediction = max(scores, key=scores.get)

        except:

            prediction = max(scores, key=scores.get)


        # ===============================
        # UNIMODAL / MULTIMODAL DETECTION
        # ===============================

        max_score = max(scores.values())

        dominant_list = [k for k, v in scores.items() if v == max_score]

        primary = dominant_list[0]

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        secondary = None

        if len(sorted_scores) > 1 and sorted_scores[1][1] >= max_score - 1:
            secondary = sorted_scores[1][0]


        if secondary and secondary != primary:

            dominant_str = primary + ", " + secondary

            learner_type = "Multimodal Learner"

        else:

            dominant_str = primary

            learner_type = "Unimodal Learner"


        # ===============================
        # COURSE RECOMMENDATION
        # ===============================

        if primary == "Kinesthetic":
            recommended = "Practical-Oriented Courses"

        elif primary in ["Visual", "Reading"]:
            recommended = "Theory-Oriented Courses"

        else:
            recommended = "Balanced Courses"


        # ===============================
        # AI RESOURCE GENERATION
        # ===============================

        resources = get_ai_resources(primary, CSE_TOPICS)


        return render_template(

            "result.html",

            name=session["username"],

            learner_type=learner_type,

            dominant=dominant_str,

            recommended=recommended,

            scores=scores,

            resources=resources

        )

    return render_template("quiz.html", questions=QUESTIONS)


# ===============================
# LOGOUT
# ===============================

@app.route("/logout")
def logout():

    session.pop("username", None)

    return redirect(url_for("login"))


# ===============================
# RUN SERVER
# ===============================

if __name__ == "__main__":
    app.run(debug=True)