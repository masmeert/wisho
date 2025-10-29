from enum import Enum


class Information(str, Enum):
    """JMdict reading information"""

    ATEJI = "ateji"  # Ateji (phonetic) reading - kanji used for sound only
    GIKUN = "gikun"  # Gikun (meaning as reading) or jukujikun (special kanji reading)
    IRREGULAR_KANJI = "iK"  # Word containing irregular kanji usage
    OUTDATED_KANJI = "oK"  # Word containing out-dated kanji
    RARELY_USED_KANJI = "rK"  # Rarely used kanji form
    IRREGULAR_KANA = "ik"  # Word containing irregular kana usage
    OUTDATED_KANA = "ok"  # Out-dated or obsolete kana usage
    OLD_IRREGULAR_KANA = "oik"  # Old or irregular kana form
    IRREGULAR_OKURIGANA = "io"  # Irregular okurigana usage
    EXCLUSIVELY_KANJI = "eK"  # Exclusively kanji
    EXCLUSIVELY_KANA = "ek"  # Exclusively kana
    USUALLY_KANJI = "uK"  # Word usually written using kanji alone
    USUALLY_KANA = "uk"  # Word usually written using kana alone


class MiscellaneousInformation(str, Enum):
    """JMdict miscellaneous indicators"""

    ABBREVIATION = "abbr"
    ARCHAIC = "arch"
    CHILDREN = "chn"
    COLLOQUIAL = "col"
    DEROGATORY = "derog"
    FAMILIAR = "fam"
    FEMALE = "fem"
    HONORIFIC = "hon"
    HUMBLE = "hum"
    IDIOMATIC = "id"
    JOCULAR = "joc"
    MALE = "male"
    MALE_SLANG = "male-sl"
    MANGA_SLANG = "m-sl"
    OBSOLETE = "obs"
    OBSCURE = "obsc"
    ONOMATOPOEIA = "on-mim"
    POETICAL = "poet"
    POLITE = "pol"
    PROVERB = "proverb"
    RARE = "rare"
    SENSITIVE = "sens"
    SLANG = "sl"
    VULGAR = "vulg"
    X_RATED = "X"
    YOJIJUKUGO = "yoji"
