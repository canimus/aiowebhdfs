import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiowebhdfs", # Replace with your own username
    version="0.0.1",
    author="Herminio Vazquez",
    author_email="canimus@gmail.com",
    description="An modern asynchronous web client for WebHDFS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/canimus/aiowebhdfs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Text Processing",
        "Topic :: Utilities"
    ],
    install_requires=[
          'aiofiles==0.4.0',
          'aiohttp==3.6.2',
          'asyncio==3.4.3',
          'opnieuw==0.0.3',
          'httpx==0.11.1'
      ],
    python_requires='>=3.6',
)