import pytest

from dmpt.tools.find_version_number import find_version_number


# Use pytest.mark.parametrize to test multiple inputs.
@pytest.mark.parametrize("filename, expected_major_version, expected_minor_version", [
    ("123456789-BGS_v1.1-data-management-plan.docx", 1, 1),
    ("123456789-GEO_v1.2-data-management-plan.docx", 1, 2),
    ("123456789-HYE_v1.3-data-management-plan.docx", 1, 3),
    ("123456789-ZKS_v2.4-data-management-plan.docx", 2, 4),
    ("123456789-ZWS_v2.9-data-management-plan.docx", 2, 9),
    ("123456789-DSC_v5.10-data-management-plan.docx", 5, 10),
    ("123456789-BGS_v10.100-data-management-plan.docx", 10, 100)
])
def test_find_version_number(filename: str, expected_major_version: str, expected_minor_version: str) -> None:
    major_version, minor_version = find_version_number(filename)
    assert major_version == expected_major_version
    assert minor_version == expected_minor_version


@pytest.mark.parametrize("filename", [
    ("randomfile.docx"),  # Case where no match is expected.
    (""),  # Empty string
    ("vasds"),  # 'v' but no version number
    ("v1asds")  # 'v' but no version number
])
def test_find_version_number_exception(filename: str) -> None:
    with pytest.raises(ValueError):
        find_version_number(filename)
