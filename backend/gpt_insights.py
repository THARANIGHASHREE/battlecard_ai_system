import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_gpt_insights(text: str):
    """
    Use OpenAI's new v1 client to get smart insights.
    """
    prompt = f"""
    Analyze this company info:
    \"\"\"{text}\"\"\"

    Give me:
    - Strengths
    - Weaknesses
    - Differentiators
    - Suggested Action

    Format clearly with labels.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content
    return answer
if __name__ == "__main__":
    print("Your key is:", os.getenv("OPENAI_API_KEY"))
