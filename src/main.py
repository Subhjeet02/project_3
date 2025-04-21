from fastapi import FastAPI
import uvicorn
from src.helper import load_read_xlsx, concate

def main():
    # Load the data from the xlsx file
    # data = load_read_xlsx( r"C:\\Users\\Shipskart\\Downloads\\data.xlsx" )
    data = load_read_xlsx(r".\\data.xlsx")
    print("data",data)
    
    # If data is empty, return empty list
    if not data:
        return []
        
    # Concatenate the data into a single list of lists
    column_to_concat = [ "Column1" , "Column4" ]
    print("column_to_concat",column_to_concat)
    # Concatenate the data into a single list of lists
    concatenated_column_data = concate( column_to_concat, data )
    print("concatenated_column_data",concatenated_column_data)

    # remove the column names from the data which are not in the column_to_concat
    for row in data:
        for key in list(row.keys()):
            if key  in column_to_concat:
                del row[key]

    print("data",data)

    # Add the concatenated column data to the data
    for i in range( len( data ) ):
        data[i][ "concatenated" ] = concatenated_column_data[ i ]
    print("data",data)


    rows = []
    headers = []
    # Append the keys as the first row of the result
    headers = list( data[0].keys() ) 

    # Convert the data to a list of lists
    for row in data:
        rows.append( list( row.values() ) )
    
    result = {"headers": headers, "rows": rows}

    print("result",result)

    return result

data = main()

print("data",data)
app = FastAPI()


@app.get("/data")
async def send_data_internal():
    # Using the global data variable
    return data

if __name__ == "__main__":
    # Run the FastAPI app with Uvicorn server
    uvicorn.run( app , host="127.0.0.1" , port = 8000 , limit_max_requests = 10 )