from dotenv import load_dotenv

import anthropic

from utils.save_run import save_run

load_dotenv()
client = anthropic.Anthropic()

STAGE = "stage0_bare"
PROMPT = """Write a Python class ShoppingCart with add_item(name, price, quantity).
Then tell me: does your code pass its tests?"""

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=4096,
    messages=[{"role": "user", "content": PROMPT}],
)

print("stop_reason:", response.stop_reason)
save_run(STAGE, PROMPT, response)