import json
import requests
import quart
import quart_cors
from quart import request, render_template_string
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


# Define the /save_code endpoint
@app.post("/save_code")
def save_code():
    # Implement your code saving logic here
    pass

# Generate Dynamic HTML for JDoodle Compiler iFrame Embedding.
@app.post("/dynamic_code")
async def generate_dynamic_html():
    logger = logging.getLogger(__name__)
    data = await request.get_json()  # Get JSON data from request
    language = data.get('language')
    code = data.get('code')
    logger.info("Generating dynamic HTML for language: %s", language)
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Python App with JavaScript</title>
    </head>
    <body>
        <div data-pym-src='https://www.jdoodle.com/plugin' data-language="{language}"
            data-version-index="0" data-libs="">
            {script_code}
        </div>
        <script src="https://www.jdoodle.com/assets/jdoodle-pym.min.js" type="text/javascript"></script>
    </body>
    </html>
    """.format(language=language, script_code=code)
    return await render_template_string(html_template)

@app.route('/form', methods=['GET'])
async def form():
    form_html = """
    <form action="https://www.jdoodle.com/api/redirect-to-post/online-java-compiler" method="post">
      Script: <textarea name="initScript" rows="8" cols="80"></textarea>
      <input type="submit" value="Submit">
    </form>
    """
    return await render_template_string(form_html)

#Method for testing. Remove later
@app.get("/")
def root_url():
    # The URL of the /run_code endpoint
    url = "http://localhost:8000/run_code"

    # The headers for the POST request to the /run_code endpoint
    headers = {"Content-Type": "application/json"}

    # The body of the POST request to the /run_code endpoint
    data = {
        "script": "print('Value is ' + input())",
        "language": "python3",
        "input": "Hello, Cppz!",
        "compileOnly": False,
    }
    
    print(f"Main Url is {url} and headers is {headers} and data is {data}")
    # Make the POST request to the /run_code endpoint
    response = requests.post(url, headers=headers, json=data)
    print(f"Response is {response}")
    # Print the response from the /run_code endpoint
    return response.json()

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
