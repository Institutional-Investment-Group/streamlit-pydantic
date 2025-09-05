from typing import Literal, Optional, Union

from pydantic import BaseModel, Field
from typing_extensions import Annotated

from streamlit_pydantic import schema_utils


class PostalAddress(BaseModel):
    contact_type: Literal["postal"]
    street: str
    city: str
    house: int


class EmailAddress(BaseModel):
    contact_type: Literal["email"]
    email: str
    send_news: bool


class ContactMethod(BaseModel):
    contact: Optional[
        Annotated[Union[PostalAddress, EmailAddress], Field(discriminator="contact_type")]
    ] = None
    text: str


def test_is_union_property_detects_discriminated_union():
    schema = ContactMethod.model_json_schema(by_alias=True)
    contact_prop = schema.get("properties", {}).get("contact")
    assert contact_prop is not None, "contact property must be present in schema"
    assert schema_utils.is_union_property(contact_prop)
