from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "deepseek/deepseek-chat-v3-0324"
BASE_URL = "https://openrouter.ai/api/v1"
TIMEOUT_SECONDS = 60


def run_student_prompt(prompt, sample_input):
    """Run the student's prompt against the LLM and return the output."""

    # Validate API key
    if not OPENROUTER_API_KEY:
        return (
            "⚠️ **API key not configured.**\n\n"
            "To enable live output, add your **OpenRouter API key** to the `.env` file:\n"
            "```\nOPENROUTER_API_KEY=sk-or-v1-...\n```"
        )

    try:
        client = OpenAI(
            base_url=BASE_URL,
            api_key=OPENROUTER_API_KEY,
            timeout=TIMEOUT_SECONDS,
        )

        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": f"{prompt}\n\nInput:\n{sample_input}"
                }
            ],
            timeout=TIMEOUT_SECONDS,
        )

        return completion.choices[0].message.content

    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "unauthorized" in error_msg.lower():
            return "⚠️ **Invalid API key.** Check your OPENROUTER_API_KEY in `.env`."
        elif "429" in error_msg or "rate limit" in error_msg.lower():
            return "⚠️ **Rate limit exceeded.** Please wait a moment and try again."
        elif "timeout" in error_msg.lower():
            return "⚠️ **Request timed out.** The model took too long to respond. Try a simpler prompt."
        else:
            return f"⚠️ **Model error:** {error_msg}"