import chess


# Reference: https://www.chessprogramming.org/Simplified_Evaluation_Function
# 1) Material: Delta between sum of piece values for white and black
# 2) Development: Delta between the number of pieces that no longer on their starting squares (except pawns).
# 3) Mobility: Delta between the number of total legal moves
# 4) Control: Delta between the number of squares controlled by both sides.
# pawn structure, king-bishop structure, castling rights can be added to make more strong evaluate function


def material(board):
    # the values for pieces
    pawn = 100
    knight = 320
    bishop = 330
    rook = 500
    queen = 900
    king = 2000

    # number of pieces on the board wrt white and black
    white_pawn = len(board.pieces(chess.PAWN, chess.WHITE))
    black_pawn = len(board.pieces(chess.PAWN, chess.BLACK))
    white_knight = len(board.pieces(chess.KNIGHT, chess.WHITE))
    black_knight = len(board.pieces(chess.KNIGHT, chess.BLACK))
    white_bishop = len(board.pieces(chess.BISHOP, chess.WHITE))
    black_bishop = len(board.pieces(chess.BISHOP, chess.BLACK))
    white_rook = len(board.pieces(chess.ROOK, chess.WHITE))
    black_rook = len(board.pieces(chess.ROOK, chess.BLACK))
    white_queen = len(board.pieces(chess.QUEEN, chess.WHITE))
    black_queen = len(board.pieces(chess.QUEEN, chess.BLACK))
    white_king = len(board.pieces(chess.KING, chess.WHITE))
    black_king = len(board.pieces(chess.KING, chess.BLACK))

    material = pawn * (white_pawn - black_pawn) + knight * (white_knight - black_knight) + \
               bishop * (white_bishop - black_bishop) + rook * (white_rook - black_rook) + \
               queen * (white_queen - black_queen) + king * (white_king - black_king)

    return material


# it can be improved later on. check the development objectives individually for the pieces (what is the importance of their positions).
# not just with respect to beginning positions.
def development(board):
    white_development = 8
    black_development = 8

    white = ["R", "N", "B", "Q", "K", "B", "N", "R"]
    black = ["r", "n", "b", "q", "k", "b", "n", "r"]
    for i in range(8):
        if board.piece_at(chess.square(i, 0)):
            if board.piece_at(chess.square(i, 0)).symbol() == white[i]:
                white_development -= 1
        if board.piece_at(chess.square(i, 7)):
            if board.piece_at(chess.square(i, 7)).symbol() == black[i]:
                black_development -= 1

    dev = white_development - black_development
    return dev * 100


def mobility(board):
    mobility1 = board.legal_moves.count()  # legal moves
    board.push(chess.Move.null())  # push one empty move to change the side
    mobility2 = board.legal_moves.count()  # opponent's legal moves
    board.pop()  # take back the move to reset the board
    if board.turn:
        mob = mobility1 - mobility2
    else:
        mob = mobility2 - mobility1
    return mob * 10


def control(board):
    # calculate for every square the delta of white attackers to black attackers and sum the deltas
    white_control = 0
    black_control = 0
    for space_square in range(64):
        white_control += len(board.attackers(chess.WHITE, space_square))
        black_control += len(board.attackers(chess.BLACK, space_square))
    cont = white_control - black_control
    return cont * 10


def evaluate_board(board):
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999

    evaluation = material(board) + development(board) + mobility(board) + control(board)
    if board.turn:
        return evaluation
    return -evaluation


# this function should always be named as ai_play and
# this function's return value is used as AI's move so it will AI's your final decision.
# You can add as many function as you want to above.
# At each turn you will get a board to ai_play and calculate best move and return it.
def ai_play(board):
    plays = []
    for play in board.legal_moves:
        plays.append(str(play))

    move = minimax_root(3, board, True)  # when I wrote 4 or 5 to depth, it does not work properly, I debugged but could not find the reason.
    return str(move)  # here I only return random legal move to show an example g2g3


# minimax algorithm to find the best decision by calculating the board evaluation which respect to moves
# it can be improved later on
def minimax_root(depth, board, is_maximizing):
    legal_moves = board.legal_moves
    best_move = -9999
    for x in legal_moves:
        move = chess.Move.from_uci(str(x))
        board.push(move)
        value = max(best_move, minimax(depth - 1, board, not is_maximizing))
        board.pop()
        if value > best_move:
            best_move = value
            final_move = move
            print("Best move: ", str(final_move))
    return final_move


def minimax(depth, board, is_maximizing):
    if depth == 0:
        return -evaluate_board(board)

    legal_moves = board.legal_moves
    if is_maximizing:
        best_move = -9999
        for x in legal_moves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            best_move = max(best_move, minimax(depth - 1, board, not is_maximizing))
            board.pop()
        return best_move
    else:
        best_move = 9999
        for x in legal_moves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            best_move = min(best_move, minimax(depth - 1, board, not is_maximizing))
            board.pop()
        return best_move
