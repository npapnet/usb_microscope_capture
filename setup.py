import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = [
    'matplotlib',
    'scipy',
    'ipykernel',
    'numpy',
    'opencv',
]

test_requirements = [
    'pytest',
    # 'pytest-pep8',
    # 'pytest-cov',
]

setuptools.setup(
    name="usb_microscope_capture", 
    version="0.0.1",
    author="N. Papadakis",
    author_email="npapnet@gmail.com",
    description="A package for capturing images using a usb microscope",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/npapnet/image_partial_registration.py/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    tests_require=test_requirements,
    python_requires='>=3.8',
)