import datetime
# django
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives, send_mail
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

# this app
from .models import Application, InformationClassification, CloudQuestionnaire
from .models import ICTRiskAssessment, ICTVendorAssessment, PrivacyAssessment
from .models import CATmeeting, IPSGmeeting
from .forms import ApplicationForm, ApplicationSubmitForm, ApplicationSecurityDecisionForm
from .forms import ApplicationPrivacyDecisionForm, ApplicationClinicalDecisionForm, ApplicationOwnerApprovalForm
from .forms import InformationClassificationForm, CloudQuestionnaireForm, ICTRiskAssessmentForm 
from .forms import ICTVendorAssessmentForm, PrivacyAssessmentForm, CATmeetingForm, ApplicationDecisionForm

# Create your views here.
class ApplicationList(ListView):
    model = Application

    def get_context_data(self, **kwargs):
        context = super(ApplicationList, self).get_context_data(**kwargs)
        context['rejected_list'] = Application.objects.filter(assess_status='R')
        context['accepted_list'] = Application.objects.filter(assess_status='P')
        return context


class ApplicationAssessList(ListView):
    model = Application
    template_name = "assess/applicationassess_list.html"

    def get_context_data(self, **kwargs):
        context = super(ApplicationAssessList, self).get_context_data(**kwargs)
        a = Application.objects.filter(assess_status='A')
        context['security_list'] = a
        context['privacy_list'] = a
        context['clinical_list'] = a
        context['assessing_list'] = a
        return context


class ApplicationRequestList(ListView):
    model = Application
    template_name = "assess/applicationrequest_list.html"

    def get_context_data(self, **kwargs):
        context = super(ApplicationRequestList, self).get_context_data(**kwargs)
        ro = self.request.user
        context['reject_list'] = Application.objects.filter(assess_status='R', requestor=ro)
        context['approve_list'] = Application.objects.filter(assess_status='P', requestor=ro)
        context['assessing_list'] = Application.objects.filter(assess_status='A', requestor=ro)
        context['owner_list'] = Application.objects.filter(assess_status='S', requestor=ro)
        context['new_list'] = Application.objects.filter(assess_status='N', requestor=ro)
        return context


class ApplicationApproveList(ListView):
    model = Application
    template_name = "assess/applicationapprove_list.html"

    def get_context_data(self, **kwargs):
        context = super(ApplicationApproveList, self).get_context_data(**kwargs)
        bo = self.request.user
        context['to_approve_list'] = Application.objects.filter(assess_status='S', business_owner=bo)
        context['approved_list'] = Application.objects.filter(assess_status__in=['A','R','P',], business_owner=bo)
        return context


class ApplicationDetail(DetailView):
    model = Application

    def get_context_data(self, **kwargs):
        context = super(ApplicationDetail, self).get_context_data(**kwargs)
        a = Application.objects.get(pk=self.kwargs['pk'])
        context['security_form'] = ApplicationSecurityDecisionForm(instance=a)
        context['privacy_form'] = ApplicationPrivacyDecisionForm(instance=a)
        context['clinical_form'] = ApplicationClinicalDecisionForm(instance=a)
        if hasattr(a, 'informationclassification'):
            context['ic'] = True
        else:
            context['ic'] = False

        if hasattr(a, 'cloudquestionnaire'):
            context['cl'] = True
        else:
            context['cl'] = False
        
        if hasattr(a, 'ictriskassessment'):
            context['bc'] = True
        else:
            context['bc'] = False
        
        if hasattr(a, 'ictvendorassessment'):
            context['va'] = True
        else:
            context['va'] = False

        if hasattr(a, 'privacyassessment'):
            context['pa'] = True
        else:
            context['pa'] = False
        
        return context


