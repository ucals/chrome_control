from setuptools import setup

setup(
    name='chrome_control',
    version='0.1.8',
    entry_points={
        'console_scripts': [
            'chrome-control = chrome_control:main',
            'ccc = chrome_control:main',
        ]
    },
    install_requires=[
        'requests',
        'pyautogui'
    ],
    package_data={'': ['*.js']}
)
