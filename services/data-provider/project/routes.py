"""Application routes"""
from flask import jsonify
from project import app
from project.sudoku import get_sudoku_game, valid_game, is_game_compelte


@app.route("/")
def index():
    """Simple Hello response"""
    return jsonify(message="Hello from data-provider")


@app.route("/sudoku/game/", defaults={"dificulty": "easy", "level": 0})
@app.route("/sudoku/game/<string:dificulty>/<int:level>")
def get_game(dificulty: str, level: int):
    """get sudoku game"""

    sudoku_game = get_sudoku_game(dificulty, level)

    return jsonify(
        dificulty=sudoku_game.difficulty,
        level=sudoku_game.level,
        sudoku=sudoku_game.sudoku,
        solution=sudoku_game.solution,
    )


@app.route("/sudoku/valid/<string:sudoku>")
def get_valid_game(sudoku: str):
    """check if a sudoku is valid"""
    result = valid_game(sudoku)
    return jsonify(result=result, sudoku=sudoku)


@app.route("/sudoku/complete/<string:sudoku>")
def get_is_game_complete(sudoku: str):
    """check if a sudoku is complete and valid """
    result = is_game_compelte(sudoku)
    return jsonify(result=result, sudoku=sudoku)


# add others routes here
