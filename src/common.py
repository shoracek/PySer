from typing import List


parsed_fields_long = [
    "title", "versions", "table_of_contents", "revisions", "bibliography"
]
parsed_fields_short = ["tit", "ver", "toc", "rev", "bib"]


def squash_whitespace(plain_text: str) -> str:
    """
    Reduce multiple consequent whitespaces to a single one
    and remove line breaks with dashes.
    """

    replaced_dash_newline = plain_text.replace("-\n", "-")
    replaced_all_newlines = " ".join(replaced_dash_newline.split())
    return replaced_all_newlines


def deduplicate_list(plain_text: List) -> List:
    return list(set(plain_text))
