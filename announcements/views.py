# announcements/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Announcement
from .forms import AnnouncementForm
from django.contrib.auth.decorators import login_required

def announcement_list(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'announcements/list.html', {'announcements': announcements})

@login_required
def announcement_create(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()
            return redirect('announcements:announcement_list')
    else:
        form = AnnouncementForm()
    return render(request, 'announcements/form.html', {'form': form})

@login_required
def announcement_update(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcements:announcement_list')
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'announcements/form.html', {'form': form})

@login_required
def announcement_delete(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        announcement.delete()
        return redirect('announcements:announcement_list')
    return render(request, 'announcements/confirm_delete.html', {'announcement': announcement})
