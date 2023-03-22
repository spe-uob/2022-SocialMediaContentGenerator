import os

invalid_dir_name = [
    '.idea',
    '.vscode',
    'pytest_cache',
    '__pycache__',
    'venv',
    'node_modules',
    'dist',
    'build'
]


def check_invalid_dir():
    passed = True
    for root, dirs, files in os.walk('.'):
        for folder in dirs:
            if folder in invalid_dir_name:
                print(f'Invalid directory: {os.path.join(root, folder)}')
                passed = False
    return passed


if __name__ == '__main__':
    result = check_invalid_dir()
    if not result:
        exit(1)
    else:
        print('No invalid directory found.')
        print('Passed!')
        exit(0)
