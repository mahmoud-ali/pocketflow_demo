from openai import OpenAI

def call_llm(prompt,model_name="deepseek-chat"):    
    client = OpenAI(
        api_key="sk-9c06d4df5a7a492aaa045541e50cd0e3", 
        base_url="https://api.deepseek.com",
        timeout=30.0,
        max_retries=3,
    )
    r = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content
    
if __name__ == "__main__":
    prompt = "What is the meaning of life?"
    print(call_llm(prompt))