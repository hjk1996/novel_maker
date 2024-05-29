from pydantic import BaseModel


class Choices(BaseModel):
    choice_1: str
    choice_2: str
    choice_3: str
    choice_4: str

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
