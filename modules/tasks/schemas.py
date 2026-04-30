from pydantic import BaseModel, Field, field_validator, ConfigDict


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    is_done: bool = False
    parent_id: int | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("title cannot be empty or whitespace only")
        return cleaned_value


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    is_done: bool | None = None
    parent_id: int | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        if value is None:
            return value

        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("title cannot be empty or whitespace only")
        return cleaned_value


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    is_done: bool
    parent_id: int | None = None