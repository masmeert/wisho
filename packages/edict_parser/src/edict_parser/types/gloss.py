from enum import Enum


class GlossType(str, Enum):
    """Types of glosses in JMdict - semantic classification of translations"""

    LITERAL = "lit"
    FIGURATIVE = "fig"
    EXPLANATION = "expl"
