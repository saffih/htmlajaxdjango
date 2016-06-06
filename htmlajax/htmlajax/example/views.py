from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

###
from django.views.generic import TemplateView
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout,Fieldset


class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    isnested=forms.BooleanField(widget = forms.HiddenInput(), required = False, initial=False)
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
            Fieldset('Hello friend - you are a legend.',
                'name',
                'message',
                'isnested',
                'submit',
            ),
        )
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2 col-xs-3'
        self.helper.field_class = 'col-md-10 col-xs-9'

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass


class ResetForm(forms.Form):
    isnested=forms.BooleanField(widget = forms.HiddenInput(), required = False, initial=True)
    def __init__(self, *args, **kwargs):
        super(ResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('reset', 'Reset'))


class NestedForm(forms.Form):
    isnested=forms.BooleanField(widget = forms.HiddenInput(), required = False, initial=True)

    def __init__(self, *args, **kwargs):
        super(NestedForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('nested', 'Nested'))




from django.views.generic.edit import FormView

class ContactView(FormView):
    template_name = 'htmlajaxform.html'
    form_class = ContactForm
    reset_form_class = ResetForm
    nested_form_class = NestedForm
    # cause redirect on success
    # success_url = 'htmlajax'
    success_url = 'htmlajaxsuccess'
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']
    # example of specific data intialization for initial form (like slug) etc.
    # enable GET to recieve a parameter to the form
    def get_form_kwargs(self):
        kwargs = super(ContactView, self).get_form_kwargs()
        if self.request.method in ('GET'):
            # kwargsp['initial'].update(request.GET)
            kwargs['initial']['isnested']= 'isnested' in self.request.GET
            

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        if 'reset_form' not in context:
            context['reset_form'] = self.reset_form_class()
        if 'nested_form' not in context:
            context['nested_form'] = self.nested_form_class()
        return context

    # example for both redirect (for outer not nested & inner forms.
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        data=form.data
        if form.data.get('isnested')=='True':
             return HttpResponse(status=200, content_type=r'text/html', content="you did well")
        return super(ContactView, self).form_valid(form)
#    def post(self, request, *args, **kwargs):
#        raise



class HtmlAjaxView(TemplateView):
    template_name = "htmlajax.html"



class HtmlAjaxSuccessView(TemplateView):
    template_name = "htmlajaxsuccess.html"


def hello(request):
    return HttpResponse("Hi there")

