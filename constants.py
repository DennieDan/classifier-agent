"""
Compatibility wrapper.

Some modules in this repo import from `constants` (top-level), while others use
`app.constants`. Render runs from the repo root, so this ensures both work.
"""

from app.constants import *  # noqa: F401,F403

