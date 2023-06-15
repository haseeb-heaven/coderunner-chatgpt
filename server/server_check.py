# Import the modules
import requests
import time
import logging
from datetime import date, datetime

# Set up the logging
logging.basicConfig(filename='server/server_log.txt', level=logging.INFO, format='%(asctime)s %(message)s')

# Define the server URL
server_url = 'https://code-runner-plugin.vercel.app/credit_limit'

# Define a function to check the server status and record the downtime
def check_server():
    # Initialize a variable to store the start time of the downtime
    start_time = None
    # Initialize a variable to store the end time of the downtime
    end_time = None
    # Initialize a variable to store the total downtime in seconds
    total_downtime = 0
    # Initialize a variable to store the delay in seconds
    delay = 5
    # Initialize a variable to store the counter for the loop
    counter = 0
    # Initialize a variable to store the limit for the loop
    limit = 10000
    # Loop indefinitely
    while True:
        try:
            # Send a GET request to the server and get the response
            response = requests.get(server_url)
            # Check if the response status code is 200 (OK)
            if response.status_code == 200:
                # Log the success message
                logging.info(f'Server is up and running.')
                # Print the response content as a JSON object
                print(f'Response: {response.json()} {datetime.now()}')
                # Check if there was a previous downtime
                if start_time is not None:
                    # Set the end time to the current time
                    end_time = time.time()
                    # Calculate the downtime in seconds
                    downtime = end_time - start_time
                    # Add the downtime to the total downtime
                    total_downtime += downtime
                    # Get the minutes and seconds from the downtime using divmod()
                    minutes, seconds = divmod(downtime, 60)
                    # Log the downtime message with date and time and formatted minutes and seconds
                    logging.info(f'Server was down from {datetime.fromtimestamp(start_time)} to {datetime.fromtimestamp(end_time)} for {minutes:.0f} minutes and {seconds:.0f} seconds.')
                    # Reset the start time and end time to None
                    start_time = None
                    end_time = None
                # Wait for 5 seconds before sending another request
                time.sleep(delay)
            else:
                # Log the error message with the status code
                logging.error(f'Server error: {response.status_code}')
                print(f'Response: {response.status_code} {datetime.now()}')
                # Check if this is the start of a downtime
                if start_time is None:
                    # Set the start time to the current time
                    start_time = time.time()
                else:
                    # Calculate the downtime in seconds
                    downtime = time.time() - start_time
                    # Add the downtime to the total downtime
                    total_downtime = downtime
                    # Get the minutes and seconds from the downtime using divmod()
                    minutes, seconds = divmod(downtime, 60)
                    # Log the downtime message with date and time and formatted minutes and seconds
                    #logging.info(f'Server has been down for {minutes:.0f} minutes and {seconds:.0f} seconds.')

        except Exception as e:
            # Log the exception message
            logging.exception(f'Exception occurred: {e}')
            # Check if this is the start of a downtime
            if start_time is None:
                # Set the start time to the current time
                start_time = time.time()
        finally:
            # Increment the counter by one after each iteration
            counter += 1
            # Check if the counter has reached the limit
            # if counter == limit:
            #     # Break out of the loop
            #     break

    # Return the total downtime in seconds
    return total_downtime

# Define a main function to run the program
def main():
    # Call the check_server function and get the result
    total_downtime = check_server()
    # Get the minutes and seconds from the total downtime using divmod()
    minutes, seconds = divmod(total_downtime, 60)
    # Print the result in the desired format
    print(f'Total downtime: {int(minutes)} minutes {int(seconds)} seconds.')

# Check if this file is executed as a script and call the main function if so    
if __name__ == '__main__':
    main()
