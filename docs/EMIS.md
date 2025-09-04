# EMIS EPR Documentation

## Overview

EMIS (Egton Medical Information Systems) is one of the leading Electronic Patient Record (EPR) systems used across the NHS, serving thousands of GP practices and healthcare organizations. This simulator provides a foundation for EMIS EPR integration testing and development.

## Current Implementation Status

🚧 **Under Development**: The EMIS EPR simulator is currently in early development stages. Full functionality will be implemented in upcoming releases.

### Planned Features

The EMIS simulator will implement comprehensive EPR functionality including:

- **Patient Management**: Complete patient record handling
- **Appointment System**: Scheduling and appointment management
- **Clinical Documentation**: Medical records and consultation notes
- **Prescribing System**: Electronic prescription management
- **Laboratory Integration**: Lab results and test ordering
- **Referral Management**: Inter-practice and specialist referrals
- **Clinical Decision Support**: Alerts and clinical guidance
- **Reporting System**: Practice and patient reporting

## EMIS System Architecture

The EMIS EPR simulator will implement:

### Communication Protocol
- **HTTP/HTTPS**: RESTful API endpoints
- **HL7 FHIR**: Standard healthcare data exchange format
- **XML/JSON**: Flexible message formatting
- **OAuth 2.0**: Secure authentication and authorization

### Core Components
- **API Gateway**: Request routing and authentication
- **Patient Service**: Patient data management
- **Appointment Service**: Scheduling functionality
- **Clinical Service**: Medical records and documentation
- **Prescription Service**: Medication management
- **Integration Hub**: Third-party system connectivity

## Planned EPR Functions

### Patient Management Functions

#### 1. PatientSearch
**Purpose**: Search for patients using various criteria
**Parameters**:
- `SearchTerm` (string): Patient name, NHS number, or date of birth
- `SearchType` (string): Type of search (NAME, NHS_NUMBER, DOB)
- `MaxResults` (integer): Maximum number of results to return
**Returns**: List of matching patients with demographics

#### 2. GetPatientDetails
**Purpose**: Retrieve complete patient demographic information
**Parameters**:
- `PatientID` (string): Unique patient identifier
- `IncludeHistory` (boolean): Include historical changes
**Returns**: Complete patient record with demographics and history

#### 3. UpdatePatientDetails
**Purpose**: Update patient demographic information
**Parameters**:
- `PatientID` (string): Patient identifier
- `UpdatedFields` (object): Fields to update with new values
**Returns**: Success status and updated patient record

#### 4. RegisterNewPatient
**Purpose**: Register a new patient in the system
**Parameters**:
- `PatientDetails` (object): Complete patient demographics
- `RegistrationDate` (date): Date of registration
**Returns**: New patient ID and registration confirmation

### Clinical Functions

#### 5. GetMedicalHistory
**Purpose**: Retrieve patient's complete medical history
**Parameters**:
- `PatientID` (string): Patient identifier
- `DateFrom` (date): Start date for history
- `DateTo` (date): End date for history
- `IncludeDeleted` (boolean): Include deleted entries
**Returns**: Comprehensive medical history records

#### 6. AddConsultationNote
**Purpose**: Add new consultation notes to patient record
**Parameters**:
- `PatientID` (string): Patient identifier
- `ConsultationDate` (datetime): Date and time of consultation
- `Notes` (string): Consultation notes
- `ClinicianID` (string): Clinician identifier
**Returns**: Consultation ID and confirmation

#### 7. GetPrescriptions
**Purpose**: Retrieve patient prescription history
**Parameters**:
- `PatientID` (string): Patient identifier
- `Status` (string): Prescription status filter
- `DateRange` (object): Date range for prescriptions
**Returns**: List of prescriptions with details

#### 8. IssuePrescription
**Purpose**: Issue new prescription for patient
**Parameters**:
- `PatientID` (string): Patient identifier
- `MedicationDetails` (object): Medication and dosage information
- `PrescriberID` (string): Prescribing clinician ID
**Returns**: Prescription ID and confirmation

### Appointment Functions

