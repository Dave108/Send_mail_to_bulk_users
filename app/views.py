from django.shortcuts import render, HttpResponseRedirect, reverse
import pandas as pd
from django.contrib import messages
from django.contrib.auth.models import User
# celery
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.utils.crypto import get_random_string
import json
from . import tasks
import datetime
from django.utils import timezone
from datetime import timedelta


# Create your views here.
tm = timezone.localtime() + timedelta(minutes=6)
print(tm, '---')


def csv_read_view(request):
    if request.method == "POST":
        file = request.FILES.get('file')
        if not file.name.endswith('.csv'):
            messages.error(request, "THIS is not a CSV file!")
            return HttpResponseRedirect(reverse('homepage'))
        df = pd.read_csv(file)
        # print(df['username'].str.replace('\t', ' '))
        print(df)
        password_column = []
        for index, row in df.iterrows():
            ltm = datetime.datetime.now() + timedelta(minutes=1)
            print(ltm)
            password = User.objects.make_random_password(12)
            user = User.objects.create_user(row['username'], row['emailid'], password)
            user.save()

            # using only celery with delay function to call

            # tasks.mailing_func_user.delay(row['username'], password)

            # -----------------------------------
            # celery code to call task and create cron tab time table

            unique_id = get_random_string(length=4)
            schedule, created = CrontabSchedule.objects.get_or_create(hour=ltm.hour, minute=ltm.minute)
            task = PeriodicTask.objects.create(crontab=schedule, name="task_scheduled_" + unique_id,
                                               task='app.tasks.mailing_func_user',
                                               args=json.dumps((row['username'], password)))

            # -----------------------------------
            password_column.append(password)
        df['password'] = password_column
        df.to_csv('updated.csv')

        messages.error(request, "Users added Successfully!")
        return HttpResponseRedirect(reverse('homepage'))
    else:
        return render(request, 'homepage.html')
