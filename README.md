# local_mcp_client
local mcp client using ollama and LangChain mcp adapters

https://medium.com/the-ai-forum/understanding-the-mcp-workflow-building-a-local-mcp-client-using-ollama-and-langchain-mcp-5997b8a5fded

<img width="1274" alt="image" src="https://github.com/user-attachments/assets/83f5b821-50a8-453e-8f4f-47ca72074534" />


(.venv) C:\Users\PLNAYAK\Documents\local_mcp_server>**python server.py --server_type=sse**

🚀Starting server...
INFO:     Started server process [27936]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:63736 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:63738 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:63739 - "POST /messages/?session_id=eb4020cf70564cf085883cb52c25f7a5 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:63739 - "POST /messages/?session_id=eb4020cf70564cf085883cb52c25f7a5 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:63739 - "POST /messages/?session_id=eb4020cf70564cf085883cb52c25f7a5 HTTP/1.1" 202 Accepted
[05/24/25 19:27:58] INFO     Processing request of type ListToolsRequest                                                                                              server.py:551
INFO:     127.0.0.1:63740 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:63741 - "POST /messages/?session_id=9ebf01c8bde8425bb5300babd3dd4ee3 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:63741 - "POST /messages/?session_id=9ebf01c8bde8425bb5300babd3dd4ee3 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:63741 - "POST /messages/?session_id=9ebf01c8bde8425bb5300babd3dd4ee3 HTTP/1.1" 202 Accepted
                    INFO     Processing request of type CallToolRequest                                                                                               server.py:551


Executing add_data with query: INSERT INTO people (name, age, profession) VALUES ('Test', 30, 'Test')
INFO:     127.0.0.1:63742 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:63743 - "POST /messages/?session_id=e9c0f4e207594b9889e64838ac3ceb08 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:63743 - "POST /messages/?session_id=e9c0f4e207594b9889e64838ac3ceb08 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:63743 - "POST /messages/?session_id=e9c0f4e207594b9889e64838ac3ceb08 HTTP/1.1" 202 Accepted
                    INFO     Processing request of type CallToolRequest                                                                                               server.py:551


Executing read_data with query: SELECT * FROM people
INFO:     127.0.0.1:63751 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:63752 - "POST /messages/?session_id=8624577b6f32465fb1c85e9f03d32486 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:63752 - "POST /messages/?session_id=8624577b6f32465fb1c85e9f03d32486 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:63752 - "POST /messages/?session_id=8624577b6f32465fb1c85e9f03d32486 HTTP/1.1" 202 Accepted
[05/24/25 19:28:26] INFO     Processing request of type CallToolRequest                                                                                               server.py:551


Executing add_data with query: INSERT INTO people (name, age, profession) VALUES ('Samiksha', 30, 'Data Scientist')
INFO:     127.0.0.1:63799 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:63800 - "POST /messages/?session_id=ee81c06fb6384535a8632cc6a7883355 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:63800 - "POST /messages/?session_id=ee81c06fb6384535a8632cc6a7883355 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:63800 - "POST /messages/?session_id=ee81c06fb6384535a8632cc6a7883355 HTTP/1.1" 202 Accepted
[05/24/25 19:29:33] INFO     Processing request of type CallToolRequest                                                                                               server.py:551


Executing read_data with query: SELECT * FROM people




(.venv) C:\Users\PLNAYAK\Documents\local_mcp_server>**python langchain_client.py**

Starting Langchain MCP Client...
Initializing LangchainMCPClient...
Connecting to MCP server at http://127.0.0.1:8000...

Initializing agent...

Initializing agent...
Testing connection to http://127.0.0.1:8000...
Checking SSE endpoint at http://127.0.0.1:8000/sse...
Connection established but timed out while reading
This is normal for SSE connections - proceeding...
Getting available tools...
Verifying tools...

