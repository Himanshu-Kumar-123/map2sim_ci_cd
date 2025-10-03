# 🧪 SimReady Test Framework

A **pytest-based testing framework** for the Sim Ready platform, providing comprehensive UI automation testing for **DSRS** and **MAP2SIM** components.

---

## 📋 Overview

The SimReady Test Framework provides automated UI testing capabilities for Drive Simulation Ready components through pytest-based test scenarios. It supports both DSRS (DriveSim Ready Studio) and MAP2SIM (HD Maps to Sim Ready) testing workflows.

### Key Features
- ✅ Pytest-based test execution
- ✅ Component-specific test organization (DSRS & MAP2SIM)
- ✅ JSON-based configuration and flag passing
- ✅ Modular test utilities and helpers
- ✅ Comprehensive UI automation libraries

---

## 📁 Framework Structure

The SimReady Test Framework is organized into the following directories:

- `simready_test_fwk/ui_tests`: Contains UI tests for Sim Ready platform.
- `simready_test_fwk/utils`: Contains utility functions for the test framework.
- `simready_test_fwk/config`: Contains configuration files for the test framework.
- `simready_test_fwk/omni_ui`: Contains test framework's core libraries.
- `simready_test_fwk/conftest.py`: Contains the pytest configuration for the test framework.
- `simready_test_fwk/README.md`: This file.

## Running Tests

To run the tests, use the following command:

```bash
pytest ui_tests/map2sim/test_asset_mapping_table.py --ip <ip> --port <port> --output_path <output_path> --json_data <json_data>
E.g.
pytest ui_tests/map2sim/test_barrier_presets.py --ip 127.0.0.1 --port 9682 --output_path ./results --json_data '{"test": "data"}'
```
##Flags with `m2s` in their name are passed to pytest UI scripts available under `simready_test_fwk/ui_tests/map2sim` as serialized json and can be decoded in pytest script using `--json_data` flag.
##Flags with `dsrs` in their name are passed to pytest UI scripts available under `simready_test_fwk/ui_tests/dsrs` as serialized json and can be decoded in pytest script using `--json_data` flag.

## Test results handling
### Success criteria
- Tests are considered successful based on pytest exit code 0. Do not add explicit "scenario is successful" prints; they are no longer required.

