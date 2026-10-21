from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic()

with client.messages.stream(
  model = "claude-haiku-4-5",
  max_tokens = 300,
  messages = [
    {"role": "user", "content": "Explain what a token is in three sentences"}
  ],
) as stream:
  for chunk in stream.text_stream:
    print(chunk, end = "", flush = True)
  print()