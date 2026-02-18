# Python virtual environments (`venv`)

This short guide explains what a `venv` is, why to use it, and how to use the existing `venv` in this repository.

**What is a `venv`?**
- A `venv` (virtual environment) is a lightweight, per-project Python environment that isolates installed packages and (optionally) the Python interpreter from the system-wide installation.
- It prevents package version conflicts between different projects and makes dependency management reproducible.

**Why use a `venv`?**
- Install project-specific packages without `sudo`.
- Keep global Python clean and avoid version clashes.
- Recreateable environments for collaboration and deployment.

**Common commands (Linux / Raspberry Pi)**

Create a new virtual environment:
```bash
python3 -m venv venv
```

Activate the venv for the current shell session:
```bash
source venv/bin/activate
# shell prompt usually changes to show (venv)
```

Install project dependencies (when activated):
```bash
pip install -r requirements.txt
```

Run a script using the active venv's Python:
```bash
python src/examples/raspberry_subscriber.py --broker 127.0.0.1
```

Deactivate the venv:
```bash
deactivate
```

Run one-off commands without activating (preferred in scripts/CI):
```bash
./venv/bin/python3 src/examples/raspberry_subscriber.py --broker 127.0.0.1
./venv/bin/pip install -r requirements.txt
```

**Tips & troubleshooting**
- If you get `ModuleNotFoundError` when running `python3` directly, either activate the `venv` or use `./venv/bin/python3`.
- `requirements.txt` pins dependencies for reproducibility. Run `pip install -r requirements.txt` after creating/activating the venv.
- If `pip` cannot find a pinned version, try using a released version available on PyPI (see changes made in this repo where `paho-mqtt` was pinned to a valid version).
- On some systems you may need `python3-venv` installed (Debian/Ubuntu):
```bash
sudo apt update && sudo apt install python3-venv
```

**Example for this repository**
1. Create (if not present):
```bash
python3 -m venv venv
```
2. Activate:
```bash
source venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Start a local broker (in another terminal):
```bash
./scripts/run_local_broker.sh
```
5. Run the Raspberry subscriber (uses venv packages):
```bash
python src/examples/raspberry_subscriber.py --broker 127.0.0.1 --topic test/topic --port 1883
```

Or run without activating:
```bash
./venv/bin/python3 src/examples/raspberry_subscriber.py --broker 127.0.0.1
```

That's it — this file is intended as a quick reference for using the `venv` in this project.
