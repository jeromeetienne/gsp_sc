from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BufferType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BYTE: _ClassVar[BufferType]
    UBYTE: _ClassVar[BufferType]
    SHORT: _ClassVar[BufferType]
    USHORT: _ClassVar[BufferType]
    LONG: _ClassVar[BufferType]
    ULONG: _ClassVar[BufferType]
    FLOAT: _ClassVar[BufferType]
    VEC2: _ClassVar[BufferType]
    VEC3: _ClassVar[BufferType]
    VEC4: _ClassVar[BufferType]
    IVEC2: _ClassVar[BufferType]
    IVEC3: _ClassVar[BufferType]
    IVEC4: _ClassVar[BufferType]
    UVEC2: _ClassVar[BufferType]
    UVEC3: _ClassVar[BufferType]
    UVEC4: _ClassVar[BufferType]
    DATETIME: _ClassVar[BufferType]
    TIMEDELTA: _ClassVar[BufferType]

class OutputType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IMAGE: _ClassVar[OutputType]
    OUTPUT_BUFFER: _ClassVar[OutputType]
    METADATA: _ClassVar[OutputType]

class OutputFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FORMAT_RGBA: _ClassVar[OutputFormat]
    FORMAT_FLOAT: _ClassVar[OutputFormat]
    FORMAT_DEPTH: _ClassVar[OutputFormat]
    FORMAT_ID: _ClassVar[OutputFormat]

class FormatType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RGB: _ClassVar[FormatType]
    RGBA: _ClassVar[FormatType]
BYTE: BufferType
UBYTE: BufferType
SHORT: BufferType
USHORT: BufferType
LONG: BufferType
ULONG: BufferType
FLOAT: BufferType
VEC2: BufferType
VEC3: BufferType
VEC4: BufferType
IVEC2: BufferType
IVEC3: BufferType
IVEC4: BufferType
UVEC2: BufferType
UVEC3: BufferType
UVEC4: BufferType
DATETIME: BufferType
TIMEDELTA: BufferType
IMAGE: OutputType
OUTPUT_BUFFER: OutputType
METADATA: OutputType
FORMAT_RGBA: OutputFormat
FORMAT_FLOAT: OutputFormat
FORMAT_DEPTH: OutputFormat
FORMAT_ID: OutputFormat
RGB: FormatType
RGBA: FormatType

class COMMAND(_message.Message):
    __slots__ = ()
    CANVAS_FIELD_NUMBER: _ClassVar[int]
    CANVAS_SET_SIZE_FIELD_NUMBER: _ClassVar[int]
    CANVAS_SET_DPI_FIELD_NUMBER: _ClassVar[int]
    VIEWPORT_FIELD_NUMBER: _ClassVar[int]
    VIEWPORT_SET_POSITION_FIELD_NUMBER: _ClassVar[int]
    VIEWPORT_SET_SIZE_FIELD_NUMBER: _ClassVar[int]
    BUFFER_FIELD_NUMBER: _ClassVar[int]
    BUFFER_SET_DATA_FIELD_NUMBER: _ClassVar[int]
    PIXELS_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_BIND_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_SET_BASE_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_SET_LEFT_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_SET_RIGHT_FIELD_NUMBER: _ClassVar[int]
    canvas: CANVAS
    canvas_set_size: CANVAST_SET_SIZE
    canvas_set_dpi: CANVAST_SET_DPI
    viewport: VIEWPORT
    viewport_set_position: VIEWPORT_SET_POSITON
    viewport_set_size: VIEWPORT_SET_SIZE
    buffer: BUFFER
    buffer_set_data: BUFFER_SET_DATA
    pixels: PIXELS
    transform: TRANSFORM
    transform_bind: TRANSFORM_BIND
    transform_set_base: TRANSFORM_SET_BASE
    transform_set_left: TRANSFORM_SET_LEFT
    transform_set_right: TRANSFORM_SET_RIGHT
    def __init__(self, canvas: _Optional[_Union[CANVAS, _Mapping]] = ..., canvas_set_size: _Optional[_Union[CANVAST_SET_SIZE, _Mapping]] = ..., canvas_set_dpi: _Optional[_Union[CANVAST_SET_DPI, _Mapping]] = ..., viewport: _Optional[_Union[VIEWPORT, _Mapping]] = ..., viewport_set_position: _Optional[_Union[VIEWPORT_SET_POSITON, _Mapping]] = ..., viewport_set_size: _Optional[_Union[VIEWPORT_SET_SIZE, _Mapping]] = ..., buffer: _Optional[_Union[BUFFER, _Mapping]] = ..., buffer_set_data: _Optional[_Union[BUFFER_SET_DATA, _Mapping]] = ..., pixels: _Optional[_Union[PIXELS, _Mapping]] = ..., transform: _Optional[_Union[TRANSFORM, _Mapping]] = ..., transform_bind: _Optional[_Union[TRANSFORM_BIND, _Mapping]] = ..., transform_set_base: _Optional[_Union[TRANSFORM_SET_BASE, _Mapping]] = ..., transform_set_left: _Optional[_Union[TRANSFORM_SET_LEFT, _Mapping]] = ..., transform_set_right: _Optional[_Union[TRANSFORM_SET_RIGHT, _Mapping]] = ...) -> None: ...

