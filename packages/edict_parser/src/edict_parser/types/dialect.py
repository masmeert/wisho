from enum import Enum


class Dialect(str, Enum):
    """JMdict dialect indicators"""

    KANSAI = "ksb"
    KYOTO = "kyb"
    OSAKA = "osb"
    KANTOU = "ktb"
    TSUGARU = "tsug"
    TOSA = "tsb"
    TOUHOKU = "thb"
    KYUUSHUU = "kyu"
    RYUUKYUU = "rkb"
    NAGANO = "nab"
    HOKKAIDO = "hob"
