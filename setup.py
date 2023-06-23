import setuptools

setuptools.setup(
    name="your-app-name",
    version="1.0",
    packages=setuptools.find_packages(),
    install_requires=[
        "streamlit",
        # Add other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "your-app-name = your_module_name:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)