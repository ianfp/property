from django.shortcuts import render_to_response, redirect
from tasks import forms, services
from django.template.context import RequestContext
import io
from django.contrib.auth.decorators import login_required

@login_required
def upload(request):
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