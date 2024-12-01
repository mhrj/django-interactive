from pyRserve import connect
from .validations import validate_script
from django.http import JsonResponse, HttpResponse

def sanitize_script(r_script):
    # Remove unwanted newline or carriage return characters
    return r_script.replace('\r\n', '\n').replace('\r', '\n').strip()

def process_r_script(user_name, r_script):
    """
    Connects to Rserve, executes the script, and returns the result.
    """
    if not validate_script(r_script):
        error_message = "Destructive commands detected in script!"
        raise ValueError(error_message)

    r_script = sanitize_script(r_script)
    conn = None
    try:
        conn = connect("localhost", 6312)
        result = conn.eval(r_script)
        if isinstance(result, bytes):  # Image data returned as bytes
            return result.decode()
        else:  # Assume text result
            return result
    except Exception as e:
        raise ValueError(str(e))
    finally:
        conn.close()

def handle_r_script_output(user_name, r_script):
    try:
        output = process_r_script(user_name, r_script)
        if isinstance(output, bytes):
            return HttpResponse(output, content_type="image/png")
        else:
            return JsonResponse({'result': str(output)})
    except ValueError as ve:
        return JsonResponse({"error": f"Validation Error: {str(ve)}"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Internal Error: {str(e)}"}, status=500)