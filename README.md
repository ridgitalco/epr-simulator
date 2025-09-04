# EPR Simulator

This project is an **EPR (Electronic Patient Record) Simulator** designed to help any company that wants to develope a software which want to communicate with NHS EPR systems for development, testing, and integration purposes. The simulator provides realistic EPR functionality and message handling to enable comprehensive testing without requiring access to live NHS systems.

## Supported EPR Systems

Currently, the simulator supports:
- [**SystemOne EPR**](docs/SystemOne.md) - Full implementation with comprehensive functionality
- [**EMIS**](docs/EMIS.md) - Implementation in progress, will be added very soon

## Requirements

- Python 3.13 or higher
- Dependencies listed in `requirements.txt`

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Installation

First, install the EPR packages to create the executable commands:

```bash
# Install SystemOne EPR (creates systemone.exe)
cd apps/systemone
pip install -e .

# Install EMIS EPR (creates emis.exe)
cd ../emis
pip install -e .
```

### 1. Start the EPR System One Server

You can start the SystemOne EPR server using the executable command:

```bash
# Using the executable (recommended)
systemone

# Or using Python directly
cd apps/systemone/src
python -m systemone.main
```

**Command Options:**
```bash
# Start with custom host and port
systemone --host 127.0.0.1 --port 8080

# Get help
systemone --help
```

The server will start and display:
```
✓ EPR System One Server started on 0.0.0.0:40700
Waiting for ClientIntegrationRequest messages...
Press Ctrl+C to stop the server
```

### 2. Start the EMIS EPR Server

You can start the EMIS EPR server using the executable command:

```bash
# Using the executable (recommended)
emis

# Or using Python directly
cd apps/emis/src
python -m emis.main
```

**Note:** EMIS implementation is currently under development.


## Support

For issues or questions:
1. Check the server logs for error messages
2. Verify XML message format
3. Test with the included client simulator
4. Review the function documentation and examples