class ApplicationSecurityAssess(SuccessMessageMixin, UpdateView):
    model = Application
    form_class = ApplicationSecurityDecisionForm
    template_name = "assess/application_assess.html"
    success_message = 'Application ICT security assessment decision successfully updated!'
    success_url = reverse_lazy('assess:application-assess-list')

    def get_context_data(self, **kwargs):
        context = super(ApplicationSecurityAssess, self).get_context_data(**kwargs)
        a = Application.objects.get(pk=self.kwargs['pk'])
        
        if hasattr(a, 'informationclassification'):
            context['ic'] = True
        else:
            context['ic'] = False

        if hasattr(a, 'cloudquestionnaire'):
            context['cl'] = True
        else:
            context['cl'] = False
        
        if hasattr(a, 'ictriskassessment'):
            context['bc'] = True
        else:
            context['bc'] = False
                
        if hasattr(a, 'ictvendorassessment'):
            context['va'] = True
        else:
            context['va'] = False

        if hasattr(a, 'privacyassessment'):
            context['pa'] = True
        else:
            context['pa'] = False

        return context


class ApplicationPrivacyAssess(SuccessMessageMixin, UpdateView):
    model = Application
    form_class = ApplicationPrivacyDecisionForm
    template_name = "assess/application_assess.html"
    success_message = 'Application privacy assess decision successfully updated!'
    success_url = reverse_lazy('assess:application-assess-list')

    def get_context_data(self, **kwargs):
        context = super(ApplicationPrivacyAssess, self).get_context_data(**kwargs)
        a = Application.objects.get(pk=self.kwargs['pk'])
        
        if hasattr(a, 'informationclassification'):
            context['ic'] = True
        else:
            context['ic'] = False

        if hasattr(a, 'cloudquestionnaire'):
            context['cl'] = True
        else:
            context['cl'] = False
        
        if hasattr(a, 'ictriskassessment'):
            context['bc'] = True
        else:
            context['bc'] = False
        
        if hasattr(a, 'ictvendorassessment'):
            context['va'] = True
        else:
            context['va'] = False

        if hasattr(a, 'privacyassessment'):
            context['pa'] = True
        else:
            context['pa'] = False

        return context


class ApplicationClinicalAssess(SuccessMessageMixin, UpdateView):
    model = Application
    form_class = ApplicationClinicalDecisionForm
    template_name = "assess/application_assess.html"
    success_message = 'Clinical Advisor decision successfully updated!'
    success_url = reverse_lazy('assess:application-assess-list')

    def get_context_data(self, **kwargs):
        context = super(ApplicationClinicalAssess, self).get_context_data(**kwargs)
        a = Application.objects.get(pk=self.kwargs['pk'])
        
        if hasattr(a, 'informationclassification'):
            context['ic'] = True
        else:
            context['ic'] = False

        if hasattr(a, 'cloudquestionnaire'):
            context['cl'] = True
        else:
            context['cl'] = False
        
        if hasattr(a, 'ictriskassessment'):
            context['bc'] = True
        else:
            context['bc'] = False
        
        if hasattr(a, 'ictvendorassessment'):
            context['va'] = True
        else:
            context['va'] = False
        
        if hasattr(a, 'privacyassessment'):
            context['pa'] = True
        else:
            context['pa'] = False

        return context


