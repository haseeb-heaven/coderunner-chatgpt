"""
Description: This use API for Kod so which is a code snippet generator for developers.
Server API : REST.
Website : https://kod.so/
"""


import requests
from datetime import datetime
import random
import gridfs

class Kodso:
    def __init__(self, database):
        # defining the api url
        self.plugin_url = "https://code-runner-plugin.vercel.app"
        self.api_url = "https://kod.so/gen"
        self.headers = {'Content-Type': 'application/json'}
        self.params = {
            "code": "",
            "num": 1,
            "title": "",
            "theme": "nord",
            "codeFontName": "fira-code",
            "tabSize": 4
        }
        self.bucket_name = "snippets"
        self.database = database

    # Method to write logs to a file.
    def write_log(self,log_msg: str):
            try:
                print(str(datetime.now()) + " " + log_msg)
            except Exception as e:
                print(str(e))

    def generate_snippet(self, code: str, **kwargs): 
        try:
            self.write_log(f"generate_snippet: method with code and kwargs: {kwargs}")
            # Update the default parameters with any additional parameters provided by the user
            self.params.update(kwargs)
            
            # Add the code parameter
            self.params["code"] = code
            
            self.write_log(f"generate_snippet: starting request to Kod.so API")
            
            # Send the request to the Kod.so API
            response = requests.get(self.api_url, headers=self.headers, params=self.params)
            self.write_log(f"generate_snippet: request to Kod.so API completed")
            
            if response.status_code == 200:
                # If successful, returns the URL of the generated code snippet
                self.write_log(f"generate_snippet: method successful") 
                return response.url 

            else:
                self.write_log(f"generate_snippet: An error occurred while generating the code: {response.text}")
                return {"output": "An error occurred while generating the code."}

        except Exception as e:
            self.write_log(f"generate_snippet: An error occurred while generating the code: {e}")
            return {"output": "An error occurred while generating the code."}
    
    def save_snippet(self, code: str, **kwargs):
        try:
            self.write_log(f"save_snippet: method with code and kwargs: {kwargs}")
            # Generate a random filename for the image
            filename = f"snippet_{random.randint(1, 10000)}.png"
            
            # Generate the URL of the code snippet
            code_url = self.generate_snippet(code, **kwargs)
            
            if not code_url:
                self.write_log(f"save_snippet: method failed to generate code_url")
                return {"output": "An error occurred while generating the code URL."}
            
            return code_url
        
            # Then download the image located in the generated URL and save it
            image_resp = requests.get(code_url)
            image_data = image_resp.content
            
            # Get the GridFSBucket object from the database object with the bucket name 'Snippets'
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
