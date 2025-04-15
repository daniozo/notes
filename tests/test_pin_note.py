import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from app.models import Note

@pytest.mark.django_db
def test_pin_note(client):
    """Test pinning and unpinning a note"""
    # Create user and note
    user = User.objects.create_user(username='testuser', password='password123')
    note = Note.objects.create(
        title="Test Note", 
        content="This is a test note", 
        user=user,
        is_pinned=False
    )
    
    # Login
    client.force_login(user)
    
    # Pin the note
    response = client.get(reverse('toggle_pin_note', args=[note.id]))
    assert response.status_code == 302  # Should redirect
    
    # Check if note is now pinned
    note.refresh_from_db()
    assert note.is_pinned is True
    
    # Unpin the note
    response = client.get(reverse('toggle_pin_note', args=[note.id]))
    
    # Check if note is now unpinned
    note.refresh_from_db()
    assert note.is_pinned is False
