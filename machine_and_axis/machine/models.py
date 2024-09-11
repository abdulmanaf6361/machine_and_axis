from django.db import models
from django.core.exceptions import ValidationError

class Machine(models.Model):
    machine_id = models.BigIntegerField(primary_key=True) 
    machine_name = models.CharField(max_length=100)   
    tool_capacity = models.PositiveIntegerField()  
    tool_offset = models.FloatField()  
    feedrate = models.PositiveIntegerField()  
    tool_in_use = models.PositiveIntegerField(blank=True,null=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Ensuring tool_offset is within range
        if not (5 <= self.tool_offset <= 40):
            raise ValidationError({'tool_offset': 'Tool offset must be between 5 and 40.'})

        # Ensuring feedrate is within range
        if not (0 <= self.feedrate <= 20000):
            raise ValidationError({'feedrate': 'Feedrate must be between 0 and 20,000.'})

        # Ensuring tool_in_use is between 1 and tool_capacity
        if not (1 <= self.tool_in_use <= self.tool_capacity):
            raise ValidationError({'tool_in_use': f'Tool in use must be between 1 and {self.tool_capacity}.'})

    def save(self, *args, **kwargs):
        # Before saving, validate constraints
        self.clean()
        super(Machine, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.machine_name} (ID: {self.machine_id})"
