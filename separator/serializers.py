from rest_framework import serializers
from spleeter.separator import Separator
import os
from django.conf import settings

class UploadFileSerializer(serializers.Serializer):
    file = serializers.FileField()

    def save(self):
        file = self.validated_data['file']
        files = self.handle_uploaded_file(file)
        return self.separate_audio(files)

    def handle_uploaded_file(self, f):
        file_name = f.name.replace(' ', '').replace('.mp3', '')
        file_path = os.path.join(settings.MEDIA_ROOT, file_name + '.mp3')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return file_name

    def separate_audio(self, file_name):
        separator = Separator('spleeter:2stems')
        file_path = os.path.join(settings.MEDIA_ROOT, file_name + '.mp3')
        output_path = os.path.join(settings.MEDIA_ROOT, 'output')
        separator.separate_to_file(file_path, output_path)
        
        vocals_path = os.path.join(output_path, f'{file_name}/vocals.wav')
        accompaniment_path = os.path.join(output_path, f'{file_name}/accompaniment.wav')
        
        # 개발 서버 주소에 맞게 경로 수정
        vocals_path = vocals_path.replace(settings.MEDIA_ROOT, 'http://127.0.0.1:8000/media').replace("\\", "/")
        accompaniment_path = accompaniment_path.replace(settings.MEDIA_ROOT, 'http://127.0.0.1:8000/media').replace("\\", "/")
        
        return {
            'vocals': vocals_path,
            'accompaniment': accompaniment_path
        }