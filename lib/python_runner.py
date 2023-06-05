import random
import string
import os
import io
import contextlib

def exec_python(code):
    try:
      # Generate a random file name
      file_name = generate_file_name()
    except Exception as e:
      return f"exec_python: {e}"

    try:
      # Write the code to the file
      write_code_to_file(code, file_name)
    except Exception as e:
      return f"exec_python: {e}"
    
    try:
      # Run the file and capture the output
      output = run_file_and_capture_output(file_name)
    except Exception as e:
      return f"exec_python: {e}"
    
    try:
      # Delete the file
      os.remove(file_name)
    except Exception as e:
      return f"exec_python: {e}"
    
    return output

# Method to executre the code using exec.
def execute_code(code):

    # Create a string buffer to store the output
    buffer = io.StringIO()
    # Redirect the standard output to the buffer
    with contextlib.redirect_stdout(buffer):
        # Execute the code as Python code
        exec(code)
    # Get the output from the buffer
    output = buffer.getvalue()
    # Return the output as a string
    return output

# Define a function to generate a random file name
def generate_file_name():
  return "".join(random.choice(string.ascii_letters) for i in range(10)) + ".py"

# Define a function to write the code to a file
def write_code_to_file(code, file_name):
  with open(file_name, "w") as f:
    f.write(code)

# Define a function to run the file and capture the output
def run_file_and_capture_output(file_name):
  return os.popen(f"python3 {file_name}").read()
