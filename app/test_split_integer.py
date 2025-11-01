import pytest
from app.split_integer import split_integer


# --- Correct expected results ---
@pytest.mark.parametrize(
    "value, parts, expected",
    [
        (8, 1, [8]),
        (6, 2, [3, 3]),
        (10, 3, [3, 3, 4]),
        (17, 4, [4, 4, 4, 5]),
        (32, 6, [5, 5, 5, 5, 6, 6]),
        (23, 7, [3, 3, 3, 3, 3, 4, 4]),
        (29, 8, [3, 3, 3, 4, 4, 4, 4, 4]),
    ],
)
def test_expected_values(value, parts, expected):
    assert split_integer(value, parts) == expected


# --- Invariants ---
@pytest.mark.parametrize("value, parts", [(10, 3), (23, 7), (32, 6), (29, 8)])
def test_invariants(value, parts):
    result = split_integer(value, parts)
    assert len(result) == parts
    assert sum(result) == value
    assert result == sorted(result)
    assert max(result) - min(result) <= 1


# --- Trap 1: detect 'equal parts' fake ---
def test_detect_equal_part_fake():
    """Should not return all equal parts when remainder exists."""
    result = split_integer(11, 3)  # remainder = 2
    # Equal-part fake would give [3,3,3]
    assert result != [3, 3, 3], f"Equal-part fake not caught: {result}"
    assert result.count(4) == 2 and result.count(3) == 1


# --- Trap 2: detect 'last-only increment' fake ---
def test_detect_last_only_increment_fake():
    """Remainder must not all go to the last element."""
    result = split_integer(14, 5)  # remainder = 4
    # Last-only fake gives [2,2,2,2,6] or similar
    assert result != sorted(result[:-1] + [result[-1] + 1]), (
        f"Last-only increment fake not caught: {result}"
    )
    assert result.count(3) == 4 and result.count(2) == 1


# --- Trap 3: detect 'incorrect parts' fake ---
def test_detect_incorrect_parts_fake():
    """No part may fall below the base value."""
    result = split_integer(9, 4)
    base = 9 // 4
    assert all(x >= base for x in result), (
        f"Incorrect parts fake not caught: {result}"
    )

    assert sum(result) == 9


# --- Trap 4: detect 'different parts' fake ---
def test_detect_different_parts_fake():
    """If evenly divisible, all parts must be identical."""
    result = split_integer(12, 4)
    # Different-parts fake makes one smaller, one larger
    assert result == [3, 3, 3, 3], f"Different-parts fake not caught: {result}"


# --- General distribution test ---
@pytest.mark.parametrize("value, parts", [(101, 9), (50, 8), (25, 4), (19, 5)])
def test_distribution_consistency(value, parts):
    result = split_integer(value, parts)
    base = value // parts
    remainder = value % parts
    assert result.count(base + 1) == remainder, f"Incorrect +1 count: {result}"
    assert result.count(base) == parts - remainder
    assert sum(result) == value
    assert result == sorted(result)
