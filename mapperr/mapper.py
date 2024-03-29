import warnings
from typing import MutableSet, Union
from mapperr.util import MappingDirection, NOT_ALLOWED_BUILTINS


class _Mapper:
    def __init__(self, direction: MappingDirection) -> None:
        self.__all_classes: MutableSet[type] = set()
        self.__direction: MappingDirection = direction

    def __read(self, src: Union[dict, object], key: str):
        value = None
        if self.__direction == MappingDirection.DICT_TO_OBJECT:
            value = src.get(key)
        else:
            value = getattr(src, key, None)
        return value

    def __write(self, dst: Union[dict, object], key: str, value: object):
        if self.__direction == MappingDirection.DICT_TO_OBJECT:
            dst.__setattr__(key, value)
        else:
            dst.update({key: value})

    def __add_class(self, class_definition: Union[str, type, object]) -> type:
        local_classs_definition = class_definition
        if isinstance(class_definition, str):
            local_classs_definition = None
            for a_class in self.__all_classes:
                if a_class.__name__ == class_definition:
                    local_classs_definition = a_class
                    break
            if local_classs_definition is None:
                warnings.warn(f"Class {class_definition} not found")
                local_classs_definition = object
        elif class_definition.__module__ not in ["typing", "builtins"]:
            self.__all_classes.add(class_definition)
        return local_classs_definition

    def __get_all_annotations(self, class_definition: type) -> dict:
        classes = [class_definition]
        while classes[0].__name__ != "object":
            self.__add_class(classes[0].__base__)
            classes.insert(0, classes[0].__base__)
        del classes[0]

        annotations = {}
        for a_class in classes:
            annotations.update(a_class.__annotations__)

        return annotations

    @staticmethod
    def __process_builtin_instance(src: object, blueprint: type):
        if blueprint.__name__ in NOT_ALLOWED_BUILTINS:
            return None

        new_src = None
        if isinstance(src, int) and blueprint == float:
            new_src = float(src)
        elif isinstance(src, blueprint):
            new_src = src

        return new_src

    def map(self, src: Union[dict, object, None], blueprint: type):
        self.__add_class(blueprint)
        mapped_item = None
        if src is None:
            mapped_item = None
        elif blueprint.__module__ == "builtins":
            mapped_item = _Mapper.__process_builtin_instance(src, blueprint)
            if mapped_item == None:
                warnings.warn(
                    f"Type {blueprint.__name__} not allowed OR value {type(src).__name__} not matched with type"
                )
        elif blueprint.__module__ == "typing":
            if blueprint.__name__ == "List" and isinstance(src, list):
                mapped_item = []
                for list_element in src:
                    mapped_item.append(self.map(list_element, blueprint.__args__[0]))
            elif blueprint.__name__ == "Dict" and isinstance(src, dict):
                mapped_item = {}
                for key, value in src.items():
                    mapped_item[self.map(key, blueprint.__args__[0])] = self.map(
                        value, blueprint.__args__[1]
                    )
            else:
                warnings.warn(
                    f"Type {blueprint.__name__} not allowed OR value {type(src).__name__} not matched with type"
                )
        else:
            mapped_item = (
                blueprint()
                if self.__direction == MappingDirection.DICT_TO_OBJECT
                else {}
            )

            annotations = self.__get_all_annotations(blueprint)

            for key, type_ in annotations.items():
                value = self.__read(src, key)
                class_def = self.__add_class(type_)
                self.__write(mapped_item, key, self.map(value, class_def))
        return mapped_item
