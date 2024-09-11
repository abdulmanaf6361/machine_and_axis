from django.db import models
from django.core.exceptions import ValidationError
from machine.models import Machine

class Axis(models.Model):
    AXIS_CHOICES = [
        ('X', 'X Axis'),
        ('Y', 'Y Axis'),
        ('Z', 'Z Axis'),
        ('A', 'A Axis'),
        ('C', 'C Axis'),
    ]

    axis_name = models.CharField(max_length=1, choices=AXIS_CHOICES)  # constant, manual update
    max_acceleration = models.PositiveIntegerField()  # constant, manual update
    max_velocity = models.PositiveIntegerField()  # constant, manual update
    actual_position = models.FloatField()  # auto-generated, -190 to +190, updates every 0.1 sec
    target_position = models.FloatField()  # auto-generated, -190 to +191, updates every 0.1 sec
    distance_to_go = models.FloatField(editable=False)  # auto-calculated as target_position - actual_position, updates every 0.1 sec
    homed = models.BooleanField()  # 0/1, updates every 0.1 sec
    acceleration = models.PositiveIntegerField()  # auto-generated, 0 to 150, updates every 0.1 sec
    velocity = models.PositiveIntegerField()  # auto-generated, 0 to 80, updates every 0.1 sec
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)  # link to the Machine model

    def clean(self):
        # Validating actual_position
        if not (-190 <= self.actual_position <= 190):
            raise ValidationError({'actual_position': 'Actual position must be between -190 and 190.'})

        # Validating target_position
        if not (-190 <= self.target_position <= 191):
            raise ValidationError({'target_position': 'Target position must be between -190 and 191.'})

        # Ensuring distance_to_go is calculated correctly
        if self.distance_to_go != self.target_position - self.actual_position:
            raise ValidationError({'distance_to_go': 'Distance to go must be target_position - actual_position.'})

        # Validating acceleration
        if not (0 <= self.acceleration <= 150):
            raise ValidationError({'acceleration': 'Acceleration must be between 0 and 150.'})

        # Validating velocity
        if not (0 <= self.velocity <= 80):
            raise ValidationError({'velocity': 'Velocity must be between 0 and 80.'})

    def save(self, *args, **kwargs):
        # Calculate distance_to_go before saving
        self.distance_to_go = self.target_position - self.actual_position
        # Validate the fields
        self.clean()
        super(Axis, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.axis_name} Axis for {self.machine.machine_name}"
