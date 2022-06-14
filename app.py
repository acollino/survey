from flask import Flask, redirect, render_template, request
from surveys import satisfaction_survey as satisfy

app = Flask(__name__)

responses = []

@app.route("/")
def home():
  return render_template("base.html", survey=satisfy)

@app.route("/questions/<number>")
def question(number):
  index = int(number)
  if index < len(satisfy.questions):
    return render_template("question.html", quest = satisfy.questions[index])
  else:
    return redirect("/")

@app.route("/answer", methods=["POST"])
def answer():
  responses.append(request.form.get("choice"))
  if(len(satisfy.questions) > len(responses)):
    return redirect(f"/questions/{len(responses)}")
  else:
    return redirect("/end")

@app.route("/end")
def thanks():
  return render_template("thanks.html")