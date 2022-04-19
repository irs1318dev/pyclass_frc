# 1. Do not delete the %%writefile ... line. It must be the first line
#    the cell.
# 2. Create your Rook and Knight classes in this cell.
# 3. Save the classes in the file pieces.py by running this cell.
# 4. If you make changes to the classes, re-run this cell to save
#    the changes to pieces.py
import math

from piece import Piece

class Rook(Piece):
    def __init__(self, color):
        super().__init__("rook", color)
        
    @property
    def can_jump(self):
        return False
    
    def get_moves(self, square):
        col = square[0]
        row = square[1]
        
        horizontal_moves = [c + row for c in "abcdefgh" if c != col]
        vertical_moves = [col + str(r) for r in range(1, 9) if r != int(row)]
        return horizontal_moves + vertical_moves     
    
    
class Knight(Piece):
    def __init__(self, color):
        super().__init__("knight", color)
        
    @property
    def can_jump(self):
        return True
        
    def get_moves(self, square):
        col = square[0]
        row = square[1]
        
        col_idx = ord(col) - 96
        row_idx = int(row)
        
        relative_moves = [(-2, -1), (-2, 1),
                          (-1, -2), (-1, 2),
                          (1, -2), (1, 2),
                          (2, -1), (2, 1)]
        
        absolute_moves = [(col_idx + rm[0], row_idx + rm[1])
                          for rm in relative_moves]
        legal_moves = [m for m in absolute_moves
                       if m[0] >= 1 and m[1] >= 1 and
                       m[0] <= 8 and m[1] <= 8]
        
        return [chr(move[0] + 96) + str(move[1]) for move in legal_moves]
                        
