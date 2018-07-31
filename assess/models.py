import datetime
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.functional import curry
from django_countries.fields import CountryField
from simple_history.models import HistoricalRecords

# Create your models here.
class DHBs(models.Model):
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.name

class ApplicationType(models.Model):
	name = models.CharField(max_length=30)
	icon_html = models.CharField(max_length=200)

	def __str__(self):
		return self.name


class Application(models.Model):
	requestor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requestor")
	business_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="business_owner")
	name = models.CharField(max_length=254, primary_key=True)
	version = models.CharField(max_length=10)
	website = models.URLField(max_length=200)
	purpose = models.CharField(max_length=254)
	cost = models.CharField(max_length=254)
	COST_CHOICES = (
		('1', 'One time payment'),
		('M', 'Monthly'),
		('Y', 'Annually'),
	)
	cost_type = models.CharField(
		max_length=1,
		choices=COST_CHOICES,
		default='Y',
		verbose_name="Renewal"
	)
	application_type = models.ManyToManyField(ApplicationType)
	ASSESSMENT_STATUS = (
		('N', 'New'),
		('S', 'Submitted'),
		('A', 'Assessing'),
		('R', 'Rejected'),
		('P', 'Approved'),
	)
	assess_status = models.CharField(
		max_length=1,
		choices=ASSESSMENT_STATUS,
		default='N',
		verbose_name="Status"
	)
	RISK_RATING = (
		('N', 'No Risk'),
		('L', 'Low Impact Risk'),
		('H', 'High Impact Risk'),
		('E', 'Extreme Risk'),
	)
	dhbs = models.ManyToManyField(DHBs)
	security_decision = models.CharField(
		max_length=1,
		choices=RISK_RATING,
		blank=True,
		null=True,
	)
	security_comments = models.CharField(max_length=254, null=True, blank=True)
	privacy_decision = models.CharField(
		max_length=1,
		choices=RISK_RATING,
		blank=True,
		null=True,
	)
	privacy_comments = models.CharField(max_length=254, null=True, blank=True)
	clinical_decision = models.CharField(
		max_length=1,
		choices=RISK_RATING,
		blank=True,
		null=True,
	)
	clinical_comments = models.CharField(max_length=254, null=True, blank=True)
	CATmeeting = models.ForeignKey('CATmeeting', on_delete=models.SET_NULL, null=True, blank=True)
	escalate_IPSG = models.BooleanField(default=False)
	business_owner_approval = models.BooleanField(default=False)
	business_owner_date = models.DateField(verbose_name='Submit Date', null=True, blank=True)
	attachments =  models.FileField(null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	history = HistoricalRecords()

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('assess:application-detail', kwargs={'pk': self.pk})


class InformationClassification(models.Model):
	app = models.OneToOneField(Application, on_delete=models.CASCADE, primary_key=True)
	medical_in_confidence = models.BooleanField(default=False, help_text="Personal health information")
	staff_in_confidence = models.BooleanField(default=False, help_text="Identifiable employee and practitioner information that is not intended for the public domain")
	commercial_in_confidence = models.BooleanField(default=False, help_text="Commercially sensitive information that needs protection from unauthorised access")
	statistical_unclassified = models.BooleanField(default=False, help_text="Statistical or financial information that is non–identifiable")
	unclassified = models.BooleanField(default=False, help_text="All other information. Cannot derive persons identity from data.")
	special_handling_sensitive_patient = models.BooleanField(default=False, help_text="Sensitive patient information (eg VIP’s)")
	special_handling_sensitive_disease = models.BooleanField(default=False, help_text="Sensitive categories of disease (eg Mental Health)")
	special_handling_sensitive_abuse = models.BooleanField(default=False, help_text="Sensitive subjects (violence and abuse; pandemics)")
	special_handling_sensitive_other = models.CharField(max_length=200, null=True, blank=True, help_text="Other")
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	history = HistoricalRecords()


class CloudQuestionnaire(models.Model):
	app = models.OneToOneField(Application, on_delete=models.CASCADE, primary_key=True)
	disclosure_risk = models.BooleanField(default=False, verbose_name='Privacy Breach', help_text="If a data breach or release of information into the public domain occurred it would compromise our obligations to a person or an organisation.")
	alteration_risk = models.BooleanField(default=False, verbose_name='Information Alteration', help_text="If the app's information is altered by mistake or intentionally by a wrongdoer, a person(s) or organisation(s) will be harmed.")
	loss_risk = models.BooleanField(default=False, verbose_name='Data Loss', help_text="If the information is lost by the cloud provider OR we can easily maintain a local copy of the information, a person(s) or orginastion will be harmed.")
	continuity_risk = models.BooleanField(default=False, verbose_name='Business Continuity', help_text="If the service is disrupted or is unavailable for an extended, we will be unable to carry out our activities .")

	def _get_help_text(self, field_name):

		for field in self._meta.fields:
			if field.name == field_name:
				return field.help_text
	
	def _get_verbose_name(self, field_name):

		for field in self._meta.fields:
			if field.name == field_name:
				return field.verbose_name

	def __init__(self, *args, **kwargs):
		super(CloudQuestionnaire, self).__init__(*args, **kwargs)

		for field in self._meta.fields:
			method_name = "get_{0}_help_text".format(field.name)
			curried_method = curry(self._get_help_text, field_name=field.name)
			setattr(self, method_name, curried_method)
			method_v_name = "get_{0}_verbose_name".format(field.name)
			curried_v_method = curry(self._get_verbose_name, field_name=field.name)
			setattr(self, method_v_name, curried_v_method)


class ICTRiskAssessment(models.Model):
	app = models.OneToOneField(Application, on_delete=models.CASCADE, primary_key=True)
	termsconditions_URL = models.URLField(help_text="1. Please copy and paste the apps terms and conditions from the vendors website. Make sure you get the T&Cs for the version of the app you want.")
	privacypolicy_URL = models.URLField(help_text="2. Please copy and paste the apps privacy policy from the vendors website. Make sure you get the privacy policy for the version of the app you want.")
	RECORD_CHOICES = (
		('TENS', '10s'),
		('HUNDREDS', '100s'),
		('THOUSANDS', '1,000s'),
		('TENTHOUSANDS', '10,000s'),
		('HUNDREDTHOUSANDS', '100,000s'),
	)
	dhb_record_volume = models.CharField(max_length=15, choices=RECORD_CHOICES, default='TENS', help_text="3. Provide an estimate of the number of records we expect to store in the application on an annual basis.")
	DOWNTIME_CHOICES = (
		('H', 'Hours'),
		('D', 'Days'),
		('M', 'Months'),
		('I', 'Indefinitely')
	)
	dhb_downtime_before_critical = models.CharField(max_length=1, choices=DOWNTIME_CHOICES, default='H', help_text="4. We can be without this app before our service can no longer function properly. Specify the time interval.")
	UNSURE_CHOICES = (
		('Y', 'Yes'),
		('N', 'No'),
		('U', 'Unsure'),
	)
	dhb_log_data_changes = models.CharField(max_length=1, choices=UNSURE_CHOICES, default='U', help_text="5. We will be able to notice if someone accidentally or maliously alters our data stored in the cloud service.")
	CONVENIENCE_CHOICES = (
		('N', 'None'),
		('I', 'Inconvenience'),
		('D', 'Disruption'),
		('P', 'Personal Injury'),
		('S', 'Significant economic loss'),
		('H', 'Human life endangered'),
	)
	dhb_small_data_loss = models.CharField(max_length=1, choices=CONVENIENCE_CHOICES, default='N', help_text="6. The effect of someone accidentally or malciously altering a SMALL amount of our data stored in the cloud service.")
	dhb_large_data_loss = models.CharField(max_length=1, choices=CONVENIENCE_CHOICES, default='N', help_text="7. The effect of someone accidentally or malciously altering a LARGE amount of our data stored in the cloud service.")
	dhb_breach_plan = models.CharField(max_length=1, choices=UNSURE_CHOICES, default='U', help_text="8. We have a plan we can put into effect if we learn that there has been a privacy or security breach concerning our data stored in the cloud service.")
	dhb_disrupt_plan = models.CharField(max_length=1, choices=UNSURE_CHOICES, default='U', help_text="9. We have a plan we can put into effect if the cloud service is disrupted for an extended period.")
	dhb_perm_loss = models.CharField(max_length=1, choices=UNSURE_CHOICES, default='U', help_text="10. We have a plan we can put into effect if the cloud service loses our data permanently.")

	def _get_help_text(self, field_name):

		for field in self._meta.fields:
			if field.name == field_name:
				return field.help_text
	
	def __init__(self, *args, **kwargs):
		super(ICTRiskAssessment, self).__init__(*args, **kwargs)

		for field in self._meta.fields:
			method_name = "get_{0}_help_text".format(field.name)
			curried_method = curry(self._get_help_text, field_name=field.name)
			setattr(self, method_name, curried_method)


class TechDelivery(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class TechInstall(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class ICTVendorAssessment(models.Model):
	app = models.OneToOneField(Application, on_delete=models.CASCADE, primary_key=True)
	UNSURE_CHOICES = (
			('Y', 'Yes'),
			('N', 'No'),
			('U', 'Unsure'),
	)
	TIME_CHOICES = (
		('H','Hours'), 
		('D', 'Days'),
		('M', 'Months'),
		('N', 'Does not'),
	)
	host_country = CountryField(help_text="1. What country or countries is the service hosted in?")
	host_service = models.CharField(max_length=120, help_text="2. Name any 3rd party suppliers used by the vendor to supply this service e.g. Microsoft Azure, Amazon Web Services.")
	host_deploy = models.ManyToManyField(TechInstall, help_text="3. The service requires the customer to do the following work")
	devices = models.ManyToManyField(TechDelivery, help_text="4. Users access the service using the following technology")
	encrypt_transmit = models.CharField(max_length=1, choices=UNSURE_CHOICES, default='U', help_text="5. The data is encrypted when it is being transmitted to the cloud service")
	encrypt_stored = models.CharField(max_length=1, choices=UNSURE_CHOICES, default='U', help_text="6. The customer’s data is encrypted inside the cloud service data store")
	anonimised = models.CharField(max_length=1, choices=UNSURE_CHOICES, default='U', help_text="7. The data is de-identified BEFORE  it is sent to the cloud service")
	back_up = models.CharField(max_length=1, choices=UNSURE_CHOICES, default='U', help_text="8. The vendor backs up the data stored in the cloud service")
	extract = models.CharField(max_length=1, choices=UNSURE_CHOICES, default='U', help_text="9. The vendor provides a means for the customer to download a copy of the  data stored  the cloud service")
	restore = models.CharField(max_length=1, choices=TIME_CHOICES, default='U', help_text="10. The vendor undertakes to re-instate the service in the event of an outage in")
	log_admin = models.CharField(max_length=1, choices=UNSURE_CHOICES, default='U', help_text="11. The vendor logs sys admin access to  the  data stored in the cloud service")
	log_access = models.CharField(max_length=1, choices=UNSURE_CHOICES, default='U', help_text="12. The vendor logs end user access to  the data stored in the cloud service")
	shares_data = models.CharField(max_length=1, choices=UNSURE_CHOICES, default='U', help_text="13. The vendor allows 3rd parties to access the data stored in the cloud service")
	notify_breach = models.CharField(max_length=1, choices=UNSURE_CHOICES, default='U', help_text="14. The vendor will tell the customer if there has been a security or privacy  incident concerning the data stored in the cloud service")
	patches = models.CharField(max_length=1, choices=UNSURE_CHOICES, default='U', help_text="15. The vendor regularly applies  security patches to applications, devices, servers and hypervisors  ")
	testing = models.CharField(max_length=1, choices=UNSURE_CHOICES, default='U', help_text="16. The vendor undertakes regular  security testing / certification")
	advise_legal_issues = models.CharField(max_length=1, choices=UNSURE_CHOICES, default='U', help_text="17. The vendor will tell the customer if there has been a Court Order concerning the data stored in the cloud service")
	ownership = models.CharField(max_length=1, choices=UNSURE_CHOICES, default='U', help_text="18. The vendor’s terms of service give the vendor ownership rights over the data stored in the cloud service")
	penalty_breach = models.CharField(max_length=1, choices=UNSURE_CHOICES, default='U', help_text="19. The vendor will pay compensation if the customer suffers a loss as a result of a privacy or security breach of data stored in the cloud service")
	penalty_outage = models.CharField(max_length=1, choices=UNSURE_CHOICES, default='U', help_text="20. The vendor will  pay compensation if the  customer suffer a loss as a result of the cloud service being unavailable for any length of time")
	report_outages = models.CharField(max_length=1, choices=UNSURE_CHOICES, default='U', help_text="21. The vendor provides a means for the customer to complain in the event of a privacy breach or service disruption")
	backgroud_checks = models.CharField(max_length=1, choices=UNSURE_CHOICES, default='U', help_text="22. The vendor’s HR procedures include background vetting of employees and contractors")

	def _get_help_text(self, field_name):

		for field in self._meta.fields:
			if field.name == field_name:
				return field.help_text
	
	def __init__(self, *args, **kwargs):
		super(ICTVendorAssessment, self).__init__(*args, **kwargs)

		for field in self._meta.fields:
			method_name = "get_{0}_help_text".format(field.name)
			curried_method = curry(self._get_help_text, field_name=field.name)
			setattr(self, method_name, curried_method)


class PrivacyAssessment(models.Model):
	LEVELS = (
			('H', 'High'),
			('M', 'Medium'),
			('L', 'Low'),
	)
	app = models.OneToOneField(Application, on_delete=models.CASCADE, primary_key=True)
	desc = models.CharField(blank=True, null=True, max_length=255, verbose_name='Brief description of the project', 
		help_text='Describe your existing systems and the main changes that are proposed. Describe the purpose of the change, including any projected benefits to your organisation or to the individuals affected. Identify the main stakeholders or entities involved, and their role in the project.')
	personal_info = models.CharField(blank=True, null=True, max_length=255, verbose_name='Personal information that the project will involve', 
		help_text='A description of the personal information that will be collected, used and/or disclosed; the source of the information; and the purpose of the information for your project.')
	substantial_change = models.BooleanField(default=False, verbose_name='A substantial change to an existing policy, process or system that involves personal information', 
		help_text='Example: New legislation or policy that makes it compulsory to collect or disclose information')
	risk_register = models.BooleanField(default=False, verbose_name='Any practice or activity that is listed on a risk register kept by your organisation', 
		help_text='Example: Practices or activities listed on your office’s privacy risk register or health and safety register')
	collection = models.BooleanField(default=False, verbose_name='A new collection of personal information', 
		help_text='Example: Collecting information about individuals’ location')
	new_collect = models.BooleanField(default=False, verbose_name='A new way of collecting personal information', 
		help_text='Example: Collecting information online rather than on paper forms')
	new_store = models.BooleanField(default=False, verbose_name='A change in the way personal information is stored or secured', 
		help_text='Example: Storing information in the cloud')
	new_sensitive = models.BooleanField(default=False, verbose_name='A change to how sensitive information is managed', 
		help_text='Example: Moving health or financial records to a new database')
	offshore = models.BooleanField(default=False, verbose_name='Transferring personal information offshore or using a third-party contractor', 
		help_text='Example: Outsourcing the payroll function or storing information in the cloud')
	disclosure = models.BooleanField(default=False, verbose_name='A new use or disclosure of personal information that is already held', 
		help_text='Example: Sharing information with other parties in a new way')
	sharing = models.BooleanField(default=False, verbose_name='Sharing or matching personal information held by different organisations or currently held in different datasets', 
		help_text='Example: Combining information with other information held on public registers, or sharing information to enable organisations to provide services jointly')
	policy = models.BooleanField(default=False, verbose_name='A change in policy that results in people having less access to information that you hold about them', 
		help_text='Example: Archiving documents into a facility from which they can’t be easily retrieved')
	new_id = models.BooleanField(default=False, verbose_name='Establishing a new way of identifying individuals', 
		help_text='Example: A unique identifier, a biometric, or an online identity system')
	monitoring = models.BooleanField(default=False, verbose_name='Surveillance, tracking or monitoring of movements, behaviour or communications', 
		help_text='Example: Installing a new CCTV system')
	premises = models.BooleanField(default=False, verbose_name='Changes to your premises that will involve private spaces where clients or customers may disclose their personal information ', 
		help_text='Example: Changing the location of the reception desk, meeting rooms  where people may discuss personal details')
	regulatory = models.BooleanField(default=False, verbose_name='New regulatory requirements that could lead to compliance action against individuals on the basis of information about them ', 
		help_text='Example: Adding a new medical condition to the requirements of a pilot’s license')
	info_handling = models.CharField(max_length=1, choices=LEVELS, default='L', verbose_name='Level of information handling',
		help_text="Amount of personal information that will be handled.")
	sensitivity = models.CharField(max_length=1, choices=LEVELS, default='L', verbose_name='Sensitivity of the information', 
		help_text="Amount of sensitive information that will be handled.")
	significance = models.CharField(max_length=1, choices=LEVELS, default='L', verbose_name='Significance of the changes',
		help_text="Magnitude of change.")
	interaction = models.CharField(max_length=1, choices=LEVELS, default='L', verbose_name='Interaction with others',
		help_text="Number of other organisations involved.")
	public_impact = models.CharField(max_length=1, choices=LEVELS, default='L', verbose_name='Public impact',
		help_text="Impact on clients and the wider public. Concerns over aspects of project; or potential for negative media.")


	def _get_help_text(self, field_name):

		for field in self._meta.fields:
			if field.name == field_name:
				return field.help_text
	
	def _get_verbose_name(self, field_name):

		for field in self._meta.fields:
			if field.name == field_name:
				return field.verbose_name

	def __init__(self, *args, **kwargs):
		super(PrivacyAssessment, self).__init__(*args, **kwargs)

		for field in self._meta.fields:
			method_name = "get_{0}_help_text".format(field.name)
			curried_method = curry(self._get_help_text, field_name=field.name)
			setattr(self, method_name, curried_method)
			method_v_name = "get_{0}_verbose_name".format(field.name)
			curried_v_method = curry(self._get_verbose_name, field_name=field.name)
			setattr(self, method_v_name, curried_v_method)


class CATmeeting(models.Model):
	meeting_date = models.DateField(default=datetime.date.today())
	attendees = models.ManyToManyField(User, related_name='attendees')
	

class IPSGmeeting(models.Model):
	pass
