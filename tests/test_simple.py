import pytest


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Деление на ноль запрещено")
    return a / b


def is_even(n):
    return n % 2 == 0


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(15, 0)
    assert divide(15, 3) == 5


def test_even_and_odd():
    assert is_even(10) is True
    assert is_even(5) is False


def test_note_title_not_empty():
    title = "  Конспект лекции по ИСИС  ".strip()
    assert len(title) > 0
