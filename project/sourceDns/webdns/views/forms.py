#-*- coding:utf-8 -*-
from django import forms

class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=100)
    file = forms.FileField()

class DomainForm(forms.Form):
    domain = forms.CharField(label=u'二级域名：', error_messages={'required':u'二级域名不能为空'})
    content = forms.CharField(label=u'作用：', error_messages={'required':u'不能为空'}, widget=forms.Textarea(attrs={'cols':80, 'rows':10}))

    def clean_domain(self):
        domain = self.cleaned_data['domain']

        if not domain:
            return ValidationError(u'二级域名不能为空')
        else:
            return domain

