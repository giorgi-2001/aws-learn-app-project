from pathlib import Path
from fastapi.templating import Jinja2Templates

TEMPLATE_DIR = Path(__file__).parent.joinpath("templates").resolve()

templates = Jinja2Templates(directory=TEMPLATE_DIR)