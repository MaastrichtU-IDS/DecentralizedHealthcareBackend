## Introduction

This guide provides instructions on how to generate and update the documentation for LUCE. We use Sphinx for documentation due to its compatibility with Python and Djando, and its ease of generating readable and organized HTML documentation.

## prerequisites

Before proceeding, ensure you have the following installed:

- Python
- Django
- Sphinx (Install via pip install sphinx)

## Initial Setup

1. Clone the Repository:

   Ensure you have the latest version of the codebase.

   ```
   git clone https://github.com/MaastrichtU-IDS/DecentralizedHealthcareBackend.git
   cd DecentralizedHealthcareBackend
   ```

2. Install Sphinx (if not already installed):

   ```
   pip install sphinx
   ```

3. Set Up Sphinx Directory:

   ```
   sphinx-quickstart docs
   ```

   This will create a docs directory with basic configuration files.

4. Configure Sphinx:

   - Edit the `conf.py` file in the `docs/source` directory. Set the `sys.path` to include Django project's root directory, so Sphinx can find the modules
   - Set Django settings modules in `conf.py`:

   ```
   import os
   import sys
   import django

   sys.path.insert(0, os.path.abspath('../../luce_vm/luce_django/luce'))

   os.environ['DJANGO_SETTINGS_MODULE'] = 'lucehome.settings'
   django.setup()
   ```

5. Create Documentation with Autodoc:

   Sphinx can automatically generate documentation from your docstrings using the autodoc extension. Enable this in your `conf.py`:

   ```
   extensions = ['sphinx.ext.autodoc']
   ```

6. add `modules` in `index.rst`:

   ```
   ================================

   .. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

   Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`
   ```

## Generating Documentation

1. Automatic .rst File Generation

   Use `sphinx-apidoc` to automatically generate `.rst` files from the codebase. Check `sphinx-apidoc --help` for more information

   ```
   # Adjust paths as necessary
   sphinx-apidoc -o ./source ../luce_vm/luce_django/luce/ ../**/migrations/* ../**/tests/* ../**/utils/* ../**/lucehome/* ../**/manage.py
   ```

2. Build the Documentation

   Generate the Documentation

   ```
   make html
   ```
