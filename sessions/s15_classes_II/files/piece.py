# Create the Piece class in this cell.
class Piece():
    
    _pieces = {("white", "king"): "♔", ("black", "king"): "♚",
               ("white", "queen"): "♕", ("black", "queen"): "♛",
               ("white", "rook"): "♖", ("black", "rook"): "♜",
               ("white", "bishop"): "♗", ("black", "bishop"): "♝",
               ("white", "knight"): "♘", ("black", "knight"): "♞",
               ("white", "pawn"): "♙", ("black", "pawn"): "♟"}
    
    
    def __init__(self, piece_type, color):
        if color.lower() in ["white", "black"]:
            self._color = color.lower()
        else:
            raise ValueError
        if piece_type.lower() in ["king", "queen", "rook",
                                  "bishop", "knight", "pawn"]:
            self._piece_type = piece_type.lower()
        else:
            raise ValueError
        
    @property
    def color(self):
        return self._color
    
    @property
    def piece_type(self):
        return self._piece_type
    
    def __str__(self):
        return self._pieces[(self.color, self.piece_type)]
