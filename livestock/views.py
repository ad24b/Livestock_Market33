from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import LivestockForm
from .models import Livestock

@login_required
def add_livestock_view(request):
    if request.method == 'POST':
        form = LivestockForm(request.POST, request.FILES)
        if form.is_valid():
            livestock = form.save(commit=False)
            livestock.seller = request.user
            livestock.save()
            return redirect('list_livestock')  # الانتقال إلى قائمة المواشي بعد الإضافة
    else:
        form = LivestockForm()
    return render(request, 'livestock/add_livestock.html', {'form': form})

def list_livestock_view(request):
    livestock = Livestock.objects.all()
    return render(request, 'livestock/list_livestock.html', {'livestock': livestock})

def livestock_detail(request, pk):
    livestock = get_object_or_404(Livestock, pk=pk)  # جلب المنتج بناءً على المفتاح الأساسي
    return render(request, 'livestock/detail.html', {'livestock': livestock})
