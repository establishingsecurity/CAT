from Cryptodome.PublicKey import RSA

from cat.rsa import attacks
from cat.utils import descriptors
from cat.utils.descriptors import Adversary


class RSAStoker(Adversary):
    """
    A convenience class for performing attacks on RSA that checks the correctness of input values.
    """

    public_key = descriptors.RSAPublicKey()
    private_key = descriptors.RSAPrivateKey()

    def fermat_factoring(self):
        """
        This attack tries to factor moduli with primes that are close to each other
        and returns a matching rsa private key.
        """
        pk = RSA.construct(self.public_key[0], self.public_key[1])
        return attacks.fermat_factoring(pk)

    def common_divisor(self, common_divisor):
        """
        This attack takes an rsa public key and some integer that is known to have a
        common divisor with the modulus and returns a matching rsa private key.
        """
        pk = RSA.construct(self.modulus[0], self.public_key[1])
        return attacks.common_divisor(pk, common_divisor)

    def lsb_oracle(self, ciphertext, oracle):
        # type: (RSAKey, RSACiphertext, Callable[[RSACiphertext], bool]) -> RSAPlaintext
        r"""
        The Least Significant Bit Oracle attack is a simpler variation on
        Bleichenbacher.

        It assumes a decryption oracle :math:`LSB(\dot)` that accepts ciphertexts and returns the
        least significant or parity bit of the decrypted plaintext.
        """
        pk = RSA.construct(self.modulus[0], self.public_key[1])
        return attacks.lsb_oracle(pk, ciphertext, oracle)
