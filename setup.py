from setuptools import setup

setup(
    name='chrome_control',
    version='0.1.4',
    install_requires=[
        'requests',
        'pyautogui'
    ],
    package_data={'': ['*.js']}
)
