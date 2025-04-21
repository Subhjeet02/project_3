import pandas as pd
import os

def concate(list_of_columns,list_of_dict_of_data):
    """
    Concatenate a list of columns values from a dictionary of data into a single string.
    >>> columns = ['name', 'age']
    >>> data = [{'name': 'John', 'age': 30, 'city': 'New York'},{'name': 'Jane', 'age': 25, 'city': 'Los Angeles'},{'name': 'Bob', 'age': 35, 'city': 'Chicago'},{'name': 'Alice', 'city': 'San Francisco'}]
    >>> concate(columns, data)
    ['John 30', 'Jane 25', 'Bob 35', 'Alice ']
    """
    result = []
    for row in list_of_dict_of_data:
        values = [str(row.get(col, '')) for col in list_of_columns]
        result.append(' '.join(values))
    return result

def load_read_xlsx(file_path):
    """
    Load a .xlsx file and return its content as a list of dictionaries.
    >>> load_read_xlsx('test.xlsx')
    [{'name': 'John', 'age': 30, 'city': 'New York'}, {'name': 'Jane', 'age': 25, 'city': 'Los Angeles'}, {'name': 'Bob', 'age': 35, 'city': 'Chicago'}, {'name': 'Alice', 'city': 'San Francisco'}]
    """
    
    df = pd.read_excel(file_path)
    
    # Handle empty DataFrame
    if df.empty:
        return []
        
    # Convert to records and remove NaN values
    records = df.to_dict(orient='records')
    
    # Clean out NaN values from records
    for record in records:
        keys_to_remove = []
        for key, value in record.items():
            if pd.isna(value):
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del record[key]
    
    return records

if __name__ == "__main__":
    import doctest
    doctest.testmod()
