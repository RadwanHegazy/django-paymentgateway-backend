from django.db import models
from users.models import User
import uuid
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

class Payment (models.Model) :
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, related_name='user_payment', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    amount = models.FloatField()
    
    class PaymentState:
        done = 'done'
        fail = 'fail'
        pending = 'pending'

    payment_state = models.CharField(max_length=10, choices=(
        (PaymentState.done,PaymentState.done),
        (PaymentState.pending,PaymentState.pending),
        (PaymentState.fail,PaymentState.fail),
    ), default=PaymentState.pending)

    datetime = models.DateTimeField(auto_now_add=True)
    exp_at = models.DateTimeField(null=True, blank=True)

    card_number = models.BigIntegerField(null=True, blank=True)
    card_cvc = models.IntegerField(null=True, blank=True)
    card_exp = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self) -> str:
        return self.user.email

    is_done = models.BooleanField(default=False)    

@receiver(post_save, sender=Payment)
def update_exp_at(created, instance:Payment, **other):
    if not created:
        return

    instance.exp_at = instance.datetime + timedelta(hours=24)
    instance.save()