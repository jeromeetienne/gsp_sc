import GSP_pb2 as GSP

id_counter = 0

# Create a canvas
canvas = GSP.CANVAS()
canvas.id = id_counter
id_counter += 1
canvas.width = 800
canvas.height = 600
canvas.dpi = 96.0

canvasSetDpi = GSP.CANVAST_SET_DPI()
canvasSetDpi.id = id_counter
id_counter += 1
canvasSetDpi.canvas_id = canvas.id
canvasSetDpi.dpi = canvas.dpi

canvasSetSize = GSP.CANVAST_SET_SIZE()
canvasSetSize.id = id_counter
id_counter += 1
canvasSetSize.canvas_id = canvas.id
canvasSetSize.width = canvas.width
canvasSetSize.height = canvas.height

# Create a viewport and attach it to the canvas
viewport = GSP.VIEWPORT()
viewport.id = id_counter
id_counter += 1
viewport.canvas_id = canvas.id
viewport.x = 0
viewport.y = 0
viewport.width = 800
viewport.height = 600

viewportSetPosition = GSP.VIEWPORT_SET_POSITON()
viewportSetPosition.id = id_counter
id_counter += 1
viewportSetPosition.viewport_id = viewport.id
viewportSetPosition.x = 10
viewportSetPosition.y = 20

viewportSetSize = GSP.VIEWPORT_SET_SIZE()
viewportSetSize.id = id_counter
id_counter += 1
viewportSetSize.viewport_id = viewport.id
viewportSetSize.width = 400
viewportSetSize.height = 300

# Create a pixels visual and attach it to the viewport
pixels = GSP.PIXELS()
pixels.id = id_counter
id_counter += 1
pixels.positions.positions_list.lists.extend([GSP.LIST(values=[0, 1, 2]), GSP.LIST(values=[3, 4, 5])])
pixels.colors.colors_single.rgba = bytes([255, 0, 0, 255])  # Red color for all pixels
# Define groups for the pixels - various options
pixels.groups.groups_size = 10
pixels.groups.group_sizes.values.extend([3, 3])
pixels.groups.group_indices.lists.extend([GSP.LIST(values=[0, 1, 2]), GSP.LIST(values=[3, 4, 5])])


# Serialize and deserialize the pixels message
serializedPixels = pixels.SerializeToString()
deserializedPixels = GSP.PIXELS.FromString(serializedPixels)

print("Original PIXELS message:")
print(pixels)
print("\nDeserialized PIXELS message:")
print(deserializedPixels)
