from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from . import models


def is_moderator(user):
    return user.is_superuser or user.groups.filter(name='Moderators').exists()


def moderator_required(view_func):
    decorated_view_func = login_required(user_passes_test(is_moderator)(view_func))
    return decorated_view_func


class PollResultsView(View):
    def get(self, request, pk):
        poll = get_object_or_404(models.Poll, pk=pk)
        user_answers = models.Answer.objects.filter(user=request.user, question__poll=poll)
        answers = []

        for answer in user_answers:
            answers.append({
                'question': answer.question.text,
                'selected_option': answer.selected_option.text
            })

        return render(request, 'polls/poll_results.html', {'poll': poll, 'answers': answers})


class PollDetailView(View):
    def get(self, request, pk):
        poll = get_object_or_404(models.Poll, pk=pk)

        # Перевірка, чи користувач вже відповів на це опитування
        if models.Answer.objects.filter(user=request.user, question__poll=poll).exists():
            return redirect('polls:poll_results', pk=poll.pk)  # Перенаправляємо на результати, якщо відповіли

        return render(request, 'polls/poll_detail.html', {'poll': poll})

    def post(self, request, pk):
        poll = get_object_or_404(models.Poll, pk=pk)

        # Перевірка, чи користувач вже відповів на це опитування
        if models.Answer.objects.filter(user=request.user, question__poll=poll).exists():
            return redirect('polls:poll_results', pk=poll.pk)  # Перенаправляємо на результати, якщо вже відповіли

        # Перевірка, чи були відправлені відповіді
        answers = []
        for question in poll.questions.all():
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id:
                selected_option = get_object_or_404(models.Option, id=selected_option_id)
                # Зберігаємо відповідь
                answer, created = models.Answer.objects.update_or_create(
                    user=request.user,
                    question=question,
                    defaults={'selected_option': selected_option}
                )
                answers.append({
                    'question': question.text,
                    'selected_option': selected_option.text
                })

        # Перенаправляємо на сторінку з результатами опитування
        return render(request, 'polls/poll_results.html', {'poll': poll, 'answers': answers})


@method_decorator(moderator_required, name='dispatch')
class PollCreateView(View):
    def get(self, request):
        return render(request, 'polls/poll_create.html')

    def post(self, request):
        title = request.POST.get('title')
        if not title:
            return render(request, 'polls/poll_create.html', {'error': 'Назва обов\u2019язкова'})

        poll = models.Poll.objects.create(title=title, created_by=request.user)
        return redirect('polls:add_question', poll_id=poll.id)


@method_decorator(moderator_required, name='dispatch')
class AddQuestionView(View):
    def get(self, request, poll_id):
        poll = get_object_or_404(models.Poll, id=poll_id)
        return render(request, 'polls/poll_add_question.html', {'poll': poll})

    def post(self, request, poll_id):
        poll = get_object_or_404(models.Poll, id=poll_id)
        text = request.POST.get('text')

        if text:
            question = models.Question.objects.create(poll=poll, text=text)
            return redirect('polls:add_option', question_id=question.id)

        return render(request, 'polls/poll_add_question.html', {'poll': poll, 'error': 'Питання обов\u2019язкове'})


@method_decorator(moderator_required, name='dispatch')
class AddOptionView(View):
    def get(self, request, question_id):
        question = get_object_or_404(models.Question, id=question_id)
        return render(request, 'polls/poll_add_option.html', {'question': question})

    def post(self, request, question_id):
        question = get_object_or_404(models.Question, id=question_id)
        text = request.POST.get('text')

        if text:
            models.Option.objects.create(question=question, text=text)

        if 'add_another_option' in request.POST:
            return redirect('polls:add_option', question_id=question.id)

        if 'add_another_question' in request.POST:
            return redirect('polls:add_question', poll_id=question.poll.id)

        return redirect('polls:poll_list')


class PollListView(View):
    def get(self, request):
        polls = models.Poll.objects.all()
        return render(request, 'polls/poll_list.html', {'polls': polls})
