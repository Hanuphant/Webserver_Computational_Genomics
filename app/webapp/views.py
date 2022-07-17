from . import models
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django import db
import os
import subprocess
import shlex
import shutil
from multiprocessing import Process
import mimetypes
from django.http import HttpResponse
import datetime

def run_background_task(job, email):
    subprocess.call(shlex.split(f"bash /projects/groupa/Team1-WebServer/backend/master_pipeline.sh -j {job.id} -z"))

    send_mail(
        'SALADS Webserver - Job Results Ready',
        f"Thank you for using the SALADS Webserver. Your results for your job (id: {job.id}) are now ready to view at the following address:\n{settings.TEAM1_SITE_URL}/jobs/{job.id}",
        None,
        [email],
        fail_silently=True
    )

    job.status = 'finished'
    job.save()

def upload_files(request):
    if request.method == "POST":
        # Fetching the form data
        email = request.POST["email"]
        paired_ends_1 = request.FILES["paired_ends_1"]
        paired_ends_2 = request.FILES["paired_ends_2"]

        # Saving the information in the database
        job = models.Job(
            email = email,
        )
        job.save()
        
        document1 = models.Document(
            title = '',
            uploaded_file = paired_ends_1,
            job = job,
        )
        document1.save()

        document2 = models.Document(
            title = '',
            uploaded_file = paired_ends_2,
            job = job,
        )
        document2.save()

        send_mail(
            'SALADS Webserver - Job Submitted',
            f"Thank you for using the SALADS Webserver. You have successfully submitted a job (id: {job.id}).\nYou will receive a second email once your results are ready.",
            None,
            [email],
            fail_silently=True
        )

        print(job.id)

        db.connections.close_all()
        p = Process(target=run_background_task, args=[job, email])
        p.start()

        # Clean old data
        jobs = models.Job.objects.filter(created_at__lte=datetime.datetime.today()-datetime.timedelta(days=15))
        for j in jobs:
            uf_dir = f"{settings.MEDIA_ROOT}/uploaded_files/{j.id}"
            if os.path.exists(uf_dir):
                shutil.rmtree(uf_dir)
            r_dir = f"{settings.MEDIA_ROOT}/results/{j.id}"
            if os.path.exists(r_dir):
                shutil.rmtree(r_dir)
        jobs.delete()
 
        return redirect(f"/jobs/{job.id}")
    else:
        return render(request, "upload.html", context = {})


def job_results(request, pk):
    job_status = models.Job.objects.get(id=pk).status
    return render(request, "job_results.html", {'pk' : pk, 'job_status' : job_status })

def download(request, pk, filename):
    filepath = f"{settings.MEDIA_ROOT}/results/{pk}/{filename}"
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
