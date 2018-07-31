#from allauth.account.models import EmailAddress
#from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_select2.forms import Select2MultipleWidget
from django import forms
from django.utils.safestring import mark_safe
from .models import Application, InformationClassification, CloudQuestionnaire 
from .models import	ICTRiskAssessment, ICTVendorAssessment, PrivacyAssessment
from .models import CATmeeting

class ApplicationForm(forms.ModelForm):
	
	class Meta:
		model = Application
		fields = ['name', 'version', 'purpose', 'application_type', 'website', 'cost', 'cost_type', 'requestor', 'business_owner', 'dhbs']
		widgets = {			
			'name': forms.TextInput(attrs={'class' : 'w3-input w3-border'}),
			'version': forms.TextInput(attrs={'class' : 'w3-input w3-border'}),
			'purpose': forms.Textarea(attrs={'class' : 'w3-input w3-border', 'cols': '40', 'rows': '3'}),
			'cost_type': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'requestor': forms.Select(attrs={'class' : 'w3-select w3-border', 'empty_value' : 'Choose a business owner'}),
			'business_owner': forms.Select(attrs={'class' : 'w3-select w3-border'}),
			'application_type': Select2MultipleWidget(attrs={'class' : 'w3-input w3-border', }),
			'dhbs': Select2MultipleWidget(attrs={'class' : 'w3-input w3-border', }),
			'cost': forms.TextInput(attrs={'class' : 'w3-input w3-border'}),
			'website': forms.TextInput(attrs={'class' : 'w3-input w3-border'}),
		}


class ApplicationSubmitForm(forms.ModelForm):
	
	class Meta:
		model = Application
		fields = ['assess_status']
		widgets = {			
			'assess_status': forms.Select(attrs={'class' : 'w3-select w3-border', 'hidden' : True,}),
		}


class ApplicationOwnerApprovalForm(forms.ModelForm):
	
	class Meta:
		model = Application
		fields = ['business_owner_approval', 'business_owner_date', 'assess_status']
		widgets = {			
			'business_owner_approval': forms.CheckboxInput(attrs={'class' : 'w3-check', 'hidden' : True,}),
			'business_owner_date': forms.DateInput(attrs={'class' : 'w3-input w3-border', 'hidden' : True,}),
			'assess_status': forms.Select(attrs={'class' : 'w3-select w3-border', 'hidden' : True, }),
		}


class ApplicationSecurityDecisionForm(forms.ModelForm):
	
	class Meta:
		model = Application
		fields = [
			'security_decision',
			'security_comments',
		]
		widgets = {			
			'security_decision': forms.RadioSelect(attrs={'class' : 'w3-ul',}),
			'security_comments': forms.Textarea(attrs={'class' : 'w3-input w3-border', 'cols': '40', 'rows': '3'}),
		}


class ApplicationPrivacyDecisionForm(forms.ModelForm):
	
	class Meta:
		model = Application
		fields = [
			'privacy_decision',
			'privacy_comments',
		]
		widgets = {			
			'privacy_decision': forms.RadioSelect(attrs={'class' : 'w3-ul',}),
			'privacy_comments': forms.Textarea(attrs={'class' : 'w3-input w3-border', 'cols': '40', 'rows': '3'}),
		}


class ApplicationClinicalDecisionForm(forms.ModelForm):

	class Meta:
		model = Application
		fields = [
			'clinical_decision',
			'clinical_comments',
		]
		widgets = {			
			'clinical_decision': forms.RadioSelect(attrs={'class' : 'w3-ul',}),
			'clinical_comments': forms.Textarea(attrs={'class' : 'w3-input w3-border', 'cols': '40', 'rows': '3'}),
		}


class InformationClassificationForm(forms.ModelForm):
	
 	class Meta:
 		model = InformationClassification
 		fields = '__all__'
 		widgets = {			
			'medical_in_confidence': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'staff_in_confidence': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'commercial_in_confidence': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'statistical_unclassified': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'special_handling_sensitive_patient': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'special_handling_sensitive_disease': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'special_handling_sensitive_abuse': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
		}


class CloudQuestionnaireForm(forms.ModelForm):
	
 	class Meta:
 		model = CloudQuestionnaire
 		fields = '__all__'
 		widgets = {			
			'disclosure_risk': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'alteration_risk': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'loss_risk': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'continuity_risk': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
		}


