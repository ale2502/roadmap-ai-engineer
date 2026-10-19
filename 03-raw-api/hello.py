from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic()

response = client.messages.create(
  model = "claude-haiku-4-5",
  max_tokens = 30,
  messages = [
    {"role": "user", "content": "Explain what a token is in three sentences"}
  ],
)

print(response.content[0].text)
print(response.usage)
print(response.stop_reason)