#### 9. GetAppointments
**Purpose**: Retrieve patient appointments
**Parameters**:
- `PatientID` (string): Patient identifier
- `DateFrom` (date): Start date range
- `DateTo` (date): End date range
- `Status` (string): Appointment status filter
**Returns**: List of appointments with details

#### 10. BookAppointment
**Purpose**: Book new appointment for patient
**Parameters**:
- `PatientID` (string): Patient identifier
- `AppointmentType` (string): Type of appointment
- `PreferredDate` (date): Preferred appointment date
- `ClinicianID` (string): Specific clinician (optional)
**Returns**: Appointment ID and booking confirmation

#### 11. CancelAppointment
**Purpose**: Cancel existing appointment
**Parameters**:
- `AppointmentID` (string): Appointment identifier
- `CancellationReason` (string): Reason for cancellation
**Returns**: Cancellation confirmation

### Laboratory Functions

#### 12. GetLabResults
**Purpose**: Retrieve laboratory test results
**Parameters**:
- `PatientID` (string): Patient identifier
- `TestType` (string): Specific test type filter
- `DateRange` (object): Date range for results
**Returns**: Laboratory results with reference ranges

#### 13. OrderLabTest
**Purpose**: Order laboratory tests for patient
**Parameters**:
- `PatientID` (string): Patient identifier
- `TestDetails` (object): Tests to be ordered
- `Priority` (string): Test priority level
- `OrderingClinicianID` (string): Clinician ordering tests
**Returns**: Order ID and confirmation

### Referral Functions

#### 14. CreateReferral
**Purpose**: Create referral to specialist or service
**Parameters**:
- `PatientID` (string): Patient identifier
- `ReferralType` (string): Type of referral
- `SpecialtyCode` (string): Specialty or service code
- `ReferralReason` (string): Clinical reason for referral
**Returns**: Referral ID and confirmation

#### 15. GetReferralStatus
**Purpose**: Check status of patient referrals
**Parameters**:
- `PatientID` (string): Patient identifier
- `ReferralID` (string): Specific referral ID (optional)
**Returns**: Referral status and tracking information

## Planned Message Formats

### FHIR R4 Support

The EMIS simulator will support HL7 FHIR R4 standard resources:

#### Patient Resource
```json
{
  "resourceType": "Patient",
  "id": "patient-123456",
  "identifier": [
    {
      "system": "https://fhir.nhs.uk/Id/nhs-number",
      "value": "9876543210"
    }
  ],
  "name": [
    {
      "use": "official",
      "family": "Smith",
      "given": ["John", "William"]
    }
  ],
  "gender": "male",
  "birthDate": "1985-03-15",
  "address": [
    {
      "use": "home",
      "line": ["123 High Street", "Flat 4B"],
      "city": "London",
      "postalCode": "SW1A 1AA"
    }
  ],
  "telecom": [
    {
      "system": "phone",
      "value": "020 7946 0958",
      "use": "home"
    },
    {
      "system": "email",
      "value": "john.smith@email.com"
    }
  ]
}
```

#### Appointment Resource
```json
{
  "resourceType": "Appointment",
  "id": "appointment-789012",
  "status": "booked",
  "serviceType": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/service-type",
          "code": "124",
          "display": "General Practice"
        }
      ]
    }
  ],
  "appointmentType": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/v2-0276",
        "code": "ROUTINE",
        "display": "Routine appointment"
      }
    ]
  },
  "start": "2024-01-15T14:30:00Z",
  "end": "2024-01-15T15:00:00Z",
  "participant": [
    {
      "actor": {
        "reference": "Patient/patient-123456"
      },
      "status": "accepted"
    },
    {
      "actor": {
        "reference": "Practitioner/practitioner-456789"
      },
      "status": "accepted"
    }
  ]
}
```

