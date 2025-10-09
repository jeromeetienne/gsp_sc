import typing


class MyTypeMeta(type):
    def __getitem__(cls, params):
        # Return a parameterized type object with the params stored
        return type(f"Parameterized{cls.__name__}", (cls,), {"_params": params, "__class_getitem__": classmethod(lambda cls, x: cls[x]), "__metaclass__": cls})

    def __instancecheck__(self, obj):
        # Custom logic for isinstance(obj, MyType[...])
        params = getattr(self, "_params", None)
        print(f"Checking {obj=} against MyType with params {params=}")
        # Example: accept any object, just for demonstration
        return True


class MyType(metaclass=MyTypeMeta):
    pass


# Example usage:
x = object()
print(isinstance(x, MyType["foo", 42]))  # Should print custom logic and return True
