#!/bin/env python3
import sys
import json
import math
import os
from difflib import SequenceMatcher

def load_file(file):
    with open(file, "r", encoding="utf8") as f:
        return json.load(f)

def check_title(actual, expected):
    if not "title" in actual.keys():
        if not "title" in expected:
            return 20
        return 0

    similarity = SequenceMatcher(None, actual["title"], expected["title"]).ratio()
    return 20 * similarity

def check_versions(actual, expected):
    if not "versions" in actual:
        if not "versions" in expected:
            return 20
        return 0

    actual = actual["versions"]
    expected = expected["versions"]

    if len(expected) == 0:
        if len(actual) == 0:
            return 20
        return 0

    max_score = len(expected) * 4
    score = 0

    for key in expected:
        if not key in actual:
            continue

        score += 1

        if len(expected[key]) == len(actual[key]):
            score += 1

        set_e = set(expected[key])
        set_a = set(actual[key])

        score += 2 * len(set_e.intersection(set_a)) / len(set_e)

    return 20 * score / max_score

def check_toc(actual, expected):
    if not "table_of_contents" in actual:
        if not "table_of_contents" in expected:
            return 20
        return 0

    actual = list(filter(lambda x: len(x) == 3, actual["table_of_contents"]))
    expected = expected["table_of_contents"]

    if len(expected) == 0:
        if len(actual) == 0:
            return 20
        return 0

    max_score = 5 * len(expected)
    score = 0

    actual_numbers = list(map(lambda x: x[0], actual))
    expected_numbers = list(map(lambda x: x[0], expected))
    score += len(expected) * SequenceMatcher(None, actual_numbers, expected_numbers).ratio()

    actual_sections = list(map(lambda x: x[1], actual))
    expected_sections = list(map(lambda x: x[1], expected))
    score += len(expected) * SequenceMatcher(None, actual_sections, expected_sections).ratio()

    actual_pages = list(map(lambda x: x[2], actual))
    expected_pages = list(map(lambda x: x[2], expected))
    score += len(expected) * SequenceMatcher(None, actual_pages, expected_pages).ratio()

    for item in actual:
        if item in expected:
            score += 2

    return 20 * score / max_score

def check_revisions(actual, expected):
    if not "revisions" in actual:
        if not "revisions" in expected:
            return 20
        return 0

    actual = list(filter(lambda x: set(x) == {"version", "date", "description"}, actual["revisions"]))
    expected = expected["revisions"]

    if len(expected) == 0:
        if len(actual) == 0:
            return 20
        return 0

    max_score = 5 * len(expected)
    score = 0

    actual_versions = list(map(lambda x: x["version"], actual))
    expected_versions = list(map(lambda x: x["version"], expected))
    score += len(expected) * SequenceMatcher(None, actual_versions, expected_versions).ratio()

    actual_dates = list(map(lambda x: x["date"], actual))
    expected_dates = list(map(lambda x: x["date"], expected))
    score += len(expected) * SequenceMatcher(None, actual_dates, expected_dates).ratio()

    actual_descriptions = list(map(lambda x: x["description"], actual))
    expected_descriptions = list(map(lambda x: x["description"], expected))
    score += len(expected) * SequenceMatcher(None, actual_descriptions, expected_descriptions).ratio()

    for item in actual:
        if item in expected:
            score += 2

    return 20 * score / max_score

def check_bibliography(actual, expected):
    if not "bibliography" in actual:
        if not "bibliography" in expected:
            return 20
        return 0

    actual = actual["bibliography"]
    expected = expected["bibliography"]

    if len(expected) == 0:
        if len(actual) == 0:
            return 20
        return 0

    max_score = 2 * len(expected)
    score = 0

    for key in actual:
        if key not in expected:
            continue
        score += 1
        score += SequenceMatcher(None, actual[key], expected[key]).ratio()

    return 20 * score / max_score


def check(actual, expected):
    checks = (check_title, check_versions, check_toc, check_revisions, check_bibliography)
    scores = [check(actual, expected) for check in checks]
    return scores


def main():
    verbose = len(sys.argv) >= 4 and sys.argv[3] == "-v"

    if os.path.isdir(sys.argv[1]) and os.path.isdir(sys.argv[2]):
        rows = []
    
        for filename in os.listdir(sys.argv[1]):
            actual_path = os.path.join(sys.argv[1], filename)
            expected_path = os.path.join(sys.argv[2], filename)
            actual = load_file(actual_path)
            expected = load_file(expected_path)
            scores = check(actual, expected)
            rows.append((scores, filename))
        
        if verbose:
            print("", "  ".join(["sum", "tit", "ver", "toc", "rev", "bib"]), "name")
        
            for scores, filename in sorted(rows, key=lambda x: sum(x[0]), reverse=True):
                print("%4.0f" % math.ceil(sum(scores)), " ".join(["%4.0f" % score for score in scores]),
                      filename)
        
        print(sum([math.ceil(sum(scores)) for scores, _ in rows]), end="")
        
        if verbose:
            for j in range(len(rows[0][0])):
                scores = [rows[i][0][j] for i in range(len(rows))]
                print("", "%4.0f" % sum(scores), end="")

        print()
        
    else:
        actual = load_file(sys.argv[1])
        expected = load_file(sys.argv[2])
        scores = check(actual, expected)

        print(math.ceil(sum(scores)), end="")
        
        if verbose:
            print("", " ".join([str(int(s)) for s in scores]))

        print()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"USAGE: {sys.argv[0]} <output_json> <reference_json> [-v]", file=sys.stderr)
        sys.exit(1)

    main()
