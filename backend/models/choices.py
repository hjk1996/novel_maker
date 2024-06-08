from pydantic import BaseModel


class Choices(BaseModel):
    first: str
    second: str
    third: str
    fourth: str

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
