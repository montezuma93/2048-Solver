from flask import Flask, jsonify, request
from Solver import Solver
import numpy
import json
from flask import Flask, request, json
from flask_restplus import Resource, Api, reqparse, Swagger,fields
from flask_cors import CORS, cross_origin
import random

app = Flask(__name__)
CORS(app)

class Executor(Resource):

    def __init__(self, app):
        self.solver = Solver()
        self.gameboard = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]];

    def create_board(self):
        print('addnumber')
        number_to_add = random.choice([2,4])
        number_added = 0
        while number_added < 2:
            random_row = random.randint(0, 3)
            random_column = random.randint(0, 3)
            if(self.gameboard[random_row][random_column] == 0):
                self.gameboard[random_row][random_column] = number_to_add
                number_added = number_added + 1  
 
    def executeKey(self, key):
            switcher = {
                "up": lambda: self.executeUp(),
                "down": lambda: self.executeDown(),
                "left": lambda: self.executeLeft(),
                "right": lambda: self.executeRight()
            }
            function_to_execute = switcher.get(key, lambda: 'Invalid');
            was_legal_move = function_to_execute()
            if was_legal_move:
                self.add_random_number()
                if self.check_game_over():
                    return "GAME_OVER"
                else:
                    return "GAME_CONTINUES"

    def executeUp(self):
        self.gameboard = numpy.array(self.gameboard).T
        was_legal_move = self.executeLeft()
        self.gameboard = self.gameboard.T.tolist()
        return was_legal_move

    def executeDown(self):
        self.gameboard = numpy.array(self.gameboard).T
        was_legal_move = self.executeRight()
        self.gameboard = self.gameboard.T.tolist()
        return was_legal_move

    def executeLeft(self):
        was_legal_move = False
        for i, row in enumerate(self.gameboard):
            merged_index = -1
            for j, cell in enumerate(row):
                print(row , ':', cell , '=', self.gameboard[i][j])
                if(self.gameboard[i][j] != 0):
                    k = j
                    while k > 0 and (merged_index == -1 or k > merged_index + 1) and (self.gameboard[i][k - 1] == 0 or self.gameboard[i][k - 1] == self.gameboard[i][j]) :
                        k = k - 1
                    if(k != j):
                        was_legal_move = True
                        if(self.gameboard[i][k] != 0):
                            merged_index = k
                        self.gameboard[i][k] = self.gameboard[i][k] + self.gameboard[i][j]
                        self.gameboard[i][j] = 0
        return was_legal_move

    def executeRight(self):
        was_legal_move = False
        for i, row in enumerate(self.gameboard):
            merged_index = -1
            for j, cell in reversed(list(enumerate(row))):
                print(row , ':', cell , '=', self.gameboard[i][j])
                if(self.gameboard[i][j] != 0):
                    k = j
                    while k < len(row) - 1 and (merged_index == -1 or k < merged_index - 1) and (self.gameboard[i][k + 1] == 0 or self.gameboard[i][k + 1] == self.gameboard[i][j]) :
                        k = k + 1
                    if(k != j):
                        was_legal_move = True     
                        if(self.gameboard[i][k] != 0):
                            merged_index = k
                        self.gameboard[i][k] = self.gameboard[i][k] + self.gameboard[i][j]
                        self.gameboard[i][j] = 0
        return was_legal_move

    def add_random_number(self):
        print('addnumber')
        number_to_add = random.choice([2,4])
        number_added = False
        while not number_added:
            random_row = random.randint(0, 3)
            random_column = random.randint(0, 3)
            if(self.gameboard[random_row][random_column] == 0):
                self.gameboard[random_row][random_column] = number_to_add
                number_added = True   

    def check_game_over(self):
        old_board = self.gameboard
        board_is_not_full = any(0 in sublist for sublist in self.gameboard)
        if(not board_is_not_full):
            if self.executeRight():
                old_board = self.gameboard
                self.gameboard = old_board
                return False
            self.gameboard = old_board
            if self.executeUp():
                self.gameboard = old_board
                return False
            self.gameboard = old_board
            if self.executeDown():
                self.gameboard = old_board
                return False
            self.gameboard = old_board
            if self.executeLeft():
                self.gameboard = old_board
                return False
            self.gameboard = old_board
            return True
        else:
            return False


@app.route('/execute_key', methods=['POST'])
@cross_origin(origin='*')
def update_gameboard():
    req_data = request.get_json()
    key = req_data['key']
    if executor.executeKey(key) != "GAME_OVER":
        return json.dumps(executor.gameboard)
    else:
        return json.dumps("GAME_OVER")

@app.route('/create_board', methods=['POST'])
@cross_origin(origin='*')
def create_board():
    executor.create_board()
    return json.dumps(executor.gameboard)



executor = Executor(app)
if __name__ == '__main__':
    app.run()