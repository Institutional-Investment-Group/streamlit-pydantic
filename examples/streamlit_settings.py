from typing import List

import streamlit as st
from pydantic import BaseModel, Field, SecretStr

import streamlit_pydantic as sp


class SubModel(BaseModel):
    things_i_like: List[str]


class MySettings(sp.StreamlitSettings):
    username: str = Field(..., description="The username for the database.")
    password: SecretStr
    my_cool_secrets: SubModel


# Provide example values so the settings can be constructed in this example
example = MySettings(
    username="example-user",
    password=SecretStr("hunter2"),
    my_cool_secrets=SubModel(things_i_like=["chocolate", "python"]),
)

st.json(example.model_dump())
