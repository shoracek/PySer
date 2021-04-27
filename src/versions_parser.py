from common import deduplicate_list, squash_whitespace
import re
from typing import Dict, List


def parse_eal(plain_text: str) -> List[str]:
    found = re.findall(r"[^\w](EAL ?[0-9]\+?)", plain_text)

    return deduplicate_list(found)


def parse_sha(plain_text: str) -> List[str]:
    versions = "512|384|256|224|3|2|1"

    plain_text = plain_text.replace(" ", "")
    found = re.findall(
        rf"SHA[-_ ]?\n?(?:{versions})(?:[-/_ ](?:{versions}))?",
        plain_text, re.MULTILINE
    )

    for i in range(len(found)):
        found[i] = squash_whitespace(found[i])
    return deduplicate_list(found)


def parse_des(plain_text: str) -> List[str]:
    found = re.findall(r"3des", plain_text, re.IGNORECASE)
    found += re.findall(r"des3", plain_text, re.IGNORECASE)
    found += re.findall(r"triple[- ]des", plain_text, re.IGNORECASE)
    found += re.findall(r"tdes", plain_text, re.IGNORECASE)

    return deduplicate_list(found)


def parse_rsa(plain_text: str) -> List[str]:
    versions = "4096|2048|1024"

    found = re.findall(
        rf"RSA[-_ ]?(?:{versions})(?:[-/_](?:{versions}))?",
        plain_text
    )

    return deduplicate_list(found)


def parse_ecc(plain_text: str) -> List[str]:
    found = re.findall(r"ECC", plain_text)
    found += re.findall(r"ECC ?[0-9]+", plain_text)
    for i in range(len(found)):
        found[i] = found[i].upper()

    return deduplicate_list(found)


def parse_global_platform(plain_text: str) -> List[str]:
    found = re.findall(r"global ?platform (?:[0-9]\.)*[0-9]",
                       plain_text, re.IGNORECASE)

    return deduplicate_list(found)


def parse_java_card(plain_text: str) -> List[str]:
    found = re.findall(r"java ?card (?:[0-9]\.)*[0-9]",
                       plain_text, re.IGNORECASE)

    return deduplicate_list(found)


def parse(plain_text: str) -> Dict[str, List[str]]:
    versions = {}
    for (version_name, parse_function) in [
        ("eal", parse_eal),
        ("sha", parse_sha),
        ("des", parse_des),
        ("rsa", parse_rsa),
        ("ecc", parse_ecc),
        ("global_platform", parse_global_platform),
        ("java_card", parse_java_card)
    ]:
        result = parse_function(plain_text)
        if result:
            versions[version_name] = result
    return versions
