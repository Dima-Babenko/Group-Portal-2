from django.shortcuts import render, get_object_or_404, redirect
from polls import models
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView


class PollListView(ListView):
    model = models.Poll
    context_object_name = "polls"
    template_name = "polls/poll_list.html"