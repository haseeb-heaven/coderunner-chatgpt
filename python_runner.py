import random
import string
import os

def exec_python(code):
        # Generate a random file name
    file_name = generate_file_name()

    # Write the code to the file
    write_code_to_file(code, file_name)

    # Run the file and capture the output
    output = run_file_and_capture_output(file_name)

    # Delete the file
    os.remove(file_name)

    return output

# Method to executre the code using exec.
def execute_code(code: str):
  try:
    output = {}
    exec(code, output)
    # return the output.
    print(f"execute_code: output is {output}")
    # check the length of the output dictionary
    if len(output) > 0:
      # use the last key in the dictionary
      key = list(output.keys())[-1]
      return output[key]
    else:
      # return None if the dictionary is empty
      return None
  except Exception as e:
    print(f"execute_code: {e}")

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
