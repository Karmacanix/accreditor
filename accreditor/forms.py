from django import forms


class HelpForm(forms.Form):
	name = forms.CharField(label="Your name", widget=forms.TextInput(attrs={'class': 'w3-border w3-padding'}))
	email_from = forms.EmailField(label="Your email", widget=forms.EmailInput(attrs={'class': 'w3-border w3-padding'}))
	comments = forms.CharField(label="What can we help you with?", widget=forms.Textarea(attrs={'class': 'w3-border w3-padding'}))