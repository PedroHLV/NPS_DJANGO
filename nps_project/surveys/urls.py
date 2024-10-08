from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.views import SurveyViewSet, ResponseViewSet, SurveyResponseView, RespondentViewSet, QuestionViewSet, AnswerViewSet

router = DefaultRouter()
router.register(r'surveys', SurveyViewSet, basename = 'surveys')
router.register(r'responses', ResponseViewSet, basename = 'responses')
router.register(r'respondents', RespondentViewSet, basename='respondents')
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'answers', AnswerViewSet, basename='answers')


urlpatterns = [
    path('', include(router.urls)),
    path('survey/<int:survey_id>/respond/<uuid:token>/', SurveyResponseView.as_view(), name='survey_response'),
]