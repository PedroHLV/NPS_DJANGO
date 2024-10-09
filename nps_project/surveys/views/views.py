from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response as DRFResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from ..serializer import SurveySerializer, RespondentSerializer, ResponseSerializer, AnswerSerializer, QuestionSerializer
from ..models.surveys import Survey
from ..models.answer import Answer
from ..models.respondent import Respondent
from ..models.response import Response
from ..models.question import Question
from ..models.invitation import Invitation
from ..utils.email_envio import send_survey_email
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

class AnswerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
class RespondentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Respondent.objects.all()
    serializer_class = RespondentSerializer
    permission_classes = [IsAuthenticated]
class SurveyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    def get(self, request, survey_id, token):
        survey = get_object_or_404(Survey, pk=survey_id)
        invitation = get_object_or_404(Invitation, token=token, survey=survey)
        respondent = invitation.respondent
        
        # Verificar se já existe uma resposta para esta invitation
        if hasattr(invitation, 'response'):
            return render(request, 'surveys/already_responded.html')
        
        return render(request, 'surveys/survey_form.html', {
            'survey': survey,
            'respondent': respondent,
            'invitation': invitation
        })

    def post(self, request, survey_id, token):
        survey = get_object_or_404(Survey, pk=survey_id)
        invitation = get_object_or_404(Invitation, token=token, survey=survey)
        respondent = invitation.respondent
        
        # Evitar múltiplas submissões para a mesma invitation
        if hasattr(invitation, 'response'):
            return render(request, 'surveys/already_responded.html')
        
        # Criar a Response
        response = Response.objects.create(
            respondent=respondent,
            survey=survey,
            invitation=invitation
        )
        
        # Salvar as respostas das perguntas
        for question in survey.questions.all():
            answer_text = request.POST.get(f'question_{question.id}')
            Answer.objects.create(
                response=response,
                question=question,
                text=answer_text
            )
        
        return render(request, 'surveys/thank_you.html')
