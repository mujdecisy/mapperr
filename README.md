# **mapperr - mapping across dictionary and class object, recursively**

If you are using python for implementing protocols, cache management, nosql or sql database manupilation with  the object oriented concepts in your code, mapperr can handle your object in your way, easily.

## Installation
`via pip`
```shell
pip3 install mapperr
```
`via direct setup`
```shell
pip3 install setuptools
python3 setup.py sdist bdist_wheel
pip3 install dist/mapperr-0.0.1-py3-none-any.whl
```

## Usage
Your classes' attributes are needed to be annotated with their types like `int`, `str`, `Book`, `List[Book]`. Parameterized constructors are not suitable, you can use it with plain objects which has most trash work. You can also fill your required options with param `op_required` as string list.

**`to_obj( dict_data: dict, destination_class: Type ) -> object`**

**`to_dict( obj: object ) -> dict`**


```python
from typing import List
from pprint import pprint
from mapperr import to_dict, to_obj

class Book:
    _id: int
    title: str
    op_required: list = ['_id', 'title']

class BookShelf:
    code: str
    books: List[Book]

class Library:
    name: str
    book_shelfs: List[BookShelf]


def retrieve_library_from_the_source() -> dict:
    return {
        "name" : "Hogwarts Library",
        "book_shelfs" : [
            {
                "code" : "A1",
                "books" : [
                    {
                    "_id" : 0,
                    "title" : "Defence Against the Dark Arts"
                    },
                    {
                    "_id" : 1,
                    "title" : "Potions"
                    },
                ]
            },
            {
                "code" : "A2",
                "books" : [
                    {
                    "_id" : 3,
                    "title" : "Charms"
                    },
                    {
                    "_id" : 4,
                    "title" : "Herbology"
                    },
                ]
            }
        ]
    }

def send_library_to_the_source(data: dict):
    pprint(data)


lib: Library = to_obj(retrieve_library_from_the_source(), Library)

new_book = Book()
new_book._id = 5
new_book.title = "Alchemy"

lib.book_shelfs[0].books.append(new_book)

send_library_to_the_source( to_dict(lib) )
```