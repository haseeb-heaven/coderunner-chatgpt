import random
import string
import os
import io
import contextlib
import multiprocessing

# setting default timeout to 120 seconds
DEFAULT_TIMEOUT = 120

def execute_code(code, timeout=DEFAULT_TIMEOUT):
    with multiprocessing.Pool(processes=1) as pool:
        res = pool.apply_async(_execute_code, (code,)) # runs in *only* one process
        try:
            output = res.get(timeout=timeout) # waits for the result for `timeout` seconds
        except multiprocessing.TimeoutError:
            output = "Code execution took too long and was terminated."
            pool.terminate()
    return output

# Method to execute the code using exec.
def _execute_code(code):
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
