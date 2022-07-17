import uuid
from django.db import models

def job_id_path(instance, filename):
    isolate_name = filename.split('_')[0]
    return f"uploaded_files/{instance.job.id}/{isolate_name}/{filename}"

class Job(models.Model):
    RUNNING = 'running'
    FINISHED = 'finished'
    STATUS_CHOICES = [
        (RUNNING, 'Running'),
        (FINISHED, 'Finished'),
    ]
    status = models.CharField(
        max_length = 9,
        choices = STATUS_CHOICES,
        default = RUNNING,
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length = 254)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
class Document(models.Model):
    title = models.CharField(max_length = 200, blank=True)
    uploaded_file = models.FileField(upload_to = job_id_path)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
