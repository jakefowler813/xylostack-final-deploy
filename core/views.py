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
    selected_stack_id = request.GET.get('stack') # Look for ?stack=ID
    
    if request.user.is_authenticated:
        base_songs = Song.objects.filter(Q(is_public=True) | Q(author=request.user))
    else:
        base_songs = Song.objects.filter(is_public=True)

    if query:
        songs = base_songs.filter(title__icontains=query)
    else:
        songs = base_songs
        
    return render(request, 'core/song_list.html', {
        'songs': songs,
        'stack_id': selected_stack_id # Pass the stack ID to the template
    })

def song_list_api(request):
    # Fetch all songs that are marked as public
    songs = Song.objects.filter(is_public=True)
    
    # Create a list of dictionaries for the JSON response
    song_data = []
    for song in songs:
        song_data.append({
            "id": song.id,
            "title": song.title,
            "tempo": song.tempo_bpm,
            "notes": song.note_sequence,
            "author": str(song.author) if song.author else "Admin"
        })
    
    # safe=False is required when returning a list instead of a dictionary
    return JsonResponse(song_data, safe=False)

def song_detail_api(request, song_id):
    # Fetch a single song or 404 if it doesn't exist
    song = get_object_or_404(Song, id=song_id)
    
    # Return just the data for this one specific song
    data = {
        "id": song.id,
        "title": song.title,
        "notes": song.note_sequence,
        "bpm": song.tempo_bpm,
        "author": str(song.author) if song.author else "Admin"
    }
    return JsonResponse(data)

@login_required
def edit_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    
    # Permission Gate
    if song.author != request.user and not request.user.is_staff:
        messages.error(request, "Access denied: You can only edit your own compositions.")
        return redirect('song_list')

    if request.method == "POST":
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{song.title}' updated successfully.")
            return redirect('song_list')
    else:
        form = SongForm(instance=song)
        
    return render(request, 'core/edit_song.html', {'form': form, 'song': song})

@login_required
def delete_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    
    # Permission Gate
    if song.author != request.user and not request.user.is_staff:
        messages.error(request, "Access denied: You cannot delete this song.")
        return redirect('song_list')

    if request.method == "POST":
        song.delete()
        messages.warning(request, f"Song '{song.title}' has been permanently removed.")
        return redirect('song_list')
        
    return render(request, 'core/delete_song_confirm.html', {'song': song})

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

