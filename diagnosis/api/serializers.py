from rest_framework import serializers

from diagnosis.models import Survey, Question, QuestionOption


class BaseSerializerSortedByPosition(serializers.SerializerMethodField):
    def __init__(self, attribute_string, serializer, method_name=None, **kwargs):
        self.attribute_string = attribute_string
        self.serializer = serializer
        super(BaseSerializerSortedByPosition, self).__init__(method_name=method_name, **kwargs)

    def to_representation(self, value):
        data = getattr(value, self.attribute_string).all().order_by('position')
        return self.serializer(data, many=True, ).data


class QuestionOptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    question = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = QuestionOption
        fields = (
            'id',
            'value',
            'text',
            'position',
            'question'
        )

    def create(self, validated_data):
        question = Question.objects.get(id=validated_data.pop('question'))
        question_option = QuestionOption.objects.create(question=question, **validated_data)
        validated_data['id'] = question_option.id
        return validated_data

    def validate_question(self, value):
        if self._context.get('questionoption_creation', False):
            if value == None:
                raise serializers.ValidationError("Question ID Field is required")
            if not Question.objects.filter(id=value):
                raise serializers.ValidationError(f"Question {value} doesn't exist")
        return value

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if self._context.get('questionoption_creation', False):
            response['question'] = int(self._context['request'].data.get('question', getattr(instance, 'question_id', '')))
        return response


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    survey = serializers.IntegerField(write_only=True, required=False, default=None)
    options = QuestionOptionSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = (
            'id',
            'type',
            'statement',
            'options',
            'position',
            'survey',
        )

    def create(self, validated_data):
        options_data = validated_data.pop('options', [])
        survey = Survey.objects.get(id=validated_data.pop('survey'))
        question = Question.objects.create(survey=survey, **validated_data)
        validated_data['options'] = options_data
        validated_data['id'] = question.id
        for option_data in options_data:
            question_option = QuestionOption.objects.create(question=question, **option_data)
            option_data['id'] = question_option.id
        return validated_data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["options"] = sorted(response.get("options", []), key=lambda x: x["position"])
        if self._context.get('question_creation', False):
            response['survey'] = int(self._context['request'].data.get('survey', getattr(instance, 'survey_id', '')))
        return response

    def update(self, instance, validated_data):
        validated_data['survey'] = Survey.objects.get(id=validated_data['survey'])
        options = validated_data.pop('options')
        options_instances = {o.id: o for o in instance.options.all()}
        for option in options:
            option_serializer = QuestionOptionSerializer(
                instance=options_instances.get(option.get('id')),
                data=option
            )
            if option_serializer.is_valid(raise_exception=True):
                option_serializer.save()
        return super().update(instance, validated_data)

    def validate_survey(self, value):
        if self._context.get('question_creation', False):
            if value == None:
                raise serializers.ValidationError("Survey ID Field is required")
            if not Survey.objects.filter(id=value):
                raise serializers.ValidationError(f"Survey {value} doesn't exist")
        return value


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Survey
        fields = (
            'id',
            'name',
            'questions'
        )
        read_only_fields = (
            'id',
        )

    def create(self, validated_data):
        survey = Survey(name=validated_data.get("name"))
        survey.save()
        validated_data['id'] = survey.id
        questions_data = validated_data.get('questions', [])
        for question_data in questions_data:
            options_data = question_data.pop('options', [])
            question_data.pop('survey', '')
            question = Question.objects.create(survey=survey, **question_data)
            question_data['options'] = options_data
            question_data['id'] = question.id
            for option_data in options_data:
                option_data.pop('question', '')
                question_option = QuestionOption.objects.create(question=question, **option_data)
                option_data['id'] = question_option.id
        return validated_data

    def update(self, instance, validated_data):
        questions = validated_data.pop('questions', [])
        instance = super(SurveySerializer, self).update(instance, validated_data)
        question_instances = {q.id: q for q in instance.questions.all()}
        for question in questions:
            question.update({'survey': instance.id})

            question_serializer = QuestionSerializer(
                instance=question_instances.get(question.get('id')), data=question
            )

            if question_serializer.is_valid(raise_exception=True):
                question_serializer.save()
        return instance

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["questions"] = sorted(response.get("questions", []), key=lambda x: x["position"])
        return response
