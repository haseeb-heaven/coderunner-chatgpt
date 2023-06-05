#Importing modules
import datetime
import os
import logging
import random
import string
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from gridfs import GridFS
from typing import Optional
import base64

#Creating MongoDB connector class
class MongoDB:
    MONGO_DB_API_KEY, DATA_API_KEY, DATA_API_URL, MONGODB_URI = None, None, None, None
    logger = None
    
    def __init__(self):
        #Creating a logger
        self._create_logger()
        
        # Loading environment variables
        self._load_env()
        
        #Creating a private method to connect to the database
        self._connect()
        #Creating gridfs instances for graphs and codes collections
        self.graphs = GridFS(self.db, "graphs")
        self.codes = GridFS(self.db, "codes")
        
    def _connect(self):
        #Connecting to the database using the URI
        try:
            self.client = MongoClient(self.MONGODB_URI)
            self.db = self.client.get_default_database()
            self.logger.info("Connected to the database successfully")
        except Exception as e:
            self.logger.error(f"Failed to connect to the database: {e}")
            raise e

    def _load_env(self):
        #Loading environment variables
        load_dotenv()
        self.MONGO_DB_API_KEY = os.getenv("MONGO_DB_API_KEY")
        self.DATA_API_KEY = os.getenv("DATA_API_KEY")
        self.DATA_API_URL = os.getenv("DATA_API_URL")
        self.MONGODB_URI = os.getenv("MONGODB_URI")
    
    def _create_logger(self):
        logger_file = __file__.replace(".py", ".log")
        logger = logging.getLogger(logger_file)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
        file_handler = logging.FileHandler(logger_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        self.logger = logger

    
    def _generate_file_name():
        return "".join(random.choice(string.ascii_letters) for i in range(10)) + ".py"

        
    def _add_data(self, data, collection):
        #Adding data to a collection
        try:
            result = self.db[collection].insert_one(data)
            self.logger.info(f"Added data to {collection} with id {result.inserted_id}")
            return result
        except Exception as e:
            self.logger.error(f"Failed to add data to {collection}: {e}")
            raise e

    def _update_data(self, query, data, collection):
        #Updating data in a collection
        try:
            result = self.db[collection].update_one(query, {"$set": data})
            self.logger.info(f"Updated {result.modified_count} document(s) in {collection} matching {query}")
            return result.modified_count
        except Exception as e:
            self.logger.error(f"Failed to update data in {collection}: {e}")
            raise e

    def _find_data(self, query, collection):
        #Finding data in a collection
        try:
            result = self.db[collection].find_one(query)
            self.logger.info(f"Found data in {collection} matching {query}")
            return result
        except Exception as e:
            self.logger.error(f"Failed to find data in {collection}: {e}")
            raise e

    def _delete_data(self, query, collection):
        #Deleting data from a collection
        try:
            result = self.db[collection].delete_one(query)
            self.logger.info(f"Deleted {result.deleted_count} document(s) from {collection} matching {query}")
            return result.deleted_count
        except Exception as e:
            self.logger.error(f"Failed to delete data from {collection}: {e}")
            raise e

    def save_code(self, script: str, language: str, code_id: str,filename:str) -> Optional[dict]:
        #Adding code to the codes collection
        try:
            # Generate a random file name
            if filename is None:
                filename = self._generate_file_name()
            document = {"script": script, "language": language, "id": code_id,"filename":filename,"timestamp":datetime.now()}
            response = self._add_data(document, "codes")
            if response:
                self.logger.info(f"Added code response: {response}")
                response = response.inserted_id
            else:
                self.logger.warning(f"Failed to add code to codes")
                response = None
            self.logger.info(f"Added code with script '{script}' and language {language} with id {response}")
            return response
        except Exception as e:
            self.logger.error(f"Error while adding code with script '{script}' and language {language} with id {code_id}: {e}")
            return None

    def update_code(self, script: str, language: str, code_id: str) -> Optional[dict]:
        #Updating code in the codes collection
        try:
            filter = {"code_id": code_id}
            update = {"script": script, "language": language}
            response = self._update_data(filter, update, "codes")
            if response:
                self.logger.info(f"Updated code response: {response}")
                response = int(response.modified_count) > 0
            else:
                self.logger.warning(f"No code found with id {code_id}")
                response = False
            self.logger.info(f"Updated code with script '{script}' and language {language} with id {code_id}")
            return response
        except Exception as e:
            self.logger.error(f"Error while updating code with script '{script}' and language {language} with id {code_id}: {e}")
            return None

    def find_code(self, filename: str) -> Optional[dict]:
        #Finding code in the codes collection
        try:
            code_id = self._find_code_id_by_filename(filename)
            self.logger.info(f"Found code with id {code_id} for filename {filename}")
            filter = {"id": code_id}
            response = self._find_data(filter, "codes")
            if response:
                self.logger.info(f"Found code response: {response}")
                code = response['script']
                if code:
                    self.logger.info(f"Found {code} with id {code_id}")
                    return code
                else:
                    self.logger.error(f"Code with id {code_id} not found")
                    return None
            else:
                self.logger.warning(f"No code found with id {code_id}")
                response = None
            self.logger.info(f"Found code with id {code_id}")
            return response
        except Exception as e:
            self.logger.error(f"Error while finding code with id {code_id}: {e}")
            return None
        
    def _find_code_id_by_filename(self, filename: str) -> Optional[dict]:
        #Finding code in the codes collection
        try:
            filter = {"filename": filename}
            response = self._find_data(filter, "codes")
            if response:
                self.logger.info(f"Found code response: {response}")
                code = response['id']
                if code:
                    self.logger.info(f"Found {code} with filename {filename}")
                    return code
                else:
                    self.logger.error(f"Code with filename {filename} not found")
                    return None
            else:
                self.logger.warning(f"No code found with filename {filename}")
                response = None
            self.logger.info(f"Found code with filename {filename}")
            return response
        except Exception as e:
            self.logger.error(f"Error while finding code with filename {filename}: {e}")
            return None

    def delete_code(self, code_id: str) -> Optional[bool]:
        #Deleting code from the codes collection
        try:
            filter = {"id": code_id}
            response = self._delete_data(filter, "codes")
            if response:
                self.logger.info(f"Deleted code response: {response}")
                response = int(response) > 0
            else:
                self.logger.warning(f"No code found with id {code_id}")
                response = False
            self.logger.info(f"Deleted code with id {code_id}")
            return response
        except Exception as e:
            self.logger.error(f"Error while deleting code with id {code_id}: {e}")
            return None
    
    def save_image(self, image_path: str, image_id: str) -> Optional[str]:
        #Storing an image in the graphs collection
        try:
            with open(image_path, "rb") as f:
                image_data = f.read()
                encoded_image = base64.b64encode(image_data).decode("utf-8")
                document = {"image": encoded_image, "id": image_id,"timestamp":datetime.now()}
                file_id = self._add_data(document, "graphs")
                if file_id:
                    self.logger.info(f"Stored image response: {file_id}")
                    file_id = str(file_id) # convert ObjectId to string
                else:
                    self.logger.warning(f"Failed to store image {image_path}")
                    file_id = None
                self.logger.info(f"Stored image {image_path} with id {file_id}")
                return file_id
        except Exception as e:
            self.logger.error(f"Failed to store image {image_path}: {e}")
            raise e

    def download_image(self, image_id: str, download_path: str) -> Optional[str]:
        #Downloading an image from the graphs collection
        try:
            filter = {"id": image_id}
            document = self._find_data(filter, "graphs")
            if document:
                self.logger.info("Found image in with id {image_id}")
                with open(download_path, "wb") as f:
                    image_data = document["image"]
                    if image_data:
                        image_data = base64.b64decode(image_data)
                        f.write(image_data)
                        self.logger.info(f"Downloaded image {image_id} to {download_path}")
                        return download_path
                    else:
                        self.logger.error(f"Image with id {image_id} not found")
                        return None
            else:
                self.logger.warning(f"No image found with id {image_id}")
                return None
        except Exception as e:
            self.logger.error(f"Failed to download image {image_id}: {e}")
            raise e

    def delete_image(self, image_id: str) -> Optional[bool]:
        #Deleting an image from the graphs collection
        try:
            filter = {"id": image_id}
            result = self._delete_data(filter, "graphs")
            if result:
                self.logger.info(f"Deleted image response: {result}")
                result = int(result) > 0
            else:
                self.logger.warning(f"No image found with id {image_id}")
                result = False
            self.logger.info(f"Deleted image {image_id}")
            return result
        except Exception as e:
            self.logger.error(f"Failed to delete image {image_id}: {e}")
            raise e
        
    # method to get total number of documents in a collection
    def _get_total_documents(self, collection):
        try:
            return self.db[collection].count_documents({})
        except Exception as e:
            self.logger.error(f"Failed to get total documents in {collection}: {e}")
            raise e
        
    def get_total_codes(self):
        return self._get_total_documents("codes")

    def get_total_images(self):
        return self._get_total_documents("graphs")
    
    # method to delete all documents in a collection
    def _delete_all_documents(self, collection):
        try:
            result = self.db[collection].delete_many({})
            self.logger.info(f"Deleted {result.deleted_count} document(s) from {collection}")
            return result.deleted_count
        except Exception as e:
            self.logger.error(f"Failed to delete documents from {collection}: {e}")
            raise e
    
    def delete_all_codes(self):
        return self._delete_all_documents("codes")
    
    def delete_all_images(self):
        return self._delete_all_documents("graphs")
    
    def reset_database(self):
        self.delete_all_codes()
        self.delete_all_images()
        self._delete_all_documents("graphs.files")
        self._delete_all_documents("graphs.chunks")
        self.logger.info("Resetting database to initial state")


