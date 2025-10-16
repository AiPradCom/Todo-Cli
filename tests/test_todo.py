import os
import tempfile
import pytest
from pathlib import Path

from todo.models import Todo
from todo.storage import TodoStorage


@pytest.fixture
def temp_storage():
    """Create a temporary storage for testing"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name

    storage = TodoStorage(temp_file)
    yield storage

    # Cleanup after test
    if Path(temp_file).exists():
        os.unlink(temp_file)


def test_create_todo():
    """Test creating a new Todo"""
    todo = Todo.create(1, "Test task")
    assert todo.id == 1
    assert todo.title == "Test task"
    assert todo.done is False
    assert todo.created_at is not None


def test_add_todo(temp_storage):
    """Test adding todos"""
    todo = temp_storage.add_todo("Buy groceries")
    assert todo.id == 1
    assert todo.title == "Buy groceries"
    assert todo.done is False

    # Add another one
    todo2 = temp_storage.add_todo("Walk the dog")
    assert todo2.id == 2


def test_list_todos(temp_storage):
    """Test loading todos"""
    temp_storage.add_todo("Task 1")
    temp_storage.add_todo("Task 2")

    todos = temp_storage.load_todos()
    assert len(todos) == 2
    assert todos[0].title == "Task 1"
    assert todos[1].title == "Task 2"


def test_complete_todo(temp_storage):
    """Test completing a todo"""
    todo = temp_storage.add_todo("Finish homework")
    assert todo.done is False

    result = temp_storage.complete_todo(todo.id)
    assert result is True

    updated_todo = temp_storage.get_todo(todo.id)
    assert updated_todo.done is True


def test_complete_nonexistent_todo(temp_storage):
    """Test completing a todo that doesn't exist"""
    result = temp_storage.complete_todo(999)
    assert result is False


def test_remove_todo(temp_storage):
    """Test removing a todo"""
    todo = temp_storage.add_todo("Temporary task")
    todos = temp_storage.load_todos()
    assert len(todos) == 1

    result = temp_storage.remove_todo(todo.id)
    assert result is True

    todos = temp_storage.load_todos()
    assert len(todos) == 0


def test_remove_nonexistent_todo(temp_storage):
    """Test removing a todo that doesn't exist"""
    result = temp_storage.remove_todo(999)
    assert result is False


def test_get_todo(temp_storage):
    """Test getting a specific todo by ID"""
    temp_storage.add_todo("Task 1")
    todo2 = temp_storage.add_todo("Task 2")

    retrieved = temp_storage.get_todo(todo2.id)
    assert retrieved is not None
    assert retrieved.title == "Task 2"

    non_existent = temp_storage.get_todo(999)
    assert non_existent is None


def test_todo_persistence(temp_storage):
    """Test that todos persist when reloading"""
    filepath = temp_storage.filepath

    temp_storage.add_todo("Persistent task")

    # Create new storage with same file
    new_storage = TodoStorage(str(filepath))
    todos = new_storage.load_todos()

    assert len(todos) == 1
    assert todos[0].title == "Persistent task"
