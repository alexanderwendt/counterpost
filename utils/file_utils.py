def load_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def save_file(file_path: str, content: str) -> str:
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
