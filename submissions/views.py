from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Submission

@login_required
def submission_list(request):
    submissions = Submission.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'submissions/submission_list.html', {'submissions': submissions})