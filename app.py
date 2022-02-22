from flask import Flask, render_template
from main_code import movieDatabase, alphaAZ, alphaZA, movieRatingsHL, movieRatingsLH, movieRunTimeHl, movieRunTimeLH

app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def home_page():
    return render_template('index.html')

@app.route('/lists.html')
def movielist():
    return render_template('lists.html',movieDatabase=movieDatabase,alphaZA=alphaZA,
    alphaAZ=alphaAZ,movieRatingsHL=movieRatingsHL,movieRatingsLH=movieRatingsLH,
    movieRunTimeHL=movieRunTimeHl,movieRunTimeLH=movieRunTimeLH)

if __name__ == "__main__":
    app.run(debug=True)
