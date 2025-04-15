from crewai.tools import BaseTool
import json


############################################################################
# --------------------------------- Code --------------------------------- #
############################################################################


class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, you agent will need this information to use it."
    )

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."
    
class CleanJSON(BaseTool):
    name: str = "Clean JSON"
    description: str = (
        "Cleans a JSON file by removing unnecessary lines at the beginning and end, and formatting it properly."
    )

    def _run(self, file_path: str) -> None:
        """
        Cleans a JSON file by removing unnecessary lines at the beginning and end,
        and formatting it properly.

        Args:
            file_path (str): The path to the JSON file to be cleaned.
        """
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Remove the first and last lines
            cleaned_lines = lines[1:-1]

            # Join the remaining lines and parse as JSON
            cleaned_content = ''.join(cleaned_lines)
            json_data = json.loads(cleaned_content)

            # Write the cleaned and formatted JSON back to the file
            with open(file_path, 'w') as file:
                json.dump(json_data, file, indent=4)

        except Exception as e:
            raise Exception(f"Error cleaning JSON file {file_path}: {e}")