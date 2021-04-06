import runpy


def test_chapter4():
    runpy.run_module("chapter4.chapter4_standard_field_types_01")
    runpy.run_module("chapter4.chapter4_standard_field_types_02")
    runpy.run_module("chapter4.chapter4_standard_field_types_03")
    runpy.run_module("chapter4.chapter4_optional_fields_default_values_01")
    runpy.run_module("chapter4.chapter4_optional_fields_default_values_02")
    runpy.run_module("chapter4.chapter4_fields_validation_01")
    runpy.run_module("chapter4.chapter4_pydantic_types_01")
