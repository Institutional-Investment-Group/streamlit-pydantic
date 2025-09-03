import datetime
from enum import Enum
from typing import Dict, List, Literal, Optional, Set

import streamlit as st
from pydantic import Base64UrlBytes, BaseModel, Field, SecretStr
from pydantic_extra_types.color import Color

import streamlit_pydantic as sp


class SelectionValue(str, Enum):
    FOO = "foo"
    BAR = "bar"


class OtherData(BaseModel):
    text: str
    integer: int


class DisabledModel(BaseModel):
    short_text: str = Field(
        ...,
        description="Short text property",
        json_schema_extra={"readOnly": True, "maxLength": 60},
    )
    password: SecretStr = Field(
        ...,
        description="Password text property",
        json_schema_extra={"readOnly": True},
    )
    long_text: str = Field(
        ...,
        description="Unlimited text property",
        json_schema_extra={"readOnly": True, "format": "multi-line"},
    )
    integer_in_range: int = Field(
        20,
        ge=10,
        le=30,
        multiple_of=2,
        description="Number property with a limited range. Optional because of default value.",
        json_schema_extra={"readOnly": True},
    )
    positive_integer: int = Field(
        ...,
        ge=0,
        multiple_of=10,
        description="Positive integer with step count of 10.",
        json_schema_extra={"readOnly": True},
    )
    float_number: float = Field(
        0.001,
        json_schema_extra={"readOnly": True},
    )
    date: datetime.date = Field(
        default_factory=datetime.date.today,
        json_schema_extra={"readOnly": True},
    )
    time: datetime.time = Field(
        default_factory=lambda: datetime.datetime.now().time(),
        description="Time property. Optional because of default value.",
        json_schema_extra={"readOnly": True},
    )
    dt: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
        description="Datetime property. Optional because of default value.",
        json_schema_extra={"readOnly": True},
    )
    boolean: bool = Field(
        False,
        description="Boolean property. Optional because of default value.",
        json_schema_extra={"readOnly": True},
    )
    colour: Color = Field(
        default_factory=lambda: Color("Blue"),
        description="Color property. Optional because of default value.",
        json_schema_extra={"readOnly": True},
    )
    read_only_text: str = Field(
        "Lorem ipsum dolor sit amet",
        description="This is a read only text.",
        json_schema_extra={"readOnly": True},
    )
    file_list: List[Base64UrlBytes] = Field(
        default_factory=list,
        description="A list of files. Optional property.",
        json_schema_extra={"readOnly": True},
    )
    single_file: Optional[Base64UrlBytes] = Field(
        None,
        description="A single file. Optional property.",
        json_schema_extra={"readOnly": True},
    )
    single_selection: SelectionValue = Field(
        ...,
        description="Only select a single item from a set.",
        json_schema_extra={"readOnly": True},
    )
    single_selection_with_literal: Literal["foo", "bar"] = Field(
        "foo",
        description="Only select a single item from a set.",
        json_schema_extra={"readOnly": True},
    )
    multi_selection: Set[SelectionValue] = Field(
        ...,
        description="Allows multiple items from a set.",
        json_schema_extra={"readOnly": True},
    )
    multi_selection_with_literal: Set[Literal["foo", "bar"]] = Field(
        default_factory=lambda: set(["foo", "bar"]),
        description="Allows multiple items from a set.",
        json_schema_extra={"readOnly": True},
    )
    single_object: OtherData = Field(
        ...,
        description="Another object embedded into this model.",
        json_schema_extra={"readOnly": True},
    )
    string_list: List[str] = Field(
        ...,
        description="List of string values",
        json_schema_extra={"readOnly": True, "maxItems": 20},
    )
    int_list: List[int] = Field(
        ...,
        description="List of int values",
        json_schema_extra={"readOnly": True},
    )
    string_dict: Dict[str, str] = Field(
        ...,
        description="Dict property with string values",
        json_schema_extra={"readOnly": True},
    )
    float_dict: Dict[str, float] = Field(
        ...,
        description="Dict property with float values",
        json_schema_extra={"readOnly": True},
    )
    object_list: List[OtherData] = Field(
        ...,
        description="A list of objects embedded into this model.",
        json_schema_extra={"readOnly": True},
    )


instance = DisabledModel(
    short_text="Some INSTANCE text",
    password=SecretStr("$uper_$ecret!"),
    long_text="This is some really long text from the INSTANCE",
    integer_in_range=28,
    positive_integer=20,
    float_number=0.00444,
    date=datetime.date(1999, 9, 9),
    time=datetime.time(9, 9, 16),
    dt=datetime.datetime(1999, 9, 9),
    boolean=True,
    colour=Color("Yellow"),
    read_only_text="INSTANCE read only text",
    file_list=[],
    single_file=b"",
    single_selection=SelectionValue.FOO,
    single_selection_with_literal="bar",
    multi_selection={SelectionValue.FOO, SelectionValue.BAR},
    multi_selection_with_literal=set(["foo", "bar"]),
    single_object=OtherData(text="nested data INSTANCE text", integer=66),
    string_list=["a", "ab", "abc"],
    int_list=[9, 99, 999],
    string_dict={"key 1": "A", "key 2": "B", "key 3": "C"},
    float_dict={"key A": 9.99, "key B": 66.0, "key C": -55.8},
    object_list=[
        OtherData(text="object list INSTANCE item 1", integer=6),
        OtherData(text="object list INSTANCE item 2", integer=99),
    ],
)


from_model_tab, from_instance_tab = st.tabs(
    ["Form inputs from model", "Form inputs from instance"]
)

with from_model_tab:
    data = sp.pydantic_input(key="my_disabled_model", model=DisabledModel)
    with st.expander("Current Input State", expanded=False):
        st.json(data)

with from_instance_tab:
    data = sp.pydantic_input(key="my_disabled_instance", model=instance)
    with st.expander("Current Input State", expanded=False):
        st.json(data)
