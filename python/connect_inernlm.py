
import requests
import json

url = 'https://internlm-chat.intern-ai.org.cn/puyu/api/v1/chat/completions'
header = {
    'Content-Type': 'application/json',
    "Authorization": ""
}
data = {
    "model": "internlm2.5-latest",
    "messages": [{
        "role": "user",
        "content": "番茄炒蛋怎么做？"
    }],
    "n": 1,
    "temperature": 0.8,
    "top_p": 0.9,
    "stream": True,
}

response = requests.post(url, headers=header, data=json.dumps(data), stream=True)
for chunk in response.iter_lines(chunk_size=8192, decode_unicode=False, delimiter=b'\n'):
    if not chunk:
        continue
    decoded = chunk.decode('utf-8')
    if not decoded.startswith("data:"):
        raise Exception(f"error message {decoded}")
    decoded = decoded.strip("data:").strip()
    if "[DONE]" == decoded:
        print("finish!")
        break
    output = json.loads(decoded)
    if output["object"] == "error":
        raise Exception(f"logic err: {output}")
    print(output["choices"][0]["delta"]["content"])
