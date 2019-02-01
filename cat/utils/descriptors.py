"""
Contains descriptors for adversary classes.

See `Python Descriptors Demystified`_ by `Chris Beaumont`_ for information on descriptors.
The code for :class:`Descriptor` and :class:`Adversary` is taken from there.


.. _`Python Descriptors Demystified`: https://nbviewer.jupyter.org/urls/gist.github.com/ChrisBeaumont/5758381/raw/descriptor_writeup.ipynb
.. _`Chris Beaumont`: http://chrisbeaumont.org/
"""
import logging

from six import add_metaclass

from cat.log.log import LIB_ROOT_LOGGER_NAME
from cat.rsa import checks as rsa_checks
from cat.rsa.checks import RSAResult
from cat.utils.result import Severity

logger = logging.getLogger(LIB_ROOT_LOGGER_NAME)


class Descriptor(object):
    def __init__(self):
        self.label = None

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.label, None)

    def __set__(self, instance, value):
        self.perform_checks(value)
        instance.__dict__[self.label] = value

    def perform_checks(self, value):
        pass


class TypedDescriptor(Descriptor):
    def __init__(self, type_, *args, **kwargs):
        self.type_ = type_
        super(TypedDescriptor, self).__init__(*args, **kwargs)

    def perform_checks(self, value):
        if not isinstance(value, self.type_):
            raise TypeError(
                "{} must be of type {}".format(self.label, self.type_.__name__)
            )


class AdversaryMeta(type):
    """
    A metaclass for all Adversaries that adds labels to all descriptors.

    Labelled descriptors allow for descriptors on non-hashable descriptor owners. That
    means instances of unhashable types can still hold attributes of our descriptors.
    Additionally, since the label of each descriptor instance is the name of the attribute
    it's assigned to, it allows reference to the attribute's name in error messages.

    Code taken from `Python Descriptors Demystified`_.
    """

    def __new__(cls, name, bases, attrs):
        for n, v in attrs.items():
            if isinstance(v, Descriptor):
                v.label = n
        return super(AdversaryMeta, cls).__new__(cls, name, bases, attrs)


@add_metaclass(AdversaryMeta)
class Adversary(object):
    """
    Common class for all adversaries to inherit from.

    Keeps other developers from being scared by the metaclass.
    """

    pass


class List(TypedDescriptor):
    """
    Describes an attribute that is a list containing a minimum number of elements.

    >>> class ListContainer(Adversary):
    ...     maybe_empty = List()
    ...     greater_three = List(min_length=3)
    >>> lc = ListContainer()
    >>> # This works
    >>> lc.greater_three = [1, 2, 3]
    >>> print(lc.greater_three)
    [1, 2, 3]
    >>> # This fails because we're not assigning a list
    >>> try:
    ...     lc.greater_three = "garbage"
    ... except TypeError as e:
    ...     print(e)
    greater_three must be of type list
    >>> # This fails because we're not assigning enough elements
    >>> try:
    ...     lc.greater_three = ['1', 2]
    ... except ValueError as e:
    ...     print(e)
    greater_three must contain at least 3 elements
    >>> # This also works
    >>> lc.maybe_empty = []
    >>> print(lc.maybe_empty)
    []
    >>> # But this doesn't because None is not of type list
    >>> try:
    ...     lc.maybe_empty = None
    ... except TypeError as e:
    ...     print(e)
    maybe_empty must be of type list
    """

    def __init__(self, min_length=0, *args, **kwargs):
        self.min_length = min_length
        super(List, self).__init__(type_=list, *args, **kwargs)

    def perform_checks(self, value):
        super(List, self).perform_checks(value)
        if not len(value) >= self.min_length:
            raise ValueError(
                "{} must contain at least {} elements".format(
                    self.label, self.min_length
                )
            )


class TypedList(List):
    """
    A :class:`List` that additionally forces all list elements to have the same type.


    >>> class ListContainer(Adversary):
    ...     my_list = TypedList(min_length=0, element_type=int)
    >>> lc = ListContainer()
    >>> lc.my_list = []     # None wouldn't work here, because it's not of type list!
    >>> print(lc.my_list)
    []
    >>> lc.my_list = [1,2,3]
    >>> print(lc.my_list)
    [1, 2, 3]
    >>> try:
    ...     lc.my_list = ['1', 2]
    ... except ValueError as e:
    ...     print(e)
    All elements of my_list must have type int
    """

    def __init__(self, min_length, element_type, *args, **kwargs):
        self.element_type = element_type
        super(TypedList, self).__init__(min_length)

    def perform_checks(self, value):
        super(TypedList, self).perform_checks(value)
        if not all([isinstance(v, self.element_type) for v in value]):
            raise ValueError(
                "All elements of {} must have type {}".format(
                    self.label, self.element_type.__name__
                )
            )


