#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Mon Feb 19 14:04:35 2024

@author: anivorlis
"""

import os

from docx import Document
from typing import List, Tuple, Dict, Optional

TARGET_TABLES = [2, 3, 4, 6, 7, 8]
PROJECT_FOLDER = "Project_BGS"
MAIL_FOLDER = "Mail_BGS"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def read_tables(doc_path: str, target_tables: Optional[List[int]] = None) -> Dict[int, List[str]]:
    """
    Read the tables from a Word document and return the content of the tables as a
    dictionary. The tables are identified by their index in the document. The
    function returns only the tables that are specified in the `target_tables`.

    Args:
        doc_path (str): The path to the Word document
        target_tables (List[int], optional): The indices of the tables to be extracted. Defaults to None.

    Returns:
        Dict[int, List[str]]: A dictionary with the content of the tables
    """
    doc = Document(doc_path)

    tables = dict()

    for index, table in enumerate(
        doc.tables
    ):  # This is a simplistic approach; a more robust method might be needed

        table_data = []
        for row in table.rows:
            row_data = [cell.text for cell in row.cells]
            table_data.append(row_data)

        if target_tables is None or index in target_tables:
            tables[index] = table_data

    return tables


def score_single_dmp_v1(tables: Dict[int, List[str]]) -> Tuple[float, float, float]:
    """
    Score a single DMP based on the content of the tables. The score is based on the
    following criteria:

    Part 1: General information [4 points]
        - Section 1.1: Title, abstract, and list of participants
        - Section 1.4: Data and code used
        - Section 1.6: Data and code generated
        - Section 1.7: Ethical and legal considerations
    Part 1: Used data and code [3 points]
    Part 1: Generated data and code [3 points]

    Part 2: How your project will enact the FAIR data principles? [4 points]
        - Section 4.1: Findable
        - Section 4.2: Accessible
        - Section 4.3: Interoperable
        - Section 4.4: Reusable
    Part 2: How will data / code be handled and backed up during research [1 points]
        - Section 5.4: Data and code handling and backup
    Part 2: How and when will data and code be shared and preserved for the long term [1 points]
        - Section 5.3: Data and code sharing and preservation

    Args:
        tables (Dict[int, List[str]]): The tables extracted from the DMP

    Returns:
        Tuple[float, float, float]: The score for each part and the total score
    """
    score_part1_target = 10  # 4 + 3 + 3
    score_part2_target = 6  # 4 + 1 + 1

    score_part1_actual = 0
    score_part2_actual = 0

    # Part 1: General information [4 points]
    for index, row in enumerate(tables[2]):
        if index in (0, 3, 5, 6):  # Section 1.1, 1.4, 1.6 and 1.7
            if len(row[-1]) > 0:
                score_part1_actual += 1
    # Part 1: Used data and code [3 points]
    total_chars = 0
    for index, row in enumerate(tables[3]):
        if index == 0:
            continue
        total_chars += sum(len(r) for r in row)
    if total_chars > 0:
        score_part1_actual += 3
    # Part 1: Generated data and code [3 points]
    total_chars = 0
    for index, row in enumerate(tables[4]):
        if index == 0:
            continue
        total_chars += sum(len(r) for r in row)
    if total_chars > 0:
        score_part1_actual += 3
    # Part 2: How your project will enact the FAIR data principles? [4 points]
    for index, row in enumerate(tables[6]):
        # Section 4.1, 4.2, 4.3 and 4.4
        if len(row[-1]) > 5:
            score_part2_actual += 1
    # Part 2: How will data / code be handled and backed up during research [1 points]
    for index, row in enumerate(tables[6]):
        if index == 3:  # Section 5.4
            if len(row[-1]) > 5:
                score_part2_actual += 2
    # Part 2: How and when will data and code be shared and preserved for the long term [1 points]
    for index, row in enumerate(tables[6]):
        if index == 4:  # Section 5.3
            if len(row[-1]) > 5:
                score_part2_actual += 2

    return (
        score_part1_actual / score_part1_target,
        score_part2_actual / score_part2_target,
        (score_part1_actual + score_part2_actual)
        / (score_part1_target + score_part2_target),
    )


def read_and_score_dmp_v1(filename: str) -> Tuple[float, float, float]:
    """
    Read the tables from a Word document and score the DMP based on the content of the
    tables.

    Args:
        filename (str): The path to the Word document

    Returns:
        Tuple[float, float, float]: The score for each part and the total score
    """
    tables = read_tables(filename)
    scores = score_single_dmp_v1(tables)
    return scores


if __name__ == "__main__":

    path = os.path.join(SCRIPT_DIR, PROJECT_FOLDER)

    with open("dmp_scores.txt", "w") as fout:
        for root, dirs, files in os.walk(path, followlinks=True):
            for file in files:
                if (file.endswith(".docx")) and (
                    "data-management-plan" in file.lower()
                ):
                    filename = os.path.join(root, file)

                    dmp_scores = read_and_score_dmp_v1(filename)
                    print(
                        f"Project {os.path.basename(root)}\nPart 1: {dmp_scores[0]:.0%} Part 2: {dmp_scores[1]:.0%} \nTotal Score: {dmp_scores[2]:.0%}\n",
                        file=fout,
                    )
