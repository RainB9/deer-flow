import openai
import json
import requests



client = openai.OpenAI(
    api_key = "1730164377737ObGGqViqNctJLfWavEq3Kn4",
    base_url = "http://120.204.73.73:8033/api/ai-gateway/v1/"
)
# response = client.chat.completions.create(
#     model="DeepSeek-V3-0324",
#     messages=[{"role": "user", "content": "你好"}]
# )
# print(response.model_dump_json(indent=2))

# 本地工具函数
def get_weather(latitude, longitude):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&current=temperature_2m&timezone=auto"
    )
    resp = requests.get(url)
    data = resp.json()
    return f"{data['current']['temperature_2m']}°C"

# 工具描述（仅供模型决定是否调用）
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for provided coordinates in celsius.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
            },
            "required": ["latitude", "longitude"]
        }
    }
}]

# 第一次提问
messages = [{"role": "user", "content": "查一下巴黎天气"}]

# Step 1: 向模型请求
response = client.chat.completions.create(
    model="Gpt-4o",
    messages=messages,
    tools=tools,
    tool_choice="auto",
    stream=False
)
# response1 = client.chat.completions.create(
#     model= "Gpt-4o",
#     messages=messages,
#     tools=tools,
#     stream=True
# )
# print("r1 stream = true回答:",response1)
# for chunk in response:
#     if 'choices' in chunk and len(chunk['choices']) > 0:
#         delta = chunk['choices'][0].get('delta', {})
#         content = delta.get('content', '')
#         print(content, end='', flush=True)
# print("r1 stream = true回答结束")
print("🤖 模型回答:", response)
tool_calls = response.choices[0].message.tool_calls

if tool_calls:
    tool_call = tool_calls[0]
    func_name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    print("📡 模型请求调用工具:", func_name)
    print("📦 参数:", args)

    # Step 2: 本地执行工具
    if func_name == "get_weather":
        result = get_weather(args["latitude"], args["longitude"])
        answer = f"根据我查到的数据，巴黎当前气温大约是 {result}。"
else:
    # 没有调用工具，直接用模型回答
    answer = response.choices[0].message.content

# ✅ 输出最终结果
print("🌤️ 最终回答:", answer)
