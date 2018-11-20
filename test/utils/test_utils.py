from cat.utils.utils import generate_brute_force


class TestBruteForce:
    """Tests for the brute force generator."""
    def test_first_yield(self):
        """Test whether first value is start value."""
        bf = generate_brute_force([0])
        assert next(bf) == [0]

    def test_second_yield(self):
        """Test whether value increases on second iteration."""
        bf = generate_brute_force([0])
        next(bf)
        assert next(bf) == [1]

    def test_256th_yield(self):
        """Test whether the 256th iteration introduces a new digit."""
        for i, guess in enumerate(generate_brute_force([0])):
            if i == 256:
                assert guess == [1, 0]
                break

    def test_257th_yield(self):
        """Test whether the lowest digit is increased after a new digit was added."""
        guess = generate_brute_force([255])
        next(guess) # returns initial value
        assert next(guess) == [1,0]
        assert next(guess) == [1,1]

    def test_third_digit_yield(self):
        """Test whether the 65536th iteration introduces a third digit."""
        guess = generate_brute_force([255, 255])
        next(guess) # returns initial value
        assert next(guess) == [1, 0, 0]

    def test_fourth_digit_yield(self):
        """Test whether the 4294967296th iteration introduces a fourth digit."""
        guess = generate_brute_force([255, 255, 255])
        next(guess) # returns initial value
        assert next(guess) == [1, 0, 0, 0]

    def test_fifth_digit_yield(self):
        """Test whether the 1099511627776th iteration introduces a fifth digit."""
        guess = generate_brute_force([255, 255, 255, 255])
        next(guess) # returns initial value
        assert next(guess) == [1, 0, 0, 0, 0]

    def test_some_yield(self):
        """Test whether the 1234567th iteration produces the correct value."""
        for i, guess in enumerate(generate_brute_force([0])):
            if i == 1234567:
                assert guess == [18, 214, 135]
                break
