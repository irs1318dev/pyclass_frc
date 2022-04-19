
import die

def test_die():
    # Check initial value
    die1 = die.DieTestable()
    assert isinstance(die1.value, int)
    assert die1.value >= 1 and die1.value <= 6
