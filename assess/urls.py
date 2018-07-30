"""iam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from assess import views

app_name = 'assess'
urlpatterns = [
    path('application/create/', views.ApplicationCreate.as_view(), name='application-create'),
    path('', views.ApplicationList.as_view(), name='application-list'),
    path('application/list/assess/', views.ApplicationAssessList.as_view(), name='application-assess-list'),
    path('application/list/approve/', views.ApplicationApproveList.as_view(), name='application-approve-list'),
    path('application/list/request/', views.ApplicationRequestList.as_view(), name='application-request-list'),
    path('application/<str:pk>/', views.ApplicationDetail.as_view(), name='application-detail'),
    path('application/<str:pk>/security/assess/', views.ApplicationSecurityAssess.as_view(), name='application-security-assess'),
    path('application/<str:pk>/privacy/assess/', views.ApplicationPrivacyAssess.as_view(), name='application-privacy-assess'),
    path('application/<str:pk>/clinical/assess/', views.ApplicationClinicalAssess.as_view(), name='application-clinical-assess'),
    path('application/<str:pk>/submit/', views.ApplicationSubmit.as_view(), name='application-submit'),
    path('application/<str:pk>/owner/approve/', views.ApplicationOwnerApproval.as_view(), name='application-owner-approve'),
    path('application/<str:pk>/update/', views.ApplicationUpdate.as_view(), name='application-update'),
    path('application/<str:pk>/delete/', views.ApplicationDelete.as_view(), name='application-delete'),
    path('CAT/', views.CatMeetingList.as_view(), name='catmeeting-list'),
    path('CAT/<int:pk>/', views.CatMeetingDetail.as_view(), name='catmeeting-detail'),
    path('CAT/create/', views.CatMeetingCreate.as_view(), name='catmeeting-create'),
    path('CAT/<str:pk>/decision/<int:catmeeting_id>/', views.CatMeetingDecisionUpdate.as_view(), name='catmeeting-decision-update'),
    path('CAT/<str:pk/delete/', views.CatMeetingDelete.as_view(), name='catmeeting-delete'),
    path('CAT/<str:pk>/update/', views.CatMeetingUpdate.as_view(), name='catmeeting-update'),
    path('cloudquestionnaire/<str:pk>/', views.CloudQuestionnaireDetail.as_view(), name='cloudquestionnaire-detail'),
    path('cloudquestionnaire/<str:pk>/create/', views.CloudQuestionnaireCreate.as_view(), name='cloudquestionnaire-create'),
    path('cloudquestionnaire/<str:pk>/update/', views.CloudQuestionnaireUpdate.as_view(), name='cloudquestionnaire-update'),
    path('cloudquestionnaire/<str:pk>/delete/', views.CloudQuestionnaireDelete.as_view(), name='cloudquestionnaire-delete'),
    path('ictriskassessment/<str:pk>/', views.ICTRiskAssessmentDetail.as_view(), name='ictriskassessment-detail'),
    path('ictriskassessment/<str:pk>/create/', views.ICTRiskAssessmentCreate.as_view(), name='ictriskassessment-create'),
    path('ictriskassessment/<str:pk>/update/', views.ICTRiskAssessmentUpdate.as_view(), name='ictriskassessment-update'),
    path('ictriskassessment/<str:pk>/delete/', views.ICTRiskAssessmentDelete.as_view(), name='ictriskassessment-delete'),
    path('ictvendorassessment/<str:pk>/', views.ICTVendorAssessmentDetail.as_view(), name='ictvendorassessment-detail'),
    path('ictvendorassessment/<str:pk>/create/', views.ICTVendorAssessmentCreate.as_view(), name='ictvendorassessment-create'),
    path('ictvendorassessment/<str:pk>/update/', views.ICTVendorAssessmentUpdate.as_view(), name='ictvendorassessment-update'),
    path('ictvendorassessment/<str:pk>/delete/', views.ICTVendorAssessmentDelete.as_view(), name='ictvendorassessment-delete'),
    path('IPSG/<int:pk>/', views.IPSGMeetingDetailView.as_view(), name='ipsgmeeting-detail'),
    path('informationclassification/<str:pk>/', views.InformationClassificationDetail.as_view(), name='informationclassification-detail'),
    path('informationclassification/<str:pk>/create/', views.InformationClassificationCreate.as_view(), name='informationclassification-create'),
    path('informationclassification/<str:pk>/update/', views.InformationClassificationUpdate.as_view(), name='informationclassification-update'),
    path('informationclassification/<str:pk>/delete/', views.InformationClassificationDelete.as_view(), name='informationclassification-delete'),
    path('privacyassessment/<str:pk>/', views.PrivacyAssessmentDetail.as_view(), name='privacyassessment-detail'),
    path('privacyassessment/<str:pk>/create/', views.PrivacyAssessmentCreate.as_view(), name='privacyassessment-create'),
    path('privacyassessment/<str:pk>/update/', views.PrivacyAssessmentUpdate.as_view(), name='privacyassessment-update'),
    path('privacyassessment/<str:pk>/delete/', views.PrivacyAssessmentDelete.as_view(), name='privacyassessment-delete'),
]
