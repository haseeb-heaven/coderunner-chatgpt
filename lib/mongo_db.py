#Importing modules
import datetime
import os
import random
import string
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from gridfs import GridFS
from typing import Optional
import base64
plugin_url = "https://code-runner-plugin.vercel.app"

#Creating MongoDB connector class
class MongoDB:
    MONGO_DB_API_KEY, DATA_API_KEY, DATA_API_URL, MONGODB_URI = None, None, None, None
    logger = None
    
    def __init__(self):
        #Creating a logger
        #self._create_logger()
        
        # Loading environment variables
        self.write_log("MongoDB loading environment variables")
        self._load_env()
        self.write_log("MongoDB loaded environment variables")
        
        #Creating a private method to connect to the database
        self._connect()
        self.write_log("MongoDB connected to the database")
        
        #Creating gridfs instances for graphs and codes collections
        self.graphs = GridFS(self.db, "graphs")
        self.codes = GridFS(self.db, "codes")
        self.docs = GridFS(self.db, "docs")
        self.img = GridFS(self.db, "img")
        self.users = GridFS(self.db, "users")
        
    def _connect(self):
        #Connecting to the database using the URI
        try:
            self.client = MongoClient(self.MONGODB_URI)
            self.db = self.client.get_default_database()
            self.write_log("Connected to the database successfully")
        except Exception as e:
            self.write_log(f"Failed to connect to the database: {e}")
            raise e

    def _load_env(self):
        #Loading environment variables
        load_dotenv()
        self.MONGO_DB_API_KEY = os.getenv("MONGO_DB_API_KEY")
        self.DATA_API_KEY = os.getenv("DATA_API_KEY")
        self.DATA_API_URL = os.getenv("DATA_API_URL")
        self.MONGODB_URI = os.getenv("MONGODB_URI")

    
    def _generate_file_name():
        return "".join(random.choice(string.ascii_letters) for i in range(10)) + ".py"

    def write_log(self,log_msg:str):
        try:
            print(str(datetime.now()) + " " + log_msg)
        except Exception as e:
            print(str(e))
        
    def _add_data(self, data, collection):
        #Adding data to a collection
        try:
            result = self.db[collection].insert_one(data)
            self.write_log(f"Added data to {collection} with id {result.inserted_id}")
            return result
        except Exception as e:
            self.write_log(f"Failed to add data to {collection}: {e}")
            raise e

    def _update_data(self, query, data, collection):
        #Updating data in a collection
        try:
            result = self.db[collection].update_one(query, {"$set": data})
            self.write_log(f"Updated {result.modified_count} document(s) in {collection} matching {query}")
            return result.modified_count
        except Exception as e:
            self.write_log(f"Failed to update data in {collection}: {e}")
            raise e

    def _find_data(self, query, collection):
        #Finding data in a collection
        try:
            result = self.db[collection].find_one(query)
            self.write_log(f"Found data in {collection} matching {query}")
            return result
        except Exception as e:
            self.write_log(f"Failed to find data in {collection}: {e}")
            raise e

    def _delete_data(self, query, collection):
        #Deleting data from a collection
        try:
            result = self.db[collection].delete_one(query)
            self.write_log(f"Deleted {result.deleted_count} document(s) from {collection} matching {query}")
            return result.deleted_count
        except Exception as e:
            self.write_log(f"Failed to delete data from {collection}: {e}")
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
                self.write_log(f"Added code response: {response}")
                response = response.inserted_id
            else:
                self.write_log(f"Failed to add code to codes")
                response = None
            self.write_log(f"Added code with script '{script}' and language {language} with id {response}")
            return response
        except Exception as e:
            self.write_log(f"Error while adding code with script '{script}' and language {language} with id {code_id}: {e}")
            return None

    def update_code(self, script: str, language: str, code_id: str) -> Optional[dict]:
        #Updating code in the codes collection
        try:
            filter = {"code_id": code_id}
            update = {"script": script, "language": language}
            response = self._update_data(filter, update, "codes")
            if response:
                self.write_log(f"Updated code response: {response}")
                response = int(response.modified_count) > 0
            else:
                self.write_log(f"No code found with id {code_id}")
                response = False
            self.write_log(f"Updated code with script '{script}' and language {language} with id {code_id}")
            return response
        except Exception as e:
            self.write_log(f"Error while updating code with script '{script}' and language {language} with id {code_id}: {e}")
            return None

    def find_code(self, filename: str) -> Optional[dict]:
        #Finding code in the codes collection
        try:
            code_id = self._find_code_id_by_filename(filename)
            self.write_log(f"Found code with id {code_id} for filename {filename}")
            filter = {"id": code_id}
            response = self._find_data(filter, "codes")
            if response:
                self.write_log(f"Found code response: {response}")
                code = response['script']
                if code:
                    self.write_log(f"Found {code} with id {code_id}")
                    return code
                else:
                    self.write_log(f"Code with id {code_id} not found")
                    return None
            else:
                self.write_log(f"No code found with id {code_id}")
                response = None
            self.write_log(f"Found code with id {code_id}")
            return response
        except Exception as e:
            self.write_log(f"Error while finding code with id {code_id}: {e}")
            return None
        
    def _find_code_id_by_filename(self, filename: str) -> Optional[dict]:
        #Finding code in the codes collection
        try:
            filter = {"filename": filename}
            response = self._find_data(filter, "codes")
            if response:
                self.write_log(f"Found code response: {response}")
                code = response['id']
                if code:
                    self.write_log(f"Found {code} with filename {filename}")
                    return code
                else:
                    self.write_log(f"Code with filename {filename} not found")
                    return None
            else:
                self.write_log(f"No code found with filename {filename}")
                response = None
            self.write_log(f"Found code with filename {filename}")
            return response
        except Exception as e:
            self.write_log(f"Error while finding code with filename {filename}: {e}")
            return None

    def delete_code(self, code_id: str) -> Optional[bool]:
        #Deleting code from the codes collection
        try:
            filter = {"id": code_id}
            response = self._delete_data(filter, "codes")
            if response:
                self.write_log(f"Deleted code response: {response}")
                response = int(response) > 0
            else:
                self.write_log(f"No code found with id {code_id}")
                response = False
            self.write_log(f"Deleted code with id {code_id}")
            return response
        except Exception as e:
            self.write_log(f"Error while deleting code with id {code_id}: {e}")
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
                    self.write_log(f"Stored image response: {file_id}")
                    file_id = str(file_id) # convert ObjectId to string
                else:
                    self.write_log(f"Failed to store image {image_path}")
                    file_id = None
                self.write_log(f"Stored image {image_path} with id {file_id}")
                return file_id
        except Exception as e:
            self.write_log(f"Failed to store image {image_path}: {e}")
            raise e

    def download_image(self, image_id: str, download_path: str) -> Optional[str]:
        #Downloading an image from the graphs collection
        try:
            filter = {"id": image_id}
            document = self._find_data(filter, "graphs")
            if document:
                self.write_log("Found image in with id {image_id}")
                with open(download_path, "wb") as f:
                    image_data = document["image"]
                    if image_data:
                        image_data = base64.b64decode(image_data)
                        f.write(image_data)
                        self.write_log(f"Downloaded image {image_id} to {download_path}")
                        return download_path
                    else:
                        self.write_log(f"Image with id {image_id} not found")
                        return None
            else:
                self.write_log(f"No image found with id {image_id}")
                return None
        except Exception as e:
            self.write_log(f"Failed to download image {image_id}: {e}")
            raise e

    def delete_image(self, image_id: str) -> Optional[bool]:
        #Deleting an image from the graphs collection
        try:
            filter = {"id": image_id}
            result = self._delete_data(filter, "graphs")
            if result:
                self.write_log(f"Deleted image response: {result}")
                result = int(result) > 0
            else:
                self.write_log(f"No image found with id {image_id}")
                result = False
            self.write_log(f"Deleted image {image_id}")
            return result
        except Exception as e:
            self.write_log(f"Failed to delete image {image_id}: {e}")
            raise e
        
    # method to get total number of documents in a collection
    def _get_total_documents(self, collection):
        try:
            return self.db[collection].count_documents({})
        except Exception as e:
            self.write_log(f"Failed to get total documents in {collection}: {e}")
            raise e
        
    def get_total_codes(self):
        return self._get_total_documents("codes")

    def get_total_images(self):
        return self._get_total_documents("graphs")
    
    # method to delete all documents in a collection
    def _delete_all_documents(self, collection):
        try:
            result = self.db[collection].delete_many({})
            self.write_log(f"Deleted {result.deleted_count} document(s) from {collection}")
            return result.deleted_count
        except Exception as e:
            self.write_log(f"Failed to delete documents from {collection}: {e}")
            raise e
    
    def delete_all_codes(self):
        return self._delete_all_documents("codes")
    
    def delete_all_graphs(self):
        self._delete_all_documents("graphs.files")
        return self._delete_all_documents("graphs.chunks")
    
    def delete_all_documents(self):
        self._delete_all_documents("docs.files")
        return self._delete_all_documents("docs.chunks")
    
    def reset_database(self):
        self.delete_all_codes()
        self.delete_all_graphs()  
        self.delete_all_documents()
        self.write_log("Resetting database to initial state")
        
    # method to list contents of a collection
    def _list_all_files(self, collection):
        try:
            return self.db[collection].find()
        except Exception as e:
            self.write_log(f"Failed to list contents of {collection}: {e}")
            raise e
        
    def list_all_collections(self):
        # append all collections to a list
        data_list = []
        collections = ["codes", "graphs.files", "graphs.chunks", "docs.files", "docs.chunks"]
        for collection in collections:
            cursor = self._list_all_files(collection)
            for item in cursor:
                filename = item.get("filename")
                if filename:
                    filename = f'{plugin_url}/download/' + filename
                    data_list.append({"filename": filename})
        return data_list
    
    # Method to restore deleted documents
    def restore_deleted_documents(self,db_name, collection_name, oplog_name):
        try:
            # Connect to the local MongoDB instance
            client = MongoClient(self.MONGODB_URI)
            db = client[db_name]
            oplog = db[oplog_name]

            # Query the Oplog for the deleted documents
            oplog_query = {
                "ns": f"{db_name}.{collection_name}",
                "op": "d"
            }

            cursor = oplog.find(oplog_query)

            # Loop through the deleted documents
            for document in cursor:
                # Get the _id of the deleted document
                deleted_id = document["o"]["_id"]
                # Find the corresponding insert operation in the Oplog
                insert_query = {
                    "ns": document["ns"],
                    "op": "i",
                    "o._id": deleted_id
                }
                insert_document = oplog.find_one(insert_query)
                # Check if the insert operation exists
                if insert_document:
                    # Get the original document that was inserted
                    original_document = insert_document["o"]
                    # Connect to the original collection
                    original_collection = db[collection_name]
                    # Insert the original document back to the collection
                    original_collection.insert_one(original_document)
                    print(f"Restored document with _id {deleted_id} to collection {insert_document['ns']}")
                else:
                    print(f"Could not find insert operation for document with _id {deleted_id} in collection {document['ns']}")
        except Exception as e:
            print("Exception: ", e)

        # Call the method with the desired parameters
        #restore_deleted_documents("YOUR-DB", "graphs.files", "oplog.rs")

    # Method to create new collection for users.
    def create_new_collection(self, collection_name):
        try:
            # Connect to the local MongoDB instance
            db = self.db
            db.create_collection(collection_name)
            print(f"Created new collection {collection_name}")
        except Exception as e:
            print("Exception: ", e)
    
    # Create now new user with user data.
    def create_user(self, user_id=None, user_email=None, user_password=None,created_at_ms=None,updated_at_ms=None,is_verified=None):
        try:
            # check for user id and email not to be none
            if user_id is None or user_email is None:
                print("db_create_user: User id and email cannot be empty")
                return
            
            # Connect to the local MongoDB instance
            db = self.db
            collection_name = "users"
            collection = db[collection_name]
            user = {
                "id": user_id,
                "email": user_email,
                "password": user_password,
                "createdAt": created_at_ms,
                "updatedAt": updated_at_ms,
                "isVerified": is_verified
            }
            collection.insert_one(user)
            print(f"Added new user to collection {collection_name}")
        except Exception as e:
            print("Exception: ", e)
    
    # Update user with new data.
    def update_user(self, user_id=None, user_email=None, user_password=None,created_at_ms=None,updated_at_ms=None,is_verified=None):
        try:
            # check for user id and email not to be none
            if user_id is None or user_email is None:
                print("db_update_user: User id and email cannot be empty")
                return
            
            # Connect to the local MongoDB instance
            db = self.db
            collection_name = "users"
            collection = db[collection_name]
            filter = {"id": user_id}
            update = {"$set": {"email": user_email, "password": user_password, "createdAt": created_at_ms, "updatedAt": updated_at_ms, "isVerified": is_verified}}
            result = collection.update_one(filter, update)
            
            if result.modified_count == 0:
                print(f"db_update_user: User not found")
            else:
                print(f"db_update_user: user successfully updated")
        except Exception as e:
            print("Exception: ", e)
            
    # Update user quota.
    def update_user_quota(self, user_id=None,quota=None):
        try:
            # check for user id and email not to be none
            if user_id is None or quota is None:
                print("db_update_quota: User id and quota cannot be empty")
                return

            # Connect to the local MongoDB instance
            db = self.db
            collection_name = "users"
            collection = db[collection_name]
            filter = {"id": user_id}
            update = {"$set": {"quota": quota}}
            result = collection.update_one(filter, update)

            if result.modified_count == 0:
                print(f"db_update_quota: User not found")
            else:
                print(f"db_update_quota: user successfully updated")
        except Exception as e:
            print("Exception: ", e)