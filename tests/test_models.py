import pytest
from django.contrib.auth.models import User
from app.models import Note

@pytest.mark.django_db
def test_note_creation():
    """Test the creation of a Note object"""
    user = User.objects.create_user(username='testuser', password='password123')
    note = Note.objects.create(
        title="Test Note",
        content="This is a test note content",
        user=user
    )
    assert note.id is not None
    assert note.title == "Test Note"
    assert note.content == "This is a test note content"
    assert note.user == user

@pytest.mark.django_db
def test_note_str_method():
    """Test the __str__ method of the Note model"""
    user = User.objects.create_user(username='testuser', password='password123')
    note = Note.objects.create(
        title="Test Note",
        content="This is a test note content",
        user=user
    )
    assert str(note) == "Test Note"
