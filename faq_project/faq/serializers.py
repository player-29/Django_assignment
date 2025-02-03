from rest_framework import serializers
from .models import FAQ

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        # fields = "__all__"
        fields = ['question', 'answer', 'language', 'question_hi', 'question_bn', 'answer_hi', 'answer_bn']
