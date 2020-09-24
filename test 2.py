import unidecode
import re
from fuzzywuzzy import fuzz


def string_reformat(string: str):
    pat_redundant_chars = re.compile(r"[\s`~!@#$%^&*()\-_+={\}\[\]\\|:;<>,./?]+")
    pat_quotations = re.compile(r'[\"«»‘’‚‛“”„‟‹›❛❜❝❞❮❯〝〞〟＂⹂]+')

    str_remove_accent = unidecode.unidecode(string).lower()                 # remove accent

    str_remove_quatation = str_remove_accent.replace("'", "")               # remove single quotations
    str_quotation = pat_quotations.sub("", str_remove_quatation)
    str_reformat_result = pat_redundant_chars.sub(" ", str_quotation)

    return str_reformat_result


def get_token_set_ratio(str1: str, str2: str):
    string_reformat1 = string_reformat(str1)
    string_reformat2 = string_reformat(str2)
    token_set_ratio = fuzz.token_set_ratio(string_reformat1, string_reformat2)
    return token_set_ratio


if __name__ == "__main__":
    str1 = 'You Don\'t Know What Love Is (You Just Do As You\'re Told) %bh ##^^ ajfdj đinh nữ giáng tiên'
    str2 = 'You Don\'t Know What Love'
    joy = get_token_set_ratio(str1, str2)
    print(string_reformat(str1))
    print(string_reformat(str2))
    print(joy)

