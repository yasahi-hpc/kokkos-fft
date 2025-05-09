# SPDX-FileCopyrightText: (C) The kokkos-fft development team, see COPYRIGHT.md file
#
# SPDX-License-Identifier: MIT OR Apache-2.0 WITH LLVM-exception

""" unit-test of derivative
"""

import numpy as np
import pytest
from derivative import (
    initialize,
    analytical_solution,
    compute_derivative,
)

@pytest.mark.parametrize("n", [16, 32])
def test_initialize(n: int) -> None:
    """
    Test the initialize function.

    This test verifies that the initialize function returns arrays with correct shapes,
    computes the grid spacing (dx, dy) accurately, and generates proper frequency
    components (dikx, diky). It also checks the Hermitian symmetry of the iky array and
    ensures that the generated field 'u' is consistent across the batch dimension.

    Parameters
    ----------
    n : int
        The grid size in one dimension, used to determine the shape (n, n) of the
        generated arrays.
    """
    X, Y, ikx, iky, u = initialize(n, n, n)

    # Check shapes
    assert X.shape == (n, n)
    assert Y.shape == (n, n)
    assert ikx.shape == (n, n//2+1)
    assert iky.shape == (n, n//2+1)
    assert u.shape == (n, n, n)

    # Check dx, dy
    lx, ly = 2*np.pi, 2*np.pi
    dx, dy = lx / n, ly / n
    np.testing.assert_allclose(X[0, 1] - X[0, 0], dx)
    np.testing.assert_allclose(Y[1, 0] - Y[0, 0], dy)

    # Check dikx, diky
    dikx, diky = 1j * 2 * np.pi / lx, 1j * 2 * np.pi / ly
    np.testing.assert_allclose(ikx[0, 1], dikx)
    np.testing.assert_allclose(iky[1, 0], diky)

    # Check the Hermitian symmetry of iky
    # iky is Hermitian, so iky[i, j] = -iky[-i, j]
    for i in range(1, n//2):
        np.testing.assert_allclose(iky[i], -iky[-i])

    # Check it is a batch
    u0 = u[0]
    for i in range(1, n):
        np.testing.assert_allclose(u[i], u0)

@pytest.mark.parametrize("n", [16, 32])
def test_analytical_solution(n: int) -> None:
    """
    Test the analytical_solution function.

    This test verifies that the analytical_solution function returns an array with the
    correct shape and that the solution is consistent across the batch dimension. The
    analytical solution is computed based on the X and Y coordinates generated by the
    initialize function.

    Parameters
    ----------
    n : int
        The grid size in one dimension, which determines the shape (n, n) of the
        generated coordinate arrays.
    """
    X, Y, *_ = initialize(n, n, n)
    dudxy = analytical_solution(X, Y, n)

    # Check shapes
    assert dudxy.shape == (n, n, n)

    # Check it is a batch
    dudxy0 = dudxy[0]
    for i in range(1, n):
        np.testing.assert_allclose(dudxy[i], dudxy0)

@pytest.mark.parametrize("n", [16, 32])
def test_derivative(n: int) -> None:
    """
    Test the compute_derivative function.

    This test verifies that the compute_derivative function executes without raising
    exceptions. It uses the grid size (n, n, n) to compute the derivative of a field.
    The test is considered successful if the function executes correctly.

    Parameters
    ----------
    n : int
        The grid size in one dimension, which determines the shape of the field computed.
    """
    # The following function fails if it is not correct
    _ = compute_derivative(n, n, n)
