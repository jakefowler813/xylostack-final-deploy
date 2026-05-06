from django import forms
from django.forms import inlineformset_factory
from .models import InstrumentStack, XyloKey, Song

class StackForm(forms.ModelForm):
    class Meta:
        model = InstrumentStack
        fields = ['title']

# This creates the "FormSet" for the keys
KeyFormSet = inlineformset_factory(
    InstrumentStack, 
    XyloKey, 
    fields=['pitch', 'color_hex', 'order'],
    extra=0,
    widgets={
        'color_hex': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
        'pitch': forms.TextInput(attrs={'placeholder': 'e.g. C4', 'class': 'form-control'}),
        'order': forms.HiddenInput(), # Hide this from the user
    }
)

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'note_sequence', 'tempo_bpm']
        widgets = {
            'note_sequence': forms.Textarea(attrs={'placeholder': 'e.g. ["C4", "E4"]', 'rows': 3}),
        }