from otterai import OtterAI


def test_is_userid_none():
    otter = OtterAI()
    assert otter._is_userid_invalid() is True

def test_is_userid_empty():
    otter = OtterAI()
    otter._userid = ""
    assert otter._is_userid_invalid() is True

def test_is_userid_valid():
    otter = OtterAI()
    otter._userid = "123456"
    assert otter._is_userid_invalid() is False