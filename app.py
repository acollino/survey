from flask import Flask, redirect, render_template
from surveys import satisfaction_survey

app = Flask(__name__)

@app.route("/")
def home():
  return render_template("base.html", survey=satisfaction_survey)

@app.route("/questions/<number>")
def question(number):
  index = int(number)
  if index < len(satisfaction_survey.questions):
    question = satisfaction_survey.questions[index]
    question_info = {"number": index, "question": question, "next": str(index+1)}
    return render_template("question.html", q_dict = question_info)
  else:
    return redirect("/")