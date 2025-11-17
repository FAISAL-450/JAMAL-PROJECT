from django.shortcuts import render, redirect
from .models import ChlorideTestReading
from .forms import ChlorideTestReadingForm

def chloridetest_dashboard(request):
    if request.method == 'POST':
        form = ChlorideTestReadingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chloridetest:chloridetest_dashboard')  # namespaced redirect
    else:
        form = ChlorideTestReadingForm()

    readings = ChlorideTestReading.objects.all().order_by('-id')

    return render(request, 'chloridetest/chloridetest_dashboard.html', {
        'form': form,
        'readings': readings,
    })




