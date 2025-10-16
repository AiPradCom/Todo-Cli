import json
from pathlib import Path
from .models import Todo


class TodoStorage:
    """Handles saving and loading todos from a JSON file"""

    def __init__(self, filepath="todos.json"):
        self.filepath = Path(filepath)
        # Create empty file if it doesn't exist
        if not self.filepath.exists():
            self.filepath.write_text("[]")

    def load_todos(self):
        """Load all todos from the JSON file"""
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                return [Todo.from_dict(item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            # If file is corrupt or missing, return empty list
            return []

    def save_todos(self, todos):
        """Save all todos to the JSON file"""
        with open(self.filepath, 'w') as f:
            json.dump([todo.to_dict() for todo in todos], f, indent=2)

    def add_todo(self, title):
        """Add a new todo and return it"""
        todos = self.load_todos()

        # Find the next available ID
        if todos:
            next_id = max(t.id for t in todos) + 1
        else:
            next_id = 1

        new_todo = Todo.create(next_id, title)
        todos.append(new_todo)
        self.save_todos(todos)

        return new_todo

    def get_todo(self, todo_id):
        """Get a specific todo by its ID"""
        todos = self.load_todos()
        for todo in todos:
            if todo.id == todo_id:
                return todo
        return None

    def complete_todo(self, todo_id):
        """Mark a todo as done. Returns True if found, False otherwise"""
        todos = self.load_todos()

        for todo in todos:
            if todo.id == todo_id:
                todo.done = True
                self.save_todos(todos)
                return True

        return False

    def remove_todo(self, todo_id):
        """Remove a todo. Returns True if found and removed, False otherwise"""
        todos = self.load_todos()
        original_len = len(todos)

        # Filter out the todo with the matching ID
        todos = [t for t in todos if t.id != todo_id]

        if len(todos) < original_len:
            self.save_todos(todos)
            return True

        return False
