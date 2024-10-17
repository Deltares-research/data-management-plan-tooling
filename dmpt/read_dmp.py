from docx import Document


def read_tables(doc_path: str, target_tables: list[int] = None) -> dict[int, list[str]]:
    """
    Read the tables from a Word document and return the content of the tables as a
    dictionary. The tables are identified by their index in the document. The
    function returns only the tables that are specified in the `target_tables`. If
    target_tables is None, all tables are returned.

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