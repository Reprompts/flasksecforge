# setup.py
import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent.resolve()
# Read the long description from README
README = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="flasksecforge",
    version="0.1.1",
    author="RePromptsQuest",
    author_email="repromptsquest@gmail.com",
    description="Scaffold a Flask‑secure boilerplate API.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/reprompts/flasksecforge",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    package_data={
        # include all files under flasksecforge/templates
        "flasksecforge": ["templates/flask_api_boilerplate/**/*"],
    },
    install_requires=[
        "click",
        "Flask>=2.0",
        "Flask-Migrate>=3.1",
        "Flask-JWT-Extended>=4.4",
        "Flask-Cors>=3.0",
        "Flask-SQLAlchemy>=2.5",
        "python-dotenv>=0.19.0",
        "marshmallow>=3.0",
        "marshmallow-sqlalchemy>=0.23.0",
        "gunicorn>=20.0",
    ],
    entry_points={
        "console_scripts": [
            "flasksecforge = flasksecforge.cli:main",
        ],
    },
    python_requires=">=3.6",
)
