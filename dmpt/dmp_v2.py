import re

import win32com.client

from tools.parsers import parse_checkboxes, project_info, text_is_not_default


def read_dmp_file(dmp_file: str) -> dict[str, str]:
    """
    Reads a Data Management Plan (DMP) file in Microsoft Word format and extracts its content.

    Args:
        dmp_file (str): The path to the DMP file to be read.
    Returns:
        dict[str, str]: A dictionary where the keys are section numbers (e.g., "1.1", "2.3") and the values are the corresponding text content.
    
    The function performs the following steps:
    1. Rebuilds the win32com cache to ensure proper functionality.
    2. Initializes a hidden instance of the Word application.
    3. Opens the specified DMP file.
    4. Extracts all paragraphs and tables from the document.
    5. Processes each table to handle merged cells and checkboxes.
    6. Closes the document and the Word application.
    7. Uses a regular expression to match section numbers and constructs a dictionary with the extracted content.
    """
    # Rebuild the win32com cache
    win32com.client.gencache.is_readonly = False
    win32com.client.gencache.Rebuild()

    # Initialize Word application
    word_app = win32com.client.Dispatch("Word.Application")
    word_app.Visible = False  # Keep Word application hidden

    # Open the document
    doc = word_app.Documents.Open(dmp_file)

    # List to hold all document content
    document_content = {
        "paragraphs": [],
        "tables": []
    }

    # Extract all paragraphs (text outside tables)
    for paragraph in doc.Paragraphs:
        paragraph_text = paragraph.Range.Text.strip()
        if paragraph_text:  # Only add non-empty paragraphs
            document_content["paragraphs"].append(paragraph_text)

    # Extract all tables
    for table in doc.Tables:
        table_data = []
        num_rows = table.Rows.Count
        num_columns = table.Columns.Count
        
        # Access rows and cells by index to handle merged cells and checkboxes
        for i in range(1, num_rows + 1):
            row_data = []
            for j in range(1, num_columns + 1):
                cell = table.Cell(i, j)
                cell_text = cell.Range.Text.strip().replace("\r\x07", "").strip()
                
                # Check for form fields (e.g., checkboxes) in the cell
                if cell.Range.FormFields.Count > 0:
                    for form_field in cell.Range.FormFields:
                        if form_field.Type == 71:  # Type 71 is a checkbox
                            checkbox_status = "Checked" if form_field.CheckBox.Value else "Unchecked"
                            cell_text += f" [{checkbox_status}]"
                
                row_data.append(cell_text)
            table_data.append(row_data)
        document_content["tables"].append(table_data)

    # Close the document and Word application
    doc.Close(False)
    word_app.Quit()

    # write to the values dict
    values = dict()

    # Regular expression pattern to match numbers with a dot at the start of the string
    pattern = r"^\d+\.\d+"

    for idx, table in enumerate(document_content["tables"]):
        for row in table:
            match = re.match(pattern, row[0])
            if match:
                key = str(match.group())
                values[key] = re.sub(r'\r+', '\n', row[1])
    return values


def score_dmp_v2(values) -> tuple[float, float, float]:
    """
    Calculate the scores for sections 1 and 4 of the DMP (Data Management Plan) and return the final scores.
    
    Args:
        values (dict): A dictionary containing the values of the DMP sections. The keys are strings representing 
                       the section and question numbers (e.g., '1.1', '1.2', '4.1', etc.), and the values are the 
                       corresponding answers.
    Returns:
        tuple[float, float, float]: A tuple containing three float values:
            - The score for section 1 as a percentage.
            - The score for section 4 as a percentage.
            - The average score of sections 1 and 4 as a percentage.
    """

    # project no data - dmp OK
    temp = parse_checkboxes(values['1.5'])
    if temp['No']:
        return (100, 100, 100)
    
    score_section1 = 0
    temp = project_info(values['1.1'])
    if "Project leader" in temp and "Project number" in temp:
        score_section1 += 2
    temp = parse_checkboxes(values['1.2'])
    if temp['Yes'] or temp['No']:
        score_section1 += 1
    temp = parse_checkboxes(values['1.3'])
    if temp['Yes'] or temp['No']:
        score_section1 += 1
    temp = parse_checkboxes(values['1.4'])
    if temp['Yes'] or temp['No']:
        score_section1 += 1
    temp = parse_checkboxes(values['1.5'])
    if temp['Yes'] or temp['No']:
        score_section1 += 1
    temp = parse_checkboxes(values['1.6'])
    if temp['Yes'] or temp['No']:
        score_section1 += 1
    if len(values['1.7']) > 0 and text_is_not_default(values['1.7']):
        score_section1 += 1
    temp = parse_checkboxes(values['1.8'])
    if temp['Yes'] or temp['No']:
        score_section1 += 1
    temp = parse_checkboxes(values['1.9'])
    if temp['Yes'] or temp['No']:
        score_section1 += 1
    temp = parse_checkboxes(values['1.10'])
    if temp['Yes'] or temp['No']:
        score_section1 += 1
    if len(values['1.11']) > 0 and text_is_not_default(values['1.11']):
        score_section1 += 1
    temp = parse_checkboxes(values['1.12'])
    if temp['Yes'] or temp['No']:
        score_section1 += 1
    temp = parse_checkboxes(values['1.13'])
    if temp['Yes'] or temp['No']:
        score_section1 += 1
    temp = parse_checkboxes(values['1.14'])
    if temp['Yes'] or temp['No']:
        score_section1 += 1
    final_score_section1 = score_section1 / 15 * 100

    score_section4 = 0
    if len(values['4.1']) > 0 and text_is_not_default(values['4.1']):
        score_section4 += 1
    if len(values['4.2']) > 0 and text_is_not_default(values['4.2']):
        score_section4 += 1
    if len(values['4.3']) > 0 and text_is_not_default(values['4.3']):
        score_section4 += 1
    if len(values['4.4']) > 0 and text_is_not_default(values['4.4']):
        score_section4 += 1
    final_score_section4 = score_section4 / 4 * 100

    return (final_score_section1, final_score_section4, 
            (final_score_section1 + final_score_section4) / 2)

def read_and_score_dmp_v2(dmp_file: str) -> tuple[float, float, float]:
    values = read_dmp_file(dmp_file)
    return score_dmp_v2(values)