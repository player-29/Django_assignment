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
                translation = translator.translate(self.question, dest=lang).text
                # print(f"Translating question to {lang}: {translation}")  # Debugging line
                setattr(self, f"question_{lang}", translation)
                
            if not getattr(self, f"answer_{lang}"):
                translation = translator.translate(self.answer, dest=lang).text
                # print(f"Translating answer to {lang}: {translation}")  # Debugging line
                setattr(self, f"answer_{lang}", translation)
        self.save()

    def get_translation(self, lang="en"):
        """Get translated text based on language."""
        question = getattr(self, f"question_{lang}", None)
        answer = getattr(self, f"answer_{lang}", None)
        return {
            "question": question if question else self.question,
            "answer": answer if answer else self.answer
        }
    
    def __str__(self):
        return self.question
