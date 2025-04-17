from django.contrib import admin
from .models import Voting, Option, Vote


class OptionInline(admin.TabularInline):
    model = Option
    extra = 1
    min_num = 1


class VotingAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_by', 'created_at')
    inlines = [OptionInline]


class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'get_voting_question')

    def get_voting_question(self, obj):
        return obj.voting.question
    get_voting_question.short_description = 'Питання'


admin.site.register(Voting, VotingAdmin)
admin.site.register(Option, OptionAdmin)