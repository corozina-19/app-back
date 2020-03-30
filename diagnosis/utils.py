from diagnosis.models import Diagnosis
from diagnosis.api.serializers import DiagnosisScoredSerializer


def calculate_percentage(diagnosis: Diagnosis) -> DiagnosisScoredSerializer:
    total_score = diagnosis.survey.total_score
    score_accumulate = sum(diagnosis.answers.all().values_list('answer_value', flat=True))
    percentage = score_accumulate/total_score*100
    diagnosis.score = score_accumulate
    diagnosis.score_percentage = percentage
    diagnosis.save()
    return DiagnosisScoredSerializer(diagnosis)
