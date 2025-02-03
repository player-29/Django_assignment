from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from .models import FAQ
from .serializers import FAQSerializer
from rest_framework import viewsets
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Welcome to the FAQ API. Use /api/faqs/ to get FAQs."})

@api_view(['GET'])
def faq_list(request):
    lang = request.GET.get('lang', 'en')  # Default to English
    cached_faqs = cache.get(f"faqs_{lang}")

    if cached_faqs:
        return Response(cached_faqs)

    faqs = FAQ.objects.all()
    faq_data = []
    
    for faq in faqs:
        faq_data.append(faq.get_translation(lang))

    # Cache the FAQ data for 1 hour (3600 seconds)
    cache.set(f"faqs_{lang}", faq_data, timeout=3600)
    return Response(faq_data)


@api_view(['POST'])
def create_faq(request):
    serializer = FAQSerializer(data=request.data)
    if serializer.is_valid():
        faq = serializer.save()
        faq.translate()  # Translate the FAQ after saving it
        cache.delete_pattern("faqs_*")  # Invalidate cache for all languages
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    @action(detail=True, methods=['get'])
    def translate(self, request, pk=None):
        lang = request.GET.get('lang', 'en')  # Default to English
        faq = self.get_object()
        
        # Get both translated question and answer
        translated_faq = faq.get_translation(lang)
        return Response({
            "translated_question": translated_faq["question"],
            "translated_answer": translated_faq["answer"]
        })
