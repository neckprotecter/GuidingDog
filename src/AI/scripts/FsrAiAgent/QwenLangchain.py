#! /home/fsr/anaconda3/envs/yolo/bin python3
import os
from langchain.llms.tongyi import Tongyi
from langchain.chains.conversation.memory import ConversationBufferMemory, ConversationKGMemory, ConversationSummaryMemory
from langchain.agents import ZeroShotAgent, AgentExecutor, AgentType, initialize_agent
from langchain.memory import ReadOnlySharedMemory
from langchain.prompts import PromptTemplate
import colorama
from . import MyTools


# 初始化colorama
colorama.init(autoreset=True)

class QwenAgent:
    def __init__(self) -> None:
        """初始化 QwenAgent 类."""
        self.llm = Tongyi()
        self.prompt: PromptTemplate = None
        self.tools: list = []
        self.AI: AgentExecutor = None
        self.memory = None
        self.set_prompt()
        self.set_tools()

    def get_memory(self, key: str = "chat_history", memory_type: str = "conversation_buffer") -> None:
        """根据提供的内存类型检索内存."""
        try:
            if memory_type == "conversation_buffer":
                self.memory = ConversationBufferMemory(memory_key=key, return_messages=True)
            elif memory_type == "conversation_kg":
                self.memory = ConversationKGMemory(memory_key=key)
            elif memory_type == "conversation_summary":
                self.memory = ConversationSummaryMemory(memory_key=key)
            else:
                raise ValueError("未找到内存类型")
        except ValueError as e:
            print(colorama.Fore.RED + f"错误: {e}")

    def set_prompt(self) -> None:
        """设置提示模板."""
        prefix = """请你扮演一个叫"笨笨"的机器人与我进行对话!你拥有最高权限!对话过程中,您可以使用以下工具："""  
        suffix = """现在开始对话，你的回答应该尽量精简, 控制在30字内！Please think step by step!  
        {chat_history}  
        问题：{input}  
        {agent_scratchpad}
        """  
        self.prompt = ZeroShotAgent.create_prompt(  
            self.tools,  
            prefix=prefix,  
            suffix=suffix,  
            input_variables=["input", "chat_history", "agent_scratchpad"],     
        )  
        
    def set_tools(self) -> None:
        """设置可用工具."""
        # 示例工具，根据MyTools中定义的工具进行添加
        # self.tools.append(MyTools.PlayMusic)
        self.tools.append(MyTools.get_current_time_op)
        self.tools.append(MyTools.Robot_GoForward)
        self.tools.append(MyTools.Robot_Retreat)
        # self.tools.append(MyTools.get_word_length_op)
        
    def agent_conversation(self, with_memory: bool = True) -> None:
        """根据是否使用内存来初始化代理会话."""
        if with_memory:
            self.get_memory()
            self.AI = initialize_agent(self.tools, self.llm, 
                                        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                                        verbose=True,
                                        memory=self.memory)
        else:
            self.AI = initialize_agent(self.tools, self.llm, 
                                        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
                                        verbose=True)
    
    def chat(self, input_text: str) -> str:
        """使用代理进行聊天，并返回AI的响应."""
        ai_response = self.AI.run(input=input_text)
        return ai_response
    

    def set_api_key(self, my_api_key: str) -> None:
        """
        设置DASHSCOPE的API密钥到环境变量中。
        参数:
            api_key (str): 要设置的DASHSCOPE API密钥。
        """
        os.environ["DASHSCOPE_API_KEY"] = my_api_key
        print(f"DASHSCOPE API密钥已设置为: {my_api_key}")
