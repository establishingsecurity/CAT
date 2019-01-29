from cat.prng.lcg import (
    construct_lattice,
    reconstruct_lcg_state,
    reconstruct_lehmer_lower,
)
from cat.utils import descriptors
from cat.utils.descriptors import Adversary


class PRNGStoker(Adversary):
    # TODO: we need to set `shift`, but `shift` is documented nowhere!
    #   - same goes for `modulus`
    #   - we might want to use mpz instead of int
    """
    A convenience class for perform attacks on PRNGs that checks the correctness of input values.

    >>> a = PRNGStoker()
    >>> a.increment = 3
    >>> a.modulus = 15
    >>> a.multiplier = 2
    >>> a.states = 
    >>> a.samples = 
    """

    increment = descriptors.Number(int, forbidden_values=[0])
    modulus = descriptors.Number(int)
    multiplier = descriptors.Number(int, forbidden_values=[0])
    samples = descriptors.TypedList(min_length=3, element_type=int)
    shift = descriptors.Number(int)
    states = descriptors.List()

    def reconstruct_lehmer_state(self):
        # type: (PRNGStoker) -> int
        r"""
        Uses the :attr:`samples` of the stoker as states of a Lehmer style LCG and
        reconstructs the first state.

        An Lehmer style LCG uses an initial state :math:`s_0` (often called seed),
        a multiplier parameter :math:`a` and a modulus :math:`m`.
        The states of a Lehmer style LCG are computed by the recurrence relation
        :math:`s_{i+1} = a \cdot s_0` \mod m.

        :returns: The first state of the recurrence relation :math:`s_1`
        """
        L = construct_lattice(self.modulus, self.multiplier, len(self.samples))

        lower_bits = reconstruct_lehmer_lower(L, self.modulus, self.samples)

        self.states = [
            (x + y) % self.modulus for (x, y) in zip(lower_bits, self.samples)
        ]

        return self.states[0]

    def reconstruct_lcg_state(self):
        # type: (PRNGStoker) -> int
        r"""
        Uses the :attr:`samples` of the stoker as states of an LCG and
        reconstructs the first state.

        An LCG uses an initial state :math:`s_0` (often called seed),
        a multiplier parameter :math:`a`, an increment :math:`b`
        and a modulus :math:`m`.
        The states of an LCG are computed by the recurrence relation
        :math:`s_{i+1} = a \cdot s_0 + b` \mod m.

        :returns: The first state of the recurrence relation :math:`s_1`
        """
        lower_bits = reconstruct_lcg_state(
            self.modulus, self.multiplier, self.increment, self.samples, self.shift
        )

        self.states = [
            (x + y) % self.modulus for (x, y) in zip(lower_bits, self.samples)
        ]

        return self.states[0]
