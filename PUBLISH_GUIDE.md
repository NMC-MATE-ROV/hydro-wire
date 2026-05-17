# Publishing rov-interface to PyPI

This guide explains how to publish the rov-interface package to PyPI (Python Package Index).

## Prerequisites

1. **PyPI Account**: Create at https://pypi.org/account/register/
2. **API Token**: Generate at https://pypi.org/manage/account/tokens/
3. **Build Tools**: `pip install build twine`

## Step-by-Step Publication

### 1. Verify Package Configuration

Ensure `pyproject.toml` is complete:

```bash
cd /home/jc/projects/rov-interface
cat pyproject.toml
```

Check that it has:
- ✅ `name = "rov-interface"`
- ✅ `version = "0.0.1"` (update as needed)
- ✅ `description`
- ✅ `readme = "README.md"`
- ✅ `license`
- ✅ `authors`
- ✅ `classifiers`

### 2. Run Tests

```bash
pytest tests/ -v
```

Make sure all tests pass!

### 3. Build the Package

```bash
python -m build
```

This creates:
- `dist/rov_interface-0.0.1.tar.gz` (source)
- `dist/rov_interface-0.0.1-py3-none-any.whl` (wheel)

### 4. Check Package

```bash
twine check dist/*
```

Look for any warnings or errors.

### 5. Test on TestPyPI (Recommended)

First, test on the test server before publishing to the real PyPI.

Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    testpypi
    pypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi_test_your_token_here

[pypi]
username = __token__
password = pypi_your_token_here
```

Upload to TestPyPI:

```bash
twine upload --repository testpypi dist/*
```

Test installation:

```bash
pip install --index-url https://test.pypi.org/simple/ rov-interface==0.0.1
```

### 6. Publish to Production PyPI

```bash
twine upload dist/*
```

Or with explicit authentication:

```bash
twine upload dist/* -u __token__ -p pypi_your_token_here
```

### 7. Verify Publication

Visit: https://pypi.org/project/rov-interface/

Package is now installable worldwide:

```bash
pip install rov-interface
```

## Updating Versions

For version 0.0.2:

```bash
# Update version in pyproject.toml
version = "0.0.2"

# Rebuild
rm -rf dist/ build/ *.egg-info/
python -m build

# Publish
twine upload dist/*
```

## Semantic Versioning

Follow [semver.org](https://semver.org/):

- `0.0.1` → Initial alpha release
- `0.1.0` → Beta with features
- `1.0.0` → First stable release
- `1.0.1` → Patch fix
- `1.1.0` → Minor feature
- `2.0.0` → Major breaking change

## Automated Publishing with GitHub Actions

The `.github/workflows/publish.yml` automatically:
- Runs tests on every push
- Publishes to PyPI when you create a tagged release

### Setup Automated Publishing

1. **Generate PyPI API Token**: https://pypi.org/manage/account/tokens/

2. **Add to GitHub Secrets**:
   - Go to Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Your PyPI token

3. **Create Release**:
   ```bash
   git tag v0.0.1
   git push origin v0.0.1
   ```
   
   GitHub automatically publishes to PyPI!

## Troubleshooting

### "403 Forbidden" Error

- Check API token is correct
- Verify package name spelling
- Ensure you own the package name

### "Filename already exists"

- PyPI doesn't allow overwriting - increment version
- Delete build files: `rm -rf dist/ build/`

### Import errors after installation

- Ensure `rov_lib` package is found in `[tool.setuptools.packages]`
- Check `__init__.py` files exist in package directories

## File Checklist

Before publishing, ensure these files exist:

- ✅ `pyproject.toml` - Complete metadata
- ✅ `LICENSE` - License file
- ✅ `README.md` - Documentation
- ✅ `MANIFEST.in` - Include supplementary files
- ✅ `rov_lib/__init__.py` - Package init
- ✅ `rov_lib/client.py` - Main module
- ✅ `rov_lib/manager.py` - Manager module
- ✅ `rov_lib/py.typed` - Type hints marker

## Useful Commands

```bash
# Check what would be packaged
tar -tzf dist/rov_interface-*.tar.gz

# View package info
twine info dist/*

# Check for issues
twine check dist/*

# Upload with verbose output
twine upload dist/* -v
```

## After Publication

- Update README.md with installation instructions
- Create GitHub release notes
- Announce on social media (if public)
- Monitor for issues and feedback

## Support

For more help:
- PyPI Help: https://pypi.org/help/
- Twine Docs: https://twine.readthedocs.io/
- Python Packaging: https://packaging.python.org/

