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
  index = int(number)
  responses = session["responses"]
  if len(responses) >= len(satisfy.questions):
    return redirect("/thanks")
  elif index != len(responses):
    flash("You tried to access an invalid question; please complete the survey in order!")
    return redirect(f"/questions/{len(responses)}")
  else:
    return render_template("question.html", quest = satisfy.questions[index])

@app.route("/answer", methods=["POST"])
def answer():
  responses = session["responses"]
  responses.append(request.form.get("choice"))
  session["responses"] = responses
  print(responses)
  return redirect(f"/questions/{len(responses)}")

@app.route("/thanks")
def thanks():
  return render_template("thanks.html")