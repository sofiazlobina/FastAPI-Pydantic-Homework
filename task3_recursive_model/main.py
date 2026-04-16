from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
import json


class Node(BaseModel):
    data: str
    child: Optional["Node"] = None


Node.model_rebuild()


# пример входных данных
example_data = {
    "data": "root",
    "child": {
        "data": "level1",
        "child": {
            "data": "level2",
            "child": {
                "data": "level3"
            }
        }
    }
}


def main():
    try:
        node = Node(**example_data)

        print("Объект успешно создан:")
        print(node)

        print("\nСериализация в JSON:")
        print(json.dumps(node.model_dump(), indent=4, ensure_ascii=False))

    except Exception as e:
        print("Ошибка:")
        print(e)


if __name__ == "__main__":
    main()