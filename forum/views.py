from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.urls import reverse
from forum import models
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from forum.mixins import UserOwnerMixin
from forum.forms import BranchForm, CommentForm
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class BranchListView(ListView):
    model = models.Branch
    context_object_name = "branches"
    template_name = "tasks/branch_list.html"


class BranchDetailView(DetailView):
    model = models.Branch
    context_object_name = "branch"
    template_name = "forum/branch_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST, request.FILES)
        branch = self.get_object()
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.branch = branch
            if comment.content or comment.media:
                comment.save()
            return redirect('forum:branch_detail', pk=branch.pk)

        context = self.get_context_data()
        context['comment_form'] = comment_form
        return self.render_to_response(context)


class BranchCreateView(LoginRequiredMixin, CreateView):
    model = models.Branch
    template_name = "forum/branch_form.html"
    form_class = BranchForm
    success_url = reverse_lazy("forum:branch_list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class BranchUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    model = models.Branch
    form_class = BranchForm
    template_name = "forum/branch_update.html"
    success_url = reverse_lazy("forum:branch_list")


class BranchDeleteView(LoginRequiredMixin, UserOwnerMixin, DeleteView):
    model = models.Branch
    template_name = "forum/branch_delete_confirmation.html"
    success_url = reverse_lazy("forum:branch_list")


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Comment
    template_name = "forum/comment_delete_confirmation.html"

    def get_success_url(self):
        return reverse('forum:branch_detail', kwargs={'pk': self.object.branch.pk})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            return redirect('forum:branch_detail', pk=obj.branch.pk)
        return super().dispatch(request, *args, **kwargs)


@login_required
def add_comment(request, pk):
    branch = get_object_or_404(models.Branch, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        media = request.FILES.get('media')
        parent_id = request.POST.get('parent_id')
        parent = models.Comment.objects.filter(id=parent_id).first() if parent_id else None

        if content or media:
            models.Comment.objects.create(
                branch=branch,
                author=request.user,
                content=content,
                media=media,
                parent=parent
            )

    return redirect('forum:branch_detail', pk=pk)