Tool 0:
  Name: add_data
  Description: Add new data to the people table using a SQL INSERT query.

    Args:
        query (str): SQL INSERT query following this format:
            INSERT INTO people (name, age, profession)
            VALUES ('John Doe', 30, 'Engineer')

    Schema:
        - name: Text field (required)
        - age: Integer field (required)
        - profession: Text field (required)
        Note: 'id' field is auto-generated

    Returns:
        bool: True if data was added successfully, False otherwise

    Example:
        >>> query = '''
        ... INSERT INTO people (name, age, profession)
        ... VALUES ('Alice Smith', 25, 'Developer')
        ... '''
        >>> add_data(query)
        True

  Type: <class 'langchain_core.tools.structured.StructuredTool'>
  Callable: True
  Methods: ['InputType', 'OutputType', 'abatch', 'abatch_as_completed', 'ainvoke', 'args', 'args_schema', 'arun', 'as_tool', 'assign', 'astream', 'astream_events', 'astream_log', 'atransform', 'batch', 'batch_as_completed', 'bind', 'callback_manager', 'callbacks', 'config_schema', 'config_specs', 'configurable_alternatives', 'configurable_fields', 'construct', 'copy', 'coroutine', 'description', 'dict', 'from_function', 'from_orm', 'func', 'get_config_jsonschema', 'get_graph', 'get_input_jsonschema', 'get_input_schema', 'get_lc_namespace', 'get_name', 'get_output_jsonschema', 'get_output_schema', 'get_prompts', 'handle_tool_error', 'handle_validation_error', 'input_schema', 'invoke', 'is_lc_serializable', 'is_single_input', 'json', 'lc_attributes', 'lc_id', 'lc_secrets', 'map', 'metadata', 'model_computed_fields', 'model_config', 'model_construct', 'model_copy', 'model_dump', 'model_dump_json', 'model_extra', 'model_fields', 'model_fields_set', 'model_json_schema', 'model_parametrized_name', 'model_post_init', 'model_rebuild', 'model_validate', 'model_validate_json', 'model_validate_strings', 'name', 'output_schema', 'parse_file', 'parse_obj', 'parse_raw', 'pick', 'pipe', 'raise_deprecation', 'response_format', 'return_direct', 'run', 'schema', 'schema_json', 'stream', 'tags', 'to_json', 'to_json_not_implemented', 'tool_call_schema', 'transform', 'update_forward_refs', 'validate', 'verbose', 'with_alisteners', 'with_config', 'with_fallbacks', 'with_listeners', 'with_retry', 'with_types']
  Full tool: {'name': 'add_data', 'description': "Add new data to the people table using a SQL INSERT query.\n\n    Args:\n        query (str): SQL INSERT query following this format:\n            INSERT INTO people (name, age, profession)\n            VALUES ('John Doe', 30, 'Engineer')\n        \n    Schema:\n        - name: Text field (required)\n        - age: Integer field (required)\n        - profession: Text field (required)\n        Note: 'id' field is auto-generated\n    \n    Returns:\n        bool: True if data was added successfully, False otherwise\n    \n    Example:\n        >>> query = '''\n        ... INSERT INTO people (name, age, profession)\n        ... VALUES ('Alice Smith', 25, 'Developer')\n        ... '''\n        >>> add_data(query)\n        True\n    ", 'args_schema': {'properties': {'query': {'title': 'Query', 'type': 'string'}}, 'required': ['query'], 'title': 'add_dataArguments', 'type': 'object'}, 'return_direct': False, 'verbose': False, 'callbacks': None, 'callback_manager': None, 'tags': None, 'metadata': None, 'handle_tool_error': False, 'handle_validation_error': False, 'response_format': 'content_and_artifact', 'func': None, 'coroutine': <function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x000002E4EF853600>}
  Testing tool call...
  Test result: true

