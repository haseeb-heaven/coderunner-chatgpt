import io
import contextlib

# Method to execute the code using exec.
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
