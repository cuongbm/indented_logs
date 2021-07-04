import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="indented-logs",
    version="1.0.1",
    author="Cuong Bui",
    author_email="buiminhcuong@hotmail.com",
    description="Decorators to indent-log function calls with parameter and timing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cuongbm/indented_logs",
    project_urls={"Bug Tracker": "https://github.com/cuongbm/indented_logs/issues",},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
