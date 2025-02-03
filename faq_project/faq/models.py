from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()
    language = models.CharField(max_length=10, default="en")

    # Translations
    question_hi = models.TextField(null=True, blank=True)
    question_bn = models.TextField(null=True, blank=True)
    answer_hi = RichTextField(null=True, blank=True)
    answer_bn = RichTextField(null=True, blank=True)

    def translate(self):
        """Translate the question and answer fields to Hindi and Bengali."""
        translator = Translator()
        languages = ["hi", "bn"]  # Hindi, Bengali
        for lang in languages:
            if not getattr(self, f"question_{lang}"):  # Only translate if missing
                setattr(self, f"question_{lang}", translator.translate(self.question, dest=lang).text)
            if not getattr(self, f"answer_{lang}"):  
                setattr(self, f"answer_{lang}", translator.translate(self.answer, dest=lang).text)
        self.save()

    def get_translation(self, lang="en"):
        """Get translated text based on language."""
        return {
            "question": getattr(self, f"question_{lang}", self.question) or self.question,
            "answer": getattr(self, f"answer_{lang}", self.answer) or self.answer
        }

    def __str__(self):
        return self.question
