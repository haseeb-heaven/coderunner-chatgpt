import json
import aiofiles
import requests
import quart
import quart_cors
from quart import request,send_file
import logging


# Quart is a Python ASGI web microframework with the same API as Flask. 
app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

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

# Method to get the JDoodle client ID and secret.
def get_jdoodle_client():
    clientId = '{}{}{}{}{}'.format('693e67ab', '032c', str(int('13')), 'c9', '0ff01e3dca2c6' + str(int('117')))
    clientSecret = '{}{}{}{}{}{}{}{}'.format('c8870a78', '9a35e488', '2de3b383', '789e0801', '1a1456e8', '8dc58892', '61748d4b', '01d4a79d')
    return clientId, clientSecret

# Method to run the code.
@app.route('/run_code', methods=['POST'])
async def run_code():
    data = await request.get_json()  # Get JSON data from request
    script = data.get('script')
    language = data.get('language')
    
    # Convert the language to the JDoodle language code.
    language_code = lang_codes.get(language, language)

    # Declare input and compileOnly optional.
    input = data.get('input', None)
    compileOnly = data.get('compileOnly', False)
    
    logs = []  # List to store log messages
    try:
        # Get the JDoodle client ID and secret.
        clientId, clientSecret = get_jdoodle_client()
        compilerApiUrl = "https://api.jdoodle.com/v1/execute"
        headers = {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        }
        
        body = {
            'clientId': clientId,
            'clientSecret': clientSecret,
            'script': script,
            'language': language_code,
            'stdin':input,
            'compileOnly': compileOnly,
            'versionIndex': '0',
        }
        body_filtered = {k: v for k, v in body.items() if k not in ['clientId', 'clientSecret','script']}

        logs.append(f"CodeRunner: body is {body_filtered}")
        response = requests.post(compilerApiUrl, headers=headers, data=json.dumps(body))
        logs.append(f"CodeRunner: response is {response}")
    except Exception as e:
        return {"error": str(e), "logs": logs}, 400
    return {"result": response.json(), "logs": logs}

# Method to save the code.
@app.route('/save_code', methods=['POST'])
async def save_code():
    data = await request.get_json() # Get JSON data from request
    filename = data.get('filename')
    code = data.get('code')
    if filename is None or code is None:
        return {"error": "filename or code not provided"}, 400

    logger = logging.getLogger(__name__)
    logger.info(f"CodeRunner: SaveCode filename is {filename} and code was present")
    async with aiofiles.open(filename, 'w') as f:
        await f.write(code)
    logger.info("CodeRunner: wrote code to file")

    download_link = f'{request.host_url}download/{filename}'
    logger.info(f"CodeRunner: download link is {download_link}")
    output = ""
    if download_link:
        output = {"download_link": download_link}
    return output

# Method to download the file.
@app.get('/download/<filename>')
async def download(filename):
    return await send_file(filename, as_attachment=True, attachment_filename=filename)

# Plugin logo.
@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

# Plugin manifest.
@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

# Plugin OpenAPI spec.
@app.get("/openapi.yaml")
async def openapi_spec():
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

# Run the app.
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
