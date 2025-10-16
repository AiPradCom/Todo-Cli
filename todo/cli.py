import argparse
import sys
from .storage import TodoStorage


def format_todo(todo):
    """Format a todo for nice display"""
    checkbox = "✓" if todo.done else " "
    return f"[{checkbox}] {todo.id}. {todo.title}"


def cmd_add(storage, title):
    """Add a new todo"""
    todo = storage.add_todo(title)
    print(f"Added todo: {todo.title} (ID: {todo.id})")


def cmd_list(storage, filter_status=None):
    """List todos, optionally filtering by done/pending"""
    todos = storage.load_todos()

    # Apply filter if specified
    if filter_status == "done":
        todos = [t for t in todos if t.done]
    elif filter_status == "pending":
        todos = [t for t in todos if not t.done]

    if not todos:
        print("No todos found.")
        return

    print(f"Total: {len(todos)} todo(s)")
    print()
    for todo in todos:
        print(format_todo(todo))


def cmd_complete(storage, todo_id):
    """Mark a todo as completed"""
    if storage.complete_todo(todo_id):
        print(f"Marked todo {todo_id} as completed.")
    else:
        print(f"Error: Todo {todo_id} not found.", file=sys.stderr)
        sys.exit(1)


def cmd_remove(storage, todo_id):
    """Remove a todo"""
    if storage.remove_todo(todo_id):
        print(f"Removed todo {todo_id}.")
    else:
        print(f"Error: Todo {todo_id} not found.", file=sys.stderr)
        sys.exit(1)


def main():
    """Entry point for the CLI"""
    parser = argparse.ArgumentParser(
        prog="todo-cli",
        description="A simple command-line Todo Manager"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    parser_add = subparsers.add_parser("add", help="Add a new todo")
    parser_add.add_argument("title", type=str, help="Todo description")

    # List command
    parser_list = subparsers.add_parser("list", help="List all todos")
    parser_list.add_argument(
        "--filter",
        type=str,
        choices=["done", "pending"],
        help="Filter todos by status"
    )

    # Complete command
    parser_complete = subparsers.add_parser("complete", help="Mark a todo as completed")
    parser_complete.add_argument("id", type=int, help="Todo ID")

    # Remove command
    parser_remove = subparsers.add_parser("remove", help="Remove a todo")
    parser_remove.add_argument("id", type=int, help="Todo ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    storage = TodoStorage()

    # Dispatch to appropriate command handler
    if args.command == "add":
        cmd_add(storage, args.title)
    elif args.command == "list":
        cmd_list(storage, args.filter)
    elif args.command == "complete":
        cmd_complete(storage, args.id)
    elif args.command == "remove":
        cmd_remove(storage, args.id)


if __name__ == "__main__":
    main()
