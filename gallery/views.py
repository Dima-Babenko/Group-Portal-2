from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import MediaFile, Category
from .forms import MediaFileForm

def gallery_view(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    media_type = request.GET.get('type')  # ← добавлено

    media_files = MediaFile.objects.filter(is_approved=True)

    if selected_category:
        media_files = media_files.filter(category__id=selected_category)

    if media_type:
        media_files = media_files.filter(media_type=media_type)  # ← фильтрация по типу

    context = {
        'categories': categories,
        'media_files': media_files,
        'media_type': media_type,  # ← передаем в шаблон
    }
    return render(request, 'gallery/gallery.html', context)

def add_media(request):
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("qwe")
            media = form.save(commit=False)
            media.is_approved = True
            media.save()
            return redirect('gallery:gallery_view')
    else:
        form = MediaFileForm()
    return render(request, 'gallery/add_media.html', {'form': form})


def edit_media(request, pk):
    media = get_object_or_404(MediaFile, pk=pk)
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES, instance=media)
        if form.is_valid():
            form.save()
            return redirect('gallery_view')
    else:
        form = MediaFileForm(instance=media)
    return render(request, 'gallery/edit_media.html', {'form': form})

def delete_media(request, pk):
    media = get_object_or_404(MediaFile, pk=pk)
    media.delete()
    return redirect('gallery_view')
