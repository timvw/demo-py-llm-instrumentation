import dotenv
from openai import OpenAI
from demo import otel

if __name__ == "__main__":
    dotenv.load_dotenv()

    otel.init_otel_tracing()
    otel.init_instrumentation()

    client = OpenAI()

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ],
        model="gpt-3.5-turbo",
    )

    print(chat_completion)
