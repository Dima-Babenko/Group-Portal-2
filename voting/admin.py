from django.contrib import admin
from .models import Voting, Option, Vote

class OptionInline(admin.TabularInline):
    model = Option
    extra = 2

class VotingAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_by', 'created_at')
    inlines = [OptionInline]

class VoteAdmin(admin.ModelAdmin):
    list_display = ('voting', 'user', 'option', 'voted_at')
    list_filter = ('voting',)

admin.site.register(Voting, VotingAdmin)
admin.site.register(Option)
admin.site.register(Vote, VoteAdmin)