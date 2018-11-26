from Cryptodome.Hash import SHA1


from cat.utils.utils import generate_brute_force, pmap


class TestPMap:
    """Tests for the parallel map function."""

    def test_doc_string(self):
        """Test for the example in the docstring codeblock."""
        fun = lambda d: SHA1.new(d).hexdigest()

        inputs = [b'1234', b'5678', b'9101', b'1121']
        outputs = ['7110eda4d09e062aa5e4a390b0a572ac0d2c0220',
                   '2abd55e001c524cb2cf6300a89ca6366848a77d5',
                   'f5a6fe40024c28967a354e591bb9fa21b784bf00',
                   '784e9240155834852dff458a730cceb50229df32']

        assert (pmap(fun, inputs) == outputs)

        filter_ = lambda d: d.endswith('0')
        outputs = ['7110eda4d09e062aa5e4a390b0a572ac0d2c0220',
                   'f5a6fe40024c28967a354e591bb9fa21b784bf00']
        assert (pmap(fun, inputs, filter_=filter_) == outputs)

    def test_multiple_inputs(self):
        """Test whether map behaves correctly on multiple inputs."""
        fun = lambda x,y: x + y
        xs = [1, 2, 3, 4, 5]
        ys = [1, 2, 3, 4, 5]

        zs = [2, 4, 6, 8, 10]
        assert (pmap(fun, xs, ys) == zs)

        filter_ = lambda z: z > 5
        zs = [6, 8, 10]
        assert (pmap(fun, xs, ys, filter_=filter_) == zs)

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
