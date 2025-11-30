

from engine import actions, result, terminal, utility, player
from heuristics import evaluate
import math

def minimax(state):
    def maxv(s):
        if terminal(s): return utility(s)
        best = -math.inf
        for a in sorted(actions(s)):
            val = minv(result(s,a))
            best = max(best, val)
        return best

    def minv(s):
        if terminal(s): return utility(s)
        best = math.inf
        for a in sorted(actions(s)):
            val = maxv(result(s,a))
            best = min(best, val)
        return best

    best_move = None
    best_val = -math.inf

    for a in sorted(actions(state)):
        val = minv(result(state,a))
        if val > best_val:
            best_val = val
            best_move = a

    return best_move
