import os.path

from chaincrafter import Chain, Prompt
from chaincrafter.loaders import load_document
from chaincrafter.models import OpenAiChat

chat_model = OpenAiChat(temperature=0.9, model_name="gpt-4", top_p=0.2, max_tokens=500)

path = os.path.dirname(__file__)
article = load_document(os.path.join(path, "data", "article.html"), 2000)
previous_articles = [
    (Prompt(
        "Here is a sample of my previous writing, apologies if you already have it on file:\n" + "\n".join(element)
    ), "__ignore") for element in article.elements
]
document = load_document(os.path.join(path, "data", "article2.html"), 1000)
chain = Chain(
    Prompt('You are the managing editor of a non-fiction technical publishing house. I will start by giving you examples of my previous writing. Do not respond to these examples.'),
    *previous_articles,
    (
        Prompt(
            "You are reviewing an article, please provide feedback and writing suggestions on the content: {content}",
            content=lambda elements: "\n".join(elements)
        ),
        "output"
    ),
)
messages = chain.run(chat_model, {"content": document.content()})
for message in messages:
    print(f"{message['role']}: {message['content']}")
