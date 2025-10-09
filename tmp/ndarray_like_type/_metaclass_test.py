class ExampleMeta(type):
    def __new__(cls, name, bases, dct):
        print(f"Creating class {name} with ExampleMeta")
        dct["added_attribute"] = "I was added by the metaclass"
        return super().__new__(cls, name, bases, dct)


class MyClass(metaclass=ExampleMeta):
    def __init__(self):
        print(f"Initializing MyClass with value")
        # self.value = value


def bar():
    print(MyClass)  # Output: MyClass
    print(MyClass)  # Output: MyClass


# print(MyClass.added_attribute)  # Output: I was added by the metaclass


def foo():
    print(MyClass)  # Output: MyClass
    print(MyClass)  # Output: MyClass


# print(MyClass.added_attribute)  # Output: I was added by the metaclass

foo()
print("---")
bar()
