from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response as DRFResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from ..serializer import SurveySerializer, RespondentSerializer, ResponseSerializer
from ..models.surveys import Survey
from ..models.answer import Answer
from ..models.respondent import Respondent
from ..models.response import Response
from ..utils.email_envio import send_survey_email
from rest_framework.permissions import IsAdminUser

class SurveyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def send(self, request, pk=None):
        survey = self.get_object()
        respondent_ids = request.data.get('respondents', [])
        respondents = Respondent.objects.filter(id__in=respondent_ids)
        for respondent in respondents:
            send_survey_email(survey, respondent)
        return DRFResponse({'status': 'email sent'})

class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

    def create(self, request, *args, **kwargs):
        respondent_data = request.data.get('respondent')
        respondent, created = Respondent.objects.get_or_create(email=respondent_data['email'], defaults={'name': respondent_data.get('name', '')})

        response = Response.objects.create(respondent=respondent, survey_id=request.data.get('survey'))

        answers_data = request.data.get('answers')
        for answer_data in answers_data:
            Answer.objects.create(
                response=response,
                question_id=answers_data['question'],
                text=answers_data['text']
            )
        serializer = self.get_serializer(response)
        return DRFResponse(serializer.data, status=status.HTTP_201_CREATED)
    
class SurveyResponseView(View):
    def get(self, request, survey_id, respondent_email):
        survey = get_object_or_404(Survey, pk=survey_id)
        respondent = get_object_or_404(Respondent, email=respondent_email)
        # Verificar se o respondente já respondeu a este survey
        if Response.objects.filter(respondent=respondent, survey=survey).exists():
            return render(request, 'surveys/already_responded.html')
        return render(request, 'surveys/survey_form.html', {'survey': survey, 'respondent': respondent})

    def post(self, request, survey_id, respondent_email):
        survey = get_object_or_404(Survey, pk=survey_id)
        respondent = get_object_or_404(Respondent, email=respondent_email)
        # Evitar múltiplas submissões
        if Response.objects.filter(respondent=respondent, survey=survey).exists():
            return render(request, 'surveys/already_responded.html')
        response = Response.objects.create(respondent=respondent, survey=survey)
        for question in survey.questions.all():
            answer_text = request.POST.get(f'question_{question.id}')
            Answer.objects.create(response=response, question=question, text=answer_text)
        return render(request, 'surveys/thank_you.html')

