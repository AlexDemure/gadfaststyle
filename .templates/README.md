## Описание

`.templates` хранит `.toml`-шаблоны для разворачивания структуры проекта.

## Правила

- Основной шаблон проекта хранится в `project.toml`.
- Каждый шаблон задает `workdir`, `folders`, `exclude`, `files` и при необходимости `scripts`.
- `folders` описывает директории относительно `workdir`.
- `exclude` описывает пути, где не нужно автоматически создавать `__init__.py` и другие package-файлы.
- `[[files]]` описывает файлы, их режим записи и содержимое.
- `[[scripts]]` описывает команды, которые выполняются после генерации.

## Примеры

```toml
workdir = "myproject"

folders = ["src", "src/static", "tests"]
exclude = ["src/static"]

[[files]]
path = "src/__init__.py"
mode = "w"
content = ""

[[scripts]]
command = "isort {{workdir}}"
check = true
```
