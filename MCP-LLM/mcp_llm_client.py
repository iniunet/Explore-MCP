from mcp import ClientSession
from mcp.client.sse import sse_client
import asyncio
from openai import OpenAI
import json

# 通过openai的api访问ollama本地管理的大模型的标准实现方式
# 和大模型的交互全部封装在以下函数里,message参数代表输入大模型的user Prompt
def llm_client(message:str):
    client = OpenAI(
    base_url='http://localhost:11434/v1/',  
    # required but ignored
    api_key='ollama',
    )
    response = client.chat.completions.create(
        model="qwen3",
        messages=[{"role":"system",
                    "content":"你是一个智能助手，根据用户的问题直接回答或者选择工具回答",
                    "role": "user", "content": message}],
        max_tokens=1000,
        temperature=0.2
    )
    # 返回大模型的回答
    return response.choices[0].message.content.strip()

# 生成输入大模型的user Prompt，把用户的问题和工具的描述一起作为提示词
def get_prompt_to_identify_tool_and_arguments(query,tools):
    tools_description = "\n".join([f"- {tool.name}, {tool.description}, {tool.inputSchema} " for tool in tools])
    return  ("你是一个智能助手，你可以使用以下工具:\n\n"
                f"{tools_description}\n"
                "请根据用户的问题选择合适的工具. \n"
                f"用户的问题: {query}\n"                
                "如果不需要使用工具，请直接回答.\n\n"
                "如果要使用工具，不需要把think的过程放到输出结果，直接按以下json格式回复调用工具的名称和相应的参数 "                
                "{\n"
                '    "tool": "tool-name",\n'
                '    "arguments": {\n'
                '        "argument-name": "value"\n'
                '    "final answer": {\n'
                '        "answers": "value"\n'

                "    }\n"
                "}\n\n")

async def AI_client(query: str):
    async with sse_client(url="http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:

            await session.initialize()

            # 获得MCP服务器的工具列表
            tools = await session.list_tools()
            # print(tools)

            # 创建输入大模型的user提示词
            prompt = get_prompt_to_identify_tool_and_arguments(query,tools.tools)
            # print("输入大模型的提示词："+prompt)

            # 第一次调用大模型，在这个部分判断是否需要调用工具
            llm_response =  llm_client(prompt)
            print('------第一次大模型输出---------------')
            print(f"LLM Response: {llm_response}")   
            print('---------------------')
            parts = llm_response.split('</think>', 1)
            if len(parts) > 1:  
                json_str = parts[1].strip()
                try: 
                    #如果存在JSON数据结构，则大模型给出需要调用工具的回答
                    jsondata = json.loads(json_str)
                
                    # 调用MCP 客户端访问MCP服务器的指定工具
                    result = str(await session.call_tool(jsondata["tool"], arguments=jsondata["arguments"])   )
                    llm_response=llm_response+"调用工具获得后面的结果："+result + "请给出最后回答"
                    # print("工具返回结果："+result)
                    # 第二次调用大模型，这次调用是让大模型结合MCP工具查询的期货价格给出最后回答
                    final_result=llm_client(llm_response)
                    print('------第二次大模型输出---------------')
                    print(final_result)     
                except:
                    print("无需调用工具")


if __name__ == "__main__":
    while True:
        query = input("请输入问题：")
        asyncio.run(AI_client(query))
