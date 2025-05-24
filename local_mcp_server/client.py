import asyncio
import nest_asyncio
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import MCPTool
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser, ReActJsonSingleInputOutputParser
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import httpx
from langchain.tools import Tool
from typing import Optional, Any, Callable, Awaitable

# Enable nested asyncio for Jupyter-like environments
nest_asyncio.apply()

REACT_TEMPLATE = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: {tool_names}
Action Input: the SQL query to execute
Observation: the result of the action
Thought: I now know the final answer
Final Answer: the final answer to the original input question

For example:
Question: add John Doe 30 year old Engineer
Thought: I need to add a new person to the database
Action: add_data
Action Input: INSERT INTO people (name, age, profession) VALUES ('John Doe', 30, 'Engineer')
Observation: Data added successfully
Thought: I have successfully added the person
Final Answer: Added John Doe (age: 30, profession: Engineer) to the database

Begin!

Question: {input}
{agent_scratchpad}"""

class LangchainMCPClient:
    def __init__(self, mcp_server_url="http://127.0.0.1:8000"):
        print("Initializing LangchainMCPClient...")
        self.llm = ChatOllama(
            model="llama3.2",
            temperature=0.6,
            streaming=False  # Disable streaming for better compatibility
        )
        # Updated server configuration with shorter timeouts
        server_config = {
            "default": {
                "url": f"{mcp_server_url}/sse",
                "transport": "sse",
                "options": {
                    "timeout": 10.0,
                    "retry_connect": True,
                    "max_retries": 2,
                    "read_timeout": 5.0,
                    "write_timeout": 5.0
                }
            }
        }
        print(f"Connecting to MCP server at {mcp_server_url}...")
        self.mcp_client = MultiServerMCPClient(server_config)
        self.chat_history = []
        
        # System prompt for the agent
        self.SYSTEM_PROMPT = """You are an AI assistant that helps users interact with a database.
        You can add and read data from the database using the available tools.
        When adding data:
        1. Format the SQL query correctly: INSERT INTO people (name, age, profession) VALUES ('Name', Age, 'Profession')
        2. Make sure to use single quotes around text values
        3. Don't use quotes around numeric values
        
        When reading data:
        1. Use SELECT * FROM people for all records
        2. Use WHERE clause for filtering: SELECT * FROM people WHERE condition
        3. Present results in a clear, formatted way
        
        Always:
        1. Think through each step carefully
        2. Verify actions were successful
        3. Provide clear summaries of what was done"""

    async def check_server_connection(self):
        """Check if the MCP server is accessible"""
        base_url = self.mcp_client.connections["default"]["url"].replace("/sse", "")
        try:
            print(f"Testing connection to {base_url}...")
            async with httpx.AsyncClient(timeout=5.0) as client:  # Shorter timeout
                # Try the SSE endpoint directly
                sse_url = f"{base_url}/sse"
                print(f"Checking SSE endpoint at {sse_url}...")
                response = await client.get(sse_url, timeout=5.0)
                print(f"Got response: {response.status_code}")
                if response.status_code == 200:
                    print("SSE endpoint is accessible!")
                    return True
                
                print(f"Server responded with status code: {response.status_code}")
                return False
                
        except httpx.ConnectError:
            print(f"Could not connect to server at {base_url}")
            print("Please ensure the server is running and the port is correct")
            return False
        except httpx.ReadTimeout:
            print("Connection established but timed out while reading")
            print("This is normal for SSE connections - proceeding...")
            return True
        except Exception as e:
            print(f"Error connecting to MCP server: {type(e).__name__} - {str(e)}")
            return False

    async def initialize_agent(self):
        """Initialize the agent with tools and prompt template"""
        print("\nInitializing agent...")
        if not await self.check_server_connection():
            raise ConnectionError("Cannot connect to MCP server. Please ensure the server is running.")
            
        try:
            print("Getting available tools...")
            mcp_tools = await self.mcp_client.get_tools()
            
            # Verify tools are properly initialized
            print("Verifying tools...")
            for i, tool in enumerate(mcp_tools):
                print(f"\nTool {i}:")
                print(f"  Name: {tool.name if hasattr(tool, 'name') else 'No name'}")
                print(f"  Description: {tool.description if hasattr(tool, 'description') else 'No description'}")
                print(f"  Type: {type(tool)}")
                print(f"  Callable: {callable(tool)}")
                print(f"  Methods: {[method for method in dir(tool) if not method.startswith('_')]}")
                print(f"  Full tool: {tool.__dict__}")
                
                # Test call
                try:
                    print("  Testing tool call...")
                    if i == 0:
                        test_query = "INSERT INTO people (name, age, profession) VALUES ('Test', 30, 'Test')"
                    else:
                        test_query = "SELECT * FROM people"
                    result = await tool.ainvoke({"query": test_query})
                    print(f"  Test result: {result}")
                except Exception as e:
                    print(f"  Test error: {type(e).__name__} - {str(e)}")
            
            if len(mcp_tools) < 2:
                raise ValueError(f"Expected 2 tools, got {len(mcp_tools)}")
            
            # Create async wrapper functions with better error handling
            async def add_data_wrapper(query: str):
                try:
                    tool = mcp_tools[0]  # add_data tool
                    if not tool:
                        print("Tool 0 (add_data) not properly initialized")
                        return "Error: Add data tool not properly initialized"
                    print(f"Executing add_data with query: {query}")
                    # Clean up the query
                    query = query.strip().replace('\n', ' ').replace('  ', ' ')
                    # Fix common formatting issues
                    if "VALUES" in query:
                        parts = query.split("VALUES")
                        if len(parts) == 2:
                            values = parts[1].strip()
                            if values.startswith("(") and values.endswith(")"):
                                values = values[1:-1].split(",")
                                if len(values) == 3:
                                    name = values[0].strip().strip("'")
                                    age = values[1].strip()
                                    profession = values[2].strip().strip("'")
                                    query = f"INSERT INTO people (name, age, profession) VALUES ('{name}', {age}, '{profession}')"
                    # Call the tool using the async method
                    result = await tool.ainvoke({"query": query})
                    print(f"Add data result: {result}")
                    if result:
                        return "Data added successfully"  # Clear success message
                    return "Failed to add data"  # Clear failure message
                except Exception as e:
                    print(f"Error in add_data_wrapper: {type(e).__name__} - {str(e)}")
                    return f"Error adding data: {str(e)}"
                
            async def read_data_wrapper(query: str = "SELECT * FROM people"):
                try:
                    tool = mcp_tools[1]  # read_data tool
                    if not tool:
                        print("Tool 1 (read_data) not properly initialized")
                        return "Error: Read data tool not properly initialized"
                    print(f"Executing read_data with query: {query}")
                    # Clean up the query
                    query = query.strip().replace('\n', ' ').replace('  ', ' ')
                    # Call the tool using the async method
                    result = await tool.ainvoke({"query": query})
                    print(f"Read data result: {result}")
                    if not result:
                        return "No records found"
                    
                    # Handle result as a list of values
                    formatted = []
                    # Each record has 4 fields (id, name, age, profession)
                    for i in range(0, len(result), 4):
                        record = result[i:i+4]  # Get next 4 values
                        formatted.append(f"ID: {record[0]}, Name: {record[1]}, Age: {record[2]}, Profession: {record[3]}")
                    return "\n".join(formatted)
                except Exception as e:
                    print(f"Error in read_data_wrapper: {type(e).__name__} - {str(e)}")
                    return f"Error reading data: {str(e)}"

            # Create Langchain tools with async functions
            self.tools = [
                Tool(
                    name="add_data",
                    description="Add a person to the database. Example: INSERT INTO people (name, age, profession) VALUES ('John Doe', 30, 'Engineer')",
                    func=lambda x: "Use async version",
                    coroutine=add_data_wrapper
                ),
                Tool(
                    name="read_data",
                    description="Read from the database. Example: SELECT * FROM people",
                    func=lambda x: "Use async version",
                    coroutine=read_data_wrapper
                )
            ]
            
            print(f"Found {len(self.tools)} tools")
            
            # Create the prompt template with system message
            system_message = SystemMessage(content=self.SYSTEM_PROMPT)
            human_message = HumanMessagePromptTemplate.from_template(REACT_TEMPLATE)
            prompt = ChatPromptTemplate.from_messages([
                system_message,
                human_message
            ]).partial(tool_names="add_data or read_data")
            
            # Create the agent with simpler configuration
            self.agent = create_react_agent(
                llm=self.llm,
                tools=self.tools,
                prompt=prompt
            )
            
            # Create the executor with better configuration
            self.agent_executor = AgentExecutor(
                agent=self.agent,
                tools=self.tools,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=1,  # Only try once
                early_stopping_method="force"  # Stop after max_iterations
            )
            
            print("\nAvailable tools:")
            for tool in self.tools:
                print(f"- {tool.name}: {tool.description}")
                
        except Exception as e:
            print(f"\nError initializing agent: {e}")
            raise

    async def process_message(self, user_input: str) -> str:
        """Process a single user message and return the agent's response"""
        try:
            print("\nProcessing message:", user_input)
            # Execute the agent
            response = await self.agent_executor.ainvoke({
                "input": user_input,
                "chat_history": self.chat_history
            })
            
            print("\nRaw response:", response)
            
            # Get the result
            if isinstance(response, dict):
                result = response.get("output", str(response))
                if "intermediate_steps" in response:
                    print("\nIntermediate steps:", response["intermediate_steps"])
            else:
                result = str(response)
            
            print("\nFormatted result:", result)
            
            # Update chat history
            self.chat_history.extend([
                HumanMessage(content=user_input),
                AIMessage(content=str(result))
            ])
            
            return str(result)
            
        except Exception as e:
            error_msg = f"Error processing message: {type(e).__name__} - {str(e)}\nPlease try rephrasing your request."
            print(f"\nError processing message: {type(e).__name__} - {str(e)}")
            print(f"Full error: {e.__dict__}")
            return error_msg

    async def interactive_chat(self):
        """Start an interactive chat session"""
        print("Chat session started. Type 'exit' to quit.")
        
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() == "exit":
                print("Ending chat session...")
                break
            
            response = await self.process_message(user_input)
            print("\nAgent:", response)

async def main():
    try:
        print("Starting Langchain MCP Client...")
        client = LangchainMCPClient()
        
        print("\nInitializing agent...")
        await client.initialize_agent()
        
        print("\nStarting interactive chat...")
        await client.interactive_chat()
        
    except ConnectionError as e:
        print(f"\nConnection Error: {e}")
        print("Please check that:")
        print("1. The MCP server is running (python server.py --server_type=sse)")
        print("2. The server URL is correct (http://127.0.0.1:8000)")
        print("3. The server is accessible from your machine")
    except Exception as e:
        print(f"\nUnexpected error: {type(e).__name__} - {str(e)}")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main()) 