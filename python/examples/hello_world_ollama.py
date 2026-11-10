import argparse
import os

from chaincrafter import Chain, Prompt
from chaincrafter.models import OpenAiChat

parser = argparse.ArgumentParser(description="Run a local chain with Ollama and Qwen 0.5B.")
parser.add_argument("--stream", action="store_true", help="Use streaming HTTP responses")
args = parser.parse_args()

# Keep this example local even if the shell is configured for OpenAI.
os.environ["OPENAI_BASE_URL"] = "http://127.0.0.1:11434/v1"
os.environ["OPENAI_API_KEY"] = "ollama"  # Required by the SDK; ignored by local Ollama.

chat_model = OpenAiChat(
    temperature=0.0,
    model_name="qwen2.5:0.5b",
    max_tokens=32,
    stream=args.stream,
)
chain = Chain(
    Prompt("Answer arithmetic questions with only the number, no explanation."),
    (Prompt("What is two plus two?"), "answer"),
    (Prompt("What is {answer} plus three?"), "followup_answer"),
)
for message in chain.run(chat_model):
    print(f"{message['role']}: {message['content']}")
chat_model.show_usage()
