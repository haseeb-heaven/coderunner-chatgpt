import requests
import json
import random
from datetime import datetime
import gridfs

class QuickChartIO:
    base_url = "https://quickchart.io/chart"
    plugin_url = "https://code-runner-plugin.vercel.app"
    database = None
    
    # Constructor to initialize the base URL and the log file name
    def __init__(self, database):
        self.database = database
        self.write_log("QuickChartIO: initialized")

    # Method to generate a chart of a given type and data
    def generate_chart(self, chart_type: str, data: dict):
        file_name = ""
        try:
            # Create the chart configuration as a JSON object
            chart_config = {
                "type": chart_type,
                "data": data
            }
            # Send a GET request to the base URL with the chart configuration as a parameter
            response = requests.get(f'{self.base_url}?c={json.dumps(chart_config)}')
            if response.status_code == 200:
                
                # Save the chart as a PNG file with a random name in the database using the save_graph method
                file_name = f"graph_{chart_type}_{random.randint(1, 100000)}.png"
                file_id = self.save_graph(file_name, response.content)
                    
                # Write a success log message to the log file
                self.write_log(f"Chart saved as {file_name} with id {file_id}")
            else:
                # Write an error log message to the log file with the status code
                self.write_log(f"Error generating chart: {response.status_code}")
            return file_name
        except Exception as e:
            # Write an exception log message to the log file with the exception details
            self.write_log(f"Error generating chart: {e}")
            return file_name

    def download_link(self,graph_file: str):
        response = f"{self.plugin_url}/download/{graph_file}"
        return response
    
    # Method to write logs to a file.
    def write_log(self,log_msg: str):
        try:
            print(str(datetime.now()) + " " + log_msg)
        except Exception as e:
            print(str(e))

    # Method to save the chart in mongodb
    def save_graph(self, filename, content):
        output = {}
        self.write_log(f"save_graph: executed script")

        # Get the gridfs bucket object from the database object with the bucket name 'graphs'
        bucket = gridfs.GridFSBucket(self.database.db, bucket_name='graphs')
        self.write_log(f"save_graph: got gridfs bucket object")

        # Store the content in mongodb using the bucket object
        file_id = bucket.upload_from_stream(filename, content)
        self.write_log(f"save_graph: stored image file in mongodb")
        # Return the file id
        return output
