from django.shortcuts import render
import json
import logging
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from websockets import connect as ws_connect
from .services import handle_r_script_output

# Logging setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename='script_errors.log')

def index(request):
    """
    View for rendering the main dashboard page.
    """
    return render(request, 'index.html')

@csrf_exempt
def run_r_script(request):
    """
    Handles running an R script submitted by the user.
    """
    if request.method == 'POST':
        user_name = request.POST.get('userName', 'Unknown User')
        r_script = request.POST.get('rScript', '').strip()

        if not r_script:
            return JsonResponse({'error': 'R script cannot be empty'}, status=400)

        try:
            # Process the script using a service function
            result = handle_r_script_output(user_name, r_script)
            return result
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


async def log_error_to_desktop(user_name, r_script, error_message):
    """
    Logs errors via websocket to a PyQt5 application.
    """
    log_data = {
        'user': user_name,
        'script': r_script,
        'error': error_message,
    }
    try:
        # Connect to PyQt5 app using WebSocket
        ws_url = "ws://localhost:8765"
        async with ws_connect(ws_url) as websocket:
            await websocket.send(json.dumps(log_data))
    except Exception as ws_error:
        logger.error(f"WebSocket Error: {ws_error}")