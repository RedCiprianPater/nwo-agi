# Publishing NWO-AGI to PyPI

## Prerequisites

1. **PyPI Account**: Create account at https://pypi.org
2. **API Token**: Generate at https://pypi.org/manage/account/token/
3. **TestPyPI Account** (optional): Create at https://test.pypi.org

## Manual Publishing Steps

### Step 1: Build the Package

```bash
# Make build script executable
chmod +x build_pypi.sh

# Run build
./build_pypi.sh
```

This will:
- Clean previous builds
- Install build dependencies
- Build source distribution (sdist)
- Build wheel distribution (bdist_wheel)
- Check package with twine

### Step 2: Test on TestPyPI (Recommended)

```bash
# Upload to TestPyPI first
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ nwo-agi
```

### Step 3: Publish to PyPI

```bash
# Upload to production PyPI
twine upload dist/*
```

You'll be prompted for:
- Username: `__token__`
- Password: Your PyPI API token

### Step 4: Verify

```bash
# Install from PyPI
pip install nwo-agi

# Check it's working
nwo-agi --help
```

## Automated Publishing with GitHub Actions

### Setup

1. Go to GitHub repo → Settings → Secrets → Actions
2. Add secret: `PYPI_API_TOKEN` = your PyPI token

### Usage

Simply push a version tag:

```bash
git tag v1.0.1
git push origin v1.0.1
```

GitHub Actions will automatically build and publish.

## Version Numbering

Follow semantic versioning:
- `MAJOR.MINOR.PATCH`
- Example: `1.0.0`, `1.0.1`, `1.1.0`, `2.0.0`

Update version in:
- `setup.cfg` (version = X.Y.Z)
- `nwo_agi/__init__.py` (__version__ = "X.Y.Z")

## Troubleshooting

### Package already exists
```
HTTPError: 400 Bad Request from https://upload.pypi.org/legacy/
File already exists.
```
**Fix**: Increment version number in setup.cfg

### Invalid API token
```
HTTPError: 403 Forbidden from https://upload.pypi.org/legacy/
Invalid or non-existent authentication information.
```
**Fix**: Use `__token__` as username, not your PyPI username

### Long description error
```
The description failed to render for 'text/x-rst'.
```
**Fix**: Ensure README.md is valid Markdown

## Post-Publication

After publishing:
1. ✅ Verify on https://pypi.org/project/nwo-agi/
2. ✅ Test installation: `pip install nwo-agi`
3. ✅ Update README with `pip install nwo-agi` (remove GitHub install)
4. ✅ Create GitHub release
5. ✅ Announce on social media
