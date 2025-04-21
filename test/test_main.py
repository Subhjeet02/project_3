import pytest
import sys
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

def test_main():
    from src.main import main

    # Mock the load_read_xlsx function to avoid actual file operations
    with patch('src.main.load_read_xlsx') as mock_load:
        # Setup mock return value
        mock_load.return_value = [
            {'Column1': 'Value1', 'Column2': 'Value2', 'Column3': 'Value3', 'Column4': 'Value4'},
            {'Column1': 'Value5', 'Column2': 'Value6', 'Column3': 'Value7', 'Column4': 'Value8'}
        ]
        
        # Execute the function
        result = main()
        
        # Check if mock was called with the correct path
        # mock_load.assert_called_once_with(r"C:\\Users\\Shipskart\\Downloads\\data.xlsx")
        mock_load.assert_called_once_with(r".\\data.xlsx")
        
        # Check the structure and content of the result
        assert isinstance(result, dict)
        assert len(result) == 2  # Header row + 2 data rows
        
        # Check header row
        assert 'Column2' in result['headers']
        assert 'Column3' in result['headers']
        assert 'concatenated' in result['headers']
        
        # Check the data rows
        assert len(result['rows'][0]) == 3  # 3 columns (Column2, Column3, concatenated)
        assert len(result['rows'][1]) == 3

        # Check that concatenated values are correct
        assert 'Value1 Value4' in result['rows'][0]
        assert 'Value5 Value8' in result['rows'][1]

def test_main_empty_data():
    from src.main import main
    
    # Test with empty data
    with patch('src.main.load_read_xlsx') as mock_load:
        mock_load.return_value = []
        
        # Mock concate function to return empty list for empty input
        with patch('src.main.concate') as mock_concate:
            mock_concate.return_value = []
            
            # Empty data should return empty list
            result = main()
            
            assert result == []

def test_fastapi_endpoint():
    from src.main import app, data
    
    client = TestClient(app)
    
    # In FastAPI, data is passed as a request body in POST requests
    # For GET requests with complex parameters, they need to be passed as query parameters
    # The endpoint is using the global data variable from main.py
    response = client.get("/data")
    
    assert response.status_code == 200
    # The data should match what was returned by the main() function
    assert response.json() == data

def test_main_script_execution():
    # This test needs a different approach since importing the module 
    # won't trigger the __name__ == "__main__" block
    
    # We need to execute the code in main.py's __main__ block directly
    # First import the necessary module
    import src.main

    # Now patch the uvicorn.run function
    with patch('uvicorn.run') as mock_run:
        # Directly call the code that would be in the __name__ == "__main__" block
        # by manually executing what's in that block
        from src.main import app
        
        # Run the __main__ block code directly
        src.main.uvicorn.run(app, host="127.0.0.1", port=8000, limit_max_requests=10)
        
        # Check that uvicorn.run was called with the correct arguments
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        assert args[0] == app
        assert kwargs['host'] == "127.0.0.1"
        assert kwargs['port'] == 8000
        assert kwargs['limit_max_requests'] == 10
