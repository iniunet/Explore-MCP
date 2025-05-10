from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client

# 为 stdio类型MCP服务器 指明如何运行MCP服务的调用指令
server_params = StdioServerParameters(
    # MCP服务器执行的命令
    command='python.exe',
    args=['mcp_stdio_server.py'],
    # 环境变量，默认为 None，表示使用当前环境变量
    env=None
)
async def client_run():
    # 1. 异步上下文管理器 (SSE 客户端)
    async with stdio_client(server_params) as (read, write):
        # 2. 异步上下文管理器 (HTTP 会话)
        async with ClientSession(read, write) as session:
            # 3. 等待初始化完成
            await session.initialize()
            
            # 4. 等待获取工具列表
            tools = await session.list_tools()
            print(tools)

            # 5. 等待调用工具 "aoe" 并获取结果
            result = await session.call_tool("aoe", arguments={"a": 4, "b": 5})
            print(result.content[0].text)

if __name__ == "__main__":
    import asyncio
    asyncio.run(client_run())  # 运行 client_run() 异步函数