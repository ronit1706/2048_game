import tkinter as tk
import colours as clr
import random

class Puzzle(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048")

        self.main_board=tk.Frame(
            self,bg=clr.GRID_COLOR,bd=3,width=600,height=600
        )

        self.main_board.grid(pady=(100,0))
        self.create_GUI()
        self.begin_game()

        self.master.bind("<Left>",self.move_left)
        self.master.bind("<Right>",self.move_right)
        self.master.bind("<Up>",self.move_up)
        self.master.bind("<Down>",self.move_down)

        self.mainloop()

    def create_GUI(self):
        self.blocks=[]
        for i in range(4):
            row=[]
            for j in range(4):
                block_frame=tk.Frame(
                self.main_board,
                bg=clr.EMPTY_CELL_COLOR,
                height=150,
                width=150
                )
                block_frame.grid(row=i,column=j,padx=5,pady=5)
                block_number=tk.Label(self.main_board,bg=clr.EMPTY_CELL_COLOR)
                block_number.grid(row=i,column=j)
                block_data={"frame":block_frame,"number":block_number}
                row.append(block_data)
            self.blocks.append(row)

        score_frame=tk.Frame(self)
        score_frame.place(relx=0.5,y=45,anchor="center")
        tk.Label(
           score_frame,text="Score",
           font= clr.SCORE_LABEL_FONT
           ).grid(row=0)
        self.score_label=tk.Label(score_frame,text="0",font= clr.SCORE_FONT)
        self.score_label.grid(row=1)

    def begin_game(self):
         self.grid_matrix=[[0] *4 for _ in range(4)]

         row=random.randint(0,3)
         col=random.randint(0,3)
         self.grid_matrix[row][col]=2
         self.blocks[row][col]["frame"].configure(bg=clr.CELL_COLORS[2])
         self.blocks[row][col]["number"].configure(
             bg=clr.CELL_COLORS[2],
             fg=clr.CELL_NUMBER_COLORS[2],
             font=clr.CELL_NUMBER_FONTS[2],
             text="2"
             )
         while(self.grid_matrix[row][col]!=0):
            row=random.randint(0,3)
            col=random.randint(0,3)
         self.grid_matrix[row][col]=2
         self.blocks[row][col]["frame"].configure(bg=clr.CELL_COLORS[2])
         self.blocks[row][col]["number"].configure(
                bg=clr.CELL_COLORS[2],
                fg=clr.CELL_NUMBER_COLORS[2],
                font=clr.CELL_NUMBER_FONTS[2],
                text="2"
             )

         self.score=0

    def consolidate(self):
        new_matrix=[[0]*4 for _ in range(4)]
        for i in range(4):
            fill_position=0
            for j in range(4):
                if self.grid_matrix[i][j]!=0:
                    new_matrix[i][fill_position]=self.grid_matrix[i][j]
                    fill_position+=1
        self.grid_matrix=new_matrix

    def merge(self):
        for i in range(4):
            for j in range(3):
                if self.grid_matrix[i][j]!=0 and self.grid_matrix[i][j]==self.grid_matrix[i][j+1]:
                    self.grid_matrix[i][j]*=2
                    self.grid_matrix[i][j+1]=0
                    self.score+=self.grid_matrix[i][j]

    def flip(self):
         new_matrix= []
         for i in range(4):
             new_matrix.append([])
             for j in range(4):
                 new_matrix[i].append(self.grid_matrix[i][3-j])

         self.grid_matrix=new_matrix

    def rotate(self):
        new_matrix=[[0]*4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j]=self.grid_matrix[j][i]

        self.grid_matrix=new_matrix

    def add_new_block(self):
        row=random.randint(0,3)
        col=random.randint(0,3)
        while(self.grid_matrix[row][col]!=0):
            row=random.randint(0,3)
            col=random.randint(0,3)
        self.grid_matrix[row][col]=random.choice([2,4])

    def refresh_GUI(self):
        for i in range(4):
            for j in range(4):
                block_value=self.grid_matrix[i][j]
                if block_value==0:
                    self.blocks[i][j]["frame"].configure(bg=clr.EMPTY_CELL_COLOR)
                    self.blocks[i][j]["number"].configure(
                        bg=clr.EMPTY_CELL_COLOR,
                        text=""
                        )
                else:
                    self.blocks[i][j]["frame"].configure(bg=clr.CELL_COLORS[block_value])
                    self.blocks[i][j]["number"].configure(
                       bg=clr.CELL_COLORS[block_value],
                       fg=clr.CELL_NUMBER_COLORS[block_value],
                       font=clr.CELL_NUMBER_FONTS[block_value],
                       text=str(block_value)
                    )
        self.score_label.configure(text=self.score)
        self.update_idletasks()

    def move_left(self,event):
        self.consolidate()
        self.merge()
        self.consolidate()
        self.add_new_block()
        self.refresh_GUI()
        self.check_game_over()

    def move_right (self,event):
         self.flip()
         self.consolidate()
         self.merge()
         self.consolidate()
         self.flip()
         self.add_new_block()
         self.refresh_GUI()
         self.check_game_over()

    def move_up (self,event):
        self.rotate()
        self.consolidate()
        self.merge()
        self.consolidate()
        self.rotate()
        self.add_new_block()
        self.refresh_GUI()
        self.check_game_over()

    def move_down(self,event):
        self.rotate()
        self.flip()
        self.consolidate()
        self.merge()
        self.consolidate()
        self.flip()
        self.rotate()
        self.add_new_block()
        self.refresh_GUI()
        self.check_game_over()

    def horizontal_move_possible(self):
        for i in range(4):
            for j in range(3):
                if self.grid_matrix[i][j]==self.grid_matrix[i][j+1]:
                    return True
        return False

    def vertical_move_possible(self):
        for i in range(3):
            for j in range(3):
                if self.grid_matrix[i][j]==self.grid_matrix[i+1][j]:
                    return True
        return False

    def check_game_over(self):
        if any (2048 in row for row in self.grid_matrix):
            game_over_frame=tk.Frame(self.main_board, borderwidth=2)
            game_over_frame.place(relx=0.5,rely=0.5,anchor="center")
            tk.Label(
                game_over_frame,
                text="YOU WIN",
                bg=clr.WINNER_BG,
                fg=clr.GAME_OVER_FONT_COLOR,
                font=clr.GAME_OVER_FONT
            ).pack()
        elif not any (0 in row for row in self.grid_matrix) and not self.horizontal_move_possible() and not self.vertical_move_possible():
            game_over_frame=tk.Frame(self.main_board, borderwidth=2)
            game_over_frame.place(relx=0.5,rely=0.5,anchor="center")
            tk.Label(
                game_over_frame,
                text="GAME OVER",
                bg=clr.LOSER_BG,
                fg=clr.GAME_OVER_FONT_COLOR,
                font=clr.GAME_OVER_FONT
            ).pack()

def main():
  Puzzle()

if __name__ == "__main__":
    main()