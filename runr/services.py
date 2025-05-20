from pyRserve import connect
from .validations import validate_script
from django.http import JsonResponse

def sanitize_script(r_script):
    """
    Sanitizes the R script to remove unwanted characters.
    """
    return r_script.replace('\r\n', '\n').replace('\r', '\n').strip()

def process_r_script(r_script):
    """
    Connects to Rserve, executes the script, and returns the result.
    """
    # Validate the R script for destructive commands
    if not validate_script(r_script):
        error_message = "Destructive commands detected in script!"
        raise ValueError(error_message)

    r_script = sanitize_script(r_script)
    conn = None
    try:
        conn = connect("rserve", 6312)
        result = conn.eval(r_script)

        # Check if the result is Base64-encoded
        if isinstance(result, str) and result.strip().startswith("data:image/png;base64,"):
            return {"type": "image", "content": result}
        else:
            return {"type": "text", "content": result}
    except Exception as e:
        raise ValueError(str(e))
    finally:
        if conn:
            try:
                conn.close()
            except Exception as close_error:
                print(f"Error closing connection: {close_error}")


def handle_r_script_output(r_script):
    """
    Handles R script execution and returns the output in a Django-compatible format.
    """
    try:
        output = process_r_script(r_script)

        # Handle image output
        if output["type"] == "image":
            # Extract the Base64 string and return it in the response
            return JsonResponse({'result': output["content"]})

        # Handle text output
        elif output["type"] == "text":
            return JsonResponse({'result': str(output["content"])})

    except ValueError as ve:
        return JsonResponse({"error": f"Validation Error: {str(ve)}"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Internal Error: {str(e)}"}, status=500)