Tool 1:
  Name: read_data
  Description: Read data from the people table using a SQL SELECT query.

    Args:
        query (str, optional): SQL SELECT query. Defaults to "SELECT * FROM people".
            Examples:
            - "SELECT * FROM people"
            - "SELECT name, age FROM people WHERE age > 25"
            - "SELECT * FROM people ORDER BY age DESC"

    Returns:
        list: List of tuples containing the query results.
              For default query, tuple format is (id, name, age, profession)

    Example:
        >>> # Read all records
        >>> read_data()
        [(1, 'John Doe', 30, 'Engineer'), (2, 'Alice Smith', 25, 'Developer')]

        >>> # Read with custom query
        >>> read_data("SELECT name, profession FROM people WHERE age < 30")
        [('Alice Smith', 'Developer')]

  Type: <class 'langchain_core.tools.structured.StructuredTool'>
  Callable: True
  Methods: ['InputType', 'OutputType', 'abatch', 'abatch_as_completed', 'ainvoke', 'args', 'args_schema', 'arun', 'as_tool', 'assign', 'astream', 'astream_events', 'astream_log', 'atransform', 'batch', 'batch_as_completed', 'bind', 'callback_manager', 'callbacks', 'config_schema', 'config_specs', 'configurable_alternatives', 'configurable_fields', 'construct', 'copy', 'coroutine', 'description', 'dict', 'from_function', 'from_orm', 'func', 'get_config_jsonschema', 'get_graph', 'get_input_jsonschema', 'get_input_schema', 'get_lc_namespace', 'get_name', 'get_output_jsonschema', 'get_output_schema', 'get_prompts', 'handle_tool_error', 'handle_validation_error', 'input_schema', 'invoke', 'is_lc_serializable', 'is_single_input', 'json', 'lc_attributes', 'lc_id', 'lc_secrets', 'map', 'metadata', 'model_computed_fields', 'model_config', 'model_construct', 'model_copy', 'model_dump', 'model_dump_json', 'model_extra', 'model_fields', 'model_fields_set', 'model_json_schema', 'model_parametrized_name', 'model_post_init', 'model_rebuild', 'model_validate', 'model_validate_json', 'model_validate_strings', 'name', 'output_schema', 'parse_file', 'parse_obj', 'parse_raw', 'pick', 'pipe', 'raise_deprecation', 'response_format', 'return_direct', 'run', 'schema', 'schema_json', 'stream', 'tags', 'to_json', 'to_json_not_implemented', 'tool_call_schema', 'transform', 'update_forward_refs', 'validate', 'verbose', 'with_alisteners', 'with_config', 'with_fallbacks', 'with_listeners', 'with_retry', 'with_types']
  Full tool: {'name': 'read_data', 'description': 'Read data from the people table using a SQL SELECT query.\n\n    Args:\n        query (str, optional): SQL SELECT query. Defaults to "SELECT * FROM people".\n            Examples:\n            - "SELECT * FROM people"\n            - "SELECT name, age FROM people WHERE age > 25"\n            - "SELECT * FROM people ORDER BY age DESC"\n    \n    Returns:\n        list: List of tuples containing the query results.\n              For default query, tuple format is (id, name, age, profession)\n    \n    Example:\n        >>> # Read all records\n        >>> read_data()\n        [(1, \'John Doe\', 30, \'Engineer\'), (2, \'Alice Smith\', 25, \'Developer\')]\n        \n        >>> # Read with custom query\n        >>> read_data("SELECT name, profession FROM people WHERE age < 30")\n        [(\'Alice Smith\', \'Developer\')]\n    ', 'args_schema': {'properties': {'query': {'default': 'SELECT * FROM people', 'title': 'Query', 'type': 'string'}}, 'title': 'read_dataArguments', 'type': 'object'}, 'return_direct': False, 'verbose': False, 'callbacks': None, 'callback_manager': None, 'tags': None, 'metadata': None, 'handle_tool_error': False, 'handle_validation_error': False, 'response_format': 'content_and_artifact', 'func': None, 'coroutine': <function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x000002E4EF8BE8E0>}
  Testing tool call...
  Test result: ['1', 'Test', '30', 'Test', '2', 'plaban nayak', '45', 'manager', '3', 'plaban nayak', '45', 'manager', '4', 'plaban nayak', '45', 'manager', '5', 'Test', '30', 'Test', '6', 'soma', '34', 'HR', '7', 'Test', '30', 'Test', '8', 'salmon', '35', 'accountant', '9', 'Test', '30', 'Test', '10', 'Kamilla', '24', 'Receptionist', '11', 'Test', '30', 'Test', '12', 'kishore', '27', 'facility manager', '13', 'Test', '30', 'Test', '14', 'Test', '30', 'Test', '15', 'Test', '30', 'Test', '16', 'Test', '30', 'Test', '17', 'Panama', '55', 'SME', '18', 'Test', '30', 'Test']
