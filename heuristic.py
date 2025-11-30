
from typing import List
from engine import GameState, winner

def evaluate(state: GameState) -> float:
    """
    Symmetric, threat-aware heuristic.
    For every window of length k in each row/col/diag:
      - if window contains only X and empty: add weight = 10^(num_X)
      - if window contains only O and empty: subtract weight = 10^(num_O)
    This gives strong preference to immediate wins and to blocking opponent threats.
    """
    w = winner(state)
    if w == 'X': return 1e6
    if w == 'O': return -1e6

    m = state.m
    k = state.k
    b = state.board

    def windows_of_length_k(line: List[str]):
        L = len(line)
        for start in range(0, L - k + 1):
            yield line[start:start+k]

    score = 0.0

    # rows
    for r in range(m):
        for seg in windows_of_length_k(b[r]):
            if 'X' in seg and 'O' not in seg:
                cnt = seg.count('X')
                score += 10 ** cnt
            elif 'O' in seg and 'X' not in seg:
                cnt = seg.count('O')
                score -= 10 ** cnt

    # cols
    for c in range(m):
        col = [b[r][c] for r in range(m)]
        for seg in windows_of_length_k(col):
            if 'X' in seg and 'O' not in seg:
                cnt = seg.count('X')
                score += 10 ** cnt
            elif 'O' in seg and 'X' not in seg:
                cnt = seg.count('O')
                score -= 10 ** cnt

    # down-right diagonals
    for r0 in range(m):
        for c0 in range(m):
            # build diag from (r0,c0) as start only if length >= k
            diag = []
            r,c = r0, c0
            while 0 <= r < m and 0 <= c < m:
                diag.append(b[r][c])
                r += 1; c += 1
            if len(diag) >= k:
                for seg in windows_of_length_k(diag):
                    if 'X' in seg and 'O' not in seg:
                        cnt = seg.count('X'); score += 10 ** cnt
                    elif 'O' in seg and 'X' not in seg:
                        cnt = seg.count('O'); score -= 10 ** cnt

    # up-right diagonals
    for r0 in range(m):
        for c0 in range(m):
            diag = []
            r,c = r0, c0
            while 0 <= r < m and 0 <= c < m:
                diag.append(b[r][c])
                r -= 1; c += 1
            if len(diag) >= k:
                for seg in windows_of_length_k(diag):
                    if 'X' in seg and 'O' not in seg:
                        cnt = seg.count('X'); score += 10 ** cnt
                    elif 'O' in seg and 'X' not in seg:
                        cnt = seg.count('O'); score -= 10 ** cnt

    return float(score)

