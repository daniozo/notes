from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Note
from .forms import NoteForm, SignUpForm

def home(request):
    """Landing page view"""
    if request.user.is_authenticated:
        return redirect('notes_list')
    return render(request, 'app/home.html')

def signup(request):
    """Register new users"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('notes_list')
    else:
        form = SignUpForm()
    return render(request, 'app/signup.html', {'form': form})

@login_required
def notes_list(request):
    """List all notes for the logged in user"""
    notes = Note.objects.filter(user=request.user)
    return render(request, 'app/notes_list.html', {'notes': notes})

@login_required
def note_detail(request, pk):
    """Show a single note"""
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'app/note_detail.html', {'note': note})

@login_required
def note_new(request):
    """Create a new note"""
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, "Note created successfully!")
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm()
    return render(request, 'app/note_edit.html', {'form': form})

@login_required
def note_edit(request, pk):
    """Edit an existing note"""
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save()
            messages.success(request, "Note updated successfully!")
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note)
    return render(request, 'app/note_edit.html', {'form': form})

@login_required
def note_delete(request, pk):
    """Delete a note"""
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == "POST":
        note.delete()
        messages.success(request, "Note deleted successfully!")
        return redirect('notes_list')
    return render(request, 'app/note_confirm_delete.html', {'note': note})

@login_required
def user_profile(request):
    """View and edit user profile"""
    user = request.user
    note_count = Note.objects.filter(user=user).count()
    
    context = {
        'user': user,
        'note_count': note_count,
    }
    
    return render(request, 'app/profile.html', context)
