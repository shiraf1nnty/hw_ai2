
from typing import List, Tuple, Optional

class GameState:
    """
    Represents a board state for generalized tic-tac-toe.
    board: List[List[str]] with 'X','O' or ' ' (space)
    m: board size
    k: win length
    to_move: 'X' or 'O'
    """
    def __init__(self, m: int = 3, k: int = 3, board: Optional[List[List[str]]] = None, to_move: str = 'X'):
        self.m = m
        self.k = k
        if board is None:
            self.board = [[' ' for _ in range(m)] for _ in range(m)]
        else:
            self.board = [row[:] for row in board]
        self.to_move = to_move

def initial_state(m: int = 3, k: int = 3) -> GameState:
    return GameState(m=m, k=k, board=None, to_move='X')

def player(state: GameState) -> str:
    return state.to_move

def actions(state: GameState):
    """Iterable of legal moves as (row, col) tuples, deterministic lexicographic order."""
    m = state.m
    for r in range(m):
        for c in range(m):
            if state.board[r][c] == ' ':
                yield (r, c)

def result(state: GameState, action: Tuple[int,int]) -> GameState:
    r, c = action
    if state.board[r][c] != ' ':
        raise ValueError("Illegal move")
    new_board = [row[:] for row in state.board]
    new_board[r][c] = state.to_move
    next_player = 'O' if state.to_move == 'X' else 'X'
    return GameState(m=state.m, k=state.k, board=new_board, to_move=next_player)

def _check_k_in_line(line: List[str], k: int) -> Optional[str]:
    """
    Sliding window for contiguous k matching markers (efficient).
    Returns 'X' or 'O' if a k-run exists, otherwise None.
    """
    m = len(line)
    if m < k:
        return None
    # sliding window count only when window contains no spaces and all same
    for start in range(0, m - k + 1):
        seg = line[start:start+k]
        first = seg[0]
        if first == ' ':
            continue
        same = True
        for x in seg:
            if x != first:
                same = False
                break
        if same:
            return first
    return None

def winner(state: GameState) -> Optional[str]:
    m = state.m
    k = state.k
    b = state.board

    # rows
    for r in range(m):
        w = _check_k_in_line(b[r], k)
        if w:
            return w

    # cols
    for c in range(m):
        col = [b[r][c] for r in range(m)]
        w = _check_k_in_line(col, k)
        if w:
            return w

    # diagonals down-right (r+i, c+i)
    # we can enumerate all diagonals of length >= k
    for r in range(m):
        for c in range(m):
            # only start where diagonal of length >= k
            if r + k - 1 < m and c + k - 1 < m:
                diag = [b[r+i][c+i] for i in range(k)]
                if diag.count(diag[0]) == k and diag[0] != ' ':
                    return diag[0]

    # diagonals up-right (r-i, c+i)
    for r in range(m):
        for c in range(m):
            if r - (k - 1) >= 0 and c + k - 1 < m:
                diag = [b[r-i][c+i] for i in range(k)]
                if diag.count(diag[0]) == k and diag[0] != ' ':
                    return diag[0]

    return None

def terminal(state: GameState) -> bool:
    if winner(state) is not None:
        return True
    # full board -> draw
    for r in range(state.m):
        for c in range(state.m):
            if state.board[r][c] == ' ':
                return False
    return True

def utility(state: GameState) -> Optional[int]:
    w = winner(state)
    if w == 'X': return 1
    if w == 'O': return -1
    if terminal(state): return 0
    return None

def pretty(state: GameState) -> str:
    return "\n".join("".join(row) for row in state.board)