class ICTRiskAssessmentForm(forms.ModelForm):
	
 	class Meta:
 		model = ICTRiskAssessment
 		fields = '__all__'
 		widgets = {			
			'termsconditions_URL': forms.TextInput(attrs={'class' : 'w3-input w3-border'}),
			'privacypolicy_URL': forms.TextInput(attrs={'class' : 'w3-input w3-border'}),
			'dhb_record_volume': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'dhb_downtime_before_critical': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'dhb_log_data_changes': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'dhb_small_data_loss': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'dhb_large_data_loss': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'dhb_breach_plan': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'dhb_disrupt_plan': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'dhb_perm_loss': forms.RadioSelect(attrs={'class': 'w3-ul'}),
		}
		

class ICTVendorAssessmentForm(forms.ModelForm):
	
 	class Meta:
 		model = ICTVendorAssessment
 		fields = '__all__'
 		widgets = {
 			'host_country': forms.Select(attrs={'class' : 'w3-select w3-border'}),
 			'host_service': forms.TextInput(attrs={'class' : 'w3-input w3-border'}),
			'host_deploy': forms.CheckboxSelectMultiple(attrs={'class': 'w3-ul'}),
			'devices': forms.CheckboxSelectMultiple(attrs={'class': 'w3-ul'}),
			'encrypt_transmit': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'encrypt_stored': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'anonimised': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'back_up': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'extract': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'restore': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'log_admin': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'log_access': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'shares_data': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'notify_breach': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'patches': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'testing': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'advise_legal_issues': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'ownership': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'penalty_breach': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'penalty_outage': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'report_outages': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'backgroud_checks': forms.RadioSelect(attrs={'class': 'w3-ul'}),
		}

		# app, host_country,host_service, host_deploy, devices, encrypt_transmit, encrypt_stored, anonimised, back_up, extract, restore, 
		# log_admin, log_access, shares_data, notify_breach, patches, testing, advise_legal_issues, ownership, penalty_breach, penalty_outage,
		#  report_outages, backgroud_checks

class PrivacyAssessmentForm(forms.ModelForm):
	
	class Meta:
		model = PrivacyAssessment
		fields = '__all__'
		widgets = {
 			'desc': forms.Textarea(attrs={'class' : 'w3-input w3-border', 'cols': '40', 'rows': '3'}),
			'personal_info': forms.Textarea(attrs={'class' : 'w3-input w3-border', 'cols': '40', 'rows': '3'}),
			'substantial_change': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'risk_register': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'collection': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'new_collect': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'new_store': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'new_sensitive': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'offshore': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'disclosure': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'sharing': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'policy': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'new_id': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'monitoring': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'premises': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'regulatory': forms.CheckboxInput(attrs={'class' : 'w3-check'}),
			'info_handling': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'sensitivity': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'significance': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'interaction': forms.RadioSelect(attrs={'class': 'w3-ul'}),
			'public_impact': forms.RadioSelect(attrs={'class': 'w3-ul'}),
		}
# char: app, desc, 
# boolean: personal_info, substantial_change, risk_register, collection, new_collect, new_store, 
# new_sensitive, offshore, disclosure, sharing, policy, new_id, monitoring, premises, regulatory
# choice: info_handling, sensitivity, significance, interaction, public_impact


class CATmeetingForm(forms.ModelForm):
	u = User.objects.filter(groups__name='cloud_assessment_team')
	attendees = forms.ModelMultipleChoiceField(
		queryset=u.distinct(), widget=Select2MultipleWidget(attrs={'class' : 'w3-input w3-border w3-xlarge'}))

	class Meta:
		model = CATmeeting
		fields = ['meeting_date', 'attendees']
		widgets = {			
			'meeting_date': forms.DateInput(attrs={'class' : 'w3-input w3-border'}),
		}


class ApplicationDecisionForm(forms.ModelForm):
	CAT_DECISION_CHOICES = (
		('R', 'Reject'),
		('P', 'Approve'),
		('E', 'Escalate to IPSG'),
	)
	cat_decision = forms.ChoiceField(choices=CAT_DECISION_CHOICES, label="CAT decision", widget=forms.RadioSelect(attrs={'class': 'w3-ul'}))

	class Meta:
		model = Application
		fields = ['name', 'CATmeeting', 'assess_status']
		widgets = {			
			'CATmeeting': forms.NumberInput(attrs={'class' : 'w3-input w3-border' }),
			'assess_status': forms.RadioSelect(attrs={'class': 'w3-ul', }),
		}


class IPSGMeetingForm(forms.ModelForm):
	pass