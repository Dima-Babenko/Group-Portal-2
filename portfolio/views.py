from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from portfolio import models
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from portfolio.forms import PortfolioForm
from django.db.models import Count
from django.db import IntegrityError
from .models import Portfolio, Like, DisLike


class PortfolioListView(ListView):
    model = Portfolio
    context_object_name = "projects"
    template_name = "portfolio/project_list.html"

    def get_queryset(self):
        return Portfolio.objects.annotate(
            like_count=Count('likes')
        ).order_by('-like_count')


class PortfolioCreateView(CreateView):
    model = models.Portfolio
    template_name = "portfolio/project_create.html"
    form_class = PortfolioForm
    success_url = reverse_lazy("portfolio:project_list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class PortfolioUpdateView(UpdateView):
    model = models.Portfolio
    form_class = PortfolioForm
    template_name = "portfolio/project_update.html"
    success_url = reverse_lazy("portfolio:project_list")


class PortfolioDeleteView(DeleteView):
    model = models.Portfolio
    template_name = "portfolio/project_delete_confirmation.html"
    success_url = reverse_lazy("portfolio:project_list")


class PortfolioLikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Portfolio, pk=pk)
        try:
            Like.objects.create(user=request.user, project=project)
        except IntegrityError:
            like = Like.objects.filter(user=request.user, project=project).first()
            if like:
                like.delete()
        return redirect('portfolio:project_list')


class PortfolioDisLikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Portfolio, pk=pk)
        try:
            DisLike.objects.create(user=request.user, project=project)
        except IntegrityError:
            dislike = DisLike.objects.filter(user=request.user, project=project).first()
            if dislike:
                dislike.delete()
        return redirect('portfolio:project_list')