Found 2 tools

Available tools:
- add_data: Add a person to the database. Example: INSERT INTO people (name, age, profession) VALUES ('John Doe', 30, 'Engineer')
- read_data: Read from the database. Example: SELECT * FROM people

Starting interactive chat...
Chat session started. Type 'exit' to quit.

You: add Samiksha 30 years old Data Scientist

Processing message: add Samiksha 30 years old Data Scientist


> Entering new AgentExecutor chain...
Question: add Samiksha 30 years old Data Scientist
Thought: I need to add a new person to the database
Action: add_data
Action Input: INSERT INTO people (name, age, profession) VALUES ('Samiksha', 30, 'Data Scientist')Executing add_data with query: INSERT INTO people (name, age, profession) VALUES ('Samiksha', 30, 'Data Scientist')
Add data result: true
Data added successfully

> Finished chain.

Raw response: {'input': 'add Samiksha 30 years old Data Scientist', 'chat_history': [], 'output': 'Agent stopped due to iteration limit or time limit.', 'intermediate_steps': [(AgentAction(tool='add_data', tool_input="INSERT INTO people (name, age, profession) VALUES ('Samiksha', 30, 'Data Scientist')", log="Question: add Samiksha 30 years old Data Scientist\nThought: I need to add a new person to the database\nAction: add_data\nAction Input: INSERT INTO people (name, age, profession) VALUES ('Samiksha', 30, 'Data Scientist')"), 'Data added successfully')]}

Final result: Successfully added Samiksha (age: 30, profession: Data Scientist) to the database

Agent: Successfully added Samiksha (age: 30, profession: Data Scientist) to the database

You: Show all records

Processing message: Show all records


> Entering new AgentExecutor chain...
Question: show all records
Thought: I need to retrieve all records from the database
Action: read_data
Action Input: SELECT * FROM peopleExecuting read_data with query: SELECT * FROM people
Read data result: ['1', 'Test', '30', 'Test', '2', 'plaban nayak', '45', 'manager', '3', 'plaban nayak', '45', 'manager', '4', 'plaban nayak', '45', 'manager', '5', 'Test', '30', 'Test', '6', 'soma', '34', 'HR', '7', 'Test', '30', 'Test', '8', 'salmon', '35', 'accountant', '9', 'Test', '30', 'Test', '10', 'Kamilla', '24', 'Receptionist', '11', 'Test', '30', 'Test', '12', 'kishore', '27', 'facility manager', '13', 'Test', '30', 'Test', '14', 'Test', '30', 'Test', '15', 'Test', '30', 'Test', '16', 'Test', '30', 'Test', '17', 'Panama', '55', 'SME', '18', 'Test', '30', 'Test', '19', 'Samiksha', '30', 'Data Scientist']
Showing 19 records:

