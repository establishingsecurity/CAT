from cat.prng.lcg import *


class PRNGStoker:
    _samples = None
    _states = None
    _multiplier = None
    _modulus = None

    @property
    def samples(self):
        return self._samples

    @samples.setter
    def samples(self, value):
        if not value:
            raise ValueError("samples must have a value")
        if not type(value) is list:
            raise TypeError("samples must be of type list")
        if not len(value) >= 3:
            raise ValueError("samples must have at least 3 samples")
        if not type(value[0]) is int:
            raise ValueError("samples elements must have at type int")
        self._samples = value

    @property
    def states(self):
        return self._states

    @property
    def multiplier(self):
        return self._multiplier

    @multiplier.setter
    def multiplier(self, value):
        if not value:
            raise ValueError("multiplier must have a value")
        if value == 0:
            raise ValueError("multiplier must have a value that is not 0")
        if not type(value) is int:
            raise TypeError("multiplier must be of type int")
        self._multiplier = value

    @property
    def modulus(self):
        return self._modulus

    @modulus.setter
    def modulus(self, value):
        if not value:
            raise ValueError("modulus must have a value")
        if not type(value) is int:
            raise TypeError("modulus must be of type int")
        self._modulus = value

    def reconstruct_lehmer_state(self):
        # type: (PRNGStoker) -> int
        """
        Uses the :attr:`samples` of the stoker as states of a Lehmer style LCG and
        reconstructs the first state.

        An Lehmer style LCG uses an initial state :math:`s_0` (often called seed),
        a multiplier parameter :math:`a` and a modulus :math:`m`.
        The states of a Lehmer style LCG are computed by the recurrence relation
        :math:`s_{i+1} = a \cdot s_0` \mod m.

        :returns: The first state of the recurrence relation :math:`s_1`
        """
        L = construct_lattice(self._modulus, self._multiplier, len(self.samples))

        lower_bits = reconstruct_lower_bits(L, self._modulus, self._samples)

        self._states = [
            (x + y) % self._modulus for (x, y) in zip(lower_bits, self._samples)
        ]

        return self._states[0]
