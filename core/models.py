from django.db import models
from django.contrib.auth.models import User

# Model 1: The Instrument Configuration (The "Stack")
class InstrumentStack(models.Model):
    title = models.CharField(max_length=100, help_text="e.g., Baby Shark Xylo")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.owner.username})"

# Model 2: The Individual Keys within a Stack
class XyloKey(models.Model):
    stack = models.ForeignKey(InstrumentStack, related_name='keys', on_delete=models.CASCADE)
    pitch = models.CharField(max_length=10, help_text="e.g., C4, D4, G#5")
    color_hex = models.CharField(max_length=7, default="#FFFFFF", help_text="Hex code: #RRGGBB")
    order = models.PositiveIntegerField(help_text="Position from left to right")

    class Meta:
        ordering = ['order']

# Model 3: The Songs in the library
class Song(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    tempo_bpm = models.PositiveIntegerField(default=120)
    is_public = models.BooleanField(default=False, help_text="Check this to make the song visible to everyone.")
    # This stores the sequence of notes as a simple list/JSON
    # e.g., ["C4", "C4", "G4", "G4"]
    note_sequence = models.JSONField(help_text="A list of pitches in order")

    def __str__(self):
        return self.title
