def is_dmp_filled_v1(tables: dict[int, list[str]]) -> dict[str, bool]:
    """
    Score a single DMP based on the content of the tables. The score is based on the
    following criteria:

    Part 1: General information
        - Section 1.1: Title, abstract, and list of participants
        - Section 1.4: Data and code used
        - Section 1.6: Data and code generated
        - Section 1.7: Ethical and legal considerations
    Part 1: Used data and code
    Part 1: Generated data and code

    Part 2: How your project will enact the FAIR data principles?
        - Section 4.1: Findable
        - Section 4.2: Accessible
        - Section 4.3: Interoperable
        - Section 4.4: Reusable
    Part 2: How will data / code be handled and backed up during research
        - Section 5.4: Data and code handling and backup
    Part 2: How and when will data and code be shared and preserved for the long term
        - Section 5.3: Data and code sharing and preservation

    Args:
        tables (dict[int, list[str]]): The tables extracted from the DMP

    Returns:
        dict[str, bool]: True or False for each section of the Data Management Plan
    """

    result = {}
    # Part 1: General information
    for index, row in enumerate(tables[2]):
        if index in (0, 3, 5, 6):  # Section 1.1, 1.4, 1.6 and 1.7
            if len(row[-1]) > 0:  # Check if there is anything written
                result[f"Section 1.{index+1}"] = True
            else:
                result[f"Section 1.{index+1}"] = False

    # Part 1: Used data and code
    total_chars = 0
    for index, row in enumerate(tables[3]):
        if index == 0:
            continue
        total_chars += sum(len(r) for r in row)
    if total_chars > 0:
        result["Section 2.1"] = True
    else:
        result["Section 2.1"] = False
        
    # Part 1: Generated data and code
    total_chars = 0
    for index, row in enumerate(tables[4]):
        if index == 0:
            continue
        total_chars += sum(len(r) for r in row)
    if total_chars > 0:
        result["Section 2.2"] = True
    else:
        result["Section 2.2"] = False

    # Part 2: How your project will enact the FAIR data principles?
    for index, row in enumerate(tables[6]):
        # Section 4.1, 4.2, 4.3 and 4.4
        if len(row[-1]) > 0:
            result[f"Section 4.{index+1}"] = True
        else:
            result[f"Section 4.{index+1}"] = False
    
    # Part 2: How will data / code be handled and backed up during research
    for index, row in enumerate(tables[7]):
        if index == 3:  # Section 5.4
            if len(row[-1]) > 0:
                result["Section 5.4"] = True
            else:
                result["Section 5.4"] = False

    # Part 2: How and when will data and code be shared and preserved for the long term
    for index, row in enumerate(tables[8]):
        if index == 4:  # Section 6.4
            if len(row[-1]) > 0:
                result["Section 6.4"] = True
            else:
                result["Section 6.4"] = False

    return result
