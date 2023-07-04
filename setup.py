from setuptools import setup

setup(
    name='chrome_control',
    version='0.1.1',
    package_dir={"": "chrome_control"},
    install_requires=[
        'requests',
        'pyautogui'
    ]
)
