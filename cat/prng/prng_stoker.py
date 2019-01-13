class PRNGStoker:
    def __init__(self):
        self._samples = None
        self._states = None
        self.multiplier = None
        self.modulus = None

    @property
    def samples(self):
        return self._samples

    @property
    def states(self):
        return self._states

    @property
    def multiplier(self):
        return self._multiplier

    @property
    def multiplier(self):
        return self._modulus

    def reconstruct_lehmer_state(self):
    # type: (PRNGStoker) -> int
    """
    Uses the :attr:`samples` of the stoker as states of a Lehmer style LCG and
    reconstructs the first state.

    An Lehmer style LCG uses an initial state :math:`s_0` (often called seed),
    a multiplier parameter :math:`a` and a modulus :math:`m`.
    The states of a Lehmer style LCG are computed by the recurrence relation
    :math:`s_{i+1} = a \cdot s_0` \mod m.

    >>> result = check_components(2, 4)
    >>> result == Result.NON_PRIME_MODULUS
    True

    :returns: The first state of the recurrence relation :math:`s_1`
    """
    if not self._multiplier:
        raise ValueError("PRNGStoker.multiplier must have a value")
    if not type(self._multiplier) is int:
        raise TypeError("PRNGStoker.multiplier must be of type int")
    if not self._modulus:
        raise ValueError("PRNGStoker.modulus must have a value")
    if not type(self._modulus) is int:
        raise TypeError("PRNGStoker.modulus must be of type int")
    if not self._samples:
        raise ValueError("PRNGStoker.samples must have a value")
    if not type(self._samples) is list:
        raise TypeError("PRNGStoker.samples must be of type list")
    if not len(self._samples) >= 3:
        raise ValueError("PRNGStoker.samples must have at least 3 samples")
    if not type(self._samples[0]) is int:
        raise ValueError("PRNGStoker.samples elements must have at type int")

    L = construct_lattice(self._modulus, self._multiplier, len(self.samples))

    lower_bits = reconstruct_lower_bits(L, self._modulus, self._samples)

    self._states = [x+y for (x,y) in zip(lower_bits, self._samples)]

    return self._states[0]
