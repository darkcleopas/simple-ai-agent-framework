prompt = """
<instructions>
Propose a plan to solve the task. 
The plan must be a sequence of valid actions.
You have access to the following actions.
If the task does not require any of the listed actions, output an empty plan.
</instructions>

<example>
    <task>This is the task description</task>
    <actions>
        * tool_name_1: description of tool_name_1
        * tool_name_2: description of tool_name_2
    </actions>
    <plan>
        I should first call tool_name_1 to gather the relevant data. 
        After obtaining the data, I should use tool_name_2 to process it and generate the required results. 
    </plan>
    <task>Tell me about Fruity Fedora</task>
    <actions>
        * fetch_product_info: Retrieves information about a product.
        * generate_query: Creates a query based on the gathered information.
        * search_engine: Searches for the required details.
    </actions>
    <plan>
        First, I'll use the fetch_product_info tool to collect relevant information. 
        Then, I'll frame a meaningful query using the generate_query tool. 
        Finally, I'll use the search_engine tool to find the required details.
    </plan>
    <task>What is the capital of Brazil?</task>
    <actions>
        * fetch_product_info: Retrieves information about a product.
        * generate_query: Creates a query based on the gathered information.
    </actions>
    <plan></plan>
</example>

<task>{user_input}</task>
<actions>
{available_tools}
</actions>
"""