from rest_framework import serializers
from .models import FAQ

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        # fields = "__all__"
        fields = ['question', 'answer', 'language', 'question_hi', 'question_bn', 'answer_hi', 'answer_bn']

        def get_question(self, obj):
            request = self.context.get('request')
            lang = request.GET.get('lang', 'en')
            return obj.get_translation(lang)
