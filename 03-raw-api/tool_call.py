from dotenv import load_dotenv
import anthropic

load_dotenv()

def get_weather(city):
  return f"18°C, sunny in {city}"

tools = [
  {
    "name": "get_weather",
    "description": "get the current weather for a given city, e.g. Paris",
    "input_schema": {
      "type": "object",
      "properties": {
        "city": {"type": "string", "description": "the intended city" },
      },
      "required": ["city"],
    },
  }
]

client = anthropic.Anthropic()

response = client.messages.create(
  model = "claude-haiku-4-5",
  max_tokens = 300,
  messages = [
    {"role": "user", "content": "What's the weather in Paris?"}
  ],
  tools = tools,
)

tool_block = response.content[0]
result = get_weather(tool_block.input["city"])

final = client.messages.create(
  model = "claude-haiku-4-5",
  max_tokens = 300,
  messages = [
    {"role": "user", "content": "What's the weather in Paris?"},
    {"role": "assistant", "content": response.content},
    {"role": "user", "content": [
      {"type": "tool_result", "tool_use_id": tool_block.id, "content": result}
    ]}
  ],
  tools = tools,
)

print(final.content[0].text)
print(final.stop_reason)