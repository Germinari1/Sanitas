import pytest
from models.hospital_rag_query import HospitalQueryInput, HospitalQueryOutput

def test_input_model_valid():
    inp = HospitalQueryInput(text="hello")
    assert inp.text == "hello"

@pytest.mark.parametrize("bad", [None, 123, {"text":"hi"}])
def test_input_model_invalid(bad):
    with pytest.raises(Exception):
        HospitalQueryInput(text=bad)

def test_output_model_valid():
    out = HospitalQueryOutput(
        input="q", output="a", intermediate_steps=["step1", "step2"]
    )
    assert out.input == "q"
    assert isinstance(out.intermediate_steps, list)
