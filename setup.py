from setuptools import setup, find_packages

setup(
    name="PetPocket",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-login',
        'flask-migrate',
        'flask-mail',
        'gunicorn',
        'razorpay'
    ],
)