from openai import OpenAI


# Initialize the client (will use environment variables)
client = OpenAI()


# Make a simple chat completion request
response = client.chat.completions.create(
   model="gpt-4.1",
   messages=[
       {"role": "system", "content": "You are a helpful assistant."},
       {"role": "user", "content": "Hello! Can you help me test this API?"}
   ],
   max_tokens=100
)


# Print the response
print(response.choices[0].message.content)
