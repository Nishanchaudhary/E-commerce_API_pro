from rest_framework.views import APIView
from rest_framework.response import Response
from elasticsearch_dsl import Q
from .documents import ProductDocument

class ProductSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')

        if not query:
            return Response({"error": "No search query provided"}, status=400)

        search_query = Q("multi_match", query=query, fields=['title', 'description', 'brand'])
        results = ProductDocument.search().query(search_query).to_queryset()

        data = [
            {
                "id": p.id,
                "title": p.title,
                "description": p.description,
                "brand": p.brand,
                "category": p.category.name if p.category else None
            }
            for p in results
        ]

        return Response(data)
