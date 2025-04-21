import pytest
import pandas as pd
import tempfile 
import os
from src.helper import concate, load_read_xlsx
# Test cases for the concat function

def test_concate_normal_case():
    columns = ['name', 'age']
    data = [
        {'name': 'John', 'age': 30, 'city': 'New York'},
        {'name': 'Jane', 'age': 25, 'city': 'Los Angeles'},
        {'name': 'Bob', 'age': 35, 'city': 'Chicago'},
        {'name': 'Alice', 'city': 'San Francisco'}
    ]
    expected = ['John 30', 'Jane 25', 'Bob 35', 'Alice ']
    assert concate(columns, data) == expected

def test_concate_missing_all_columns():
    columns = ['name', 'age']
    data = [{'city': 'Seattle'}]
    expected = [' ']
    assert concate(columns, data) == expected

def test_concate_empty_data():
    columns = ['name', 'age']
    data = []
    expected = []
    assert concate(columns, data) == expected

def test_concate_empty_columns():
    columns = []
    data = [{'name': 'John', 'age': 30}]
    expected = ['']
    assert concate(columns, data) == expected

def test_concate_non_string_values():
    columns = ['id', 'valid']
    data = [{'id': 101, 'valid': True}, {'id': 102, 'valid': False}]
    expected = ['101 True', '102 False']
    assert concate(columns, data) == expected



# ✅ 1. Happy path: valid data
def test_load_read_xlsx_valid():
    test_data = [
        {'name': 'John', 'age': 30, 'city': 'New York'},
        {'name': 'Jane', 'age': 25, 'city': 'Los Angeles'},
        {'name': 'Bob', 'age': 35, 'city': 'Chicago'},
        {'name': 'Alice', 'city': 'San Francisco'}
    ]

    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        pd.DataFrame(test_data).to_excel(tmp.name, index=False)
        result = load_read_xlsx(tmp.name)

    os.remove(tmp.name)
    assert result == test_data

# ⚠️ 2. Missing column in one or more rows
def test_load_read_xlsx_missing_columns():
    test_data = [
        {'name': 'Alice', 'city': 'Seattle'},  # missing 'age'
        {'name': 'Tom', 'age': 40, 'city': 'Miami'}
    ]

    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        pd.DataFrame(test_data).to_excel(tmp.name, index=False)
        result = load_read_xlsx(tmp.name)

    os.remove(tmp.name)
    assert result == test_data

# ❌ 3. Empty file
def test_load_read_xlsx_empty_file():
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        # Save an empty dataframe
        pd.DataFrame().to_excel(tmp.name, index=False)

        result = load_read_xlsx(tmp.name)

    os.remove(tmp.name)
    assert result == []  # Expecting an empty list

# ❌ 4. File with only headers
def test_load_read_xlsx_only_headers():
    headers = ['name', 'age', 'city']
    df = pd.DataFrame(columns=headers)

    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        df.to_excel(tmp.name, index=False)
        result = load_read_xlsx(tmp.name)

    os.remove(tmp.name)
    assert result == []

# ❌ 5. Non-existent file
def test_load_read_xlsx_non_existent_file():
    with pytest.raises(FileNotFoundError):
        load_read_xlsx("non_existent_file.xlsx")

# ❌ 6. Corrupted or non-Excel file
def test_load_read_xlsx_invalid_format():
    with tempfile.NamedTemporaryFile(suffix=".xlsx", mode='w', delete=False) as tmp:
        tmp.write("This is not a valid Excel content")

    with pytest.raises(Exception):
        load_read_xlsx(tmp.name)

    os.remove(tmp.name)