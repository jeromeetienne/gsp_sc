import os
import json
import numpy as np
import pytest
from gsp_sc.transform import TransformChain, TransformSerialisation


def test_transform_serialisation_roundtrip(tmp_path):
    # Create a TransformChain
    chain = TransformChain([4, 5, 6]).assert_shape((3,)).math_op("add", 2).lambdaFunc(lambda x: x * 3).complete()
    # Serialize to JSON
    json_array = TransformSerialisation.to_json(chain)
    # Write to file
    file_path = tmp_path / "chain.json"
    with open(file_path, "w") as f:
        json.dump(json_array, f)
    # Read from file and deserialize
    with open(file_path, "r") as f:
        loaded_json = json.load(f)
    chain_deserialized = TransformSerialisation.from_json(loaded_json)
    # Run and check result
    result = chain_deserialized.run()
    expected = np.array([(4 + 2) * 3, (5 + 2) * 3, (6 + 2) * 3])
    assert np.array_equal(result, expected)


def test_transform_serialisation_invalid_json():
    # Pass invalid JSON (not a transform chain)
    with pytest.raises(Exception):
        TransformSerialisation.from_json({"invalid": "data"})  # type: ignore


def test_transform_serialisation_identity():
    # Test with identity transform
    chain = TransformChain([7, 8, 9]).complete()
    json_array = TransformSerialisation.to_json(chain)
    chain_deserialized = TransformSerialisation.from_json(json_array)
    result = chain_deserialized.run()
    expected = np.array([7, 8, 9])
    assert np.array_equal(result, expected)
