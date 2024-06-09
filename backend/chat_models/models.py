from langchain.pydantic_v1 import BaseModel, Field


class Prompt(BaseModel):
    prompt: str = Field(description="prompt")


class NextStory(BaseModel):
    content: str = Field(description="A story that fits well with the previous one.")


class Choices(BaseModel):
    first: str = Field(description="Choice 1")
    second: str = Field(description="Choice 2")
    third: str = Field(description="Choice 3")
    fourth: str = Field(description="Choice 4")

    def __getitem__(self, index):
        match index:
            case 1:
                return self.first
            case 2:
                return self.second
            case 3:
                return self.third
            case 4:
                return self.fourth
            case _:
                raise IndexError("Choices index out of range")
