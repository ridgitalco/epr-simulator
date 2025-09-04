# SystemOne EPR Documentation

## Overview

SystemOne is a comprehensive Electronic Patient Record (EPR) system used widely across the NHS. This simulator provides a complete implementation of the SystemOne API, allowing developers to test integrations and develop applications that work with SystemOne EPR systems.

## System Architecture

The SystemOne EPR simulator implements a TCP server that listens on port **40700** and handles XML-based communication using `ClientIntegrationRequest` and `ClientIntegrationResponse` messages.

### Key Components

- **TCP Server**: Handles incoming connections on port 40700
- **XML Message Parser**: Processes ClientIntegrationRequest messages
- **Function Executor**: Executes EPR functions based on requests
- **Data Generators**: Creates realistic UK healthcare data using Faker
- **Response Builder**: Constructs XML responses

## Supported Functions

The SystemOne simulator implements the following EPR functions:

### 1. GetFunctions
**Purpose**: Retrieve a list of all available EPR functions
**Parameters**: None required
**Returns**: List of available functions with versions and descriptions

### 2. GetOrganisationMetadata
**Purpose**: Get metadata about the healthcare organization
**Parameters**: None required
**Returns**: Organization name, code, and configuration details

### 3. GetCurrentActivity
**Purpose**: Get information about current user activity
**Parameters**: None required
**Returns**: User ID, session ID, activity type, start time, and status

### 4. GetCurrentSession
**Purpose**: Retrieve current session information
**Parameters**: None required
**Returns**: Session ID, user ID, login time, last activity, and status

### 5. PatientSearch
**Purpose**: Search for patients using various criteria
**Parameters**:
- `SearchTerm` (string): Search term for patient name or NHS number
**Returns**: List of matching patients with basic demographics

### 6. GetPatientRecord
**Purpose**: Retrieve complete patient record including appointments and documents
**Parameters**:
- `PatientID` (string): Unique patient identifier
**Returns**: Complete patient record with appointments and documents

### 7. UpdatePatientRecord
**Purpose**: Update patient information
**Parameters**:
- `PatientID` (string): Patient to update
- Additional parameters for fields to update
**Returns**: Success status and confirmation message

### 8. GetDocument
**Purpose**: Retrieve a specific document by ID
**Parameters**:
- `DocumentID` (string): Unique document identifier
**Returns**: Document details including content, type, and metadata

### 9. DeleteFromPatientRecord
**Purpose**: Delete items from patient records
**Parameters**:
- `PatientID` (string): Patient identifier
- `ItemType` (string): Type of item (APPOINTMENT, DOCUMENT)
- `ItemID` (string): ID of item to delete
**Returns**: Success status and confirmation

### 10. GetAppointmentSlots
**Purpose**: Get available appointment slots
**Parameters**:
- `Date` (string): Date for appointment slots (YYYY-MM-DD)
- `ClinicianID` (string): Specific clinician ID (optional)
**Returns**: List of available time slots

### 11. GetDiary
**Purpose**: Retrieve diary entries for a specific date and clinician
**Parameters**:
- `Date` (string): Date for diary entries (YYYY-MM-DD)
- `ClinicianID` (string): Clinician identifier
**Returns**: List of scheduled appointments and activities

### 12. ExitClient
**Purpose**: End the current client session
**Parameters**: None required
**Returns**: Success confirmation

### 13. DataExtract
**Purpose**: Extract data based on specified criteria
**Parameters**:
- `ExtractType` (string): Type of data (PATIENTS, APPOINTMENTS, DOCUMENTS)
- `DateFrom` (string): Start date for extract (optional)
- `DateTo` (string): End date for extract (optional)
**Returns**: Extracted data matching criteria

### 14. LaunchFunctionality
**Purpose**: Launch specific SystemOne functionality
**Parameters**:
- `Functionality` (string): Name of functionality to launch
**Returns**: Launch URL and success status

### 15. GetXSDFiles
**Purpose**: Retrieve XML schema definition files
**Parameters**: None required
**Returns**: List of available XSD files with descriptions

### 16. IsPatientRetrieved
**Purpose**: Check if a patient is currently retrieved in the session
**Parameters**:
- `PatientID` (string): Patient identifier to check
**Returns**: Retrieval status and timestamp

## Message Format

### ClientIntegrationRequest

All requests to the SystemOne EPR follow this XML structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ClientIntegrationRequest>
    <APIKey>f31e26725b5491f2</APIKey>
    <DeviceID>392752167bd7f69b</DeviceID>
    <DeviceVersion>v1.0</DeviceVersion>
    <RequestUID>99DDDEE0-B335-11E3-A459-010000004280</RequestUID>
    <Function>FunctionName</Function>
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

#### Required Fields:
- **APIKey**: Authentication key for the request
- **DeviceID**: Unique identifier for the requesting device
- **RequestUID**: Unique identifier for this specific request
- **Function**: Name of the EPR function to execute
- **FunctionVersion**: Version of the function to use

#### Optional Fields:
- **DeviceVersion**: Version of the requesting device
- **OutputScheme**: Preferred output format specifications
- **FunctionParameters**: Parameters specific to the requested function

### ClientIntegrationResponse

All responses from the SystemOne EPR follow this XML structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ClientIntegrationResponse>
    <DeviceID>392752167bd7f69b</DeviceID>
    <RequestUID>99DDDEE0-B335-11E3-A459-010000004280</RequestUID>
    <Function>FunctionName</Function>
    <FunctionVersion>1.0</FunctionVersion>
    <ResponseUID>6F175F30-B338-11E3-9804-010000005129</ResponseUID>
    <Response>
        <!-- Function-specific response data -->
    </Response>
