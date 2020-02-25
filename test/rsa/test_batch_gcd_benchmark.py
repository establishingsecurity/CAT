import pytest

from cat.rsa.batch_gcd import (
    _compute_product_0,
    _compute_product_1,
    _build_product_tree_0,
    _build_product_tree_1,
    _attack_batch_gcd_0,
    _attack_batch_gcd_1,
)

INTS = list(range(1, 10000))

@pytest.mark.skip(reason="Benchmark not an actual test")
@pytest.mark.slow
def test_compute_product_0(benchmark):
    benchmark(_compute_product_0, INTS)


@pytest.mark.skip(reason="Benchmark not an actual test")
@pytest.mark.slow
def test_compute_product_1(benchmark):
    benchmark(_compute_product_1, INTS)


@pytest.mark.skip(reason="Benchmark not an actual test")
@pytest.mark.slow
def test_build_product_tree_0(benchmark):
    benchmark(_build_product_tree_0, INTS)


@pytest.mark.skip(reason="Benchmark not an actual test")
@pytest.mark.slow
def test_build_product_tree_1(benchmark):
    benchmark(_build_product_tree_1, INTS)


MODULI = [65537] * 5000 + [997] * 5000 + [65537 * 997]


@pytest.mark.skip(reason="Benchmark not an actual test")
@pytest.mark.slow
def test_attack_batch_gcd_0_moduli(benchmark):
    benchmark(_attack_batch_gcd_0, MODULI)


@pytest.mark.skip(reason="Benchmark not an actual test")
@pytest.mark.slow
def test_attack_batch_gcd_0_ints(benchmark):
    benchmark(_attack_batch_gcd_0, INTS)


@pytest.mark.skip(reason="Benchmark not an actual test")
@pytest.mark.slow
def test_attack_batch_gcd_1_moduli(benchmark):
    benchmark(_attack_batch_gcd_1, MODULI)


@pytest.mark.skip(reason="Benchmark not an actual test")
@pytest.mark.slow
def test_attack_batch_gcd_1_ints(benchmark):
    benchmark(_attack_batch_gcd_1, INTS)
