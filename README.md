# 🐍 Cstack - Python made Easy
An Opinionated Full Stack Framework for Web Development. Built on Python, Vite, and Vue. 

This stack can be used to create a fullstack application that can be deployed on Deta, or another python hosting.
It includes:
- Monadic Error Handling
- ORM
- Testing Library
- CLI Generator
- Type Safety

## Project Structure
```
app/
 | api/                  -- Python Project
    | app.py             -- API Entrypoint
    | models/            -- Database ORM Models
    | config/            -- Pydantic Configuration
       | db.py           -- Database Configuration
       | env.py          -- Environment Variables
       | settings.py     -- Application Settings
    | features/          -- Feature Libraries
    | shared/            -- Shared Code
    | tests/             -- Pytest Tests
 | view/                 -- Vue Project
 __init__.py             -- Application File
.env                     -- Env File
cstack                   -- CLI Tool
pyproject.toml           -- Poetry File
```


### Features

This is the lifeblood of a Cstack project.
Cstack is feature-driven, rather than layered.
The reason is feature code is co-located, rather than spread across directories.
A feature includes:
- `__init__.py`
- `router.py`
- `services/`
- `repositories/`
- `repositories/mocks/`
- `DTOs/`

#### `router.py`

This is the fastapi router.
All endpoints for this function should be defined here.

#### `services/`

This is collection of services.
These services can be defined as a either a class or as a collection of functions.
They should be pure operations, and contain most of the business logic.
The reason for purity is testability and portability.
If for a reason you move away from Cstack, the code is easily usable again.
It also means that the feature logic could be shared if needed.

A service can be generated as well, these are injected into routes through FastAPI's dependency injection.
A service includes:
- `{{service_name}}.py`
- `test_{{service_name}}.py`

#### `repositories/`

A repository communicates with the database. The reason for both repositories and an ORM is it allows the business logic
to be completely decoupled from the database pattern. This is also means the services are easily testable.
A repository includes:
- `{{repository_name}}.py`
- `mocks/{{repository_name}}.py`

The mocks folder contains dummy implementations of the repo, for use in testing.

#### `DTOs/`

This a collection of Pydantic Objects.
These are used for communicating data for the given feature.

> ORM Models ARE NOT DTOs. Use a Pydantic Model. Leave ORM code in the Repositories.

### `config/db.py`

All the database setup code is contained here.
It is exposed to the user if the need arises to modify it.
All models should import the declared Database base.

### `config/settings.py`

This includes versioning info, as well as other global settings used in the project.
This is instantiated as a singleton, and should only be used through that singleton.

### `config/env.py`

This is influenced by T3-stack's env folder, where they define a runtime schema for Environment Variables.
These variables are defined here, and parsed through Pydantic.
This is instantiated as a singleton and should only be used through that singleton.