r"""
References
    * :cite:`furtula_atom-bond_2016`
"""

import numpy as np

from ._base import Descriptor
from ._graph_matrix import DistanceMatrix


__all__ = ('ABCIndex', 'ABCGGIndex',)


class ABCIndexBase(Descriptor):
    @classmethod
    def preset(cls):
        yield cls()

    explicit_hydrogens = False

    def __reduce_ex__(self, version):
        return self.__class__, ()

    def __str__(self):
        return self.__class__.__name__[:-5]

    rtype = float


class ABCIndex(ABCIndexBase):
    r"""atom-bond connectivity indez descriptor.
    """

    @staticmethod
    def _each_bond(bond):
        du = bond.GetBeginAtom().GetDegree()
        dv = bond.GetEndAtom().GetDegree()

        return np.sqrt(float(du + dv - 2) / (du * dv))

    def calculate(self, mol):
        return float(sum(
            self._each_bond(bond)
            for bond in mol.GetBonds()
        ))


class ABCGGIndex(ABCIndexBase):
    r"""Graovac-Ghorbani atom-bond connectivity index descriptor.
    """

    def dependencies(self):
        return {'D': DistanceMatrix(self.explicit_hydrogens)}

    @staticmethod
    def _each_bond(bond, D):
        u = bond.GetBeginAtomIdx()
        v = bond.GetEndAtomIdx()

        nu = np.sum(D[u, :] < D[v, :])
        nv = np.sum(D[v, :] < D[u, :])

        return np.sqrt(float(nu + nv - 2) / (nu * nv))

    def calculate(self, mol, D):
        return float(sum(
            self._each_bond(bond, D)
            for bond in mol.GetBonds()
        ))


if __name__ == '__main__':
    from .__main__ import submodule
    submodule()
