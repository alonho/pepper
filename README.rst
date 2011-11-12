======
Pepper
======

Pepper was conceived while I was staring at ugly code, I wanted to make it more readable (conform with PEP8 and my brain).

Pepper is a source to source processor that reads python code and writes it back properly formatted whitespace-wise.

Pepper DOES NOT change anything other than whitespace so unless a bug is lurking somewhere it should never break the code or change it's behavior.

Pepper DOES NOT comply to PEP8 in several issues i had no will to solve like maximum length of a line (who uses a 80 chars terminal these days anyway..).

Pepper emits comments (not docstrings, only comments) due to lack of support from python's ast parser, I'll might solve that in a future version.

**For example output look at pepper.py, it was self-generated.**

Installation
============

::

    pip install pepper

Usage
=====

::

    usage: pepper.py [-h] [input] [output]

    Pepper.py parses python code and re-generates it with proper whitespace and
    formatting, as agreed on the holy PEP8.

    positional arguments:
      input       path to input file (default: /dev/stdin)
      output      path to output file (default: /dev/stdout)

    optional arguments:
      -h, --help  show this help message and exit

Whats next?
===========

Started working on coding conventions automatic refactoring, still unsure whether such a thing is usable.

