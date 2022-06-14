from flask import Flask, render_template
from surveys import satisfaction_survey

app = Flask(__name__)

@app.route("/")
def home():
  return render_template("base.html", survey=satisfaction_survey)