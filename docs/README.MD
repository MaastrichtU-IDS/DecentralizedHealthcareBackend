## Introduction

This guide provides instructions on how to generate and update the documentation for LUCE. We use Sphinx for documentation due to its compatibility with Python and Djando, and its ease of generating readable and organized HTML documentation.

## prerequisites

Before proceeding, ensure you have the following installed:

- Python
- Django
- Sphinx (Install via pip install sphinx)

## Initial Setup

1. **Clone the Repository:**
   Ensure you have the latest version of the codebase.

```
git clone https://github.com/MaastrichtU-IDS/DecentralizedHealthcareBackend.git

cd DecentralizedHealthcareBackend
```

2. Install Sphinx (if not already installed):

```
pip install sphinx
```

3. Navigate to the Documentation Directory:

```
cd docs
```

## Generating Documentation

Use `sphinx-apidoc` to automatically generate `.rst` files from the codebase.

```
# Adjust paths as necessary
sphinx-apidoc -o . ..
```
