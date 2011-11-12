from setuptools import setup

setup(name='pepper',
      version='0.1',
      classifiers = ["Development Status :: 4 - Beta",
                     "Intended Audience :: Developers",
                     "License :: OSI Approved :: BSD License",
                     "Programming Language :: Python :: 2.7"],
      description='Pepper is a source to source processor that reads python code and writes it back properly formatted whitespace-wise',
      author='Alon Horev',
      author_email='alon@horev.net',
      py_modules=['pepper'],
      license='BSD',
      url='https://github.com/alonho/pepper',
      entry_points={'console_scripts': ['pepper=pepper:main']})
