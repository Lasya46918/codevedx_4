import os
import hmac
from flask import Flask, request, render_template, redirect, url_for, flash
from chatbot import get_answer, add_faq

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "local-demo-only-change-before-deployment")
ADMIN_PASSWORD = os.environ.get("HELPDESK_ADMIN_PASSWORD", "")

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/ask")
def ask():
    question = request.form.get("question", "").strip()
    if not question:
        flash("Please enter a question.")
        return redirect(url_for("index"))
    result = get_answer(question)
    return render_template("index.html", question=question, result=result)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        supplied = request.form.get("password", "")
        if not ADMIN_PASSWORD:
            flash("Set HELPDESK_ADMIN_PASSWORD in your environment before using admin.")
            return redirect(url_for("admin"))
        if not hmac.compare_digest(supplied, ADMIN_PASSWORD):
            flash("Incorrect admin password.")
            return redirect(url_for("admin"))
        question = request.form.get("question", "")
        answer = request.form.get("answer", "")
        intent = request.form.get("intent", "")
        keywords = request.form.get("keywords", "")
        try:
            add_faq(question, answer, intent, keywords)
            flash("FAQ added successfully.")
        except ValueError as exc:
            flash(str(exc))
        return redirect(url_for("admin"))
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
