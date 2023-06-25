from django.http import HttpResponse
from django.shortcuts import render
from .models import Speach, Question, MeetUpUser

def index(request):
    result = f'<h1>Python Week 2023 MeetUp</h1>\
        <h3>Запросы бота для спикеров</h3>\
        <b>Speach.get_speakers()</b> - выдает список всех зарегистрированных спикеров</br>\
        speakers = {Speach.get_speakers()}</br>\
        <b>Question.get_questions()</b> - выдает список вопросов к докладу первому в текущем временном диапазоне</br>\
        questions = {Question.get_questions()}\
        <h3>Запросы бота для пользователей</h3>\
        <b>MeetUpUser.get_users_telegram_id()</b> - Получение списка телеграм id всех пользователей</br>\
        users_id = {MeetUpUser.get_users_telegram_id()}</br>\
        <b>Speach.get_speaker_details</b> - Получение словаря спикера который выступает сейчас</br>\
        speaker_details = {Speach.get_speaker_details()}</br>\
        <b>Speach.get_speakers_details</b> - Получение списка всех выступлений спикеров</br>\
        speakers = {Speach.get_speakers_details()}</br>\
        <b>Speach.get_programs</b> - Получение списка словарей(ключ-дата события, значение список из времени)</br>\
        programs = {Speach.get_programs()}'

    return HttpResponse(result)

