import json
import aiofiles
import requests
import quart
import quart_cors
from quart import request, render_template_string, send_file
import logging
# Main Quart app.
# Quart is a Python ASGI web microframework with the same API as Flask. 
# It is intended to provide the easiest way to use asyncio in a web context, especially with existing Flask apps.

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")
LANGUAGE_CODES = {
    'C': 'c',
    'C++': 'cpp',
    'Java': 'java',
    'Ruby': 'ruby',
    'Scala': 'scala',
    'C#': 'csharp',
    'Objective C': 'objc',
    'Swift': 'swift',
    'JavaScript': 'nodejs',
    'Kotlin': 'kotlin',
    'Python': 'python3',
    'GO Lang': 'go',
}

@app.route('/run_code', methods=['POST'])
async def run_code():
    data = await request.get_json()  # Get JSON data from request
    script = data.get('script')
    language = data.get('language')
    # Convert language to JDoodle language code
    #language=LANGUAGE_CODES[language]
    
    # Declare input and compileOnly optional.
    input = data.get('input', None)
    compileOnly = data.get('compileOnly', False)
    
    logs = []  # List to store log messages
    try:
        # Replace these with your actual JDoodle client ID and secret
        clientId = "693e67ab032c13c90ff01e3dca2c6117"
        clientSecret = "c8870a789a35e4882de3b383789e08011a1456e88dc5889261748d4b01d4a79d"
        compilerApiUrl = "https://api.jdoodle.com/v1/execute"
        headers = {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        }
        logs.append(f"CodeRunner: code is '{script}' and language is '{language}'")
        body = {
            'clientId': clientId,
            'clientSecret': clientSecret,
            'script': script,
            'language': language,
            'stdin':input,
            'compileOnly': compileOnly,
            'versionIndex': '0',
        }
        logs.append(f"CodeRunner: body is {body}")
        response = requests.post(compilerApiUrl, headers=headers, data=json.dumps(body))
        logs.append(f"CodeRunner: response is {response}")
    except Exception as e:
        return {"error": str(e), "logs": logs}, 400
    return {"result": response.json(), "logs": logs}


from quart import Response, stream_with_context
import base64
from quart import Response

api_key = '8r9xowq-IugV3EaScZ5dRbWHhNpQd7_9'

@app.route('/save_code', methods=['POST'])
async def save_code():
    data = await request.get_json() # Get JSON data from request
    filename = data.get('filename')
    code = data.get('code')
    if filename is None or code is None:
        return {"error": "filename and code are required"}, 400

    logger = logging.getLogger(__name__)
    logger.info(f"CodeRunner: filename is {filename} and code was present")

    # Upload the file to Pastebin
    data = {
        'api_dev_key': api_key,
        'api_option': 'paste',
        'api_paste_code': code,
        'api_paste_name': filename,
        'api_paste_format': 'cpp',
        'api_paste_private': '0',
        'api_paste_expire_date': 'N'
    }
    logger.info(f"CodeRunner: uploading file to Pastebin\n{data}")
    response = requests.post('https://pastebin.com/api/api_post.php', data=data)
    logger.info(f"CodeRunner: response from Pastebin is {response}")

    if response.status_code == 200:
        paste_url = response.text
        download_url = paste_url.replace('.com/', '.com/raw/')
        logger.info(f"CodeRunner: download URL is {download_url}")

        # Return the download URL in the response
        return download_url
    else:
        logger.error(f"CodeRunner: error uploading file: {response.text}")
        return {"error": "error uploading file"}, 400


@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
