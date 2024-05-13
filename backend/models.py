from langchain.pydantic_v1 import BaseModel, Field


class Choices(BaseModel):
    choice_1: str = Field(..., alias="Choice 1")
    choice_2: str = Field(..., alias="Choice 2")
    choice_3: str = Field(..., alias="Choice 3")
    choice_4: str = Field(..., alias="Choice 4")

    def __getitem__(self, index):
        match index:
            case 1:
                return self.choice_1
            case 2:
                return self.choice_2
            case 3:
                return self.choice_3
            case 4:
                return self.choice_4
            case _:
                raise IndexError("Choices index out of range")
