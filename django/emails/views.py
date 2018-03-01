from django.core.mail import EmailMessage
from django.shortcuts import render, redirect

from emails.forms import EmailsForm


def send_email(request):

    result = 0
    if request.method == 'POST':

        # subject_text = request.POST.get['subject_text']
        # body_text = request.POST.get['body_text']
        # to_email = request.POST.get['to_email']

        form = EmailsForm(request.POST)
        if form.is_valid():
            email_to = form.cleaned_data['email_to']
            subject_text = form.cleaned_data['subject_text']
            body_text = form.cleaned_data['body_text']

            email = EmailMessage(subject_text, body_text, to=[email_to])
            result = email.send()
    # else:
    form = EmailsForm()
    context = {
        'emails_form': form,
        'result': result,
    }
    return render(request, 'emails/send.html', context)

