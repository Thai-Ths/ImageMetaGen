from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Type, ClassVar
from agents import Agent, Runner

class MetadataAgent:
    def __init__(
        self,
        max_title_length: int = 70,
        max_keywords: int = 20,
        api_key: Optional[str] = None
    ):
        self.max_title_length = max_title_length
        self.max_keywords = max_keywords
        self.api_key = api_key

        self.output_type = self._build_output_model()
        self.instructions = self._build_system_prompt()

        self.agent = Agent(
            name="Adobe Stock Generate Metadata",
            instructions=self.instructions,
            output_type=self.output_type,
            model="gpt-4o-mini"
        )

    def _build_output_model(self) -> Type[BaseModel]:
        """
        Dynamically defines the Pydantic output schema for metadata.
        """

        max_keywords = self.max_keywords
        max_title_length = self.max_title_length

        class NameKeyword(BaseModel):
            MAX_KEYWORDS: ClassVar[int] = max_keywords

            filename: str = Field(..., description="Original image filename for mapping/logging")
            title: str = Field(..., description=f"SEO-optimized title, max {max_title_length} characters")
            keywords: List[str] = Field(..., description=f"Up to {max_keywords} ordered keywords")

            @field_validator('keywords')
            def limit_keywords(cls, value):
                return value[:cls.MAX_KEYWORDS]

        return NameKeyword

    def _build_system_prompt(self) -> str:
        """
        Returns detailed system instructions for generating metadata.
        """
        return f"""You are an expert metadata generator for Adobe Stock.

Your job is to write professional, SEO-optimized metadata for stock images. Follow these rules:

1. Generate an SEO-friendly **title** (max {self.max_title_length} characters), aiming for the limit.
2. Provide exactly **{self.max_keywords} individual keywords**, separated by commas. **Each keyword must be a single word**, not phrases or sentences.
3. Order keywords by **visual relevance**: subjects > environment > style > abstract ideas.
4. Group them into **2–3 categories** by subject, setting, mood/style.
5. Avoid brand names, logos, copyrighted terms.
6. Eliminate duplicates and overly generic terms. Think like a buyer searching for this image.
"""

    def _build_user_prompt(self, filename: str, image_b64: str, use_filename: bool) -> str:
        """
        Builds the user prompt to feed into the agent, optionally using filename for context.
        """
        base_prompt = f"Here is the image in base64 format: {image_b64}"
        if use_filename:
            return (
                f"{base_prompt}\nUse the filename \"{filename}\" to infer image context."
                " It may hint at subject, scene, or concept. Do not copy it directly."
            )
        return (
            f"{base_prompt}\nFilename: {filename}. Focus on the image content to suggest relevant metadata."
        )

    async def process_image(
        self,
        filename: str,
        image_b64: str,
        use_filename: bool = False
    ):
        """
        Processes a single image and generates metadata using the LLM agent.
        """
        try:
            prompt = self._build_user_prompt(filename, image_b64, use_filename)
            return await Runner.run(self.agent, prompt)
        except Exception as e:
            print(f"❌ Error processing image {filename}: {e}")
            return None
