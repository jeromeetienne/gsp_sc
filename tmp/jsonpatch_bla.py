import json
# from jsonpatch import JsonPatch, apply_patch
import jsonpatch

# 1. Define the original and modified JSON documents (as Python dicts/lists)
original_doc = {
    "name": "Jane Doe",
    "details": {
        "age": 30,
        "city": "New York",
        "hobbies": ["reading", "hiking"]
    },
    "status": "active"
}

modified_doc = {
    "name": "Jane Smith",  # Changed name
    "details": {
        "age": 31,  # Changed age
        "city": "New York",
        "hobbies": ["reading", "baking", "hiking"]  # Added 'baking'
    },
    "new_field": True,  # Added new field
    # 'status' field is removed
}

print("--- Original Document ---")
print(json.dumps(original_doc, indent=2))
print("\n--- Modified Document ---")
print(json.dumps(modified_doc, indent=2))

# 2. Generate the Diff (JSON Patch)
# JsonPatch.from_diff(original, modified) creates the patch to get from original to modified
patch_list = jsonpatch.JsonPatch.from_diff(original_doc, modified_doc)

print("\n--- Generated JSON Patch (Diff) ---")
# The patch is a list of operation dictionaries
print(json.dumps(patch_list.patch, indent=2))

# 3. Apply the Diff (Patch)
# apply_patch(document, patch) applies the patch to the original document
patched_doc = jsonpatch.apply_patch(original_doc, patch_list)

print("\n--- Document After Applying Patch ---")
print(json.dumps(patched_doc, indent=2))

# 4. Verify the result
print("\n--- Verification ---")
if patched_doc == modified_doc:
    print("Patch applied successfully! The patched document matches the modified document.")
else:
    print("Patch application failed.")