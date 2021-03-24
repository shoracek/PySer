import json
import re
from typing import Dict, List
import argparse


def find_title(input: str) -> str:
    # For documents starting with 4 numbers only.
    input = input.replace("\n", " ")
    iter = re.findall(r"for\s+(.*?)\s+from", input, re.MULTILINE)

    return iter[0]


def find_eal(input: str) -> List[str]:
    found = re.findall(r"eal ?[0-9]\+?", input, re.IGNORECASE)

    return list(set(found))


def find_sha(input: str) -> List[str]:
    input = input.replace(" ", "")
    found = re.findall(r"sha-[0-9]+", input, re.IGNORECASE)

    return list(set(found))


def find_des(input: str) -> List[str]:
    found = re.findall(r"3des", input, re.IGNORECASE)
    found += re.findall(r"triple-des", input, re.IGNORECASE)

    return list(set(found))


def find_versions(input: str) -> Dict[str, List[str]]:
    versions = {}
    for i in [("eal", find_eal),
              ("sha", find_sha),
              ("des", find_des)]:
        result = i[1](input)
        if result:
            versions[i[0]] = result
    return versions


def find_bibliography(input: str) -> Dict[str, str]:
    found = re.findall(r"\[.*?\]", input)
    
    res = {}
    for i in found:
        found_ = re.findall(rf"{re.escape(i)} +([^\[]*)", input)
        if found_:
            res[i] = found_[-1]

    return res


def generate_json(input: str) -> str:
    return json.dumps(
        {
            "title": find_title(input),
            "versions": find_versions(input),
            "table_of_contents": [],
            "revisions": [],
            "bibliography": find_bibliography(input),
            "other": [],
        }, indent=4, sort_keys=True)


def generate_json_files(input_path: str, output_path: str):
    with open(input_path, "r", encoding="utf8") as file:
        input = file.read()

    output = generate_json(input)

    with open(output_path, "w", encoding="utf8") as file:
        file.write(output)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    parser.add_argument("--output_file", type=str, default="output.json")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    generate_json_files(args.input_file, args.output_file)
