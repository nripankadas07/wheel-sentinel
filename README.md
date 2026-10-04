# wheel-sentinel

Bounded read-only Python wheel path and RECORD hash verifier.

An offline Python 3.10+ MVP with no runtime dependencies.

## Install and first useful result

```sh
git clone https://github.com/nripankadas07/wheel-sentinel.git
cd wheel-sentinel
python -m venv .venv
# POSIX; on Windows use .venv\Scripts\activate
. .venv/bin/activate
python -m pip install .
wheel-sentinel --help
python demo.py
```

The demo creates temporary synthetic inputs and prints the actual report; it does not require accounts, services, API keys or user data. CLI exit status: 0 = accepted/clean; 1 = review findings; 2 = invalid input or operational error.

## CLI example

```sh
wheel-sentinel dist/package.whl --max-bytes 100000000
```

Pass a wheel file path; archives are inspected without extracting files.

## Validate

```sh
python -m unittest discover -v
python -m compileall -q wheel_sentinel.py
python demo.py
```

## Limits

Checks archive structure and RECORD integrity, not authenticity, signatures, malware, advisory status, complete wheel metadata validity or installability. RECORD hashes are attacker-editable. Trust the source of an artifact separately. ZIP metadata budget is checked before reads; no extraction occurs.

See [RESEARCH.md](RESEARCH.md) for the user brief and dated comparisons, [VALIDATION.md](VALIDATION.md) for exact check coverage, and [SUPPORT.md](SUPPORT.md) for contributions and security reporting. MIT licensed; original implementation, with standard-library dependencies. No competitor code or prose copied.
