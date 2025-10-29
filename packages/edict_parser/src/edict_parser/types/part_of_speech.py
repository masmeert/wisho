from enum import Enum


class PartOfSpeech(str, Enum):
    """JMdict part-of-speech indicators"""

    # Adjectives (11 types) - Japanese adjective system
    ADJ_F = "adj-f"  # Pre-noun verb (noun or verb describing a noun)
    ADJ_I = "adj-i"  # I adjective (keiyoushi) - standard Japanese adjective ending in い
    ADJ_IX = "adj-ix"  # I adjective (conjugated like いい/よい) - special conjugation pattern
    ADJ_KARI = "adj-kari"  # 'kari' adjective (archaic)
    ADJ_KU = "adj-ku"  # Ku adjective - archaic form ending in く
    ADJ_NA = "adj-na"  # Na adjective - adjectives requiring な before nouns
    ADJ_NARI = "adj-nari"  # Formal form of na adjective - classical Japanese
    ADJ_NO = "adj-no"  # No adjective - adjectival nouns using の particle
    ADJ_PN = "adj-pn"  # Pre-noun adjective - always placed before the noun
    ADJ_SHIKU = "adj-shiku"  # Shiku adjective - archaic classical form
    ADJ_T = "adj-t"  # Taru adjective - descriptive adjectives ending in たる

    # Adverbs (2 types)
    ADV = "adv"  # Standard adverb - modifies verbs, adjectives, other adverbs
    ADV_TO = "adv-to"  # Adverb taking particle 'to' - mimetic/onomatopoeic adverbs

    # Auxiliary (3 types) - Helper words
    AUX = "aux"  # Auxiliary word - general helper word
    AUX_ADJ = "aux-adj"  # Auxiliary adjective - helper adjective
    AUX_V = "aux-v"  # Auxiliary verb - helper verb (like である, だ)

    # Basic grammatical types
    CONJ = "conj"  # Conjunction - connecting words (そして, しかし, etc.)
    COP_DA = "cop-da"  # Copula (だ/である)
    CTR = "ctr"  # Counter - numerical classifiers (個, 本, 人, etc.)
    EXP = "exp"  # Expression - idiomatic phrases and expressions
    INT = "int"  # Interjection - exclamations (はい, いえ, etc.)
    IV = "iv"  # Irregular verb

    # Nouns (6 types) - Japanese noun classification
    N = "n"  # Standard noun - basic noun
    N_ADV = "n-adv"  # Adverbial noun - noun that can function as adverb
    N_PREF = "n-pref"  # Noun prefix - appears before other nouns
    N_PR = "n-pr"  # Proper noun
    N_SUF = "n-suf"  # Noun suffix - appears after other nouns
    N_T = "n-t"  # Temporal noun - time-related nouns (今日, 昨日, etc.)

    # Other word types
    NUM = "num"  # Numeric - numbers and numerical expressions
    PN = "pn"  # Pronoun - personal pronouns (私, あなた, etc.)
    PREF = "pref"  # General prefix - prefixes for various word types
    PRT = "prt"  # Particle - Japanese particles (は, が, を, etc.)
    SFX = "sfx"  # Sound effect - onomatopoeia and sound symbolism
    SUF = "suf"  # General suffix - suffixes for various word types
    UNC = "unc"  # Unclassified - words that don't fit other categories

    # Verbs - Basic types
    V_UNSPEC = "v-unspec"  # Unspecified verb - verb type not determined
    V1 = "v1"  # Ichidan verb - る-verbs (食べる, 見る, etc.)
    V1_S = "v1-s"  # Ichidan kureru verb - special ichidan subtype
    VZ = "vz"  # Ichidan zuru verb - verbs ending in ずる
    VK = "vk"  # Kuru verb - irregular verb 来る (to come)
    VI = "vi"  # Intransitive verb - does not take direct object
    VT = "vt"  # Transitive verb - takes direct object

    # Irregular verbs (6 types) - Special conjugation patterns
    VN = "vn"  # Irregular nu verb
    VR = "vr"  # Irregular ru verb, plain form ends with -ri
    VS = "vs"  # Noun or participle which takes the aux. verb suru
    VS_I = "vs-i"  # Suru verb - irregular
    VS_S = "vs-s"  # Suru verb - special class
    VS_C = "vs-c"  # Su verb - precursor to the modern suru

    # Godan verbs (14 endings) - five-row conjugation verbs
    V5ARU = "v5aru"  # Godan verb - -aru special class
    V5B = "v5b"  # Godan verb with 'bu' ending
    V5G = "v5g"  # Godan verb with 'gu' ending
    V5K = "v5k"  # Godan verb with 'ku' ending
    V5K_S = "v5k-s"  # Godan verb - Iku/Yuku special class
    V5M = "v5m"  # Godan verb with 'mu' ending
    V5N = "v5n"  # Godan verb with 'nu' ending
    V5R = "v5r"  # Godan verb with 'ru' ending
    V5R_I = "v5r-i"  # Godan verb with 'ru' ending (irregular verb)
    V5S = "v5s"  # Godan verb with 'su' ending
    V5T = "v5t"  # Godan verb with 'tsu' ending
    V5U = "v5u"  # Godan verb with 'u' ending
    V5U_S = "v5u-s"  # Godan verb with 'u' ending (special class)
    V5URU = "v5uru"  # Godan verb - Uru old class verb (old form of Eru)

    # Nidan verbs (archaic, 23 types) - Classical Japanese two-row conjugation
    V2A_S = "v2a-s"  # Nidan verb with 'u' ending (archaic)
    V2B_K = "v2b-k"  # Nidan verb (upper class) with 'bu' ending (archaic)
    V2B_S = "v2b-s"  # Nidan verb (lower class) with 'bu' ending (archaic)
    V2D_K = "v2d-k"  # Nidan verb (upper class) with 'dzu' ending (archaic)
    V2D_S = "v2d-s"  # Nidan verb (lower class) with 'dzu' ending (archaic)
    V2G_K = "v2g-k"  # Nidan verb (upper class) with 'gu' ending (archaic)
    V2G_S = "v2g-s"  # Nidan verb (lower class) with 'gu' ending (archaic)
    V2H_K = "v2h-k"  # Nidan verb (upper class) with 'hu/fu' ending (archaic)
    V2H_S = "v2h-s"  # Nidan verb (lower class) with 'hu/fu' ending (archaic)
    V2K_K = "v2k-k"  # Nidan verb (upper class) with 'ku' ending (archaic)
    V2K_S = "v2k-s"  # Nidan verb (lower class) with 'ku' ending (archaic)
    V2M_K = "v2m-k"  # Nidan verb (upper class) with 'mu' ending (archaic)
    V2M_S = "v2m-s"  # Nidan verb (lower class) with 'mu' ending (archaic)
    V2N_S = "v2n-s"  # Nidan verb (lower class) with 'nu' ending (archaic)
    V2R_K = "v2r-k"  # Nidan verb (upper class) with 'ru' ending (archaic)
    V2R_S = "v2r-s"  # Nidan verb (lower class) with 'ru' ending (archaic)
    V2S_S = "v2s-s"  # Nidan verb (lower class) with 'su' ending (archaic)
    V2T_K = "v2t-k"  # Nidan verb (upper class) with 'tsu' ending (archaic)
    V2T_S = "v2t-s"  # Nidan verb (lower class) with 'tsu' ending (archaic)
    V2W_S = "v2w-s"  # Nidan verb (lower class) with 'u' ending and 'we' conjugation (archaic)
    V2Y_K = "v2y-k"  # Nidan verb (upper class) with 'yu' ending (archaic)
    V2Y_S = "v2y-s"  # Nidan verb (lower class) with 'yu' ending (archaic)
    V2Z_S = "v2z-s"  # Nidan verb (lower class) with 'zu' ending (archaic)

    # Yodan verbs (archaic, 9 types) - Classical Japanese four-row conjugation
    V4B = "v4b"  # Yodan verb with 'bu' ending (archaic)
    V4G = "v4g"  # Yodan verb with 'gu' ending (archaic)
    V4H = "v4h"  # Yodan verb with 'hu/fu' ending (archaic)
    V4K = "v4k"  # Yodan verb with 'ku' ending (archaic)
    V4M = "v4m"  # Yodan verb with 'mu' ending (archaic)
    V4N = "v4n"  # Yodan verb with 'nu' ending (archaic)
    V4R = "v4r"  # Yodan verb with 'ru' ending (archaic)
    V4S = "v4s"  # Yodan verb with 'su' ending (archaic)
    V4T = "v4t"  # Yodan verb with 'tsu' ending (archaic)
