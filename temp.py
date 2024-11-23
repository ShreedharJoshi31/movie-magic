import os
from dotenv import load_dotenv
load_dotenv()
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_parse import LlamaParse
from llama_index.core.tools import QueryEngineTool


openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")


# settings
Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0, api_key=openai_api_key)

# function tools
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and returns the product"""
    return a * b

multiply_tool = FunctionTool.from_defaults(fn=multiply)

def add(a: float, b: float) -> float:
    """Add two numbers and returns the sum"""
    print(a, b)
    return a + b

add_tool = FunctionTool.from_defaults(fn=add)


def sub(a: float, b: float) -> float:
    """Subtract two numbers and returns the sum"""
    return a - b

sub_tool = FunctionTool.from_defaults(fn=sub)

# rag pipeline
documents = LlamaParse(result_type="markdown", api_key=openai_api_key).load_data("2023_canadian_budget.pdf")
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

budget_tool = QueryEngineTool.from_defaults(
    query_engine, 
    name="canadian_budget_2023",
    description="A RAG engine with some basic facts about the 2023 Canadian federal budget. Ask natural-language questions about the budget."
)

agent = ReActAgent.from_tools([multiply_tool, add_tool, budget_tool, sub_tool], verbose=True)

response = agent.chat("I have 4 apples and my friend has 3 apples if I take their apples how many apples do I have ?")

print(response)

response = agent.chat("Now my friend takes 9 apples from me how many apples do I have ?")

print(response)

# response = agent.chat("How much was the total of those two allocations added together? Use a tool to answer any questions.")

# print(response)