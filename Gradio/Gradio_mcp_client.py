# 安装 Gradio mcp client
# pip install gradio_client

from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		word="Hello!!",
		letter="l",
		api_name="/predict"
)
print(result)
