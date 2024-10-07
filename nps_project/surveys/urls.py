from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.views import SurveyViewSet, ResponseViewSet, SurveyResponseView

router = DefaultRouter()
router.register(r'surveys', SurveyViewSet, basename = 'survey')
router.register(r'responses', ResponseViewSet, basename = 'response')

urlpatterns = [
    path('', include(router.urls)),
    path('survey/<int:survey_id>/respond/<str:respondent_email>/', SurveyResponseView.as_view(), name='survey_response'),

]
