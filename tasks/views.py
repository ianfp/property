from django.shortcuts import render_to_response, redirect
from tasks import forms, services
from django.template.context import RequestContext
import io
from django.contrib.auth.decorators import login_required
from tasks.models import Task

@login_required
def upload(request):
    """
    Upload a CSV file of tasks into the system.
    """
    if request.method == 'POST':
        form = forms.UploadForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.cleaned_data['property']
            upload = request.FILES['csv_file']
            f = io.TextIOWrapper(upload.file, encoding=request.encoding)
            services.import_csv(prop, f)
            return redirect('admin:tasks_task_changelist')
    else:
        form = forms.UploadForm()
        
    context = RequestContext(request, {
        'form': form
    })
    return render_to_response('tasks/upload.html', context)


def report(request):
    """
    View a report of tasks that need to be done.
    """
    all_tasks = Task.objects.exclude(last_done=None).order_by('asset__name')
    year = 2014
    tasks = [ task for task in all_tasks if task.next_due and task.next_due.year <= year ]
    total_estimate = 0
    for task in tasks:
        if task.estimate is not None:
            total_estimate += task.extended_estimate
    
    context = RequestContext(request, { 
        'year': year,
        'tasks': tasks,
        'total_estimate': total_estimate
    })
    return render_to_response('tasks/report.html', context)