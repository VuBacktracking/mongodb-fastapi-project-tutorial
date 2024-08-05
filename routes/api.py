import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import APIRouter
from endpoints import users, books, addresses  # Make sure these are correctly imported

router = APIRouter()
router.include_router(books.router)
router.include_router(users.router)
router.include_router(addresses.router)