import gradio as gr
# 升级Gradio
# pip install --upgrade gradio
# 安装Gradio mcp相关python包
# pip install "gradio[mcp]"

def letter_counter(word, letter):
    """
    计算在一个单词里指定字母出现的次数.

    Args:
        word (str): The input text to search through
        letter (str): The letter to search for

    Returns:
        str: A message indicating how many times the letter appears
    """
    word = word.lower()
    letter = letter.lower()
    count = word.count(letter)
    return count

demo = gr.Interface(
    fn=letter_counter,
    inputs=["textbox", "textbox"],
    outputs="number",
    title="Letter Counter",
    description="Enter text and a letter to count how many times the letter appears in the text."
)

if __name__ == "__main__":
    # demo.launch()
    demo.launch(mcp_server=True)    
