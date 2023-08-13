from unstructured.partition.auto import partition
from unstructured.staging.base import convert_to_dict

from chaincrafter.splitters import split_processed_content


class Document:
    def __init__(self, elements: list):
        self.elements = elements

    def __iter__(self) -> iter:
        return iter(self.elements)

    def __str__(self) -> str:
        return f"{super().__str__()}: {len(self.elements)} elements"

    def content(self) -> str:
        return "\n".join(["\n".join(chunk) for chunk in self.elements])


def load_document(path: str, char_limit: int = 4000) -> Document:
    """
    Uses unstructured to load a document and partition it into elements
    """
    with open(path, 'rb') as f:
        elements = partition(file=f)
        content = convert_to_dict(elements)
        return Document(split_processed_content(content, char_limit))
