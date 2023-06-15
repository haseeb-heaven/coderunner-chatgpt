"""
Description: This is ChatGPT Plugin for CodeRunner. Which can run and save code in 70+ languages.
This is a FastAPI Web Server which is used to run the code and return the output.
Server API : FastAPI.
Language: Python.
Date: 14/06/2023.
Author : HeavenHM
"""

# Importing the required libraries.
from datetime import datetime
from io import StringIO
import io
import traceback
from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse,StreamingResponse,RedirectResponse,JSONResponse,HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
import gridfs
import requests
import json
import uvicorn
from pathlib import Path
from starlette.requests import Request
from contextvars import ContextVar
import random
import string
import os
from lib.mongo_db import MongoDB
from lib.python_runner import exec_python,execute_code

# defining the url's
plugin_url = "https://code-runner-plugin.vercel.app"
chatgpt_url = "https://chat.openai.com"
credit_spent_url = "https://api.jdoodle.com/v1/credit-spent"
compiler_url = "https://api.jdoodle.com/v1/execute"


# setting the database.
global database
database = None

try:
  # setting the database
  database = MongoDB()
except Exception as e:
  print("Exception while connecting to the database : " + str(e))
  

#defining the origin for CORS
ORIGINS = [
 plugin_url ,chatgpt_url
]