#### Observation Resource (Lab Results)
```json
{
  "resourceType": "Observation",
  "id": "observation-345678",
  "status": "final",
  "category": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/observation-category",
          "code": "laboratory",
          "display": "Laboratory"
        }
      ]
    }
  ],
  "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "33747-0",
        "display": "Hemoglobin A1c"
      }
    ]
  },
  "subject": {
    "reference": "Patient/patient-123456"
  },
  "effectiveDateTime": "2024-01-10T09:30:00Z",
  "valueQuantity": {
    "value": 6.8,
    "unit": "%",
    "system": "http://unitsofmeasure.org",
    "code": "%"
  },
  "referenceRange": [
    {
      "low": {
        "value": 4.0,
        "unit": "%"
      },
      "high": {
        "value": 6.0,
        "unit": "%"
      }
    }
  ]
}
```

### REST API Endpoints

The EMIS simulator will expose RESTful endpoints:

#### Patient Endpoints
- `GET /api/v1/patients` - Search patients
- `GET /api/v1/patients/{id}` - Get patient details
- `PUT /api/v1/patients/{id}` - Update patient
- `POST /api/v1/patients` - Register new patient

#### Appointment Endpoints
- `GET /api/v1/patients/{id}/appointments` - Get patient appointments
- `POST /api/v1/appointments` - Book appointment
- `PUT /api/v1/appointments/{id}` - Update appointment
- `DELETE /api/v1/appointments/{id}` - Cancel appointment

#### Clinical Endpoints
- `GET /api/v1/patients/{id}/medical-history` - Get medical history
- `POST /api/v1/patients/{id}/consultations` - Add consultation notes
- `GET /api/v1/patients/{id}/prescriptions` - Get prescriptions
- `POST /api/v1/prescriptions` - Issue prescription

#### Laboratory Endpoints
- `GET /api/v1/patients/{id}/lab-results` - Get lab results
- `POST /api/v1/lab-orders` - Order lab tests

## Configuration

### Planned Server Settings
- **Protocol**: HTTPS (with HTTP fallback for testing)
- **Port**: 8080 (configurable)
- **Authentication**: OAuth 2.0 with JWT tokens
- **Data Format**: JSON (primary), XML (optional)
- **FHIR Version**: R4

### Security Features
- **OAuth 2.0**: Industry-standard authentication
- **JWT Tokens**: Secure session management
- **TLS Encryption**: Encrypted data transmission
- **Role-Based Access**: Granular permissions
- **Audit Logging**: Complete activity tracking

## Development Roadmap

### Phase 1: Foundation (Current)
- [x] Project structure setup
- [ ] Basic server framework
- [ ] Authentication system
- [ ] Database schema design

### Phase 2: Core Functions
- [ ] Patient management functions
- [ ] Basic appointment system
- [ ] Clinical documentation
- [ ] FHIR resource support

### Phase 3: Advanced Features
- [ ] Prescription management
- [ ] Laboratory integration
- [ ] Referral system
- [ ] Clinical decision support

### Phase 4: Integration & Testing
- [ ] Comprehensive testing suite
- [ ] Performance optimization
- [ ] Documentation completion
- [ ] Integration examples

## Integration Guidelines

### Prerequisites
- EMIS Web API access credentials
- Understanding of HL7 FHIR R4 standard
- OAuth 2.0 implementation capability
- JSON/XML processing capabilities

### Best Practices
1. **Authentication**: Implement proper OAuth 2.0 flows
2. **Error Handling**: Handle HTTP status codes appropriately
3. **Rate Limiting**: Respect API rate limits
4. **Data Validation**: Validate FHIR resources before sending
5. **Logging**: Implement comprehensive audit logging

### Testing Recommendations
1. **Unit Testing**: Test individual API endpoints
2. **Integration Testing**: Test complete workflows
3. **Performance Testing**: Test with realistic data volumes
4. **Security Testing**: Validate authentication and authorization
5. **FHIR Validation**: Ensure FHIR resource compliance

## Support and Documentation

### Resources
- EMIS Web API Documentation (when available)
- HL7 FHIR R4 Specification
- NHS Digital FHIR Implementation Guide
- OAuth 2.0 Specification

### Community
- NHS Developer Community
- HL7 FHIR Community
- EMIS Developer Forums

---

**Note**: This documentation describes the planned implementation of the EMIS EPR simulator. Features and functionality are subject to change during development. Check back regularly for updates as the implementation progresses.
