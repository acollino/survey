from flask import Flask, redirect, render_template, request, flash, session
from surveys import satisfaction_survey as satisfy

app = Flask(__name__)
app.secret_key = "many random chars"


@app.route("/")
def home():
    return render_template("base.html", survey=satisfy)


@app.route("/responses", methods=["POST"])
def log_responses():
    session["responses"] = []
    return redirect("/questions/0")


@app.route("/questions/<number>")
def question(number):
    responses = session.get("responses", [])
    index = len(responses)
    try:
        url_num = int(number)
    except ValueError:
        flash("That URL didn't look correct; you've been returned to the survey.")
        return redirect(f"/questions/{index}")
    if index >= len(satisfy.questions):
        return redirect("/thanks")
    elif url_num != len(responses):
        flash(
            "You tried to access an invalid question; please complete the survey in order!")
        return redirect(f"/questions/{index}")
    else:
        return render_template("question.html", quest=satisfy.questions[index])


@app.route("/answer", methods=["POST"])
def answer():
    responses = session.get("responses", [])
    responses.append(request.form.get("choice"))
    session["responses"] = responses
    print(responses)
    return redirect(f"/questions/{len(responses)}")


@app.route("/thanks")
def thanks():
    responses = session.get("responses", [])
    if len(responses) < len(satisfy.questions):
        flash("Please complete the survey!")
        return redirect(f"/questions/{len(responses)}")
    return render_template("thanks.html", responses=session["responses"], questions=satisfy.questions)


@app.errorhandler(404)
def nonexistent_page(error):
    responses = session.get("responses", [])
    if len(responses) == 0:
        flash("Sorry, that page doesn't exist. You've been redirected back to the survey.")
        return redirect("/")
    else:
        flash("Sorry, that page doesn't exist. You've been redirected back to the survey.")
        return redirect(f"/questions/{len(responses)}")
