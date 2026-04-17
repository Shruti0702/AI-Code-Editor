import json
import subprocess
import tempfile
import os

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import SavedSnippet
from submissions.models import Submission


@login_required
def editor_page(request):
    return render(request, 'editor/editor.html')

import json
import os
import subprocess
import tempfile

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from submissions.models import Submission


@csrf_exempt
@login_required
def run_code(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
        code = data.get("code", "")
        stdin_data = data.get("stdin", "")

        if not code.strip():
            return JsonResponse({"error": "Code cannot be empty"}, status=400)

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "main.py")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)

            docker_cmd = [
                "docker", "run", "--rm",
                "-i",
                "-v", f"{temp_dir}:/app",
                "-w", "/app",
                "python:3.12-alpine",
                "python", "main.py"
            ]

            result = subprocess.run(
                docker_cmd,
                input=stdin_data,
                capture_output=True,
                text=True,
                timeout=30
            )

        output = result.stdout
        error = result.stderr
        status_value = "success" if result.returncode == 0 else "error"

        Submission.objects.create(
            user=request.user,
            language="python",
            code=code,
            stdin=stdin_data,
            output=output,
            error=error,
            status=status_value
        )

        return JsonResponse({
            "output": output,
            "error": error
        })

    except subprocess.TimeoutExpired:
        return JsonResponse({"error": "Code execution timed out"}, status=408)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@login_required
def save_snippet(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
        title = data.get('title', '')
        code = data.get('code', '')
        language = data.get('language', 'python')

        snippet = SavedSnippet.objects.create(
            user=request.user,
            title=title,
            code=code,
            language=language
        )

        return JsonResponse({
            'message': 'Snippet saved successfully',
            'snippet_id': snippet.id
        })

    except Exception as e:
        return JsonResponse({'error': str(e)})


@login_required
def snippet_list(request):
    snippets = SavedSnippet.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'editor/snippets.html', {'snippets': snippets})