class POSITIONS(_message.Message):
    __slots__ = ()
    POSITIONS_BUFFER_FIELD_NUMBER: _ClassVar[int]
    POSITIONS_TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    POSITIONS_LIST_FIELD_NUMBER: _ClassVar[int]
    positions_buffer: BUFFER
    positions_transform: TRANSFORM
    positions_list: NESTED_LIST
    def __init__(self, positions_buffer: _Optional[_Union[BUFFER, _Mapping]] = ..., positions_transform: _Optional[_Union[TRANSFORM, _Mapping]] = ..., positions_list: _Optional[_Union[NESTED_LIST, _Mapping]] = ...) -> None: ...

class COLOR(_message.Message):
    __slots__ = ()
    RGBA_FIELD_NUMBER: _ClassVar[int]
    rgba: bytes
    def __init__(self, rgba: _Optional[bytes] = ...) -> None: ...

class COLORS(_message.Message):
    __slots__ = ()
    COLORS_SINGLE_FIELD_NUMBER: _ClassVar[int]
    COLORS_BUFFER_FIELD_NUMBER: _ClassVar[int]
    COLORS_TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    colors_single: COLOR
    colors_buffer: BUFFER
    colors_transform: TRANSFORM
    def __init__(self, colors_single: _Optional[_Union[COLOR, _Mapping]] = ..., colors_buffer: _Optional[_Union[BUFFER, _Mapping]] = ..., colors_transform: _Optional[_Union[TRANSFORM, _Mapping]] = ...) -> None: ...

class LIST(_message.Message):
    __slots__ = ()
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, values: _Optional[_Iterable[int]] = ...) -> None: ...

class NESTED_LIST(_message.Message):
    __slots__ = ()
    LISTS_FIELD_NUMBER: _ClassVar[int]
    lists: _containers.RepeatedCompositeFieldContainer[LIST]
    def __init__(self, lists: _Optional[_Iterable[_Union[LIST, _Mapping]]] = ...) -> None: ...

class GROUPS(_message.Message):
    __slots__ = ()
    GROUPS_SIZE_FIELD_NUMBER: _ClassVar[int]
    GROUP_SIZES_FIELD_NUMBER: _ClassVar[int]
    GROUP_INDICES_FIELD_NUMBER: _ClassVar[int]
    groups_size: int
    group_sizes: LIST
    group_indices: NESTED_LIST
    def __init__(self, groups_size: _Optional[int] = ..., group_sizes: _Optional[_Union[LIST, _Mapping]] = ..., group_indices: _Optional[_Union[NESTED_LIST, _Mapping]] = ...) -> None: ...