</ClientIntegrationResponse>
```

#### Response Fields:
- **DeviceID**: Echo of the requesting device ID
- **RequestUID**: Echo of the original request UID
- **Function**: Echo of the requested function name
- **FunctionVersion**: Echo of the requested function version
- **ResponseUID**: Unique identifier for this response
- **Response**: Function-specific response data

### Error Responses

When errors occur, the response includes error information:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ClientIntegrationResponse>
    <Error>true</Error>
    <ErrorMessage>Error description</ErrorMessage>
    <ResponseUID>ERROR-response-uuid</ResponseUID>
</ClientIntegrationResponse>
```

## Data Models

### Patient Record
```xml
<patient>
    <patient_id>P100001</patient_id>
    <first_name>John</first_name>
    <last_name>Smith</last_name>
    <date_of_birth>1985-03-15</date_of_birth>
    <gender>M</gender>
    <nhs_number>123456789</nhs_number>
    <address>
        <line1>123 High Street</line1>
        <line2>Flat 4B</line2>
        <city>London</city>
        <postcode>SW1A 1AA</postcode>
    </address>
    <phone>020 7946 0958</phone>
    <email>john.smith@email.com</email>
</patient>
```

### Appointment Record
```xml
<appointment>
    <appointment_id>A100001</appointment_id>
    <patient_id>P100001</patient_id>
    <appointment_type>GP_CONSULTATION</appointment_type>
    <scheduled_time>2024-01-15T14:30:00</scheduled_time>
    <duration_minutes>30</duration_minutes>
    <status>SCHEDULED</status>
    <location>Main Surgery</location>
    <clinician_id>CLIN1234</clinician_id>
    <notes>Regular check-up</notes>
</appointment>
```

### Document Record
```xml
<document>
    <document_id>DOC100001</document_id>
    <patient_id>P100001</patient_id>
    <document_type>CONSULTATION</document_type>
    <title>Consultation Notes</title>
    <content>Patient consultation notes...</content>
    <created_date>2024-01-15T14:45:00</created_date>
    <author>Dr. Johnson</author>
    <status>FINAL</status>
</document>
```

## Example Usage

### Example 1: Get Available Functions

**Request:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
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
<?xml version="1.0" encoding="UTF-8"?>
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
                <description>Execute GetFunctions function</description>
            </Item>
            <Item>
                <name>PatientSearch</name>
                <version>1.0</version>
                <description>Execute PatientSearch function</description>
            </Item>
            <!-- More functions... -->
        </functions>
    </Response>
</ClientIntegrationResponse>
```

### Example 2: Search for Patients

**Request:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<ClientIntegrationRequest>
    <APIKey>f31e26725b5491f2</APIKey>
    <DeviceID>392752167bd7f69b</DeviceID>
    <RequestUID>search-123-456</RequestUID>
    <Function>PatientSearch</Function>
    <FunctionVersion>1.0</FunctionVersion>
    <FunctionParameters>
        <SearchTerm>Smith</SearchTerm>
    </FunctionParameters>
</ClientIntegrationRequest>
```

**Response:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<ClientIntegrationResponse>
    <DeviceID>392752167bd7f69b</DeviceID>
    <RequestUID>search-123-456</RequestUID>
    <Function>PatientSearch</Function>
    <FunctionVersion>1.0</FunctionVersion>
    <ResponseUID>response-789-012</ResponseUID>
    <Response>
        <patients>
            <Item>
                <patient_id>P100001</patient_id>
                <first_name>John</first_name>
                <last_name>Smith</last_name>
                <date_of_birth>1985-03-15</date_of_birth>
                <nhs_number>123456789</nhs_number>
            </Item>
        </patients>
        <total_count>1</total_count>
        <search_term>Smith</search_term>
    </Response>
</ClientIntegrationResponse>
```

## Configuration

### Server Settings
- **Host**: 0.0.0.0 (listens on all interfaces)
- **Port**: 40700
- **API Key**: f31e26725b5491f2 (configurable)
- **Device ID**: 392752167bd7f69b (configurable)

### Sample Data
The simulator initializes with:
- 20 sample patients with realistic UK demographics
- 50 sample appointments across different types
- 30 sample documents of various types
- Realistic NHS numbers, addresses, and contact information

## Security Considerations

⚠️ **Important**: This is a simulation server for development and testing purposes only.

- Do not use in production healthcare environments
- API key validation is minimal (for demonstration only)
- No encryption is implemented (add TLS for production use)
- Consider implementing proper authentication for production environments

## Error Handling

The SystemOne simulator handles various error conditions:

### Common Errors
- **Invalid XML format**: Malformed XML in requests
- **Unknown functions**: Requests for non-existent functions
- **Missing parameters**: Required parameters not provided
- **Patient not found**: Requests for non-existent patients
- **Connection errors**: Network-related issues

### Error Response Format
All errors return structured XML responses with error details for debugging and logging purposes.

## Integration Guidelines

### Best Practices
1. Always validate XML before sending requests
2. Handle error responses gracefully
3. Use unique RequestUIDs for tracking
4. Implement proper timeout handling
5. Log all requests and responses for debugging

### Testing Recommendations
1. Test all supported functions
2. Verify error handling scenarios
3. Test with various patient data
4. Validate XML schema compliance
5. Performance test with concurrent connections
