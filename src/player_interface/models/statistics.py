from typing import Optional, Self


class Statistics:
    _hsh: Optional[int] = 0
    _msh: Optional[int] = 0
    _lsh: Optional[int] = 0
    _hg: Optional[int] = 0
    _mg: Optional[int] = 0
    _lg: Optional[int] = 0
    _a: Optional[int] = 0
    _gb: Optional[int] = 0
    _t: Optional[int] = 0
    _ct: Optional[int] = 0
    _p: Optional[int] = 0
    _k: Optional[int] = 0
    _ms: Optional[int] = 0
    _hga: Optional[int] = 0
    _mga: Optional[int] = 0
    _lga: Optional[int] = 0
    _hgs: Optional[int] = 0
    _mgs: Optional[int] = 0
    _lgs: Optional[int] = 0
    _fow: Optional[int] = 0
    _fol: Optional[int] = 0

    def __init__(
        self,
        hsh: Optional[int],
        msh: Optional[int],
        lsh: Optional[int],
        hg: Optional[int],
        mg: Optional[int],
        lg: Optional[int],
        a: Optional[int],
        gb: Optional[int],
        t: Optional[int],
        ct: Optional[int],
        p: Optional[int],
        k: Optional[int],
        ms: Optional[int],
        hga: Optional[int],
        mga: Optional[int],
        lga: Optional[int],
        hgs: Optional[int],
        mgs: Optional[int],
        lgs: Optional[int],
        fow: Optional[int],
        fol: Optional[int],
    ) -> None:
        self._hsh = hsh
        self._msh = msh
        self._lsh = lsh
        self._hg = hg
        self._mg = mg
        self._lg = lg
        self._a = a
        self._gb = gb
        self._t = t
        self._ct = ct
        self._p = p
        self._k = k
        self._ms = ms
        self._hga = hga
        self._mga = mga
        self._lga = lga
        self._hgs = hgs
        self._mgs = mgs
        self._lgs = lgs
        self._fow = fow
        self._fol = fol

    @property
    def hsh(self) -> int:
        return self._hsh

    @property
    def msh(self) -> int:
        return self._msh

    @property
    def lsh(self) -> int:
        return self._lsh

    @property
    def hg(self) -> int:
        return self._hg

    @property
    def mg(self) -> int:
        return self._mg

    @property
    def lg(self) -> int:
        return self._lg

    @property
    def a(self) -> int:
        return self._a

    @property
    def gb(self) -> int:
        return self._gb

    @property
    def t(self) -> int:
        return self._t

    @property
    def ct(self) -> int:
        return self._ct

    @property
    def p(self) -> int:
        return self._p

    @property
    def k(self) -> int:
        return self._k

    @property
    def ms(self) -> int:
        return self._ms

    @property
    def hga(self) -> int:
        return self._hga

    @property
    def mga(self) -> int:
        return self._mga

    @property
    def lga(self) -> int:
        return self._lga

    @property
    def hgs(self) -> int:
        return self._hgs

    @property
    def mgs(self) -> int:
        return self._mgs

    @property
    def lgs(self) -> int:
        return self._lgs

    @property
    def fow(self) -> int:
        return self._fow

    @property
    def fol(self) -> int:
        return self._fol

    def to_dict(self) -> dict:
        return {
            "hsh": self._hsh,
            "msh": self._msh,
            "lsh": self._lsh,
            "hg": self._hg,
            "mg": self._mg,
            "lg": self._lg,
            "a": self._a,
            "gb": self._gb,
            "t": self._t,
            "ct": self._ct,
            "p": self._p,
            "k": self._k,
            "ms": self._ms,
            "hga": self._hga,
            "mga": self._mga,
            "lga": self._lga,
            "hgs": self._hgs,
            "mgs": self._mgs,
            "lgs": self._lgs,
            "fow": self._fow,
            "fol": self._fol,
        }
