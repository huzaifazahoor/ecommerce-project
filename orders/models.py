from django.db import models


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("shipped", "Shipped"),
        ("cancelled", "Cancelled"),
    )

    user_id = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by User {self.user_id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_id = models.IntegerField()
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Item {self.id} of Order {self.order.id}"
