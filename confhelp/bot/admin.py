from django.contrib import admin
from .models import MeetUpUser, Speach, Question
from django.utils.html import format_html
from django.db.models import Count

@admin.register(MeetUpUser)
class MeetUpUserAdmin(admin.ModelAdmin):
    list_display = [
        'get_meet_up_user_full_name',
        'get_meet_up_user_email',
        'phone',
        'is_speaker',
        ]
    list_filter = ['is_speaker',]
    search_fields = ('user__email',
                     'user__first_name',
                     'user__last_name',
                     'phone')


    def get_meet_up_user_full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

    get_meet_up_user_full_name.short_description = 'Пользователь'


    def get_meet_up_user_email(self, obj):
        return obj.user.email

    get_meet_up_user_email.short_description = 'Почта'


@admin.register(Speach)
class SpeachAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'get_speaker',
        'start_at',
        'end_at',
        ]

    def get_speaker(self, obj):
        return f'{obj.speaker.user.first_name} {obj.speaker.user.last_name}'

    get_speaker.short_description = 'Докладчик'
    # start_at.admin_order_field = 'start_at'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "speaker":
            kwargs["queryset"] = MeetUpUser.objects.filter(is_speaker=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'get_title',
        'get_speach',
        'get_user_count',]

    raw_id_fields = ['speach', 'user',]


    def get_title(self, obj):
        question = obj.title
        if len(question) > 50:
            return f'{question[:50]}...'

        return question

    get_title.short_description = 'Вопрос'


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _user_count=Count("user", distinct=True),
        )
        return queryset


    def get_speach(self, obj):
        speach = obj.speach.title
        if len(speach) > 50:
            return f'{speach[:50]}...'

        return speach

    get_speach.short_description = 'К докладу'


    def get_user_count(self, obj):
        return format_html("<b><i>{}</i></b>", obj._user_count)

    get_user_count.short_description = 'Кол-во вопросов'
    get_user_count.admin_order_field = '_user_count'
