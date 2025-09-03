from typing import Optional

import streamlit as st
from pydantic import Base64UrlBytes, BaseModel, Field

import streamlit_pydantic as sp


class ExampleModel(BaseModel):
    text: str = Field(
        ...,
        description="A text field",
        json_schema_extra={"maxLength": 100, "st_kwargs_max_chars": 500},
    )
    number: int = Field(
        10,
        description="A numeric field",
        json_schema_extra={
            "st_kwargs_min_value": 10,
            "st_kwargs_max_value": 100,
            "st_kwargs_step": 5,
        },
    )
    single_file: Base64UrlBytes = Field(
        b"",
        json_schema_extra={"st_kwargs_type": ["png", "jpg"]},
    )


data = sp.pydantic_form(key="my_form", model=ExampleModel)
if data:
    st.json(data.model_dump_json())

st.subheader("Pydantic Output")
sp.pydantic_output(data)
