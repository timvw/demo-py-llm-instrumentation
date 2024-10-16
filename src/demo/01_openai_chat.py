import dotenv
from openai import OpenAI
from openinference.instrumentation.openai import OpenAIInstrumentor

if __name__ == "__main__":
    dotenv.load_dotenv()

    OpenAIInstrumentor().instrument()

    client = OpenAI()

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ],
        model="gpt-4o-mini",
    )

    print(chat_completion)
