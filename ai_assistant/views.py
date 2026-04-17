import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from groq import Groq

client = Groq(api_key=settings.GROQ_API_KEY)


@csrf_exempt
@login_required
def explain_error(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
        code = data.get('code', '')
        error = data.get('error', '')

        if not code.strip():
            return JsonResponse({'error': 'Code is required'}, status=400)

        if not error.strip():
            return JsonResponse({'error': 'No error found to explain'}, status=400)

        prompt = f"""
You are a beginner-friendly Python tutor.

The user wrote this code:
{code}

They got this error:
{error}

Please explain in this exact format:

Cause:
<what caused the error>

Fix:
<how to fix it>

Beginner Explanation:
<simple explanation in beginner-friendly language>

Improved Code:
<corrected code only>
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful beginner-friendly coding teacher."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=800
        )

        explanation = response.choices[0].message.content

        return JsonResponse({'explanation': explanation})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)