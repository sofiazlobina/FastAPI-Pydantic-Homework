from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
import json


class Node(BaseModel):
    data: str
    child: Optional["Node"] = None


Node.model_rebuild()


# тестовые данные (произвольная вложенность)
example_data = {
    "data": "root",
    "child": {
        "data": "level1",
        "child": {
            "data": "level2",
            "child": {
                "data": "level3",
                "child": {
                    "data": "level4"
                }
            }
        }
    }
}


def main():
    try:
        node = Node(**example_data)

        print("Объект создан успешно:\n")
        print(node)

        print("\JSON (serialize):\n")
        print(json.dumps(node.model_dump(), indent=4, ensure_ascii=False))

    except Exception as e:
        print("Ошибка:")
        print(e)


if __name__ == "__main__":
    main()