class Number(TypedDescriptor):
    """
    A descriptor for Numbers of a certain type.
    It's possible to disallow certain numbers by setting :attr:`forbidden_values`.

    >>> class NumberContainer(Adversary):
    ...     floating = Number(type_=float)
    ...     whole_number = Number(type_=int, forbidden_values=[0,-1])
    >>> nc = NumberContainer()
    >>> nc.floating = 1.0
    >>> print(nc.floating)
    1.0
    >>> try:
    ...     nc.floating = 1
    ... except TypeError as e:
    ...     print(e)
    floating must be of type float
    >>> nc.whole_number = 1
    >>> print(nc.whole_number)
    1
    >>> try:
    ...     nc.whole_number = 1.0
    ... except TypeError as e:
    ...     print(e)
    whole_number must be of type int
    >>> try:
    ...     nc.whole_number = 0
    ... except ValueError as e:
    ...     print(e)
    whole_number cannot be any of [0, -1]
    """

    def __init__(self, type_, forbidden_values=None, *args, **kwargs):
        self.forbidden_values = forbidden_values if forbidden_values else []
        super(Number, self).__init__(type_=type_, *args, **kwargs)

    def perform_checks(self, value):
        super(Number, self).perform_checks(value)
        if value in self.forbidden_values:
            raise ValueError(
                "{} cannot be any of {}".format(self.label, self.forbidden_values)
            )


class Int(Number):
    """
    A descriptor for Integers.
    It's possible to disallow certain numbers by setting :attr:`forbidden_values`.
    """

    def __init__(self, forbidden_values=None, *args, **kwargs):
        super(Int, self).__init__(int, forbidden_values, *args, **kwargs)


class RSAKey(TypedDescriptor):
    """ A descriptor for an RSAKey (i.e. a tuple containing an exponent and a modulus). """

    def __init__(self, *args, **kwargs):
        super(RSAKey, self).__init__(type_=tuple, *args, **kwargs)

    def perform_checks(self, value):
        super(RSAKey, self).perform_checks(value)
        if len(value) != 2:
            raise ValueError(
                "You need to provide a tuple containing an exponent and a modulus."
            )


class RSAPublicKey(RSAKey):
    """
    A descriptor for an RSA public key (i.e. a tuple (N, e)).

    Runs :func:`cat.rsa.checks.check_public_key` on :code:`N, e` and logs the results via
    the logger.

    .. warning::
        You need to have logging enabled to see the results of the checks.
        See :mod:`cat.log`.

    >>> class RSAContainer(Adversary):
    ...     n = RSAPublicKey()
    >>> rc = RSAContainer()
    >>> rc.n = (15, 24)
    >>> # Would e.g. log that the modulus is composite.
    """

    def perform_checks(self, value):
        super(RSAPublicKey, self).perform_checks(value)
        N, e = value
        results = rsa_checks.check_public_key(N, e)
        for result in results:
            if result != RSAResult.OK:
                if result.severity == Severity.OK:
                    logger.info(result)
                else:
                    logger.warning(result)


class RSAPrivateKey(RSAKey):
    """ A descriptor for an RSA private key (i.e. a tuple (N, d)).

    Runs :func:`cat.rsa.checks.check_private_key` on :code:`N, d` and logs the results via
    the logger.

    .. warning::
        You need to have logging enabled to see the results of the checks.
        See :mod:`cat.log`.

    >>> class RSAContainer(Adversary):
    ...     n = RSAPrivateKey()
    >>> rc = RSAContainer()
    >>> rc.n = (15, 24)
    >>> # Would e.g. log that the modulus is composite.
    """

    def perform_checks(self, value):
        super(RSAPrivateKey, self).perform_checks(value)
        N, d = value
        results = rsa_checks.check_private_key(N, d)
        for result in results:
            if result != RSAResult.OK:
                if result.severity == Severity.OK:
                    logger.info(result)
                else:
                    logger.warning(result)
