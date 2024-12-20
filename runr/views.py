from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import handle_r_script_output

def index(request):
    """
    Renders the main dashboard page.
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
            response = handle_r_script_output(r_script)
            return response  # Return the appropriate HttpResponse or JsonResponse
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)