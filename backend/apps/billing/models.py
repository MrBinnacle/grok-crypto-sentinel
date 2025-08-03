"""Billing models for TFDT subscription system"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class SubscriptionTier(models.Model):
    """Subscription tier definitions"""

    TIER_CHOICES = [
        ("free", "Free"),
        ("pro", "Pro"),
        ("enterprise", "Enterprise"),
    ]

    name = models.CharField(max_length=20, choices=TIER_CHOICES, unique=True)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)
    analyses_per_month = models.IntegerField()
    outcome_tracking = models.BooleanField(default=False)
    priority_support = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ${self.monthly_price}/month"


class UserSubscription(models.Model):
    """User subscription tracking"""

    STATUS_CHOICES = [
        ("active", "Active"),
        ("cancelled", "Cancelled"),
        ("past_due", "Past Due"),
        ("trialing", "Trialing"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.ForeignKey(SubscriptionTier, on_delete=models.PROTECT)
    stripe_subscription_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="trialing")
    current_period_start = models.DateTimeField(default=timezone.now)
    current_period_end = models.DateTimeField()
    analyses_used_this_month = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def can_analyze(self):
        """Check if user can perform analysis"""
        if self.status != "active":
            return False
        return self.analyses_used_this_month < self.tier.analyses_per_month

    def increment_usage(self):
        """Increment analysis usage counter"""
        self.analyses_used_this_month += 1
        self.save()


class Payment(models.Model):
    """Payment transaction tracking"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE)
    stripe_payment_intent_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
