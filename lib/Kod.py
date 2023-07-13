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
        
        # defining the themes list
        self.themes = {
        "alternight","css-variables","dark-plus",
        "dracula-soft","dracula","github-dark-dimmed",
        "github-dark","github-light","light-plus",
        "material-darker","material-default","material-lighter",
        "material-ocean","material-palenight","min-dark",
        "min-light","minimus","monokai","nord","one-dark-pro","poimandres","slack-dark",
        "slack-ochin","solarized-dark","solarized-light","vitesse-dark","vitesse-light"
        }

        self.params = {
            "code": "",
            "num": 1,
            "title": "Code Snippet",
            "theme": "nord",
            "codeFontName": "fira-code",
            "tabSize": 4,
            "watermark": "Code Runner Plugin",
            "menuColor": 0,
            "paddingtb": 15,
            "paddinglr": 15,
            "header": 0,
            "background": "miaka",
            "opacity": 0.7
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
            
            download_png_url = code_url + "&output=png&download=1"
            download_jpg_url = code_url + "&output=jpg&download=1"
            download_svg_url = code_url + "&output=svg&download=1"
            return code_url, download_png_url, download_jpg_url, download_svg_url
        
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
    
    def get_snippet_theme(self):
        try:
            # return a random theme from the list
            return random.choice(self.themes_list)
        except Exception as e:
            self.write_log(f"An error occurred while getting the theme: {e}")
            return "nord"