from dotenv import load_dotenv
import anthropic
import json

load_dotenv()

client = anthropic.Anthropic()

invoice_text = "Hi, this is Acme Ltd. Please pay the 1,250.00 EUR for October's hosting by 15 November 2026."

response = client.messages.create(
  model = "claude-haiku-4-5",
  max_tokens = 300,
  messages = [
    {"role": "user", "content": f"Extract the invoice details: {invoice_text}"}
  ],
  output_config = {
    "format": {
      "type": "json_schema",
      "schema": {
        "type": "object",
        "properties": {
          "vendor": {"type": "string"},
          "amount": {"type": "number"},
          "currency": {"type": "string"},
          "due_date": {"type": "string"},
        },
        "required": ["vendor", "amount", "currency", "due_date"],
        "additionalProperties": False,
      },
    },
  },
)

print(response.content[0].text)
print(type(response.content[0].text))

# The reply is JSON text, not a dict, so parse it before reading fields
data = json.loads(response.content[0].text)
print(type(data))
print(data["amount"])