from pydantic import BaseModel

import streamlit_pydantic as sp


class ExampleModel(BaseModel):
    some_text: str
    some_number: int = 10  # Optional
    some_boolean: bool = True  # Option


from streamlit_pydantic.ui_renderer import GroupOptionalFieldsStrategy

input_data = sp.pydantic_input(
    "model_input", model=ExampleModel, group_optional_fields=GroupOptionalFieldsStrategy.SIDEBAR
)
