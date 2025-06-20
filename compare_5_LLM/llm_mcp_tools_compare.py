from mcp import ClientSession
from mcp.client.sse import sse_client
import asyncio
from openai import OpenAI
import json

# 通过openai的api访问ollama本地管理的大模型的标准实现方式
# 和大模型的交互全部封装在以下函数里,message参数代表输入大模型的user Prompt
def llm_client(message:str,model:str):
    client = OpenAI(
    base_url='http://localhost:11434/v1/',  
    # required but ignored
    api_key='ollama',
    )
    response = client.chat.completions.create(
        model=model,
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
                "如果不需要使用工具，请直接回答并且不要输出json格式的回答\n\n"
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
            model_list = ["qwen3","gemma3","qwen2.5-coder:3b","deepseek-r1:7b","llama3.2"] 
            # 创建输入大模型的user提示词
            user_prompt = get_prompt_to_identify_tool_and_arguments(query,tools.tools)

            # 对不同的大模型问同一个问题
            for model in model_list:         
                # 输出不同大模型的回答
                llm_response =  llm_client(user_prompt,model)
                print("-----开始-----"+model+"----输出----")
                print(llm_response)
                print("-----结束-----"+model+"----输出----")
            return llm_response

if __name__ == "__main__":
    
    while True:
        query = input("请输入问题：")
        asyncio.run(AI_client(query))

                    
        # for mol in model_list:
            
