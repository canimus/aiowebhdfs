import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiowebhdfs", # Replace with your own username
    version="0.0.2",
    author="Herminio Vazquez",
    author_email="canimus@gmail.com",
    description="A modern and asynchronous web client for WebHDFS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/canimus/aiowebhdfs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Session",
        "Topic :: System :: Distributed Computing",
        "Topic :: System :: Filesystems",
        "Development Status :: 3 - Alpha"
    ],
    install_requires=[
          'aiofiles==0.4.0',
          'aiohttp==3.6.2',
          'asyncio==3.4.3',
          'opnieuw==0.0.3',
          'httpx==0.11.1',
          'furl==2.1.0',
      ],
    python_requires='>=3.6',
)