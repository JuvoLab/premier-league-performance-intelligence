"""Shared locations; data can be isolated for reproducibility checks."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = Path(os.environ.get('PLPI_DATA_DIR', ROOT / 'data')).resolve()
SOURCE_COMMIT = '4b73468fc5b0f1950f9f66fada70ad3a4f9327cb'
