from django import forms
from .models import Audio


class AudioForm(forms.ModelForm):
    class Meta:
        model = Audio
        fields = ("audio_file",)

    def run_llm_model(self):
        audio_file = self.cleaned_data.get("audio_file")

        if audio_file:
            filename = audio_file.name  # Get the filename here
            # print(filename)
            # Perform any additional validation on filename if needed

        return filename
