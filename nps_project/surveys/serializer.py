from rest_framework import serializers
from .models.answer import Answer
from .models.question import Question
from .models.respondent import Respondent
from .models.response import Response
from .models.surveys import Survey

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type']

class SurveySerializer(serializers.ModelSerializer):
    questions = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), many=True)

    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'questions']

class RespondentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respondent
        fields = ['id', 'email', 'name']

class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.StringRelatedField()

    class Meta:
        model = Answer
        fields = ['question', 'text', 'choice', 'rating']

class ResponseSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    respondent = RespondentSerializer()

    class Meta:
        model = Response
        fields = ['id', 'respondent', 'survey', 'submitted_at', 'answers']