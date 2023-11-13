from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "fjkhn654i8gv22oop9n" #Random secret key NOT from solution

boggle_game = Boggle()


@app.route("/")
def homepage():
    """Show Board"""

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    return render_template("index.html", board = board, highscore = highscore, nplays = nplays)

@app.rout("/check-word")
def check_word():
    """Check if word is in dictionary"""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'results': response})

@app.route("/post-score", methods=["POST"])
def post_score():
    """Recive score, update nplays, update high score (if applicable)"""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)