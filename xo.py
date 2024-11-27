import tkinter as tk
from tkinter import messagebox

class XO:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("X & O")
        self.current_player = 'X'  
        self.buttons = [[None] * 3 for _ in range(3)]
        self.create_board()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text='', font=('Arial', 40), width=3, height=1,
                                           command=lambda i=i, j=j: self.action(i, j))
                self.buttons[i][j].grid(row=i, column=j)

        self.ai_move()

    def action(self, row, col):
        if self.buttons[row][col]["text"] == '':
            self.buttons[row][col]["text"] = self.current_player
            if self.check_winner(row, col):
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_board()
            elif self.is_board_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.current_player == 'X':  
                    self.ai_move()
        else:
            messagebox.showwarning("Invalid Move", "That position is already taken.")

    def check_winner(self, row, col):
        if self.buttons[row][0]["text"] == self.buttons[row][1]["text"] == self.buttons[row][2]["text"] != '':
            return self.buttons[row][0]["text"]
        if self.buttons[0][col]["text"] == self.buttons[1][col]["text"] == self.buttons[2][col]["text"] != '':
            return self.buttons[0][col]["text"]
        if (
            self.buttons[0][0]["text"] == self.buttons[1][1]["text"] == self.buttons[2][2]["text"] != '') or (
            self.buttons[0][2]["text"] == self.buttons[1][1]["text"] == self.buttons[2][0]["text"] != ''):
            # print( self.buttons[0][2]["text"])
            return self.buttons[1][1]["text"]
        return None


    def is_board_full(self):
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]["text"] == '':
                    return False
        return True

    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = ''
        self.current_player = 'X'
        self.ai_move()
        # self.create_board()

    def run(self):
        self.root.mainloop()


    def ai_move(self):
        
        best_score, best_move = self.elagage_alpha_beta(-float('inf'), float('inf'),False)
        # print(best_score)
        # print(best_move)
        if best_move:
            i, j = best_move
            self.buttons[i][j]["text"] = 'X'  
            self.current_player = 'O'

            if self.check_winner(i, j):
                messagebox.showinfo("Game Over", "X wins!")
                self.reset_board()

            elif self.is_board_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_board()


    def elagage_alpha_beta(self, alpha, beta, is_maximizing, depth=0):
        winner = self.check_winner(0, 0)
        if winner == 'X':  
            return 1, None
        elif winner == 'O':  
            return -1, None
        elif self.is_board_full():
            return 0, None  

        best_score = -float('inf') if is_maximizing else float('inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]["text"] == '':
                    self.buttons[i][j]["text"] = 'X' 

                    
                    if self.check_winner(i, j) == 'X':
                        # print (self.check_winner(i, j) )
                        self.buttons[i][j]["text"] = ''  
                        return 1, (i, j)
                    self.buttons[i][j]["text"] = 'O' 

                    
                    if self.check_winner(i, j) == 'O':
                        # print (self.check_winner(i, j) )
                        self.buttons[i][j]["text"] = '' 
                        return -1, (i, j)  
                    

                    self.buttons[i][j]["text"] = '' 

        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]["text"] == '':
                    self.buttons[i][j]["text"] = 'X' if is_maximizing else 'O'
                    
                    score, _ = self.elagage_alpha_beta(alpha, beta, not is_maximizing, depth + 1)

                    self.buttons[i][j]["text"] = ''  

                    if is_maximizing:
                        if score > best_score:
                            best_score = score
                            best_move = (i, j)
                            alpha = max(alpha, best_score)
                            if alpha >= beta:
                                return best_score, best_move  
                    else:
                        if score < best_score:
                            best_score = score
                            best_move = (i, j)
                            beta = min(beta, best_score)
                            if alpha >= beta:
                                return best_score, best_move  

        return best_score, best_move


if __name__ == "__main__":
    game = XO()
    game.run()
