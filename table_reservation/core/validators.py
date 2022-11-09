from django.core.exceptions import ValidationError
import datetime

def future_datetime_only(date_with_time: datetime.datetime) -> None:
    """Validate if the provided datetime is in the future"""
    now = datetime.datetime.now()
    if date_with_time < now:
        raise ValidationError('Dátum a čas nemôže byť z minulosti.')

