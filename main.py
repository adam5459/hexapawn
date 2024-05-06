import copy 

class Hexapawn:
    def __init__(self):
        self.board = [[2,2,2],
                      [0,0,0],
                      [1,1,1]]
        self.player = 1

    def display_board(self):
        for row in self.board:
            print(row)
        print("~"*10)

    def ai_turn(self):
            move = self.minimax(3, float('-inf'), float('inf'), True)[1]
            if move:
                self.make_move(move, self.board)
                print("AI moves:", move)
                self.display_board()
            else:
                print("AI has no valid moves.")
    def player_turn(self):
        self.display_board()
        player_move = self.get_player_move()
        self.make_move(player_move, self.board)
        if self.is_game_over():
            self.display_board()
            print("Player wins!")
            return

    def play_game(self):
        self.display_board()
        while True:
            self.player_turn()
            self.player = 1 if self.player == 2 else 2
            if self.is_game_over():
                break
            self.ai_turn()
            self.player = 1 if self.player == 2 else 2
            if self.is_game_over():
                self.display_board()
                print("AI wins!")

                break

    def evaluate_board(self):
        player1_pawns = sum(row.count(1) for row in self.board)
        player2_pawns = sum(row.count(2) for row in self.board)
        return player1_pawns- player2_pawns
    def get_player_move(self):
        while True:
            try:
                orow, ocol = map(int, input("Enter row and column of the pawn you want to move (e.g., 0 1): ").split())
                nrow, ncol = map(int, input("Enter row and column of the destination (e.g., 1 1): ").split())
                move = ((orow, ocol), (nrow, ncol))
                if move in self.get_possible_moves():
                    return move
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Please enter row and column numbers separated by a space.")
    def make_move(self, move, board):
        orow,ocol = move[0]
        nrow,ncol = move[1]
        board[nrow][ncol] = board[orow][ocol]
        board[orow][ocol] = 0
    def undo_move(self, move, board):
        orow, ocol = move[0]
        nrow, ncol = move[1]
        board[orow][ocol] = board[nrow][ncol]
        board[nrow][ncol] = 0   
    def is_game_over(self):
        if not self.get_possible_moves():
            return True
        for col in range(len(self.board[0])):
            if self.board[0][col] == 1 or self.board[2][col] == 2:
                return True

        return False
    
        

    def get_possible_moves(self):
        possible = []
        opponent=2 if self.player == 1 else 1

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == self.player:
                    if self.player == 1:
                        #diagonal
                        #r
                        if row -1 >= 0 and col +1 <= 2 and self.board[row-1][col+1] == opponent:
                            possible.append(((row,col),(row-1,col+1)))
                        #l
                        if row-1 >= 0 and col-1 >= 0 and self.board[row-1][col-1] == opponent:
                            possible.append(((row,col),(row-1,col-1)))
                        #vert
                        if row -1 >= 0 and self.board[row-1][col] == 0:
                            possible.append(((row,col),(row-1,col)))
                    elif self.player == 2:
                        #diag
                        #r
                        if row+1 <= 2 and col +1 <= 2 and self.board[row+1][col+1] == opponent:
                            possible.append(((row,col), (row+1, col+1)))
                        #l
                        if row+1 <= 2 and col -1 >= 0 and self.board[row+1][col-1] == opponent:
                            possible.append(((row,col),(row+1, col-1)))
                        #vert
                        if row+1 <= 2 and self.board[row+1][col] == 0:
                            possible.append(((row,col), (row+1, col)))
        return possible

                    
    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_game_over():
            return self.evaluate_board(), None
        board = copy.deepcopy(self.board)

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in self.get_possible_moves():
                self.make_move(move, board)
                evaluate = self.minimax(depth-1,alpha, beta, False)[0]
                self.undo_move(move, board)
                if evaluate > max_eval:
                    max_eval = evaluate
                    best_move = move
                alpha = max(alpha, evaluate)
                if beta <= alpha:
                    break
            return max_eval, best_move

        else:
            min_eval= float('inf')
            for move in self.get_possible_moves():
                self.make_move(move, board)
                evaluate = self.minimax(depth-1, alpha, beta, True)[0]
                self.undo_move(move, board)
                if evaluate<min_eval:
                    min_eval = evaluate
                beta = min(beta, evaluate)
                if beta <= alpha:
                    break
            return min_eval, None

if __name__ == "__main__":
    game = Hexapawn()
    game.display_board()
    game.play_game()
