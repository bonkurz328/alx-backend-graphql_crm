import graphene
from graphene_django import DjangoObjectType
from django.db.models import F
from customers.models import Product

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass

    products = graphene.List(ProductType)
    message = graphene.String()
    updated_count = graphene.Int()

    def mutate(self, info):
        # Query products with stock < 10
        low_stock_products = Product.objects.filter(stock__lt=10)
    
        # Get the product IDs before update
        product_ids = list(low_stock_products.values_list('id', flat=True))
    
        # Update stock by incrementing by 10
        updated_count = low_stock_products.update(stock=F('stock') + 10)
    
        # Get the updated products
        updated_products = Product.objects.filter(id__in=product_ids)
    
        return UpdateLowStockProducts(
            products=updated_products,
            message=f"Successfully updated {updated_count} low-stock products",
            updated_count=updated_count
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()
