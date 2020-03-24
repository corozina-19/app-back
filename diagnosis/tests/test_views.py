from rest_framework.test import APITestCase
from django.urls import reverse
from diagnosis.models import Survey, Question, QuestionOption


class SurveyViewTests(APITestCase):

    def test_get_survey_structure(self):
        """
            Ensure we can get survey structure from endpoint, data structure must be organized by position field.
        """
        survey = Survey.objects.create(name="COVID-19 Diagnosis Survey")
        question_1 = Question.objects.create(survey=survey, statement="Did you go out today?", position=1)
        QuestionOption.objects.create(question=question_1, value=10, text='Yes', position=1)
        QuestionOption.objects.create(question=question_1, value=0, text='No', position=0)
        question_2 = Question.objects.create(survey=survey, statement="Did you wash your hands today?", position=0)
        QuestionOption.objects.create(question=question_2, value=0, text='Yes', position=0)
        QuestionOption.objects.create(question=question_2, value=10, text='No', position=1)
        url = reverse('survey-detail', args=(survey.id,))
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        response = response.json()
        self.assertEqual(response['questions'][0]['statement'], 'Did you wash your hands today?')
        self.assertEqual(response['questions'][1]['options'][0]['text'], 'No')
        survey_data = {
            'id': 1,
            'name': 'COVID-19 Diagnosis Survey',
            'questions': [
                {
                    'id': 2,
                    'type': 0,
                    'statement': 'Did you wash your hands today?',
                    'position': 0,
                    'options': [
                        {
                            'id': 3,
                            'value': 0,
                            'text': 'Yes',
                            'position': 0,
                        },
                        {
                            'id': 4,
                            'value': 10,
                            'text': 'No',
                            'position': 1,
                        }
                    ]
                },
                {
                    'id': 1,
                    'type': 0,
                    'statement': 'Did you go out today?',
                    'position': 1,
                    'options': [
                        {
                            'id': 2,
                            'value': 0,
                            'text': 'No',
                            'position': 0,
                        },
                        {
                            'id': 1,
                            'value': 10,
                            'text': 'Yes',
                            'position': 1,
                        },
                    ]
                },
            ]
        }
        self.assertDictEqual(survey_data, response)

    def test_create_survey(self):
        """
            Ensure we can create a survey with a name.
        """
        url = reverse('survey-list')
        required_data = {
            'id': 1,
            'name': 'COVID-19 Diagnosis Survey',
            'questions': []
        }
        insert_data = {
            'name': "COVID-19 Diagnosis Survey"
        }
        response = self.client.post(url, data=insert_data, format='json')
        self.assertEqual(201, response.status_code)
        self.assertDictEqual(required_data, response.json())

        insert_data = {
            'name': "ZIKA Diagnosis Survey",
            'questions': []
        }
        required_data = {
            'id': 2,
            'name': 'ZIKA Diagnosis Survey',
            'questions': []
        }
        response = self.client.post(url, data=insert_data, format='json')
        self.assertEqual(201, response.status_code)
        self.assertDictEqual(required_data, response.json())

    def test_create_survey_with_question(self):
        """
            Ensure we can create a survey with a question.
        """
        url = reverse('survey-list')
        survey_data = {
            'id': 1,
            'name': 'COVID-19 Diagnosis Survey',
            'questions': [
                {
                    'id': 1,
                    'type': 0,
                    'statement': 'Did you wash your hands today?',
                    'position': 0,
                    'options': [
                    ]
                },
            ]
        }
        data_to_insert = {
            "name": "COVID-19 Diagnosis Survey",
            "questions": [
                {
                    "type": 0,
                    "statement": "Did you wash your hands today?",
                    "position": 0,
                    "options": [
                    ]
                }
            ]
        }
        response = self.client.post(url, data=data_to_insert, format='json')
        self.assertDictEqual(survey_data, response.json())

    def test_create_survey_with_question_and_option(self):
        """
            Ensure we can create a survey with a question and it's option.
        """
        url = reverse('survey-list')
        survey_data = {
            'id': 1,
            'name': 'COVID-19 Diagnosis Survey',
            'questions': [
                {
                    'id': 1,
                    'type': 0,
                    'statement': 'Did you wash your hands today?',
                    'position': 0,
                    'options': [
                        {
                            'id': 2,
                            'value': 0,
                            'text': 'No',
                            'position': 0,
                        },
                        {
                            'id': 1,
                            'value': 10,
                            'text': 'Yes',
                            'position': 1,
                        },
                    ]
                },
            ]
        }
        data_to_insert = {
            "name": "COVID-19 Diagnosis Survey",
            "questions": [
                {
                    "type": 0,
                    "statement": "Did you wash your hands today?",
                    "position": 0,
                    "options": [
                        {
                            'value': 10,
                            'text': 'Yes',
                            'position': 1,
                        },
                        {
                            'value': 0,
                            'text': 'No',
                            'position': 0,
                        }
                    ]
                }
            ]
        }
        response = self.client.post(url, data=data_to_insert, format='json')
        self.assertDictEqual(survey_data, response.json())

    def test_update_survey_name(self):
        survey = Survey.objects.create(name="COVID-19 Diagnosis Survey")
        url = reverse('survey-detail', args=(survey.id,))
        data = {
            "id": 1,
            "name": "ZIKA Diagnosis Survey",
            "questions": []
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(data == response.json())
        response = self.client.put(url,data={'name': "ZIKA Diagnosis Survey"})
        self.assertDictEqual(data, response.json())


class QuestionViewTest(APITestCase):
    def test_create_question(self):
        """
            Ensure we can create a question.
        """
        url_survey = reverse('survey-list')
        url_question = reverse('question-list')
        insert_data = {
            'name': "COVID-19 Diagnosis Survey",
        }
        response = self.client.post(url_survey, data=insert_data, format='json')
        self.assertEqual(201, response.status_code)
        survey_data = response.json()
        insert_data = {
            'type': 0,
            'statement': 'Did you wash your hands today?',
            'position': 1,
            'survey': 8
        }
        response = self.client.post(url_question, data=insert_data, format='json')
        self.assertEqual(400, response.status_code)
        insert_data = {
            'type': 0,
            'statement': 'Did you wash your hands today?',
            'position': 1,
            'survey': survey_data['id'],
            'options': [
                {
                    'value': 5,
                    'text': 'prueba',
                    'position':1
                }
            ]
        }
        data = {
            'id': 1,
            'type': 0,
            'statement': 'Did you wash your hands today?',
            'position': 1,
            'survey': survey_data['id'],
            'options': [
                {
                    'id': 1,
                    'value': 5,
                    'text': 'prueba',
                    'position': 1
                }
            ]
        }
        response = self.client.post(url_question, data=insert_data, format='json')
        self.assertEqual(201, response.status_code)
        self.assertDictEqual(data, response.json())


