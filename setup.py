import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="booru-barrel", # Replace with your own username
    version="0.0.1",
    author="Dillon Dickerson",
    author_email="diltdicker@gmail.com",
    description="gui + cli for downloading images from image boards",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    extras_require = {
        'dev': [],
        'build': []
    },
    install_requires= [
        'Kivy==1.11.1',
        'pygame==1.9.6',
        'requests==2.23.0',
        'Pillow==7.1.2'
    ]
)