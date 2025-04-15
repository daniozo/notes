import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from app.models import Note

@pytest.mark.django_db
def test_home_view_unauthenticated(client):
    """Test home view for unauthenticated user"""
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'Welcome to NoteKeeper' in response.content.decode()

@pytest.mark.django_db
def test_home_view_authenticated(client):
    """Test home view redirects for authenticated user"""
    user = User.objects.create_user(username='testuser', password='password123')
    client.force_login(user)
    response = client.get(reverse('home'))
    assert response.status_code == 302  # Redirect to notes_list
    assert response.url == reverse('notes_list')

@pytest.mark.django_db
def test_notes_list_view(client):
    """Test notes list view for authenticated user"""
    user = User.objects.create_user(username='testuser', password='password123')
    Note.objects.create(title="Test Note 1", content="Content 1", user=user)
    Note.objects.create(title="Test Note 2", content="Content 2", user=user)
    
    client.force_login(user)
    response = client.get(reverse('notes_list'))
    assert response.status_code == 200
    
    content = response.content.decode()
    assert 'Test Note 1' in content
    assert 'Test Note 2' in content

@pytest.mark.django_db
def test_note_create_view(client):
    """Test note creation"""
    user = User.objects.create_user(username='testuser', password='password123')
    client.force_login(user)
    
    # GET request should display the form
    response = client.get(reverse('note_new'))
    assert response.status_code == 200
    
    # POST request should create a new note
    response = client.post(reverse('note_new'), {
        'title': 'New Test Note',
        'content': 'New content created from test'
    })
    assert response.status_code == 302  # Redirect after success
    
    # Verify note was created
    assert Note.objects.filter(title='New Test Note').exists()
