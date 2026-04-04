# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

Project overview
- Language/runtime: Python 3.10+
- Package name: sysyphus
- Purpose: Library to query and analyze meteorite data from the MetBull database via a preprocessed monthly dataset hosted on GitHub.
- Primary entrypoint for users: sysyphus.Boulder (high-level orchestration class)

Prerequisites
- macOS/Linux with Python 3.10+
- Internet connection required for most flows: Boulder() checks connectivity and loads a remote dataset from GitHub; tests instantiate Boulder and will fail offline.

Common commands
- Create and activate venv
```bash path=null start=null
python3.10 -m venv venv
source venv/bin/activate
```

- Install (dev) dependencies and the package in editable mode
```bash path=null start=null
pip install --upgrade pip
pip install -r dev-requirements.txt
pip install -e .
```

- Lint and format
```bash path=null start=null
flake8 .
black .
```

- Run all tests (pytest is configured via pytest.ini to add pythonpath)
```bash path=null start=null
pytest -q
```

- Run tests with coverage
```bash path=null start=null
pytest --cov=sysyphus --cov-report=term-missing
```

- Run a single test file or a specific test
```bash path=null start=null
# Single file
pytest tests/test_boulder.py -q
# Specific test by node id
pytest tests/test_boulder.py::TestBoulder::test_validate_selection -q
# Or via pattern
pytest -k validate_selection -q
```

- Build distributions (sdist and wheel)
```bash path=null start=null
python setup.py sdist bdist_wheel
```

- Publish to PyPI (requires credentials set via environment variables; do not echo secrets)
```bash path=null start=null
# Example: TWINE_USERNAME and TWINE_PASSWORD must be set in the environment
python -m twine upload dist/*
```

CI pipeline (GitHub Actions)
- Workflow: .github/workflows/ci.yml
- Triggers: push and pull_request on branch staging
- Jobs: ubuntu-latest; setup Python 3.10.11; pip install -r requirements.txt; run pytest

High-level architecture
- sysyphus/__init__.py
  - Exposes Boulder as the primary public API.

- Models
  - sysyphus/models/meteorite.py: Meteorite domain object encapsulating parsed properties from a MetBull detail page. Fetches HTML (requests + BeautifulSoup), extracts fields, converts coordinates and cleans numeric values. Provides get_properties(as_pd=False|True) for dict/DataFrame output.
  - sysyphus/models/boulder.py: Orchestrator. On init: checks internet, loads remote dataset (JSON or pickle) into a pandas DataFrame, normalizes dtypes. Provides:
    - make_search(verbose_results=True): interactive prompts to collect filters; calls search.* functions; stores selected_meteorites.
    - validate_selection(): optionally warns for large selections; constructs Meteorite objects via user_requests.make_meteorites.
    - request_metbull(rate_limiter=25): validates selection, then parallelizes Meteorite.extract_properties across the selection with a capped thread pool.
    - display_search(ommit=[], as_pandas=True): aggregates properties via rendering.show_properties, normalizes mass with preprocessing.handle_mass, returns DataFrame or dict.
    - dump_search(): clears selection and internal lists; resets made_requests.

- Scripts (functional modules)
  - sysyphus/scripts/remote_load.py:
    - check_internet_connection(): simple GET to confirm online status.
    - get_remote_data(as_pd=True, use_json=True): fetches preprocessed monthly dataset from GitHub (JSON by default, pickle optional) and returns a DataFrame.
  - sysyphus/scripts/search.py:
    - Input/validation helpers (get_prompt, validate_name, validate_numeric_range, validate_country, validate_mtype).
    - search_prompts(): orchestrates interactive collection of filters (name/ID range/country/type).
    - search_by_name / search_by_country / search_by_type: filter functions operating on the DataFrame. Country/type validators use local JSON files if present; otherwise fetch from the repo’s raw URLs.
  - sysyphus/scripts/user_requests.py:
    - make_meteorites(selected_meteorites): build Meteorite objects from selected rows.
    - request_selected(meteorites, rate_limiter=25): ThreadPoolExecutor + tqdm progress over extract_properties.
  - sysyphus/scripts/rendering.py:
    - show_properties(meteorite_list, ommit=[], as_pd=True): validate inputs, collect selected fields from Meteorite objects, return DataFrame indexed by name (or dict).
  - sysyphus/scripts/preprocessing.py:
    - dms_to_decimal / handle_coordinates: parse diverse latitude/longitude formats into decimal degrees.
    - remove_uncertainty: strip uncertainty annotations from strings, return numeric float.
    - handle_mass: convert strings to grams, supporting units like “kg” and raw numeric values.

Testing
- Location: tests/*.py (unittest-style classes executed via pytest)
- Network note: Some tests instantiate Boulder(), which checks internet connectivity and fetches remote data. CI and local runs need network access to pass as written.

Key repository configs
- setup.py: package metadata, install_requires, python_requires (>=3.10), long_description from README.md.
- pytest.ini: pythonpath includes . and sysyphus so tests can import without extra sys.path manipulation.
- .flake8: max-line-length=120

Usage context from README
- The typical user entrypoint is Boulder with interactive prompts for filtering and tools to request and display enriched data. See README.md and notebooks/ for examples and the monthly dataset links.

