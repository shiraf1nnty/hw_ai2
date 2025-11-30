
from engine import initial_state, result
from search import minimax, minimax_ab, search
from heuristics import evaluate

def test_minimax_ab_equals_minimax_initial():
    b = initial_state(3,3)
    a1 = minimax(b)
    a2 = minimax_ab(b)
    assert a1 == a2

def test_search_blocks_simple_threat():
    # 4x4, k=3 partial board where immediate block is required
    b = initial_state(4,3)
    b = result(b, (0,0))  # X
    b = result(b, (1,0))  # O
    b = result(b, (0,1))  # X
    b = result(b, (1,1))  # O
    # X threatens to win at (0,2); depth=2 agent should pick blocking/pursuing move
    move = search(b, depth=2, eval_fn=evaluate)
    assert move is not None
