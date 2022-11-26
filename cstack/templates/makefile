##
# {{ project_name }}
#
# @file
# @version 0.1

install:
  python -m venv .venv
  source ./.venv/bin/activate
  pip install -r requirements.txt
  deactivate

dev:
  source ./.venv/bin/activate
  uvicorn run "cstack:{{project_name|lower}}" --reload & npm run build --watch
  deactivate

# end
