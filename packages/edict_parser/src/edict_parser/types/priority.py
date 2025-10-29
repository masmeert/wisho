from enum import Enum


class PriorityType(str, Enum):
    """JMdict priority indicators"""

    News = "news"  # Newspaper frequency - from news media analysis
    Ichi = "ichi"  # Ichimanen (10,000) - most common Japanese words
    Spec = "spec"  # Specialized frequency - domain-specific common words
    Gai = "gai"  # Gairaigo - foreign loanword frequency rankings
    Nf = "nf"  # Name frequency - proper noun and name rankings
