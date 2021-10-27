# 1. Do not delete the %%writefile ... line. It must be the first line
#    the cell.
# 2. Create your Board class in this cell.
# 3. Save the Board class in the file deck.py by running this cell.
# 4. If you make changes to the class, re-run this cell to save
#    the changes to Board.py
from piece import Piece

class Board():
    
    def __init__(self):
        coords = [col + str(row) for col in "abcdefgh"[::-1] for row in range(8, 0, -1)]
        self._board = {coord: "-" for coord in coords}
    
    def place_piece(self, square, piece):
        if self[square.lower()] == "-":
            self._board[square.lower()] = piece
            return True
        else:
            return False
        
    def __getitem__(self, square):
        return self._board[square.lower()]
    
    def __str__(self):
        output = []
        for row in range(8, 0, -1):
            output.append(str(row) + "\t")            
            for col in "abcdefgh":
                output.append(str(self[col + str(row)]) + "\t")
            output.append("\n")
        output.append("\t")
        for col in "abcdefgh":
            output.append(col + "\t")
        return "".join(output)
    
    def show_moves(self, square):
        piece = self[square]
        if not isinstance(piece, Piece):
            return
        
        moves = piece.get_moves(square)
        for move in moves:
            if self[move] == "-":
                self._board[move] = "X"
                
    def clear_moves(self):
        for square in self._board.keys():
            if self[square] == "X":
                self._board[square] = "-"
