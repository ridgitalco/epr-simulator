# EPR System One Server

This Python application implements a System One EPR (Electronic Patient Record) server that listens on TCP port 407000 and handles XML-based `ClientIntegrationRequest`/`Response` messages according to the System One API specification.

## Features

- **XML-based Communication**: Handles `ClientIntegrationRequest` and `ClientIntegrationResponse` messages
- **EPR Functions**: Implements core EPR functions like patient management, appointments, prescriptions, and lab results
- **Realistic Data**: Uses Faker library to generate realistic UK healthcare data
- **TCP Server**: Listens on port 407000 for client connections
- **Client Simulator**: Includes a client simulator for testing the server
- **Error Handling**: Comprehensive error handling and XML validation

## EPR Functions Implemented

1. **GetFunctions** - Get list of available EPR functions
2. **GetPatients** - Get list of patients with optional search criteria
3. **GetPatient** - Get specific patient details by ID
4. **GetAppointments** - Get patient appointments
5. **GetPrescriptions** - Get patient prescriptions
6. **GetLabResults** - Get patient lab results
7. **AddPatient** - Add new patient to the system
8. **UpdatePatient** - Update existing patient information

## Requirements

- Python 3.7 or higher
- Dependencies listed in `requirements.txt`

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Start the EPR System One Server

Start the main EPR server that listens on port 407000:

```bash
python main.py
```

The server will start and display:
```
✓ EPR System One Server started on 0.0.0.0:407000
Waiting for ClientIntegrationRequest messages...
Press Ctrl+C to stop the server
```

### 2. Test with the Client Simulator

In a new terminal, run the client simulator:

```bash
python epr_client_simulator.py
```

This will provide an interactive menu to test various EPR functions.

### 3. Optional: Simple Test Server

For basic XML message testing, you can also run:

```bash
python tcp_server.py
```

This starts a simple test server on port 407001.

## XML Message Format

### ClientIntegrationRequest

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ClientIntegrationRequest>
    <APIKey>f31e26725b5491f2</APIKey>
    <DeviceID>392752167bd7f69b</DeviceID>
    <DeviceVersion>v1.0</DeviceVersion>
    <RequestUID>99DDDEE0-B335-11E3-A459-010000004280</RequestUID>
    <Function>GetFunctions</Function>
    <FunctionVersion>1.0</FunctionVersion>
    <OutputScheme>
        <Drugs>Multiplex</Drugs>
        <Codes>CTV3</Codes>
    </OutputScheme>
    <FunctionParameters>
        <!-- Function-specific parameters -->
    </FunctionParameters>
</ClientIntegrationRequest>
```

### ClientIntegrationResponse

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ClientIntegrationResponse>
    <DeviceID>392752167bd7f69b</DeviceID>
    <RequestUID>99DDDEE0-B335-11E3-A459-010000004280</RequestUID>
    <Function>GetFunctions</Function>
    <FunctionVersion>1.0</FunctionVersion>
    <ResponseUID>6F175F30-B338-11E3-9804-010000005129</ResponseUID>
    <Response>
        <!-- Function-specific response data -->
    </Response>
</ClientIntegrationResponse>
```

## Example Usage

### Get Available Functions

**Request:**
```xml
<ClientIntegrationRequest>
    <APIKey>f31e26725b5491f2</APIKey>
    <DeviceID>392752167bd7f69b</DeviceID>
    <RequestUID>12345678-1234-1234-1234-123456789012</RequestUID>
    <Function>GetFunctions</Function>
    <FunctionVersion>1.0</FunctionVersion>
</ClientIntegrationRequest>
```

**Response:**
```xml
<ClientIntegrationResponse>
    <DeviceID>392752167bd7f69b</DeviceID>
    <RequestUID>12345678-1234-1234-1234-123456789012</RequestUID>
    <Function>GetFunctions</Function>
    <FunctionVersion>1.0</FunctionVersion>
    <ResponseUID>87654321-4321-4321-4321-210987654321</ResponseUID>
    <Response>
        <functions>
            <Item>
                <name>GetFunctions</name>
                <version>1.0</version>
                <description>Get list of available functions</description>
            </Item>
            <!-- More functions... -->
        </functions>
    </Response>
</ClientIntegrationResponse>
```

### Get Patient Details

**Request:**
```xml
<ClientIntegrationRequest>
    <APIKey>f31e26725b5491f2</APIKey>
    <DeviceID>392752167bd7f69b</DeviceID>
    <RequestUID>12345678-1234-1234-1234-123456789012</RequestUID>
    <Function>GetPatient</Function>
    <FunctionVersion>1.0</FunctionVersion>
    <FunctionParameters>
        <PatientID>P100000</PatientID>
    </FunctionParameters>
</ClientIntegrationRequest>
```

## Client Simulator Menu

The client simulator provides an interactive menu:

```
==================================================
           EPR CLIENT SIMULATOR MENU
==================================================
1. Get Available Functions
2. Get All Patients
3. Search Patients by Last Name
4. Get Specific Patient
5. Get Patient Appointments
6. Get Patient Prescriptions
7. Get Patient Lab Results
8. Add New Patient
9. Update Patient
0. Exit
==================================================
```

## Server Configuration

### Default Settings
- **Host**: 0.0.0.0 (listens on all interfaces)
- **Port**: 407000
- **API Key**: f31e26725b5491f2
- **Device ID**: 392752167bd7f69b

### Sample Data
The server initializes with 10 sample patients with realistic UK healthcare data including:
- Names, addresses, phone numbers
- NHS numbers
- Date of birth and gender
- Contact information

## Error Handling

The server handles various error conditions:
- Invalid XML format
- Unknown functions
- Missing required parameters
- Patient not found
- Connection errors

Error responses include:
```xml
<ClientIntegrationResponse>
    <Error>true</Error>
    <ErrorMessage>Error description</ErrorMessage>
    <ResponseUID>response-uuid</ResponseUID>
</ClientIntegrationResponse>
```

## Development and Testing

### Testing Individual Functions

You can test specific functions using the client simulator or by sending raw XML requests to the server.

### Adding New Functions

1. Add a new method to the `EPRSystemOneServer` class
2. Add the function to the `_execute_function` method
3. Update the `_get_functions` method to include the new function

### Customizing Data

- Modify the `_initialize_sample_data` method to change initial data
- Adjust Faker settings for different regional data
- Modify function implementations for different response formats

## Security Notes

- This is a simulation server for development and testing purposes
- Do not use in production healthcare environments
- API key validation is minimal (for demonstration only)
- Consider implementing proper authentication and encryption for production use

## Troubleshooting

### Common Issues

1. **Port already in use**:
   - Check if another service is using port 407000
   - Use `netstat -an | grep 407000` to check port usage

2. **Connection refused**:
   - Ensure the EPR server is running
   - Check firewall settings
   - Verify host and port configuration

3. **XML parsing errors**:
   - Validate XML format before sending
   - Check for proper encoding (UTF-8)
   - Ensure all required elements are present

### Debug Mode

- Check server logs for detailed request/response information
- Use the simple test server for basic XML message testing
- Validate XML format using online XML validators

## License

This EPR System One server is provided as-is for educational and development purposes.

## Support

For issues or questions:
1. Check the server logs for error messages
2. Verify XML message format
3. Test with the included client simulator
4. Review the function documentation and examples
