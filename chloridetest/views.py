from django.shortcuts import render, redirect
from .models import ChlorideTestReading
from .forms import ChlorideTestReadingForm

def ctr_dashboard(request):
    if request.method == 'POST':
        form = ChlorideTestReadingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ctr_dashboard')
    else:
        form = ChlorideTestReadingForm()

    readings = ChlorideTestReading.objects.all().order_by('-id')

    return render(request, 'ctr_dashboard.html', {
        'form': form,
        'readings': readings,
    })


