from distutils.core import setup
setup(
    name = "catcam",
    packages = ['catcam'],
    version = "0.1",
    description = "Render video streams in terminal",
    author = "Murad Salahi",
    install_requires = [
        "Pillow>=2.6.1",
        "numpy==1.9.1",
        "requests==2.4.3",
        "scikit-learn==0.15.2",
        "scipy==0.14.0"]
)
