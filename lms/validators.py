import re
from rest_framework import serializers

def youtube_validator(value):
    # Регулярное выражение для проверки ссылки на youtube.com
    youtube_regex = re.compile(
        r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$'
    )
    if not youtube_regex.match(value):
        raise serializers.ValidationError('Ссылка должна вести на youtube.com')