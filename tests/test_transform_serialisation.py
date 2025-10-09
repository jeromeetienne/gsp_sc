import os
import json
import numpy as np
import pytest
from gsp.transform import TransformSerialisation, TransformLinkLoad, TransformLinkImmediate, TransformLinkLambda


def test_transform_serialisation_roundtrip(tmp_path):
    # Create a Transform chain
    chain = TransformLinkImmediate(np.array([4, 5, 6])).chain(TransformLinkLambda(lambda x: x + 2))
    chain = chain.chain(TransformLinkLambda(lambda x: x * 3))
    # Serialize to JSON
    json_array = TransformSerialisation.to_json(chain)
    # Deserialize from JSON
    chain_deserialized = TransformSerialisation.from_json(json_array)
    # Run and check result
    result = chain_deserialized.run()
    print("Result:", result)
    expected = np.array([(4 + 2) * 3, (5 + 2) * 3, (6 + 2) * 3])
    assert np.array_equal(result, expected)


def test_transform_serialisation_invalid_json():
    # Pass invalid JSON (not a transform chain)
    with pytest.raises(Exception):
        TransformSerialisation.from_json({"invalid": "data"})  # type: ignore


def test_transform_serialisation_identity():
    # Test with identity transform
    chain = TransformLinkImmediate(np.array([4, 5, 6]))
    json_array = TransformSerialisation.to_json(chain)
    chain_deserialized = TransformSerialisation.from_json(json_array)
    result = chain_deserialized.run()
    expected = np.array([4, 5, 6])
    assert np.array_equal(result, expected)
