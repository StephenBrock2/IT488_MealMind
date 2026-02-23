## how to run backend api

### start a virtual environment (optional)

### install libraries
change terminal path to the backend api folder

`pip install -r requirements.txt`

### run the api
`fastapi dev .\main.py`

### access the api on browser
uvicorn main:app --reload
http://127.0.0.1:8000
http://127.0.0.1:8000/docs