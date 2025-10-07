from .transform_link_base import TransformLinkBase

class TransformLinkDB():
    _database: dict[str, type['TransformLinkBase']] = {}
    """
    A registry for transformation classes.
    Maps class names to transformation class types.
    """

    @staticmethod
    def add_link(class_name: str, transform_class: type['TransformLinkBase']) -> None:
        """
        Register a transformation class with a name.
        """
        TransformLinkDB._database[class_name] = transform_class

    @staticmethod
    def get_link(class_name: str) -> type['TransformLinkBase']:
        """
        Retrieve a transformation class by name.
        """
        if class_name not in TransformLinkDB._database:
            raise ValueError(f"Transform '{class_name}' not found in the database.")
        return TransformLinkDB._database[class_name]