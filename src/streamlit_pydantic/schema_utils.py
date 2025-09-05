"""Utilities to help with JSON Schema.

lazydocs: ignore
"""

from typing import Dict, List


def resolve_reference(reference: str, references: Dict) -> Dict:
    return references[reference.split("/")[-1]]

def filter_nullable(property: Dict) -> Dict:
    # if it is optional and nullable, it may be
    # - {'anyOf': [{'type': '<type>'}, {'type': 'null'}]
    # - {'anyOf': [{'$ref': '<ref>'}, {'type': 'null'}]
    # we want to remove the "null" type
    union_prop = property.get("oneOf", property.get("anyOf"))
    if union_prop is not None:
        # Remove the null type, while keeping the `$ref` and other types
        where = [i for i,d in enumerate(union_prop) if d.get('type') == "null"]
        where.reverse()
        for i in where:
            del union_prop[i]
        if len(union_prop) == 1: # it is fine, we wrap the type to the original object
            for key in union_prop[0]:
                property[key] = union_prop[0][key]

            del property["anyOf"] # now we can delete the key

    return property

def get_single_reference_item(property: Dict, references: Dict) -> Dict:
    # Ref can either be directly in the properties or the first element of allOf
    reference = property.get("$ref")
    if reference is None:
        reference = property["allOf"][0]["$ref"]
    return resolve_reference(reference, references)


def get_union_references(property: Dict, references: Dict) -> List[Dict]:
    # Ref can either be directly in the properties or the first element of allOf
    # anyOf is used for union property prior to pydantic < 1.10
    union_references = property.get("oneOf", property.get("anyOf"))
    resolved_references: List[Dict] = []
    for reference in union_references:  # type: ignore
        if reference.get("oneOf") is not None:
            for disc_ref in reference["oneOf"]:
                resolved_references.append(
                    resolve_reference(disc_ref["$ref"], references)
                )
        elif reference.get("$ref") is not None:
            resolved_references.append(resolve_reference(reference["$ref"], references))
    return resolved_references


def is_single_string_property(property: Dict) -> bool:
    return property.get("type") == "string"


def is_single_color_property(property: Dict) -> bool:
    if property.get("type") != "string":
        return False
    return property.get("format") in ["color"]


def is_single_datetime_property(property: Dict) -> bool:
    if property.get("type") != "string":
        return False
    return property.get("format") in ["date-time", "time", "date"]


def is_single_boolean_property(property: Dict) -> bool:
    return property.get("type") == "boolean"


def is_single_number_property(property: Dict) -> bool:
    return property.get("type") in ["integer", "number"]


def is_single_file_property(property: Dict) -> bool:
    if property.get("type") != "string":
        return False
    return property.get("format") in ["base64", "base64url"]


def is_multi_enum_property(property: Dict, references: Dict) -> bool:
    if property.get("type") != "array":
        return False

    if property.get("uniqueItems") is not True:
        # Only relevant if it is a set or other datastructures with unique items
        return False

    try:
        # Uses literal
        _ = property["items"]["enum"]
        return True
    except Exception:
        pass

    try:
        # Uses enum
        _ = resolve_reference(property["items"]["$ref"], references)["enum"]
        return True
    except Exception:
        return False


def is_single_enum_property(property: Dict, references: Dict) -> bool:
    if property.get("enum"):
        return True

    try:
        _ = get_single_reference_item(property, references)["enum"]
        return True
    except Exception:
        return False


def is_single_dict_property(property: Dict) -> bool:
    if property.get("type") != "object":
        return False
    return "additionalProperties" in property


def is_single_reference(property: Dict) -> bool:
    if property.get("type") is not None:
        return False

    return bool(property.get("$ref"))


def is_multi_file_property(property: Dict) -> bool:
    if property.get("type") != "array":
        return False

    if property.get("items") is None:
        return False

    try:
        return property["items"]["format"] in ["base64", "base64url"]
    except Exception:
        return False


def is_single_object(property: Dict, references: Dict) -> bool:
    try:
        object_reference = get_single_reference_item(property, references)
        if object_reference["type"] != "object":
            return False
        return "properties" in object_reference
    except Exception:
        return False


def is_union_property(property: Dict) -> bool:
    # Union properties may use either `oneOf` or `anyOf` depending on Pydantic
    # version and schema generation details. Prefer `oneOf` when present.
    union_prop = property.get("oneOf", property.get("anyOf"))

    if union_prop is None:
        return False

    if len(union_prop) == 0:
        return False

    discriminated = False

    for reference in union_prop:
        # If this reference is itself a discriminated wrapper (contains oneOf),
        # validate its inner choices.
        if reference.get("oneOf") is not None or reference.get("anyOf") is not None:
            discriminated = True
            inner_choices = reference.get("oneOf") or reference.get("anyOf")
            for discriminated_reference in inner_choices:
                if not is_single_reference(discriminated_reference):
                    return False

        # Otherwise, allow either a direct $ref or simple type refs
        if not discriminated and not is_single_reference(reference):
            return False

    return True


def is_property_list(property: Dict) -> bool:
    if property.get("type") != "array":
        return False

    if property.get("items") is None:
        return False

    try:
        return property["items"]["type"] in ["string", "number", "integer"]
    except Exception:
        return False


def is_object_list_property(property: Dict, references: Dict, key:str, schema_ref) -> bool:
    if property.get("type") != "array":
        return False

    try:
        if property["items"].get("$ref") is not None:
            object_reference = resolve_reference(property["items"]["$ref"], references)
        else:
            object_reference = property["items"]

        if object_reference["type"] == "string":
            return True
        elif object_reference["type"] != "object":
            return False
        else:
            return "properties" in object_reference
    except Exception:
        return False
