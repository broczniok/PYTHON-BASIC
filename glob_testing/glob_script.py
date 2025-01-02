import glob
import fnmatch
import os


# Get all files recursively in the directory (including subdirectories)
data = [
    {"id": 1, "name": "files/dir_1/file1.csv", "size": 123},
    {"id": 2, "name": "files/dir_2/file1.avro", "size": 456},
    {"id": 3, "name": "files/dir_3/file2.csv", "size": 789},
    {"id": 4, "name": "files/dir_4/file1.txt", "size": 101},
    {"id": 5, "name": "files/dir_1/file1.txt", "size": 202},
    {"id": 6, "name": "files/dir_1/file1.avro", "size": 303},
    {"id": 7, "name": "files/dir_2/file3.csv", "size": 404},
    {"id": 8, "name": "files/dir_2/file3.txt", "size": 505},
]

# Define patterns to exclude, user can input these
exclude_patterns_2 = [
    'temp/**/*',          # everything in temp folder
    'abc/*.log',          # .log files only in abc folder
    '*.tmp',              # all .tmp files everywhere
    'build/**/*.class',   # .class files in build folder and its subfolders
    '!build/important/**' # but don't exclude anything in build/important
]

exclude_pattern = [
    'files/**/*.csv',          # .log files only in abc folder
    '!*/file2.csv'
]


def filter_dicts_by_name(data, exclude_patterns):
    """
    Filters a list of dictionaries, excluding entries based on the 'name' field and exclusion patterns.

    Parameters:
    - data (list of dict): A list of dictionaries, each containing at least a 'name' key.
    - exclude_patterns (list of str): Glob patterns to exclude. Negated patterns start with '!'.

    Returns:
    - list of dict: Filtered list of dictionaries.
    """
    negate_patterns = [pattern[1:] for pattern in exclude_patterns if pattern.startswith('!')]
    exclude_patterns = [pattern for pattern in exclude_patterns if not pattern.startswith('!')]

    filtered_data = []

    for entry in data:
        if 'name' not in entry:
            filtered_data.append(entry)
            continue

        name = entry['name']

        matches_exclusion = any(fnmatch.fnmatch(name, pattern) for pattern in exclude_patterns)
        print(f"name: {name} matches_exclusion: {matches_exclusion}")

        matches_negation = any(fnmatch.fnmatch(name, pattern) for pattern in negate_patterns)
        print(f"name: {name} matches_negation: {matches_negation}")
        if not matches_exclusion or matches_negation:
            filtered_data.append(entry)

    return filtered_data

filtered_data = filter_dicts_by_name(data, exclude_pattern)
print(filtered_data)

csv_files = [f for f in filtered_data if f['name'].endswith('.csv')]

print(csv_files)