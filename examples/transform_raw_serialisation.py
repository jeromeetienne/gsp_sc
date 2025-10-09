import gsp
import numpy as np
import os
import json
from gsp.transform import TransformSerialisation, TransformLinkAssertShape, TransformLinkLambda, TransformLinkImmediate

# import a user-defined TransformLink
from common.transform import TransformLinkMathOp

__dirname__ = os.path.dirname(os.path.abspath(__file__))

###############################################################################
# Create a Transform chain and serialize it
#

# Create a Transform chain using only TransformLinks
transform_chain = (
    TransformLinkImmediate(np.array([1, 2, 3]))
    .chain(TransformLinkAssertShape((3,)))
    .chain(TransformLinkMathOp("mul", 10))
    .chain(TransformLinkLambda(lambda x: x + 1))
)

print(f"transform_chain: {transform_chain}")

# Convert to JSON
json_array = TransformSerialisation.to_json(transform_chain)

# Pretty print the JSON
print(f"json_array: {json.dumps(json_array, indent=8)}")

# Write it in a file
file_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}.transform.json"
with open(file_path, "w") as file_writer:
    json.dump(json_array, file_writer)

print(f"Transform chain JSON written to {file_path}")


###############################################################################
# Deserialize the Transform chain from JSON and run it
#

# Recreate the Transform chain from JSON
transform_deserialized = TransformSerialisation.from_json(json_array)

# Run the deserialized transform chain
np_array = transform_deserialized.run()

# Display the result
print(f"np_array_deserialized: {np_array}")

###############################################################################
# Validate the result
#

assert np.array_equal(np_array, np.array([11, 21, 31])), "Deserialized transform did not produce the expected result"
