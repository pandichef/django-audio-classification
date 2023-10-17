from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .forms import AudioForm
from .models import Audio
from time import time


@csrf_exempt
def upload_audio(request):
    t0 = time()
    if request.method == "POST":
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            obj = Audio.objects.last()
            # obj.audio_file
            # filename = form.run_llm_model()
            # filename = obj.audio_file.name
            speaker = obj.identify_speaker()
            # process LLM model
            obj.delete()
            return JsonResponse(
                {"status": speaker + " (" + str(round(time() - t0, 1)) + " ms)"}
            )
        else:
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)


def record_audio_page(request):
    return render(request, "record_audio.html")
