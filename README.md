# Todo CLI

A simple, efficient command-line Todo Manager written in Python.

## Features

- Add new todos with descriptions
- List all todos with status indicators
- Filter todos by completion status (done/pending)
- Mark todos as completed
- Remove todos
- Persistent storage using JSON
- Clean, intuitive command-line interface
- Full test coverage with pytest

## Installation

### From Source

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd todo-cli
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

   Or with development dependencies (for testing):
   ```bash
   pip install -e ".[dev]"
   ```

## Usage

### Add a Todo

```bash
todo-cli add "Buy milk"
todo-cli add "Finish homework"
```

### List All Todos

```bash
todo-cli list
```

Output:
```
Total: 2 todo(s)

[ ] 1. Buy milk
[ ] 2. Finish homework
```

### List Todos by Status

List only pending todos:
```bash
todo-cli list --filter pending
```

List only completed todos:
```bash
todo-cli list --filter done
```

### Mark a Todo as Completed

```bash
todo-cli complete 1
```

Output:
```
Marked todo 1 as completed.
```

Now listing will show:
```
Total: 2 todo(s)

[✓] 1. Buy milk
[ ] 2. Finish homework
```

### Remove a Todo

```bash
todo-cli remove 2
```

Output:
```
Removed todo 2.
```

### Get Help

```bash
todo-cli --help
todo-cli add --help
todo-cli list --help
```

## Data Storage

Todos are stored in a `todos.json` file in the directory where you run the command. Each todo contains:

- `id`: Unique identifier
- `title`: Task description
- `done`: Completion status (true/false)
- `created_at`: ISO 8601 timestamp of creation

## Testing

Run the test suite using pytest:

```bash
pytest
```

Run tests with coverage report:

```bash
pytest --cov=todo --cov-report=term-missing
```

Run specific test file:

```bash
pytest tests/test_todo.py
```

## Project Structure

```
todo-cli/
├── todo/
│   ├── __init__.py       # Package initialization
│   ├── cli.py            # Command-line interface
│   ├── storage.py        # JSON storage layer
│   └── models.py         # Data models
├── tests/
│   └── test_todo.py      # Unit tests
├── pyproject.toml        # Project configuration and dependencies
└── README.md             # This file
```

## Development

### Code Style

This project follows PEP8 conventions. All functions and classes include type hints and docstrings.

### Adding New Features

1. Implement the feature in the appropriate module
2. Add corresponding tests in `tests/test_todo.py`
3. Update the README with usage examples
4. Run tests to ensure nothing breaks

## Requirements

- Python 3.8 or higher
- No external dependencies for core functionality
- pytest (optional, for running tests)

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