class ApplicationCreate(SuccessMessageMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    success_message = 'Application successfully registered!'
    success_url = reverse_lazy('assess:application-list')

    def form_valid(self, form):
        #add requestor to the requestors group
        ro = form.cleaned_data['requestor']
        if not ro.groups.filter(name='requestors').exists():
            rg = Group.objects.get(name='requestors')
            rg.user_set.add(ro)

        #add the business owner to the business owner group
        bo = form.cleaned_data['business_owner']
        if not bo.groups.filter(name='owners').exists():
            og = Group.objects.get(name='owners')
            og.user_set.add(bo)

        return super().form_valid(form)

    def get_initial(self):
        initial = super(ApplicationCreate, self).get_initial()
        initial['requestor'] = self.request.user
        return initial


class ApplicationUpdate(SuccessMessageMixin, UpdateView):
    model = Application
    form_class = ApplicationForm
    success_message = 'Application details successfully updated!'


class ApplicationSubmit(SuccessMessageMixin, UpdateView):
    model = Application
    form_class = ApplicationSubmitForm
    template_name="assess/application_confirm_submit.html"
    success_message = 'Application submitted successfully for assessment!'

    def form_valid(self, form):
        a = Application.objects.get(pk=self.kwargs['pk'])
        r = User.objects.get(username=a.requestor)
        b = User.objects.get(username=a.business_owner)
        subject_line = "Approval Required"
        message_body = "User: "+str(self.request.user)+" has initiated the app accredition process. You have been nominated by the requestor as the future Business Owner for "+str(a.name)+". Due to the time and resources required by this process, you will need to provide an approval to continue. Please log into the App Accreditor and decide whether to accept or decline this assessment request."
        send_mail(subject_line, message_body, r.email, [b.email])
        return super().form_valid(form)

    def get_initial(self):
        initial = super(ApplicationSubmit, self).get_initial()
        initial['assess_status'] = 'S'
        return initial


class ApplicationOwnerApproval(SuccessMessageMixin, UpdateView):
    model = Application
    form_class = ApplicationOwnerApprovalForm
    template_name="assess/application_owner_approval.html"
    success_message = 'Business owner approved request for assessment!'

    def form_valid(self, form):
        a = Application.objects.get(pk=self.kwargs['pk'])
        b = User.objects.get(username=a.business_owner)
        cat = list(User.objects.filter(groups__name='cloud_assessment_team').values_list('email', flat=True))
        print(cat)
        subject_line = "New App to Assess"
        message_body = "Business owner: "+str(self.request.user)+" has approved an app ("+str(a.name)+") to be accredited. Please log into the App Accreditor and assess this application."
        send_mail(subject_line, message_body, b.email, cat)
        return super().form_valid(form)

    def get_initial(self):
        initial = super(ApplicationOwnerApproval, self).get_initial()
        initial['assess_status'] = 'S'
        initial['business_owner_date'] = datetime.date.today()
        initial['business_owner_approval'] = True
        return initial


class ApplicationDelete(SuccessMessageMixin, DeleteView):
    model = Application
    success_url = reverse_lazy('assess:application-list')
    success_message = "Application deleted!"


class InformationClassificationDetail(DetailView):
    model = InformationClassification


class InformationClassificationCreate(SuccessMessageMixin, CreateView):
    model = InformationClassification
    form_class = InformationClassificationForm
    success_message = 'Information Classification successfully saved!'

    def get_initial(self):
        initial = super(InformationClassificationCreate, self).get_initial()
        initial['app'] = self.kwargs['pk']
        return initial

    def get_success_url(self):
        return reverse('assess:application-detail', kwargs={'pk': self.kwargs['pk']})


class InformationClassificationUpdate(SuccessMessageMixin, UpdateView):
    model = InformationClassification
    form_class = InformationClassificationForm
    success_message = 'Information Classification successfully updated!'

    def get_success_url(self):
        return reverse('assess:application-detail', kwargs={'pk': self.kwargs['pk']})


class InformationClassificationDelete(SuccessMessageMixin, DeleteView):
    model = InformationClassification
    #success_url = reverse_lazy('assess:application-list')
    success_message = "Information Classification deleted!"
    
    def get_success_url(self):
        return reverse('assess:application-detail', kwargs={'pk': self.kwargs['pk']})


class CloudQuestionnaireDetail(DetailView):
    model = CloudQuestionnaire


class CloudQuestionnaireCreate(SuccessMessageMixin, CreateView):
    model = CloudQuestionnaire
    form_class = CloudQuestionnaireForm
    success_message = 'Cloud Questionnaire successfully saved!'
    #success_url = reverse_lazy('assess:application-list')

    def get_initial(self):
        initial = super(CloudQuestionnaireCreate, self).get_initial()
        initial['app'] = self.kwargs['pk']
        return initial

    def get_success_url(self):
        return reverse('assess:application-detail', kwargs={'pk': self.kwargs['pk']})


class CloudQuestionnaireUpdate(SuccessMessageMixin, UpdateView):
    model = CloudQuestionnaire
    form_class = CloudQuestionnaireForm
    success_message = 'Cloud Questionnaire successfully updated!'

    def get_success_url(self):
        return reverse('assess:application-detail', kwargs={'pk': self.kwargs['pk']})


class CloudQuestionnaireDelete(SuccessMessageMixin, DeleteView):
    model = CloudQuestionnaire
    #success_url = reverse_lazy('assess:application-list')
    success_message = "Cloud Questionnaire deleted!"

    def get_success_url(self):
        return reverse('assess:application-detail', kwargs={'pk': self.kwargs['pk']})

#ICTRiskAssessment
class ICTRiskAssessmentDetail(DetailView):
    model = ICTRiskAssessment


class ICTRiskAssessmentCreate(SuccessMessageMixin, CreateView):
    model = ICTRiskAssessment
    form_class = ICTRiskAssessmentForm
    success_message = 'ICT Risk Assessment successfully saved!'
    #success_url = reverse_lazy('assessment:application-list')

    def get_initial(self):
        initial = super(ICTRiskAssessmentCreate, self).get_initial()
        initial['app'] = self.kwargs['pk']
        return initial

    def get_success_url(self):
        return reverse('assess:application-detail', kwargs={'pk': self.kwargs['pk']})


class ICTRiskAssessmentUpdate(SuccessMessageMixin, UpdateView):
    model = ICTRiskAssessment
    form_class = ICTRiskAssessmentForm
    success_message = 'ICT Risk Assessment successfully updated!'

    def get_success_url(self):
        return reverse('assess:application-detail', kwargs={'pk': self.kwargs['pk']})


class ICTRiskAssessmentDelete(SuccessMessageMixin, DeleteView):
    model = ICTRiskAssessment
    # success_url = reverse_lazy('assess:application-list')
    success_message = "ICT Risk Assessment deleted!"

    def get_success_url(self):
        return reverse('assess:application-detail', kwargs={'pk': self.kwargs['pk']})

#ICTVendorAssessment
class ICTVendorAssessmentDetail(DetailView):
    model = ICTVendorAssessment


class ICTVendorAssessmentCreate(SuccessMessageMixin, CreateView):
    model = ICTVendorAssessment
    form_class = ICTVendorAssessmentForm
    success_message = 'ICT Vendor Assessment successfully saved!'
    #success_url = reverse_lazy('assess:application-list')

    def get_initial(self):
        initial = super(ICTVendorAssessmentCreate, self).get_initial()
        initial['app'] = self.kwargs['pk']
        return initial

    def get_success_url(self):
        return reverse('assess:application-detail', kwargs={'pk': self.kwargs['pk']})


class ICTVendorAssessmentUpdate(SuccessMessageMixin, UpdateView):
    model = ICTVendorAssessment
    form_class = ICTVendorAssessmentForm
    success_message = 'ICT Vendor Assessment successfully updated!'

    def get_success_url(self):
        return reverse('assess:application-detail', kwargs={'pk': self.kwargs['pk']})


class ICTVendorAssessmentDelete(SuccessMessageMixin, DeleteView):
    model = ICTVendorAssessment
    #success_url = reverse_lazy('assess:application-list')
    success_message = "ICT Vendor Assessment deleted!"

    def get_success_url(self):
        return reverse('assess:application-detail', kwargs={'pk': self.kwargs['pk']})


# PRIVACY ASSESSMENT
class PrivacyAssessmentDetail(DetailView):
    model = PrivacyAssessment


class PrivacyAssessmentCreate(SuccessMessageMixin, CreateView):
    model = PrivacyAssessment
    form_class = PrivacyAssessmentForm
    success_message = 'Privacy Assessment successfully saved!'
    #success_url = reverse_lazy('assess:application-list')

    def get_initial(self):
        initial = super(PrivacyAssessmentCreate, self).get_initial()
        initial['app'] = self.kwargs['pk']
        return initial

    def get_success_url(self):
        return reverse('assess:application-detail', kwargs={'pk': self.kwargs['pk']})


class PrivacyAssessmentUpdate(SuccessMessageMixin, UpdateView):
    model = PrivacyAssessment
    form_class = PrivacyAssessmentForm
    success_message = 'Privacy Assessment successfully updated!'

    def get_success_url(self):
        return reverse('assess:application-detail', kwargs={'pk': self.kwargs['pk']})


class PrivacyAssessmentDelete(SuccessMessageMixin, DeleteView):
    model = PrivacyAssessment
    #success_url = reverse_lazy('assess:application-list')
    success_message = "Privacy Assessment deleted!"

    def get_success_url(self):
        return reverse('assess:application-detail', kwargs={'pk': self.kwargs['pk']})


# CAT MEETINGS
class CatMeetingList(ListView):
    model = CATmeeting
    template_name="assess/catmeeting_list.html"


class CatMeetingDetail(DetailView):
    model = CATmeeting

    def get_context_data(self, **kwargs):
        context = super(CatMeetingDetail, self).get_context_data(**kwargs)
        context['decision_list'] = Application.objects.filter(CATmeeting=self.kwargs['pk'])
        context['app_list'] = Application.objects.filter(
            assess_status='A', 
            security_decision__isnull=False, 
            privacy_decision__isnull=False, 
            clinical_decision__isnull=False,
            CATmeeting__isnull=True,
            )
        return context 


class CatMeetingCreate(SuccessMessageMixin, CreateView):
    model = CATmeeting
    form_class   = CATmeetingForm
    success_message = 'CAT Meeting successfully saved!'
    success_url = reverse_lazy('assess:catmeeting-list')


class CatMeetingUpdate(SuccessMessageMixin, UpdateView):
    model = CATmeeting
    form_class = CATmeetingForm
    success_message = 'CAT Meeting successfully updated!'
    success_url = reverse_lazy('assess:catmeeting-list')


class CatMeetingDelete(SuccessMessageMixin, DeleteView):
    model = CATmeeting
    success_message = "CAT Meeting deleted!"
    template_name="assess/catmeeting_confirm_delete.html"

    def get_success_url(self):
        return reverse('assess:catmeeting-detail', kwargs={'pk': self.kwargs['pk']})
    

class CatMeetingDecisionUpdate(SuccessMessageMixin, UpdateView):
    model = Application
    form_class = ApplicationDecisionForm
    template_name="assess/catmeeting_decision_form.html"
    success_message = 'Application decision updated successfully!'
    success_url = reverse_lazy('assess:catmeeting-list')

    def post(self, request, *args, **kwargs):
        cat = self.kwargs['catmeeting_id']
        app = self.kwargs['pk']
        req = Application.objects.filter(name=app)
        print("Cat:",cat, "App:", app, "Req:", req)
        # get variables - app, cat meeting number and the decision
        # save the application model with the new status and the CAT meeting
        # email the requestor and business owner.
        if request.method == 'POST':
            f = ApplicationDecisionForm(request.POST)
            d = f['cat_decision'].value()
            if d == "E":
                req.update(escalate_IPSG = True)

            if d == "R":
                req.update(assess_status = "R")

            if d == "P":
                req.update(assess_status = "P")

            if not f['CATmeeting'].value():
                req.update(CATmeeting = cat) 

        return HttpResponseRedirect(reverse('assess:catmeeting-list'))

    def form_valid(self, form):
        a = Application.objects.get(pk=self.kwargs['pk'])
        b = User.objects.get(username=a.business_owner)
        r = User.objects.get(username=a.requestor)
        c = CATmeeting.objects.get(pk=a.catmeeting)
        d = c.meeting_date
        if a.assess_status == 'R':
            s = "is not secure or private enough and has been Blacklisted from use at the DHB."

        if a.assess_status == 'A':
            s = "met 3DHB's security and privacy policy threshold for compliance. It has been Whitelisted for use at the DHB."

        if a.assess_status == 'E':
            s = "exceeded our comfort threshold for reasonable privacy and security risks.  This request has been escalated to the IPSG."

        subject_line = "App Accreditor CAT Decision"
        message_body = "To "+str(b)+", "+str(r)+".  "+"The cloud assessment team met "+str(d)+". They have decided that "+str(a.name)+" "+str(s)
        send_mail(subject_line, message_body, "app_accreditor@3dhb.org.nz", [b, r])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CatMeetingDecisionUpdate, self).get_context_data(**kwargs)
        context['catmeeting'] = self.kwargs['catmeeting_id']
        context['app'] = self.kwargs['pk']
        return context 

    def get_queryset(self):
        queryset = super(CatMeetingDecisionUpdate, self).get_queryset()
        queryset = queryset.filter(name=self.kwargs['pk'])
        return queryset


class IPSGMeetingDetailView(DetailView):
    pass