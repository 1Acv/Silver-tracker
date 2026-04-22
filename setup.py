from setuptools import setup, find_packages

setup(
    name="silver-tracker",
    version="1.1.0",
    description="Precious metals & junk silver coin value tracker for antique hunters",
    author="Your Name",
    python_requires=">=3.8",
    install_requires=[
        "ttkbootstrap>=1.10.0",
        "cloudscraper>=1.2.71",
        "beautifulsoup4>=4.12.0",
    ],
    py_modules=["silver_tracker"],
    entry_points={
        "console_scripts": [
            "silver-tracker=silver_tracker:main",
        ],
        "gui_scripts": [
            "silver-tracker-gui=silver_tracker:main",
        ],
    },
)
