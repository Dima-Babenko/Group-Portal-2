from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Voting, Option, Vote


def is_moderator_or_admin(user):
    return user.is_authenticated and user.role in ['moderator', 'admin']


@login_required
def voting_list(request):
    votings = Voting.objects.all()
    return render(request, 'voting/voting_list.html', {'votings': votings})


@login_required
def voting_detail(request, voting_id):
    voting = get_object_or_404(Voting, id=voting_id)
    try:
        vote = Vote.objects.get(voting=voting, user=request.user)
    except Vote.DoesNotExist:
        vote = None

    if request.method == 'POST':
        option_id = request.POST.get('option')
        option = get_object_or_404(Option, id=option_id, voting=voting)

        if vote:
            vote.option = option
            vote.save()
        else:
            Vote.objects.create(voting=voting, user=request.user, option=option)

        return redirect('voting:voting_results', voting_id=voting.id)

    return render(request, 'voting/voting_detail.html', {'voting': voting, 'vote': vote})


@login_required
def voting_results(request, voting_id):
    voting = get_object_or_404(Voting, id=voting_id)
    options = voting.options.all()
    total_votes = Vote.objects.filter(voting=voting).count()

    results = []
    for option in options:
        count = Vote.objects.filter(voting=voting, option=option).count()
        percentage = (count / total_votes * 100) if total_votes > 0 else 0
        results.append((option.text, count, percentage))

    return render(request, 'voting/voting_results.html', {
        'voting': voting,
        'results': results,
        'total_votes': total_votes
    })


@user_passes_test(is_moderator_or_admin)
def create_voting(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        options = request.POST.getlist('options')
        voting = Voting.objects.create(question=question, created_by=request.user)

        for text in options:
            if text:
                Option.objects.create(voting=voting, text=text)

        return redirect('voting:voting_list')

    return render(request, 'voting/create_voting.html')


def is_admin(user):
    return user.is_authenticated and user.role == 'admin'


@login_required
@user_passes_test(is_admin)
def delete_voting(request, pk):
    voting = get_object_or_404(Voting, pk=pk)
    voting.delete()
    return redirect('voting:voting_list')