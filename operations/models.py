from django.db import models
from django.conf import settings


class Field(models.Model):
    class Stage(models.TextChoices):
        PLANTED = 'PLANTED', 'Planted'
        GROWING = 'GROWING', 'Growing'
        READY = 'READY', 'Ready'
        HARVESTED = 'HARVESTED', 'Harvested'

    name = models.CharField(max_length=255)
    crop_type = models.CharField(max_length=100)

    # Nullable so Admins can create fields in the READY state before planting
    planting_date = models.DateField(null=True, blank=True)

    # Default set to READY
    stage = models.CharField(
        max_length=20,
        choices=Stage.choices,
        default=Stage.READY
    )

    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_fields'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def status(self):
        """Computes the status dynamically based on stage and recent issues."""
        if self.stage == self.Stage.HARVESTED:
            return 'Completed'

        latest_update = self.updates.order_by('-created_at').first()
        if latest_update and latest_update.is_issue:
            return 'At Risk'

        return 'Active'

    def __str__(self):
        return f"{self.name} - {self.crop_type}"


class FieldUpdate(models.Model):
    field = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        related_name='updates'
    )
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    note = models.TextField()
    is_issue = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Update on {self.field.name} by {self.agent.username}"