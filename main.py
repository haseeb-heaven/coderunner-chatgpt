import json
import aiofiles
import requests
import quart
import quart_cors
from quart import request,send_file
import logging


# Quart is a Python ASGI web microframework with the same API as Flask. 
app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

@app.route('/run_code', methods=['POST'])
async def run_code():
    data = await request.get_json()  # Get JSON data from request
    script = data.get('script')
    language = data.get('language')

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

@app.get('/download/<filename>')
async def download(filename):
    return await send_file(filename, as_attachment=True, attachment_filename=filename)

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
