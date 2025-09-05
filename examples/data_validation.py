import streamlit as st
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from pydantic_extra_types.color import Color

import streamlit_pydantic as sp


class ExampleModel(BaseModel):
    url: HttpUrl = Field(..., description="A valid URL, e.g. https://example.com")
    color: Color = Field(Color("blue"), json_schema_extra={"format": "text"})
    email: EmailStr = Field(..., description="A valid email address, e.g. user@example.com")


data = sp.pydantic_form(key="my_form", model=ExampleModel)
if data:
    st.json(data.model_dump())
