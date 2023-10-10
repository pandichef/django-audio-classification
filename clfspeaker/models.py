import os
from django.db import models


def get_upload_to(instance, filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    return f"audio/{name}.wav"


class Audio(models.Model):
    audio_file = models.FileField(upload_to=get_upload_to)

    def delete(self, *args, **kwargs):
        # Delete the file from the filesystem
        if os.path.isfile(self.audio_file.path):
            os.remove(self.audio_file.path)

        # Call the parent class's delete method to remove the database record
        super(Audio, self).delete(*args, **kwargs)

    def identify_speaker(self):
        return "Speaker 1"
