import os
from django.db import models
from transformers import (
    pipeline,
    AutoModelForAudioClassification,
    AutoTokenizer,
    AutoFeatureExtractor,
)

tokenizer = AutoTokenizer.from_pretrained("facebook/wav2vec2-base")
feature_extractor = AutoFeatureExtractor.from_pretrained("facebook/wav2vec2-base")
model_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "facebook_wav2vec2-base_tuned",
)

model = AutoModelForAudioClassification.from_pretrained(model_path)
clf = pipeline(
    "audio-classification",
    model=model,
    tokenizer=tokenizer,
    feature_extractor=feature_extractor,
)


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
        result = clf(self.audio_file.path)
        # print(result[0]["label"].split('_')[1])
        speaker_id = result[0]["label"].split("_")[1]
        if speaker_id == "9":
            return "silence"
        else:
            return f"Actor #{speaker_id}"
