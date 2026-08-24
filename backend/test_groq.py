from app.ai.groq_client import client


response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful AI data analyst."
        },
        {
            "role": "user",
            "content": "Explain what a dataframe is in simple terms."
        }
    ]
)


print(response.choices[0].message.content)