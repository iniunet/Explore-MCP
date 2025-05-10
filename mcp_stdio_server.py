from mcp.server.fastmcp import FastMCP

# 创建MCP实例
mcp = FastMCP()

#### 声明工具 ####
@mcp.tool()
def aoe(a: int, b: int) -> int:
    """定义了一个新的运算符aoe，根据aoe函数返回aoe运算符的结果"""
    return a * b * b

if __name__ == "__main__":
    # 声明MCP服务器的和MCP客户端的通讯方式是stdio，此时不需要独立运行MCP服务器进程
    mcp.run(transport='stdio')