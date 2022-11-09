from django.core.exceptions import ValidationError
import datetime

def future_date_only(date: datetime.date) -> None:
    """Validate if the provided datte is in the future"""
    now = datetime.date.today()
    if date < now:
        raise ValidationError('Dátum nemôže byť z minulosti.')
