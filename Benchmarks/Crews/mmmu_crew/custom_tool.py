import base64
import requests
from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, you agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        return "this is an example of a tool output, ignore it and move along."

class LLaVAImageToolInput(BaseModel):
    """Input schema for LLaVAImageTool."""
    prompt: str = Field(default="Describe with details this image", description="Instruction for the LLaVA model")

class LLaVAImageTool(BaseTool):
    name: str = "ImageInterpreter"
    description: str = "Analyzes the provided image using the LLaVA model from Ollama. The image is already loaded, just provide a prompt/question about the image."
    args_schema: Type[BaseModel] = LLaVAImageToolInput
    image_base64: Optional[str] = Field(default=None, description="Base64 encoded image data")

    def __init__(self, image_base64: str = None, **kwargs):
        super().__init__(image_base64=image_base64, **kwargs)

    def _run(self, prompt: str = "Describe with details this image"):
        """
        prompt: Instruction for the LLaVA model about what to analyze in the image.
        """
        if not self.image_base64:
            return "Error: No image data provided to the tool."
            
        payload = {
            "model": "llava",
            "prompt": prompt,
            "images": [self.image_base64],
            "stream": False
        }

        try:
            response = requests.post("http://localhost:11434/api/generate", json=payload)
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            return f"Error calling LLaVA: {str(e)}"