from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import InstrumentStack, Song, XyloKey
from django.shortcuts import redirect, get_object_or_404
from .forms import StackForm, KeyFormSet, inlineformset_factory, SongForm
from django.http import JsonResponse 
from django.contrib import messages
from django import forms
from django.db.models import Q


def home(request):
    return render(request, 'core/index.html')

@login_required
def dashboard(request):
    # Fetch only the stacks owned by the logged-in user
    user_stacks = InstrumentStack.objects.filter(owner=request.user)
    return render(request, 'core/dashboard.html', {'stacks': user_stacks})

@login_required
def delete_stack(request, stack_id):
    stack = get_object_or_404(InstrumentStack, id=stack_id, owner=request.user)
    
    if request.method == "POST":
        stack.delete()
        messages.warning(request, f"Stack '{stack.title}' has been deleted.")
        return redirect('dashboard')
        
    return render(request, 'core/delete_confirm.html', {'stack': stack})

@login_required
def add_stack(request):
    AddKeyFormSet = inlineformset_factory(
        InstrumentStack, 
        XyloKey, 
        fields=['pitch', 'color_hex', 'order'],
        extra=8, 
        widgets={
            'color_hex': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
            'pitch': forms.TextInput(attrs={'placeholder': 'e.g. C4', 'class': 'form-control'}),
            'order': forms.HiddenInput(),
        }
    )

    if request.method == 'POST':
        form = StackForm(request.POST)
        formset = AddKeyFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            stack = form.save(commit=False)
            stack.owner = request.user
            stack.save()
            formset.instance = stack
            formset.save()
            return redirect('dashboard')
    else:
        form = StackForm()
        formset = AddKeyFormSet(queryset=XyloKey.objects.none())

    return render(request, 'core/add_stack.html', {
        'form': form,
        'formset': formset
    })

@login_required
def edit_stack(request, stack_id):
    stack = get_object_or_404(InstrumentStack, id=stack_id, owner=request.user)
    
    if request.method == "POST":
        form = StackForm(request.POST, instance=stack)
        formset = KeyFormSet(request.POST, instance=stack)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Stack updated successfully!")
            return redirect('dashboard')
    else:
        form = StackForm(instance=stack)
        formset = KeyFormSet(instance=stack)
        
    return render(request, 'core/edit_stack.html', {
        'form': form, 
        'formset': formset,
        'stack': stack
    })

def song_list(request):
    query = request.GET.get('q')
    
    # Filter: Show public songs OR songs user created themself
    if request.user.is_authenticated:
        base_songs = Song.objects.filter(Q(is_public=True) | Q(author=request.user))
    else:
        # If not logged in, only show public songs
        base_songs = Song.objects.filter(is_public=True)

    if query:
        songs = base_songs.filter(title__icontains=query)
    else:
        songs = base_songs
        
    return render(request, 'core/song_list.html', {'songs': songs})

def song_detail_api(request, song_id):
    # This fetches the song data as a dictionary
    song = get_object_or_404(Song, id=song_id)
    data = {
        "title": song.title,
        "notes": song.note_sequence,
        "bpm": song.tempo_bpm
    }
    # This turns the dictionary into a JSON response the browser can read
    return JsonResponse(data)

@login_required
def play_song(request, song_id, stack_id):
    song = get_object_or_404(Song, id=song_id)
    stack = get_object_or_404(InstrumentStack, id=stack_id, owner=request.user)
    
    # Create a dictionary of {pitch: color} for easy lookup
    color_map = {key.pitch: key.color_hex for key in stack.keys.all()}
    
    # Map the song's notes to the colors in this specific stack
    colored_notes = []
    for pitch in song.note_sequence:
        color = color_map.get(pitch, "#CCCCCC") # Default gray if note isn't in stack
        colored_notes.append({'pitch': pitch, 'color': color})
        
    return render(request, 'core/play.html', {
        'song': song,
        'stack': stack,
        'colored_notes': colored_notes
    })

def help_page(request):
    return render(request, 'core/help.html')

@login_required
def profile(request):
    return render(request, 'core/profile.html')

@login_required
def add_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            song = form.save(commit=False)
            song.author = request.user # Automatically assign the logged-in user
            song.save()
            messages.success(request, f"'{song.title}' saved to your library!")
            return redirect('song_list')
    else:
        form = SongForm()
    return render(request, 'core/add_song.html', {'form': form})