# Defining the app.
app = FastAPI(openapi_url=None,docs_url="/docs")    
app.add_middleware(
  CORSMiddleware,
  allow_origins=ORIGINS,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# Mount the .well-known directory.
#app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")

# Context variable to store the request.
# Credit - https://sl.bing.net/ib0YUGReKZg
request_var: ContextVar[Request] = ContextVar("request")

# JDoodle language codes.
# Credit - https://sl.bing.net/jbo456vZ8Eu
lang_codes = {
  'java': 'java',
  'c': 'c',
  'c++': 'cpp14',
  'cpp': 'cpp17',
  'php': 'php',
  'perl': 'perl',
  'python': 'python3',
  'ruby': 'ruby',
  'go': 'go',
  'scala': 'scala',
  'bash': 'bash',
  'sql': 'sql',
  'pascal': 'pascal',
  'csharp': 'csharp',
  'vbnet': 'vbn',
  'haskell': 'haskell',
  'objectivec': 'objc',
  'swift': 'swift'
}

# Method to write logs to a file.
def write_log(log_msg:str):
  try:
    print(str(datetime.now()) + " " + log_msg)
  except Exception as e:
    print(str(e))


def generate_code_id(length=10):
  try:
    characters = string.ascii_letters + string.digits
    unique_id = ''.join(random.choice(characters) for i in range(length))
    return unique_id
  except Exception as e:
    write_log(e)
    return ""

# Method to get the JDoodle client ID and secret.
def get_jdoodle_client_1():
  client_id = '{}{}{}{}{}'.format('693e67ab', '032c', str(int('13')), 'c9',
                                  '0ff01e3dca2c6' + str(int('117')))
  client_secret = '{}{}{}{}{}{}{}{}'.format('c8870a78', '9a35e488', '2de3b383',
                                            '789e0801', '1a1456e8', '8dc58892',
                                            '61748d4b', '01d4a79d')
  return client_id, client_secret


def get_jdoodle_client_2():
  client_id = '{}{}{}{}'.format('e0c1fdfe', '9506fe7e', '35186a25', '9e36e5f5')
  client_secret = '{}{}{}{}{}{}'.format('e19a110c', '7ce8934c', '4f78017a',
                                        'acb55073', 'e3a0670c',
                                        'b871442dfcc40e28a40f66b3')
  return client_id, client_secret

# Method to get the JDoodle client.
def get_jdoodle_client():
  try:
    index = 1
    write_log(f"get_jdoodle_client: Getting jdoodle client {index}")
    credits_used = get_credits_used()
    if credits_used < 200:
      write_log("get_jdoodle_client: return client_1")
      return get_jdoodle_client_1()
    else:
      write_log("Credits exhaused for client_1")
      write_log("get_jdoodle_client: return client_2")
  except Exception as e:
    write_log(f"get_jdoodle_client: {e}")
    return get_jdoodle_client_2()


# Method to call the JDoodle "credit-spent" API.
def get_jdoodle_credit_spent():
  try:
    client_id, client_secret = get_jdoodle_client_1()
    headers = {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
    }

    body = {"clientId": client_id, "clientSecret": client_secret}
    write_log(f"get_jdoodle_credit_spent: sending request with url {credit_spent_url}")
    credit_spent = requests.post(credit_spent_url, headers=headers, data=json.dumps(body))
    write_log(f"get_jdoodle_credit_spent: {credit_spent}")
  except Exception as e:
    write_log(f"get_jdoodle_credit_spent: {e}")
  return credit_spent


# Helper method to get the request.
def get_request():
  try:
    return request_var.get()
  except Exception as e:
    write_log(f"get_request: {e}")


def set_request(request: Request):
  try:
    request_var.set(request)
  except Exception as e:
    write_log(f"set_request: {e}")


@app.middleware("http")
async def set_request_middleware(request: Request, call_next):
    try:
        set_request(request)
        response = await call_next(request)
        return response
    except Exception as e:
        write_log(f"set_request_middleware: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Define a method to save the plot in mongodb
def save_plot(filename):
    output = {}
    global database
    write_log(f"save_plot: executed script")
    
    # Save the plot as an image file in a buffer
    buffer = io.BytesIO()
    write_log(f"save_plot: saving plot")
    
    # Using matplotlib to save the plot as an image file in a buffer
    import matplotlib.pyplot as plt
    plt.savefig(buffer, format='png')
    write_log(f"save_plot: saved plot")

    # Get the gridfs bucket object from the database object with the bucket name 'graphs'
    bucket = gridfs.GridFSBucket(database.db, bucket_name='graphs')
    write_log(f"save_plot: got gridfs bucket object")
    
    # Store the image file in mongodb using the bucket object
    file_id = bucket.upload_from_stream(filename, buffer.getvalue())
    write_log(f"save_plot: stored image file in mongodb")
    # Return the file id
    return output

# Method to run the code.
@app.post('/run_code')
async def run_code():
  try:
    request = get_request()
    data = await request.json()
    write_log(f"run_code: data is {data}")
    script = data.get('code')
    language = data.get('language')

    # Convert the language to the JDoodle language code.
    language_code = lang_codes.get(language, language)
    write_log(f"run_code: language code is {language_code}")

    # Run the code locally if the language is python3.
    if language_code == 'python3':
      response = {}
      try:
        write_log("Trying to run Python code locally with all Libs installed.")
        graph_file = ""
        contains_graph = False

        # check is script has graphic libraries imported like matplotlib, seaborn, etc.
        if any(library in script for library in ['import matplotlib', 'import seaborn', 'import plotly']):
          write_log("Graphic libraries found in script. Trying to run Python code locally with all Libs installed.")
          
          # check if script contains "show()" method.
          if any(method in script for method in ['show()', 'plt.show()', 'pyplot.show()']):
            contains_graph = True
            # generate random name for graph file.
            graph_file = f"graph_{random.randrange(1, 100000)}.png"

            # replacing the line if it contains show() method
            script = "\n".join([line for line in script.splitlines() if "show()" not in line])
          
            response = execute_code(script)
            write_log(f"run_code: executed script")
            
            # Save the plot as an image file in a buffer
            if contains_graph:
              write_log(f"run_code: saving plot")
              response = save_plot(graph_file)

            if response.__len__() == 0 and contains_graph:
              response = {"success":f"{plugin_url}/download/{graph_file}"}
            else:
              response = {"result": response}
              
            # Return the response as JSON
            write_log(f"run_code: response is {response}")
        else:
          write_log(f"run_code: running script locally no graphic libraries found")
          response = execute_code(script)
          return {"result": response}
        return response
      except Exception as e:
        stack_trace = traceback.format_exc()
        write_log(f"run_code: failed to execute script: {e}\nStack: {stack_trace}")
        raise e


    # Declare input and compileOnly optional.
    input = data.get('input', None)
    compile_only = data.get('compileOnly', False)

    # Get the JDoodle client ID and secret.
    client_id, client_secret = get_jdoodle_client()
    headers = {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
    }

    body = {
      'clientId': client_id,
      'clientSecret': client_secret,
      'script': script,
      'language': language_code,
      'stdin': input,
      'compileOnly': compile_only,
      'versionIndex': '0',
    }
    # Filter out the client ID, client secret from the body.
    body_filtered = {
      k: v
      for k, v in body.items() if k not in ['clientId', 'clientSecret']
    }

    write_log(f"run_code: body is {body_filtered}")
    response_data = requests.post(compiler_url,headers=headers,data=json.dumps(body))
    response = json.loads(response_data.content.decode('utf-8'))

    # Check reponse status code before appending the code id.
    if response_data.status_code == 200:
      unique_id = generate_code_id(response)
      response['id'] = unique_id

    write_log(f"run_code: {response}")
  except Exception as e:
    return JSONResponse({"error": str(e)}, status_code=500)
  return JSONResponse(response)


# Method to save the code.
@app.post('/save_code')
async def save_code():
  try:
    global database
    write_log(f"save_code: database is {database}")
    # check if database is connected
    if database is None:
      write_log(f"save_code: database is not connected")
      database = setup_database()
      write_log(f"save_code: database is {database}")
    
    request = get_request()
    data = await request.json()  # Get JSON data from request
    write_log(f"save_code: data is {data}")
    filename = data.get('filename')
    code = data.get('code')
    code_id = generate_code_id()
    language = filename.split('.')[-1]

    if filename is None or code is None:
      return {"error": "filename or code not provided"}, 400

    directory = 'codes'
    filepath = os.path.join(directory, filename)

    write_log(f"save_code: filename is {filepath} and code was present")
    
    # Saving the code to database
    if database is not None:
      database.save_code(code,language,code_id,filename)
    else:
      write_log(f"Database not connected {database}")
      return {"error": "Database not connected"}
    
    write_log(f"save_code: wrote code to file {filepath}")
    download_link = f'{request.url_for("download",filename=filename)}'
    write_log(f"save_code: download link is {download_link}")
    output = ""
    if download_link:
      output = {"download_link": download_link}
  except Exception as e:
    write_log(f"save_code: {e}")
  return output

# Create a route to save the file either document or image into database and return its url.
# Create a route to save the file with filename and its data into database and return its url.
@app.post('/upload')
async def upload():
  try:
    global database
    # get the request data
    request = get_request()
    data = await request.json()
    write_log(f"upload: data is {data}")
    
    # get the filename and data from the request
    filename = data.get('filename')
    file_data = data.get('data')
    
    # check the file extension using os.path.splitext
    file_extension = os.path.splitext(filename)[1].lower()
    write_log(f"upload: file extension is {file_extension}")
    
    # save the file in the database according to the extension
    if file_extension in ['.png', '.jpg', '.jpeg', '.gif']:
      write_log(f"upload: image filename is {filename}")
      # convert the data to bytes
      contents = bytes(file_data, 'utf-8')
      # save the file in the database
      database.img.put(contents, filename=filename)
      write_log(f"upload: saved image to database")
      # return the download link
      return {"download_link": f"{plugin_url}/download/{filename}"}
    
    elif file_extension in ['.pdf', '.doc', '.docx','.csv','.xls','.xlsx','.txt','.json']:
      write_log(f"upload: code filename is {filename}")
      # convert the data to bytes
      contents = bytes(file_data, 'utf-8')
      # save the file in the database
      database.docs.put(contents, filename=filename)
      write_log(f"upload: saved code to database")
      # return the download link
      return {"download_link": f"{plugin_url}/download/{filename}"}
  except Exception as e:
    write_log(f"upload: {e}")
    return JSONResponse(status_code=500, content={"error": str(e)})


# Method to download the file.
@app.get('/download/{filename}')
async def download(filename: str):
  try:
    global database
    # check the file extension
    if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
      
      write_log(f"download: image filename is {filename}")
      # get the file-like object from gridfs by its filename
      file = database.graphs.find_one({"filename": filename})
      
      # check if the file exists
      if file:
        # create a streaming response with the file-like object
        response = StreamingResponse(file, media_type="image/png")
        # set the content-disposition header to indicate a file download
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        return response
      else:
        write_log(f"download: failed to get file by filename {filename}")
        # handle the case when the file is not found
        return {"error": "File not found"}
      
    elif filename.endswith(('.pdf', '.doc', '.docx','.csv','.xls','.xlsx','.txt','.json')):
      write_log(f"download: document filename is {filename}")
      file = database.docs.find_one({"filename": filename})
      
      # check if the file exists
      if file:
        write_log(f"download: document filename is {filename}")
        # create a streaming response with the file-like object
        response = StreamingResponse(file, media_type="text/plain")
        # set the content-disposition header to indicate a file download
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        return response
    
    else:
      write_log(f"download: code filename is {filename}")
      # get the code from the database by its filename
      code = database.find_code(filename)
      
      # create a file-like object with the code
      if code:
        code_file = StringIO(code)
        
        if code_file:
          # create a streaming response with the file-like object
          response = StreamingResponse(code_file, media_type="text/plain")
          # set the content-disposition header to indicate a file download
          response.headers["Content-Disposition"] = f"attachment; filename={filename}"
          return response
        else:
          write_log(f"download: failed to get code by filename {filename}")
          # handle the case when the file is not found
          return {"error": "File not found"}
      
      else:
        write_log(f"download: failed to get code by filename {filename}")
        # handle the case when the file is not found
        return {"error": "File not found"}
      return response
  except Exception as e:
    write_log(f"download: {e}")
    return JSONResponse(status_code=500, content={"error": str(e)})


from fastapi.responses import JSONResponse
from functools import lru_cache

# Cache the logo file
@lru_cache(maxsize=1)
def read_logo_file():
    with open("logo.png", "rb") as f:
        return f.read()

# Cache the manifest file
@lru_cache(maxsize=1)
def read_manifest_file():
    with open("./.well-known/ai-plugin.json", "r") as f:
        return f.read()

# Cache the OpenAPI specification file
@lru_cache(maxsize=1)
def read_openapi_file():
    with open("openapi.json", "r") as f:
        return f.read()

# Plugin logo
@app.get("/logo.png", response_class=FileResponse)
async def plugin_logo():
    return FileResponse(Path("logo.png"), content=read_logo_file())

@app.get("/.well-known/ai-plugin.json", response_class=JSONResponse)
async def plugin_manifest():
    return JSONResponse(content=read_manifest_file())

@app.get("/openapi.json", response_class=JSONResponse)
async def openapi_spec():
    return JSONResponse(content=read_openapi_file())



# Docs for the plugin.
@app.get("/docs", include_in_schema=False)
async def plugin_docs():
  try:
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Code Runner Docs",
    )
  except Exception as e:
    write_log(f"plugin_docs: {e}")

def get_credits_used():
  try:
    write_log("get_credits_used: called")
    response = get_jdoodle_credit_spent()
    credit_spent = response.json()
    credits_used = 0
    write_log(f"get_credits_used response : {credit_spent}")

    if credit_spent:
      credits_used = credit_spent['used']
      write_log(f"get_credits_used Credits used: {credits_used}")

    return credits_used
  except Exception as e:
    write_log("Exception in get_credits_used: " + str(e))


@app.get('/credit_limit')
def show_credits_spent():
  try:
    credits_used = get_credits_used()
    return {"credits:": credits_used}
  except Exception as e:
    return JSONResponse(status_code=500, content={"error": str(e)})


@app.get('/help')
@app.get('/')
async def help():
  write_log("help: Displayed for Plugin Guide")
  # how to redirect to /docs
  return RedirectResponse(url='/docs', status_code=302)

# Define a single method that reads the HTML content from a file and returns it as a response
@app.get("/privacy")
def privacy_policy():
    # Define the file name
    file_name = "privacy/privacy.html"
    # Read the file content as a string
    with open(file_name, "r") as f:
        html_content = f.read()
        write_log("privacy_policy Content read success")
    # Return the HTML content as a response
    return HTMLResponse(content=html_content)

def make_dirs():
  if not os.path.exists('codes'):
    os.makedirs('codes')

def setup_database():
  try:
      database = MongoDB()
      write_log(f"Database connected successfully {database}")
      return database
  except Exception as e:
    write_log(str(e))

# Run the app.
# Will only work with python script.py
if __name__ == "__main__":
  try:
    write_log("CodeRunner starting")
    uvicorn.run(app)
    write_log("CodeRunner started")
  except Exception as e:
    write_log(str(e))

