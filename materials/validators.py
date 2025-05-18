from rest_framework.exceptions import ValidationError


class LinkValidator:
    def __init__(self, field):
        self.filed = field

    def __call__(self, value):
        youtube_url = "https://www.youtube.com/"
        if value.get("link"):
            if youtube_url not in value.get("link"):
                raise ValidationError("Нужна ссылка только youtube.com")
        return None
