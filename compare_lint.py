import json
import sys

def load_results(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def compare_results(previous, current):
    previous_errors = set(previous.keys())
    current_errors = set(current.keys())

    fixed_errors = previous_errors - current_errors
    new_errors = current_errors - previous_errors

    print(f"Fixed Errors: {len(fixed_errors)}")
    print(f"New Errors: {len(new_errors)}")

    for error in new_errors:
        print(f"New: {error}")
    for error in fixed_errors:
        print(f"Fixed: {error}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: compare_lint.py <previous_results.json> <current_results.json>")
        sys.exit(1)

    previous_results = load_results(sys.argv[1])
    current_results = load_results(sys.argv[2])

    compare_results(previous_results, current_results)
