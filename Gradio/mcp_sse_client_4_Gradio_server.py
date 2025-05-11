from mcp import ClientSession 
from mcp.client.sse import sse_client #sse服务器对应的客户端必须import sse_client

async def client_run():
    # 1. 异步上下文管理器 (SSE 客户端)
    async with sse_client(url="http://127.0.0.1:7860/gradio_api/mcp/sse") as streams:        
        # 2. 异步上下文管理器 (HTTP 会话)
        async with ClientSession(*streams) as session:
            # 3. 等待初始化完成
            await session.initialize()
            
            # 4. 等待获取工具列表
            tools = await session.list_tools()
            print(tools)

            # 5. 等待调用工具 "predict" 并获取结果
            result = await session.call_tool("predict", arguments={"word": "hello", "letter": "l"})            
            print(result.content[0].text)

if __name__ == "__main__":
    import asyncio
    asyncio.run(client_run())  # 运行 client_run() 异步函数