| Name          | Age | Profession       |
|---------------|-----|------------------|
| Test          | 30    | Test             |
| plaban nayak  | 45    | manager          |
| plaban nayak  | 45    | manager          |
| plaban nayak  | 45    | manager          |
| Test          | 30    | Test             |
| soma          | 34    | HR               |
| Test          | 30    | Test             |
| salmon        | 35    | accountant       |
| Test          | 30    | Test             |
| Kamilla       | 24    | Receptionist     |
| Test          | 30    | Test             |
| kishore       | 27    | facility manager |
| Test          | 30    | Test             |
| Test          | 30    | Test             |
| Test          | 30    | Test             |
| Test          | 30    | Test             |
| Panama        | 55    | SME              |
| Test          | 30    | Test             |
| Samiksha      | 30    | Data Scientist   |

> Finished chain.

Raw response: {'input': 'Show all records', 'chat_history': [HumanMessage(content='add Samiksha 30 years old Data Scientist', additional_kwargs={}, response_metadata={}), AIMessage(content='Successfully added Samiksha (age: 30, profession: Data Scientist) to the database', additional_kwargs={}, response_metadata={})], 'output': 'Agent stopped due to iteration limit or time limit.', 'intermediate_steps': [(AgentAction(tool='read_data', tool_input='SELECT * FROM people', log='Question: show all records\nThought: I need to retrieve all records from the database\nAction: read_data\nAction Input: SELECT * FROM people'), 'Showing 19 records:\n\n| Name          | Age | Profession       |\n|---------------|-----|------------------|\n| Test          | 30    | Test             |\n| plaban nayak  | 45    | manager          |\n| plaban nayak  | 45    | manager          |\n| plaban nayak  | 45    | manager          |\n| Test          | 30    | Test             |\n| soma          | 34    | HR               |\n| Test          | 30    | Test             |\n| salmon        | 35    | accountant       |\n| Test          | 30    | Test             |\n| Kamilla       | 24    | Receptionist     |\n| Test          | 30    | Test             |\n| kishore       | 27    | facility manager |\n| Test          | 30    | Test             |\n| Test          | 30    | Test             |\n| Test          | 30    | Test             |\n| Test          | 30    | Test             |\n| Panama        | 55    | SME              |\n| Test          | 30    | Test             |\n| Samiksha      | 30    | Data Scientist   |')]}

Final result: Showing 19 records:

| Name          | Age | Profession       |
|---------------|-----|------------------|
| Test          | 30    | Test             |
| plaban nayak  | 45    | manager          |
| plaban nayak  | 45    | manager          |
| plaban nayak  | 45    | manager          |
| Test          | 30    | Test             |
| soma          | 34    | HR               |
| Test          | 30    | Test             |
| salmon        | 35    | accountant       |
| Test          | 30    | Test             |
| Kamilla       | 24    | Receptionist     |
| Test          | 30    | Test             |
| kishore       | 27    | facility manager |
| Test          | 30    | Test             |
| Test          | 30    | Test             |
| Test          | 30    | Test             |
| Test          | 30    | Test             |
| Panama        | 55    | SME              |
| Test          | 30    | Test             |
| Samiksha      | 30    | Data Scientist   |

Agent: Showing 19 records:

| Name          | Age | Profession       |
|---------------|-----|------------------|
| Test          | 30    | Test             |
| plaban nayak  | 45    | manager          |
| plaban nayak  | 45    | manager          |
| plaban nayak  | 45    | manager          |
| Test          | 30    | Test             |
| soma          | 34    | HR               |
| Test          | 30    | Test             |
| salmon        | 35    | accountant       |
| Test          | 30    | Test             |
| Kamilla       | 24    | Receptionist     |
| Test          | 30    | Test             |
| kishore       | 27    | facility manager |
| Test          | 30    | Test             |
| Test          | 30    | Test             |
| Test          | 30    | Test             |
| Test          | 30    | Test             |
| Panama        | 55    | SME              |
| Test          | 30    | Test             |
| Samiksha      | 30    | Data Scientist   |

You:

