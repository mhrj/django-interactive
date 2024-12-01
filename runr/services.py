from pyRserve import connect
from .validations import validate_script
from .websocket import log_error
from django.http import JsonResponse, HttpResponse

def sanitize_script(r_script):
    # Remove unwanted newline or carriage return characters
    return r_script.replace('\r\n', '\n').replace('\r', '\n').strip()

def process_r_script(user_name, r_script):
    """
    Connects to Rserve, executes the script, and returns the result.
    """
    # Validate the R script for destructive commands
    if not validate_script(r_script):
        error_message = "Destructive commands detected in script!"
        log_error(user_name, r_script, error_message)
        raise ValueError(error_message)
    r_script = sanitize_script(r_script)
    conn = None
    try:
        # Connect to Rserve on localhost:6312
        conn = connect("localhost", 6312)
        result = conn.eval(r_script)
        if isinstance(result, bytes):  # Image data returned as bytes
            return result
        else:  # Assume text result
            return result.decode() if isinstance(result, bytes) else result

    except Exception as e:
        # Log error and re-raise
        log_error(user_name, r_script, str(e))
        raise

    finally:
        # Ensure the connection is closed properly
        if conn:
            try:
                conn.close()
            except Exception as close_error:
                # Log the connection close error, if any
                log_error(user_name, r_script, f"Error closing connection: {close_error}")

def handle_r_script_output(user_name, r_script):
    """
    Django view to handle R script execution and return output.
    """
    try:
        # Process the R script
        output = process_r_script(user_name, r_script)

        if isinstance(output, bytes):  # If output is binary, send as image
            return HttpResponse(output, content_type="image/png")
        else:  # If output is text, return JSON response
            return JsonResponse({"result": output})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)