from django.contrib import admin
from django import forms
from .models import Event, Question, UserEvent, Tickie

class QuestionInline(admin.TabularInline):
    model = Question
    extra=0

class TickieInline(admin.TabularInline):
    model = Tickie
    exclude = ('image',)
    extra=0



class UserEventInline(admin.TabularInline):
    model = UserEvent
    extra=0


class EventAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInline,
        TickieInline,
        UserEventInline
    ]



admin.site.register(Event,EventAdmin)
