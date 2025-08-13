from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from products.models import Product

# Elasticsearch index
product_index = Index('products')
product_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@registry.register_document
class ProductDocument(Document):
    category = fields.ObjectField(properties={
        'name': fields.TextField(),
        'slug': fields.TextField()
    })

    class Index:
        name = 'products'

    class Django:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'brand',
            'slug',
        ]
