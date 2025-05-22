from langchain.prompts import PromptTemplate

main_prompt_template_single = PromptTemplate(input_variables=["file_path_context", "file_path_python", "inputs", "logging_utils",
                                                       "base_code", "context_info", "main_example"],
    template=""" You're a coding assistant. You will load the context file and update the Python code based on the context.
    
    Instructions:
    - Load {file_path_context} and update the Python code in {file_path_python} based on the context.
    - Try to modify the code as little as possible.
    - Based on the {file_path_context} file, if each task has a single expert, only modify the dictonary of inputs of the main.py file
                in each function with the new inputs will be {inputs}.
    - Before the run function, add a basic logging setup using the {logging_utils} file and taking into account
        how it is made in {main_example}. The {logging_utils} file will be on the utils folder. 
    - Do not add a _main_ due to the fact that the code will be executed using a cli.
    - Add the necessary imports to the top of the file. Take into account the improrts that are already in {base_code}.
    - Do not add imports that are not used in the code.
    - Use only Ascii characters in the code.
    
    Directory of context: {file_path_context}
    Directory of Python code: {file_path_python}
    Directory of logging utils: {logging_utils}
    
    Additional instructions:
    Format the code like this:
    ```python
    {base_code}
    ```
    
    
    Return ONLY the modified code without any other text.
    """
)

crew_prompt_template_single = PromptTemplate(input_variables=["file_path_context_task", "file_path_context_agents", 
                                                              "file_path_python", "inputs",
                                                                "base_code", "tasks_context_info", 
                                                                "agents_context_info", "crew_example"],
    template=""" You're a coding assistant. You will load the context file and update the Python code based on the context.
    
    Instructions:
    - Load {file_path_context_task} and {file_path_context_agents} and update the Python code in {file_path_python} based on the 
        new agents and tasks.
    - Enviroment variables as in {crew_example} file will not be avaliable.
    - Try to modify the code as little as possible.
    - Do not add a _main_ due to the fact that the code will be executed using a cli.
    - Add the necessary imports to the top of the file. Take into account the improrts that are already in {base_code}.
    - Do not add imports that are not used in the code.
    - Based on the {file_path_context_task} and {file_path_context_agents} files, modificate the code 
        and create the new functions of agents and tasks.
    - For the each agent and task use the same format as in {crew_example} file, invoking the agent or task, modifying the
        config and output file like it is done in the {crew_example} file.
    - Add a manager like in {crew_example} file, out of the class and above it.
    - Change the process to hierarchical and add the manager agent.
    - Allow verbose mode in agents and crew.
    - The output of the tasks will be an .md file.
    - Use only Ascii characters in the code.
    

    Directory of Python code: {file_path_python}
    Directory of tasks context: {file_path_context_task}
    Directory of agents context: {file_path_context_agents}
    Directory of crew example: {crew_example}
    
    Additional instructions:
    Format the code like this:
    ```python
    {base_code}
    ```
    
    
    Return ONLY the modified code without any other text.
    
    """
)