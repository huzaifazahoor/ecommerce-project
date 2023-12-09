import graphene
from graphene_django import DjangoObjectType
from .models import Order, OrderItem


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields = "__all__"


class Query(graphene.ObjectType):
    all_orders = graphene.List(OrderType)
    order = graphene.Field(OrderType, order_id=graphene.Int())
    order_items = graphene.List(OrderItemType, order_id=graphene.Int())

    def resolve_all_orders(root, info):
        # Querying all orders
        return Order.objects.all()

    def resolve_order(root, info, order_id):
        # Querying a single order
        return Order.objects.get(pk=order_id)

    def resolve_order_items(root, info, order_id):
        # Querying items for a specific order
        return OrderItem.objects.filter(order_id=order_id)


class CreateOrder(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        total_amount = graphene.Decimal(required=True)
        status = graphene.String()

    order = graphene.Field(OrderType)

    def mutate(root, info, user_id, total_amount, status="pending"):
        order = Order(user_id=user_id, total_amount=total_amount, status=status)
        order.save()
        return CreateOrder(order=order)


class CreateOrderItem(graphene.Mutation):
    class Arguments:
        order_id = graphene.Int(required=True)
        product_id = graphene.Int(required=True)
        quantity = graphene.Int(required=True)
        price_per_unit = graphene.Decimal(required=True)

    order_item = graphene.Field(OrderItemType)

    def mutate(root, info, order_id, product_id, quantity, price_per_unit):
        order_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price_per_unit=price_per_unit,
        )
        order_item.save()
        return CreateOrderItem(order_item=order_item)


class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
    create_order_item = CreateOrderItem.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
