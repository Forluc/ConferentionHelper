from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime
from django.db.models import Q


class MeetUpUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь')

    telegram_id = models.CharField(
        'Telegram id',
        max_length=50,
        db_index=True)

    is_speaker = models.BooleanField(
        default=False,
        verbose_name='Докладчик')

    phone = PhoneNumberField(
        'Номер телефона',
        null=True,
        blank=True,
        db_index=True)


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


    def get_users_telegram_id():
        users_telegram_id = []
        users_telegram_id_set = MeetUpUser.objects.all()
        for user_telegram_id in users_telegram_id_set:
            users_telegram_id.append(user_telegram_id.telegram_id)
        return users_telegram_id


class Speach(models.Model):
    title = models.CharField(
        'Наименование',
        max_length=200,)

    description = models.TextField(
        'Описание', blank=True)

    speaker = models.ForeignKey(
        MeetUpUser,
        on_delete=models.CASCADE,
        related_name='speachs',
        verbose_name='Спикер')

    start_at = models.DateTimeField(
        verbose_name='Начало')

    end_at = models.DateTimeField(
        verbose_name='Окончание')


    def __str__(self):
        return self.title


    def get_speakers():
        speakers_set = MeetUpUser.objects.filter(is_speaker=True)
        speakers = []
        for speaker in speakers_set:
            speakers.append(f'{speaker.user.first_name} {speaker.user.last_name}')
        return speakers


    def get_speaker_details():
        curent_date_time = datetime.now().astimezone()
        speach = Speach.objects.filter(
            start_at__lte=curent_date_time,
            end_at__gte=curent_date_time).first()
        if not speach:
            return None
        speaker_details = {
            'speaker': f'{speach.speaker.user.first_name} {speach.speaker.user.last_name}',
            'date': speach.start_at.strftime('%Y-%m-%d'),
            'start_time': speach.start_at.strftime('%H:%M'),
            'end_time': speach.end_at.strftime('%H:%M'),
            'lecture': speach.title,
            'description': speach.description,
            }
        return speaker_details


    def get_speakers_details():
        speakers_details = {}
        speakers_set = MeetUpUser.objects.filter(is_speaker=True)
        for speaker in speakers_set:
            speachs = speaker.speachs.all().order_by('start_at')
            speaker_name = f'{speaker.user.first_name} {speaker.user.last_name}'

            speach_details =[]
            for speach in speachs:
                speach_details.append(
                    {
                    'date': speach.start_at.strftime('%Y-%m-%d'),
                    'start_time': speach.start_at.strftime('%H:%M'),
                    'end_time': speach.end_at.strftime('%H:%M'),
                    'lecture': speach.title,
                    'description': speach.description,
                    })
            speakers_details[speaker_name] = speach_details
        return speakers_details


    def get_programs():
        programs_set = Speach.objects.all().order_by('start_at')
        programs = []
        for program_set in programs_set:
            date_str = program_set.start_at.strftime('%Y-%m-%d')
            time_range = f'{program_set.start_at.strftime("%H:%M")} - {program_set.end_at.strftime("%H:%M")}'
            for key, program in enumerate(programs):
                if program.get(date_str):
                    t_r = program.get(date_str)
                    print(t_r)
                    t_r.append(time_range)
                    print(t_r)
                    programs[key] = {date_str: [t_r]}
                    break
            else:
                programs.append({date_str: [time_range]})

        return programs


class Question(models.Model):
    title = models.TextField(
        'Вопрос',)

    speach = models.ForeignKey(
        Speach,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='К докладу',)

    user = models.ManyToManyField(
        User,
        related_name='questions',
        verbose_name='Кто задал вопрос')


    def __str__(self):
        return self.title


    def get_questions():
        questions = []
        curent_date_time = datetime.now().astimezone()

        speach = Speach.objects.filter(
            start_at__lte=curent_date_time,
            end_at__gte=curent_date_time).first()
        if not speach:
            return None

        questions_set = speach.questions.all()
        if not questions_set:
            return None

        for question in questions_set:
            questions.append(question.title)
        return questions

