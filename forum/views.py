from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from forum import models
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from forum.mixins import UserOwnerMixin
from forum.forms import BranchForm, CommentForm
from django.http import HttpResponseRedirect


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
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.branch = self.get_object()
            comment.save()
            return redirect('forum:branch_detail', pk=comment.branch.pk)
        else:
            pass


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
