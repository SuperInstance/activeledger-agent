from activeledger_agent import ActiveledgerAgent

def test_create():
    a = ActiveledgerAgent()
    assert a is not None
