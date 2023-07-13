"""
Description: This use API for Carbon.sh which is a code snippet generator for developers.
Carbon.sh is a website that allows you to generate beautiful images of your source code. visit https://carbon.sh/ for more information.
Server API : REST.
Language: Javascript.
Author : Peter Solopov (https://github.com/petersolopov)
Github : https://github.com/petersolopov/carbonara
"""

from datetime import datetime
from quart import jsonify
import requests
import json
import gridfs
import random

class Carbonara:
    def __init__(self, database):
        # defining the url's
        self.plugin_url = "https://code-runner-plugin.vercel.app"
        self.api_url = "https://carbonara.solopov.dev/api/cook"
        self.headers = {'Content-Type': 'application/json'}
        self.bucket_name = "snippets"
        
        # defining the themes list
        self.themes = {
        "3024 Night", "A11y Dark", "Blackboard",
        "Base 16 (Dark)", "Cobalt", "Duotone",
        "Hopscotch", "Lucario", "Material",
        "Monokai", "Night Owl", "Nord",
        "Oceanic Next", "One Light", "Panda Syntax",
        "Paraiso Dark", "Seti", "Shades of Purple",
        "Solarized Dark", "Solarized Light", "SynthWave '84",
        "Twilight", "Verminal", "VSCode",
        "Yeti", "Zenburn"
         }

        self.params = {
            "backgroundColor": "rgba(171, 184, 195, 1)",
            "dropShadow": True,
            "dropShadowBlurRadius": "68px",
            "dropShadowOffsetY": "20px",
            "exportSize": "2x",
            "fontCustom": "",
            "fontSize": "14px",
            "fontFamily": "Hack",
            "firstLineNumber": 1,
            "language": "auto",
            "lineHeight": "133%",
            "lineNumbers": False,
            "paddingHorizontal": "56px",
            "paddingVertical": "56px",
            "prettify": False,
            "theme": "seti",
            "watermark": False,
            "width": 536,
            "widthAdjustment": True,
            "windowControls": True,
            "windowTheme": "none"
        }
        self.database = database

    # Method to write logs to a file.
    def write_log(self,log_msg: str):
            try:
                print(str(datetime.now()) + " " + log_msg)
            except Exception as e:
                print(str(e))
                
    """
        Generate an image of the given code using the carbonara API.

        :param code: The source code to be displayed in the image.
        :param kwargs: Additional parameters to be included in the request.
        :return: The image data that can be used to create an image of the source code.
    """
        
    def generate_snippet(self, code: str, **kwargs):
        try:
            self.write_log(f"generate_snippet: method with code and kwargs: {kwargs}")
            # Update the default parameters with any additional parameters provided by the user
            self.params.update(kwargs)
            
            # Add the code parameter
            self.params["code"] = code
            
            self.write_log(f"generate_snippet: starting request to carbonara API")
            
            # Send the request to the carbonara API
            response = requests.post(self.api_url, headers=self.headers, data=json.dumps(self.params))
            self.write_log(f"generate_snippet: request to carbonara API completed")
            
            # Check if the request was successful
            if response.status_code == 200:
                # Return the image data
                self.write_log(f"generate_snippet: method successful")
                return response.content
            else:
                self.write_log(f"generate_snippet: An error occurred while generating the image: {response.text}")
                return jsonify({"output": "An error occurred while generating the image."})
        except Exception as e:
            self.write_log(f"generate_snippet: An error occurred while generating the image: {e}")
        return jsonify({"output": "An error occurred while generating the image."})

    """
        Generate an image of the given code using the carbonara API and save it to a MongoDB database using GridFS.

        :param code: The source code to be displayed in the image.
        :param kwargs: Additional parameters to be included in the request.
    """
    def save_snippet(self, code: str, **kwargs):
        try:
            self.write_log(f"save_snippet: method with code and kwargs: {kwargs}")
            # Generate a random filename for the image
            filename = f"snippet_{random.randint(1, 10000)}.png"
            
            # Generate the image data
            image_data = self.generate_snippet(code, **kwargs)
            
            if not image_data:
                self.write_log(f"save_snippet: method failed to generate image")
                return {"output": "An error occurred while generating the image."}
            
            # Get the gridfs bucket object from the database object with the bucket name 'Snippets'
            bucket = gridfs.GridFSBucket(self.database.db, bucket_name=self.bucket_name)
            
            # Store the image file in mongodb using the bucket object
            file_id = bucket.upload_from_stream(filename, image_data)
            
            if file_id:
                self.write_log("save_snippet: Image saved to database successfully.")
                # Return the download link for the image.
                download_link = f"{self.plugin_url}/download/{filename}"
                return download_link
            
        except Exception as e:
            self.write_log(f"An error occurred while saving the code snippet to the database: {e}")
        return {"output": "An error occurred while saving the code snippet to the database."}