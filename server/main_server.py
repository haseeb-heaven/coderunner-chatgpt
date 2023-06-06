"""
Description: This is ChatGPT Plugin for CodeRunner. Which can run and save code in 70+ languages.
This is a FastAPI Web Server which is used to run the code and return the output.
Server API : FastAPI.
Language: Python.
Date: 16/05/2023.
Author : HeavenHM
"""

# Importing the required libraries.
from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import aiofiles
import requests
import json
import logging
import uvicorn
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from contextvars import ContextVar
import random
import string
import os
from python_runner import exec_python

plugin_url = 'https://coderunner-plugin.haseebmir.repl.co'

# defining the origin for CORS
ORIGINS = [
 plugin_url, "https://chat.openai.com"
]

# Main application for FastAPI Web Server
app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=ORIGINS,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# Mount the .well-known directory.
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")

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
def write_log(log_msg: str):
  try:
    with open('CodeRunner.log', 'a') as f:
      f.write(log_msg + '\n')
  except Exception as e:
    print(str(e))


# Method to configure logs.
def configure_logger(name: str, filename: str):
  try:
    global logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(filename)
    formatter = logging.Formatter(
      '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
  except Exception as e:
    write_log(e)
  return logger


# Setup logging for the application.
logger = configure_logger('CodeRunner', 'CodeRunner.log')


def generate_code_id(response, length=10):
  try:
    characters = string.ascii_letters + string.digits
    unique_id = ''.join(random.choice(characters) for i in range(length))
    response['id'] = unique_id
  except Exception as e:
    write_log(e)
  return response


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


def get_jdoodle_client():
  try:
    index = 1
    logger.info(f"get_jdoodle_client: Getting jdoodle client {index}")
    credits_used = get_credits_used()
    if credits_used < 200:
      logger.info("get_jdoodle_client: return client_1")
      return get_jdoodle_client_1()
    else:
      logger.error("Credits exhaused for client_1")
      logger.info("get_jdoodle_client: return client_2")
  except Exception as e:
    logger.error(f"get_jdoodle_client: {e}")
    return get_jdoodle_client_2()


# Method to call the JDoodle "credit-spent" API.
def get_jdoodle_credit_spent():
  try:
    client_id, client_secret = get_jdoodle_client_1()
    url = "https://api.jdoodle.com/v1/credit-spent"
    headers = {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
    }

    body = {"clientId": client_id, "clientSecret": client_secret}
    logger.info(f"get_jdoodle_credit_spent: sending request with url {url}")
    credit_spent = requests.post(url, headers=headers, data=json.dumps(body))
    logger.info(f"get_jdoodle_credit_spent: {credit_spent}")
  except Exception as e:
    logger.error(f"get_jdoodle_credit_spent: {e}")
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
    write_log(f"set_request_middleware Error: {e}")
  return None


# Method to run the code.
@app.post('/run_code')
async def run_code():
  try:
    request = get_request()
    data = await request.json()
    logger.info(f"run_code: data is {data}")
    script = data.get('script')
    language = data.get('language')

    # Convert the language to the JDoodle language code.
    language_code = lang_codes.get(language, language)
    logger.info(f"run_code: language_code is {language_code}")

    # Run the code locally if the language is python3.
    if language_code == 'python3':
      write_log("Trying to run Python code locally with all Libs installed.")
      graph_file = ""

      # check is script has graphic libraries imported like matplotlib, seaborn, etc.
      if script.find("import matplotlib") != -1 or script.find(
          "import seaborn") != -1 or script.find("import plotly") != -1:
        write_log(
          "Graphic libraries found in script. Trying to run Python code locally with all Libs installed."
        )
        # append save graph method to file.
        graph_file = f"graph_{random.randint(1, 1000)}.png"
        # append data to string called script.
        # replacing the line if it contains show() method
        for line in script.splitlines():
          if line.find("show()") != -1:
            script = script.replace(line, "")
        script = script + "\nplt.savefig('graphs/" + graph_file + "')"

      # run the script again.
      output = exec_python(script)
      if output is None or output == "":
        directory = 'graphs'
        filepath = os.path.join(directory, graph_file)
        logger.info(f"Graph download filename is {filepath}")
        graph_file_path = (plugin_url + '/' + filepath)
        output = graph_file_path
      
      response = {"output": output}
      logger.info(f"run_code: response is {response}")
      return response

    # Declare input and compileOnly optional.
    input = data.get('input', None)
    compile_only = data.get('compileOnly', False)

    # Get the JDoodle client ID and secret.
    client_id, client_secret = get_jdoodle_client()
    compiler_url = "https://api.jdoodle.com/v1/execute"
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

    logger.info(f"run_code: body is {body_filtered}")
    response_data = requests.post(compiler_url,
                                  headers=headers,
                                  data=json.dumps(body))
    response = json.loads(response_data.content.decode('utf-8'))

    # Check reponse status code before appending the code id.
    if response_data.status_code == 200:
      response = generate_code_id(response)

    logger.info(f"run_code: {response}")
  except Exception as e:
    return {"error": str(e)}
  return {"result": response}


# Method to save the code.
@app.post('/save_code')
async def save_code():
  try:
    request = get_request()
    data = await request.json()  # Get JSON data from request
    logger.info(f"save_code: data is {data}")
    filename = data.get('filename')
    code = data.get('code')

    if filename is None or code is None:
      return {"error": "filename or code not provided"}, 400

    directory = 'codes'
    filepath = os.path.join(directory, filename)

    logger.info(f"save_code: filename is {filepath} and code was present")
    async with aiofiles.open(filepath, 'w') as f:
      await f.write(code)
    logger.info(f"save_code: wrote code to file {filepath}")
    download_link = f'{request.url_for("download",filename=filename)}'
    logger.info(f"save_code: download link is {download_link}")
    output = ""
    if download_link:
      output = {"download_link": download_link}
  except Exception as e:
    logger.error(f"save_code: {e}")
  return output


# Method to download the file.
@app.get('/download/{filename}')
async def download(filename: str):
  try:
    # check if file is type of image 
    if filename.find(".png") != -1 or filename.find(".jpg") != -1 or filename.find(".jpeg") != -1:
      directory = 'graphs'
    else:
        directory = 'codes'
    filepath = os.path.join(directory, filename)
    logger.info(f"download filename is {filepath}")
    return FileResponse(filepath, filename=filepath)
  except Exception as e:
    logger.error(f"download: {e}")

# Graphs file.
@app.get('/graphs/{filename}')
async def graphs_dir(filename:str):
  try:
    directory = 'graphs'
    filepath = os.path.join(directory, filename)
    logging.info(f"Graphs filename is {filepath}")
    return FileResponse(filepath, filename=filepath)
  except Exception as e:
    logger.error(f"graphs: {e}")


# Plugin logo.
@app.get("/logo.png")
async def plugin_logo():
  try:
    filename = 'logo.png'
    logging.info(f"logo filename is {filename}")
  except Exception as e:
    logger.error(f"plugin_logo: {e}")
  return FileResponse(filename)


# Plugin manifest.
@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
  try:
    text = ""
    with open("./.well-known/ai-plugin.json") as f:
      text = f.read()
  except Exception as e:
    logger.error(f"plugin_manifest: {e}")
  return Response(text, media_type="text/json")


# Plugin OpenAPI spec.
@app.get("/openapi.yaml")
async def openapi_spec():
  try:
    text = ""
    with open("openapi.yaml") as f:
      text = f.read()
  except Exception as e:
    logger.error(f"openapi_spec: {e}")
  return Response(text, media_type="text/yaml")


def get_credits_used():
  try:
    logger.info("get_credits_used: called")
    response = get_jdoodle_credit_spent()
    credit_spent = response.json()
    credits_used = 0
    logger.info(f"get_credits_used response : {credit_spent}")

    if credit_spent:
      credits_used = credit_spent['used']
      logger.info(f"get_credits_used Credits used: {credits_used}")

    return credits_used
  except Exception as e:
    write_log("Exception in get_credits_used: " + str(e))


@app.get('/credit_limit')
def show_credits_spent():
  credit_spent = 0
  try:
    credits_used = get_credits_used()
    return {"credits:": credits_used}
  except Exception as e:
    return {"error": str(e)}


@app.get('/help')
@app.get('/')
async def help():
  write_log("help: Displayed for Plugin Guide")
  json_data = {
    "title":
    "Code Runner Guide",
    "features": [{
      "name": "Run Code",
      "description": "Runs the code in the current editor."
    }, {
      "name":
      "Save Code",
      "description":
      "Saves the code in the current editor to a file."
    }, {
      "name":
      "Download Code",
      "description":
      "Downloads the code in the current editor to a file."
    }],
    "prompts": [{
      "name":
      "Write me C++ program for factorial of number and Run the program.",
      "description":
      "Writes a C++ program for factorial of number and runs the program."
    }, {
      "name": "Given the program [YOUR_CODE] and only compile the program.",
      "description": "Compiles the program [YOUR_CODE]."
    }, {
      "name":
      "Save the program [YOUR_CODE] with filename [YOUR_FILENAME].",
      "description":
      "Saves the program [YOUR_CODE] with filename [YOUR_FILENAME]."
    }, {
      "name":
      "Download the code  filename [YOUR_FILENAME].",
      "description":
      "Downloads the code with filename [YOUR_FILENAME]."
    }]
  }
  return json_data


def make_dirs():
  if not os.path.exists('codes'):
    os.makedirs('codes')
  if not os.path.exists('graphs'):
    os.makedirs('graphs')


# Run the app.
# Will only work with python main.py
if __name__ == "__main__":
  try:
    write_log("Starting CodeRunner")

    #logger = configure_logger('CodeRunner', 'CodeRunner.log')
    write_log("Logger configured")

    # Create missing directories
    make_dirs()

    uvicorn.run("main:app", host='0.0.0.0', port=8080,reload=True)
    write_log("CodeRunner started")
  except Exception as e:
    write_log(str(e))