from mcp.server.fastmcp import FastMCP
import mdsql as db

# 创建MCP实例
mcp = FastMCP()

#### 声明工具：从sqlite数据库查询期货价格信息 ####
@mcp.tool()
def get_qh_price_from_sqlite(qh_name: str) -> dict:
    """
    获得指定期货品种的最新价格.
    Args:
        qh_name (str): 期货品种名称    

    Returns:
        dict: 包含指定期货品种的最新价格相关信息
    """
    my_dict=db.get_close_4_comm(qh_name)
    return my_dict

@mcp.tool()
def get_weather(city: str) -> dict:
    """
    获得指定城市的天气.
    Args:
        city (str): 城市名称    

    Returns:
        dict: 包含指定城市的天气信息
    """
    
    return city+":下雨"

if __name__ == "__main__":
    # 声明MCP服务器的和MCP客户端的通讯方式是sse
    mcp.run(transport='sse')