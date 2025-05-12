import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from PetPocket import create_app

app = create_app()