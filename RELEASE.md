# Release checklist

0. Spell check:

```bash
export PATH="$HOME/.cargo/bin:$PATH"
~/.cargo/bin/typos docs/source \
  --exclude docs/source/_build \
  --exclude docs/source/_static
```

1. Start clean:

```bash
cd $HOME/projects/sphinx-tabular
git status --short
```

Does not include:

    docs/_build/
    dist/
    build/
    src/*.egg-info/
    .venv/
    bin/
    lib/
    lib64
    pyvenv.cfg
    node_modules/


2. Update version in `pyproject.toml` and `src/__init__.py`.

    version = "0.1.9"

Find and replace all instances of version with the new version.

3. Create a clean local environment

```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev,docs]"
```

4. Run tests

```bash
python -m pytest
```

5. Build docs

```bash
rm -rf docs/_build
sphinx-build -b html -W --keep-going docs/source docs/_build/html
```


6. Build and check package

```bash
rm -rf dist build src/*.egg-info
python -m build
python -m twine check dist/*
```


7. Test the built wheel locally

```bash
python -m venv /tmp/sphinx-tabular-wheel-test
source /tmp/sphinx-tabular-wheel-test/bin/activate

python -m pip install --upgrade pip
python -m pip install "$HOME/projects/sphinx-tabular"/dist/*.whl

python - <<'PY'
import sphinx_tabular
print(sphinx_tabular.__file__)
PY

deactivate
cd $HOME/projects/sphinx-tabular
source .venv/bin/activate
```


8. Check Git status again

```bash
git status --short
```

Remove build outputs to be safe: 

```bash
rm -rf docs/_build dist build src/*.egg-info
```

9. Commit release changes

```bash
git add pyproject.toml LICENSE .gitignore .github/workflows docs/source tests README.md RELEASE.md
git commit -m "Release 0.1.9"
git push
```

If some paths did not change, Git will ignore them.

10. Create and push the release tag

```bash
git tag v0.1.9
git push origin v0.1.9
```


11. Publish the GitHub release

    GitHub → Releases → Draft a new release → Choose tag v0.1.9 → Publish release

Publishing the GitHub release triggers .github/workflows/publish.yml.

12. Confirm PyPI publish

After the publish workflow succeeds, test from PyPI in a fresh environment:

```bash
python3 -m venv /tmp/sphinx-tabular-pypi-test
source /tmp/sphinx-tabular-pypi-test/bin/activate

python -m pip install --upgrade pip
python -m pip install sphinx-tabular==0.1.9

python - <<'PY'
import sphinx_tabular
print(sphinx_tabular.__file__)
PY
```