class BUFFER(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: int
    count: int
    type: BufferType
    def __init__(self, id: _Optional[int] = ..., count: _Optional[int] = ..., type: _Optional[_Union[BufferType, str]] = ...) -> None: ...

class BUFFER_SET_DATA(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    id: int
    offset: int
    data: bytes
    def __init__(self, id: _Optional[int] = ..., offset: _Optional[int] = ..., data: _Optional[bytes] = ...) -> None: ...

class CANVAS(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    DPI_FIELD_NUMBER: _ClassVar[int]
    VIEWPORTS_FIELD_NUMBER: _ClassVar[int]
    id: int
    width: int
    height: int
    dpi: float
    viewports: _containers.RepeatedCompositeFieldContainer[VIEWPORT]
    def __init__(self, id: _Optional[int] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., dpi: _Optional[float] = ..., viewports: _Optional[_Iterable[_Union[VIEWPORT, _Mapping]]] = ...) -> None: ...

class CANVAST_SET_SIZE(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    CANVAS_ID_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    id: int
    canvas_id: int
    width: int
    height: int
    def __init__(self, id: _Optional[int] = ..., canvas_id: _Optional[int] = ..., width: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...

class CANVAST_SET_DPI(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    CANVAS_ID_FIELD_NUMBER: _ClassVar[int]
    DPI_FIELD_NUMBER: _ClassVar[int]
    id: int
    canvas_id: int
    dpi: float
    def __init__(self, id: _Optional[int] = ..., canvas_id: _Optional[int] = ..., dpi: _Optional[float] = ...) -> None: ...

class VIEWPORT(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    CANVAS_ID_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    id: int
    canvas_id: int
    x: int
    y: int
    width: int
    height: int
    def __init__(self, id: _Optional[int] = ..., canvas_id: _Optional[int] = ..., x: _Optional[int] = ..., y: _Optional[int] = ..., width: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...

class VIEWPORT_SET_POSITON(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    VIEWPORT_ID_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    id: int
    viewport_id: int
    x: int
    y: int
    def __init__(self, id: _Optional[int] = ..., viewport_id: _Optional[int] = ..., x: _Optional[int] = ..., y: _Optional[int] = ...) -> None: ...

class VIEWPORT_SET_SIZE(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    VIEWPORT_ID_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    id: int
    viewport_id: int
    width: int
    height: int
    def __init__(self, id: _Optional[int] = ..., viewport_id: _Optional[int] = ..., width: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...

class VISUAL(_message.Message):
    __slots__ = ()
    PIXELS_FIELD_NUMBER: _ClassVar[int]
    pixels: PIXELS
    def __init__(self, pixels: _Optional[_Union[PIXELS, _Mapping]] = ...) -> None: ...

class PIXELS(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITIONS_FIELD_NUMBER: _ClassVar[int]
    COLORS_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    id: int
    positions: POSITIONS
    colors: COLORS
    groups: GROUPS
    def __init__(self, id: _Optional[int] = ..., positions: _Optional[_Union[POSITIONS, _Mapping]] = ..., colors: _Optional[_Union[COLORS, _Mapping]] = ..., groups: _Optional[_Union[GROUPS, _Mapping]] = ...) -> None: ...

class TRANSFORM(_message.Message):
    __slots__ = ()
    COLORMAP_FIELD_NUMBER: _ClassVar[int]
    ACCESSOR_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    MEASURE_FIELD_NUMBER: _ClassVar[int]
    colormap: TRANSFORM_COLORMAP
    accessor: TRANSFORM_ACCESSOR
    operator: TRANSFORM_OPERATOR
    measure: TRANSFORM_MEASURE
    def __init__(self, colormap: _Optional[_Union[TRANSFORM_COLORMAP, _Mapping]] = ..., accessor: _Optional[_Union[TRANSFORM_ACCESSOR, _Mapping]] = ..., operator: _Optional[_Union[TRANSFORM_OPERATOR, _Mapping]] = ..., measure: _Optional[_Union[TRANSFORM_MEASURE, _Mapping]] = ...) -> None: ...

class TRANSFORM_BIND(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    BUFFER_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    buffer_id: int
    def __init__(self, id: _Optional[int] = ..., buffer_id: _Optional[int] = ...) -> None: ...

class TRANSFORM_SET_BASE(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    transform_id: int
    def __init__(self, id: _Optional[int] = ..., transform_id: _Optional[int] = ...) -> None: ...

class TRANSFORM_SET_LEFT(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    RIGHT_BUFFER_FIELD_NUMBER: _ClassVar[int]
    RIGHT_TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    id: int
    right_buffer: int
    right_transform: int
    def __init__(self, id: _Optional[int] = ..., right_buffer: _Optional[int] = ..., right_transform: _Optional[int] = ...) -> None: ...

class TRANSFORM_SET_RIGHT(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    RIGHT_BUFFER_FIELD_NUMBER: _ClassVar[int]
    RIGHT_TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    id: int
    right_buffer: int
    right_transform: int
    def __init__(self, id: _Optional[int] = ..., right_buffer: _Optional[int] = ..., right_transform: _Optional[int] = ...) -> None: ...

class TRANSFORM_COLORMAP(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VMIN_FIELD_NUMBER: _ClassVar[int]
    VMAX_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    vmin: float
    vmax: float
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., vmin: _Optional[float] = ..., vmax: _Optional[float] = ...) -> None: ...

class TRANSFORM_ACCESSOR(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    W_FIELD_NUMBER: _ClassVar[int]
    id: int
    x: float
    y: float
    z: float
    w: float
    def __init__(self, id: _Optional[int] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ..., w: _Optional[float] = ...) -> None: ...

class TRANSFORM_OPERATOR(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    ADD_FIELD_NUMBER: _ClassVar[int]
    SUBTRACT_FIELD_NUMBER: _ClassVar[int]
    MULTIPLY_FIELD_NUMBER: _ClassVar[int]
    DIVIDE_FIELD_NUMBER: _ClassVar[int]
    id: int
    add: int
    subtract: int
    multiply: int
    divide: int
    def __init__(self, id: _Optional[int] = ..., add: _Optional[int] = ..., subtract: _Optional[int] = ..., multiply: _Optional[int] = ..., divide: _Optional[int] = ...) -> None: ...

class TRANSFORM_MEASURE(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    PIXEL_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    INCH_FIELD_NUMBER: _ClassVar[int]
    CM_FIELD_NUMBER: _ClassVar[int]
    id: int
    pixel: int
    point: int
    inch: int
    cm: int
    def __init__(self, id: _Optional[int] = ..., pixel: _Optional[int] = ..., point: _Optional[int] = ..., inch: _Optional[int] = ..., cm: _Optional[int] = ...) -> None: ...

class RENDER(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    CANVAS_ID_FIELD_NUMBER: _ClassVar[int]
    VIEWPORT_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    REQUEST_DATA_FIELD_NUMBER: _ClassVar[int]
    TARGET_BUFFER_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    canvas_id: int
    viewport_id: int
    output: OutputType
    format: OutputFormat
    request_data: bool
    target_buffer_id: int
    def __init__(self, id: _Optional[int] = ..., canvas_id: _Optional[int] = ..., viewport_id: _Optional[int] = ..., output: _Optional[_Union[OutputType, str]] = ..., format: _Optional[_Union[OutputFormat, str]] = ..., request_data: _Optional[bool] = ..., target_buffer_id: _Optional[int] = ...) -> None: ...
