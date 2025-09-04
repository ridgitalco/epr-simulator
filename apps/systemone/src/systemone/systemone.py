import random
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timedelta
from logging import getLogger
from uuid import UUID, uuid4

from faker import Faker


@dataclass
class ClientIntegrationRequest:
    """Client Integration Request."""

    api_key: str
    device_id: str
    device_version: str
    request_uid: str
    function_name: str
    fucntion_version: str
    output_schema: dict
    fucntion_parameters: dict

    def __post_init__(self) -> None:
        if self.api_key != "fake-api-key":  # pragma: allowlist secret
            raise ValueError("Invalid API key")


@dataclass
class ClientIntegrationResponse:
    """Client Integration Response."""

    device_id: str
    request_uid: str
    function_name: str
    function_version: str
    response_uid: str
    response: dict


class SystemOne:
    """System One EPR Server."""

    def __init__(self) -> None:
        self._list_available_functions: list[str] = [
            "GetFunctions",
            "GetOrganisationMetadata",
            "GetCurrentActivity",
            "GetCurrentSession",
            "PatientSearch",
            "GetPatientRecord",
            "UpdatePatientRecord",
            "GetDocument",
            "DeleteFromPatientRecord",
            "GetAppointmentSlots",
            "GetDiary",
            "ExitClient",
            "DataExtract",
            "LaunchFunctionality",
            "GetXSDFiles",
            "IsPatientRetrieved",
        ]
        self._clients: dict[UUID, list[tuple[UUID, UUID]]] = {}
        self._received_messages: dict[UUID, ClientIntegrationRequest] = {}
        self._processed_messages: dict[UUID, ClientIntegrationResponse] = {}
        self._logger = getLogger(__name__)
        self._device_id = "fake-device-id"
        self._fake = Faker("en_GB")
        self._patient_database = self._initialize_patient_database()
        self._appointment_database = self._initialize_appointment_database()
        self._document_database = self._initialize_document_database()

    def _initialize_patient_database(self) -> dict:
        """Initialize sample patient database."""
        patients = {}
        for i in range(20):
            patient_id = f"P{100000 + i}"
            patients[patient_id] = {
                "patient_id": patient_id,
                "first_name": self._fake.first_name(),
                "last_name": self._fake.last_name(),
                "date_of_birth": self._fake.date_of_birth(
                    minimum_age=18, maximum_age=90
                ).isoformat(),
                "gender": random.choice(["M", "F", "U"]),  # nosec
                "nhs_number": f"{random.randint(100000000, 999999999)}",  # nosec
                "address": {
                    "line1": self._fake.building_number()
                    + " "
                    + self._fake.street_name(),
                    "line2": (
                        self._fake.secondary_address()
                        if random.choice([True, False])  # nosec
                        else ""
                    ),
                    "city": self._fake.city(),
                    "postcode": self._fake.postcode(),
                },
                "phone": self._fake.phone_number(),
                "email": self._fake.email(),
            }
        return patients

    def _initialize_appointment_database(self) -> dict:
        """Initialize sample appointment database."""
        appointments = {}
        for i in range(50):
            appointment_id = f"A{100000 + i}"
            appointments[appointment_id] = {
                "appointment_id": appointment_id,
                "patient_id": f"P{100000 + random.randint(0, 19)}",  # nosec
                "appointment_type": random.choice(
                    [
                        "GP_CONSULTATION",
                        "SPECIALIST_REFERRAL",
                        "BLOOD_TEST",
                        "VACCINATION",
                        "REVIEW",
                    ]
                ),  # nosec
                "scheduled_time": (
                    datetime.now()
                    + timedelta(
                        days=random.randint(1, 30),  # nosec
                        hours=random.randint(9, 17),  # nosec
                    )
                ).isoformat(),
                "duration_minutes": random.choice([15, 20, 30, 45, 60]),  # nosec
                "status": random.choice(
                    ["SCHEDULED", "CONFIRMED", "CANCELLED", "COMPLETED", "NO_SHOW"]
                ),  # nosec
                "location": random.choice(
                    ["Main Surgery", "Branch Surgery", "Community Clinic", "Hospital"]
                ),  # nosec
                "clinician_id": f"CLIN{random.randint(1000, 9999)}",  # nosec
                "notes": random.choice(
                    [
                        "Regular check-up",
                        "Follow-up appointment",
                        "New patient consultation",
                        "Annual review",
                    ]
                ),  # nosec
            }
        return appointments

    def _initialize_document_database(self) -> dict:
        """Initialize sample document database."""
        documents = {}
        for i in range(30):
            doc_id = f"DOC{100000 + i}"
            documents[doc_id] = {
                "document_id": doc_id,
                "patient_id": f"P{100000 + random.randint(0, 19)}",  # nosec
                "document_type": random.choice(
                    ["CONSULTATION", "LETTER", "REPORT", "PRESCRIPTION", "LAB_RESULT"]
                ),  # nosec
                "title": random.choice(
                    [
                        "Consultation Notes",
                        "Referral Letter",
                        "Lab Report",
                        "Prescription",
                        "Discharge Summary",
                    ]
                ),  # nosec
                "content": self._fake.text(max_nb_chars=500),
                "created_date": (
                    datetime.now() - timedelta(days=random.randint(1, 365))  # nosec
                ).isoformat(),
                "author": f"Dr. {self._fake.last_name()}",
                "status": random.choice(
                    ["DRAFT", "FINAL", "SENT", "ARCHIVED"]
                ),  # nosec
            }
        return documents

    def _parse_xml_request(self, xml_data: str) -> ClientIntegrationRequest:
        """Parse XML request into ClientIntegrationRequest dataclass."""
        root = ET.fromstring(xml_data)

        # Extract basic fields
        api_key = root.find("APIKey").text if root.find("APIKey") is not None else ""
        device_id = (
            root.find("DeviceID").text if root.find("DeviceID") is not None else ""
        )
        device_version = (
            root.find("DeviceVersion").text
            if root.find("DeviceVersion") is not None
            else ""
        )
        request_uid = (
            root.find("RequestUID").text if root.find("RequestUID") is not None else ""
        )
        function_name = (
            root.find("Function").text if root.find("Function") is not None else ""
        )
        function_version = (
            root.find("FunctionVersion").text
            if root.find("FunctionVersion") is not None
            else "1.0"
        )

        # Extract output schema
        output_schema = {}
        output_scheme_elem = root.find("OutputScheme")
        if output_scheme_elem is not None:
            for child in output_scheme_elem:
                output_schema[child.tag] = child.text

        # Extract function parameters
        function_parameters = {}
        function_params_elem = root.find("FunctionParameters")
        if function_params_elem is not None:
            for child in function_params_elem:
                function_parameters[child.tag] = child.text

        return ClientIntegrationRequest(
            api_key=api_key,
            device_id=device_id,
            device_version=device_version,
            request_uid=request_uid,
            function_name=function_name,
            fucntion_version=function_version,
            output_schema=output_schema,
            fucntion_parameters=function_parameters,
        )

    def _execute_function(self, request: ClientIntegrationRequest) -> dict:
        """Execute the requested function and return response data."""
        function_name = request.function_name.lower()

        match function_name:
            case "getfunctions":
                return self._get_functions()
            case "getorganisationmetadata":
                return self._get_organisation_metadata()
            case "getcurrentactivity":
                return self._get_current_activity()
            case "getcurrentsession":
                return self._get_current_session()
            case "patientsearch":
                return self._patient_search(request.fucntion_parameters)
            case "getpatientrecord":
                return self._get_patient_record(request.fucntion_parameters)
            case "updatepatientrecord":
                return self._update_patient_record(request.fucntion_parameters)
            case "getdocument":
                return self._get_document(request.fucntion_parameters)
            case "deletefrompatientrecord":
                return self._delete_from_patient_record(request.fucntion_parameters)
            case "getappointmentslots":
                return self._get_appointment_slots(request.fucntion_parameters)
            case "getdiary":
                return self._get_diary(request.fucntion_parameters)
            case "exitclient":
                return self._exit_client()
            case "dataextract":
                return self._data_extract(request.fucntion_parameters)
            case "launchfunctionality":
                return self._launch_functionality(request.fucntion_parameters)
            case "getxsdfiles":
                return self._get_xsd_files()
            case "ispatientretrieved":
                return self._is_patient_retrieved(request.fucntion_parameters)
            case _:
                return {"error": f"Unknown function: {request.function_name}"}

    def _get_functions(self) -> dict:
        """Get list of available functions."""
        return {
            "functions": [
                {
                    "name": func,
                    "version": "1.0",
                    "description": f"Execute {func} function",
                }
                for func in self._list_available_functions
            ]
        }

    def _get_organisation_metadata(self) -> dict:
        """Get organisation metadata."""
        return {"organisation": {"name": "System One Test Practice", "code": "TEST001"}}

    def _get_current_activity(self) -> dict:
        """Get current activity information."""
        return {
            "current_activity": {
                "user_id": f"USER{random.randint(1000, 9999)}",  # nosec
                "session_id": str(uuid4()),
                "activity_type": random.choice(
                    ["CONSULTATION", "ADMIN", "REPORTING"]
                ),  # nosec
                "start_time": datetime.now().isoformat(),
                "status": "ACTIVE",
            }
        }

    def _get_current_session(self) -> dict:
        """Get current session information."""
        return {
            "session": {
                "session_id": str(uuid4()),
                "user_id": f"USER{random.randint(1000, 9999)}",  # nosec
                "login_time": (
                    datetime.now() - timedelta(hours=random.randint(1, 8))  # nosec
                ).isoformat(),
                "last_activity": datetime.now().isoformat(),
                "status": "ACTIVE",
            }
        }

    def _patient_search(self, params: dict) -> dict:
        """Search for patients."""
        search_term = params.get("SearchTerm", "")
        patients = []

        for patient_id, patient_data in self._patient_database.items():
            if (
                search_term.lower() in patient_data["first_name"].lower()
                or search_term.lower() in patient_data["last_name"].lower()
                or search_term in patient_data["nhs_number"]
            ):
                patients.append(patient_data)

        return {
            "patients": patients,
            "total_count": len(patients),
            "search_term": search_term,
        }

    def _get_patient_record(self, params: dict) -> dict:
        """Get specific patient record."""
        patient_id = params.get("PatientID", "")

        if patient_id in self._patient_database:
            patient = self._patient_database[patient_id]
            # Add related appointments and documents
            appointments = [
                apt
                for apt in self._appointment_database.values()
                if apt["patient_id"] == patient_id
            ]
            documents = [
                doc
                for doc in self._document_database.values()
                if doc["patient_id"] == patient_id
            ]

            return {
                "patient": patient,
                "appointments": appointments,
                "documents": documents,
                "found": True,
            }
        else:
            return {
                "patient": None,
                "found": False,
                "error": f"Patient {patient_id} not found",
            }

    def _update_patient_record(self, params: dict) -> dict:
        """Update patient record."""
        patient_id = params.get("PatientID", "")

        if patient_id in self._patient_database:
            # Update patient data
            for key, value in params.items():
                if key != "PatientID" and key in self._patient_database[patient_id]:
                    self._patient_database[patient_id][key] = value

            return {
                "success": True,
                "patient_id": patient_id,
                "message": "Patient record updated successfully",
            }
        else:
            return {"success": False, "error": f"Patient {patient_id} not found"}

    def _get_document(self, params: dict) -> dict:
        """Get document by ID."""
        document_id = params.get("DocumentID", "")

        if document_id in self._document_database:
            return {"document": self._document_database[document_id], "found": True}
        else:
            return {
                "document": None,
                "found": False,
                "error": f"Document {document_id} not found",
            }

    def _delete_from_patient_record(self, params: dict) -> dict:
        """Delete item from patient record."""
        patient_id = params.get("PatientID", "")
        item_type = params.get("ItemType", "")
        item_id = params.get("ItemID", "")

        if patient_id in self._patient_database:
            if item_type == "APPOINTMENT" and item_id in self._appointment_database:
                del self._appointment_database[item_id]
            elif item_type == "DOCUMENT" and item_id in self._document_database:
                del self._document_database[item_id]

            return {
                "success": True,
                "message": f"{item_type} {item_id} deleted from patient {patient_id}",
            }
        else:
            return {"success": False, "error": f"Patient {patient_id} not found"}

    def _get_appointment_slots(self, params: dict) -> dict:
        """Get available appointment slots."""
        date = params.get("Date", datetime.now().strftime("%Y-%m-%d"))
        clinician_id = params.get("ClinicianID", "")

        slots = []
        for hour in range(9, 17):  # 9 AM to 5 PM
            for minute in [0, 30]:  # Every 30 minutes
                if random.choice([True, False, True]):  # nosec
                    slots.append(
                        {
                            "slot_id": f"SLOT{hour:02d}{minute:02d}",
                            "date": date,
                            "time": f"{hour:02d}:{minute:02d}",
                            "duration": 30,
                            "clinician_id": clinician_id,
                            "available": True,
                        }
                    )

        return {
            "appointment_slots": slots,
            "date": date,
            "clinician_id": clinician_id,
            "total_slots": len(slots),
        }

    def _get_diary(self, params: dict) -> dict:
        """Get diary entries."""
        date = params.get("Date", datetime.now().strftime("%Y-%m-%d"))
        clinician_id = params.get("ClinicianID", "")

        # Get appointments for the specified date and clinician
        diary_entries = []
        for appointment in self._appointment_database.values():
            if appointment["clinician_id"] == clinician_id and appointment[
                "scheduled_time"
            ].startswith(date):
                diary_entries.append(appointment)

        return {
            "diary_entries": diary_entries,
            "date": date,
            "clinician_id": clinician_id,
            "total_entries": len(diary_entries),
        }

    def _exit_client(self) -> dict:
        """Exit client session."""
        return {"success": True, "message": "Client session ended successfully"}

    def _data_extract(self, params: dict) -> dict:
        """Extract data based on criteria."""
        extract_type = params.get("ExtractType", "")
        date_from = params.get("DateFrom", "")
        date_to = params.get("DateTo", "")

        extracted_data = []
        if extract_type == "PATIENTS":
            extracted_data = list(self._patient_database.values())
        elif extract_type == "APPOINTMENTS":
            extracted_data = list(self._appointment_database.values())
        elif extract_type == "DOCUMENTS":
            extracted_data = list(self._document_database.values())

        return {
            "extract_type": extract_type,
            "date_from": date_from,
            "date_to": date_to,
            "extracted_data": extracted_data,
            "record_count": len(extracted_data),
        }

    def _launch_functionality(self, params: dict) -> dict:
        """Launch specific functionality."""
        functionality = params.get("Functionality", "")

        return {
            "success": True,
            "functionality": functionality,
            "message": f"Launching {functionality}",
            "launch_url": f"systemone://launch/{functionality.lower()}",
        }

    def _get_xsd_files(self) -> dict:
        """Get XSD schema files."""
        return {
            "xsd_files": [
                {
                    "filename": "ClientIntegrationRequest.xsd",
                    "version": "1.0",
                    "description": "Schema for client integration requests",
                },
                {
                    "filename": "ClientIntegrationResponse.xsd",
                    "version": "1.0",
                    "description": "Schema for client integration responses",
                },
            ]
        }

    def _is_patient_retrieved(self, params: dict) -> dict:
        """Check if patient is currently retrieved."""
        patient_id = params.get("PatientID", "")

        return {
            "patient_id": patient_id,
            "is_retrieved": patient_id in self._patient_database,
            "retrieval_time": (
                datetime.now().isoformat()
                if patient_id in self._patient_database
                else None
            ),
        }

    def _create_response_xml(
        self, request: ClientIntegrationRequest, response_data: dict
    ) -> str:
        """Create XML response from response data."""
        response_uid = str(uuid4()).upper()

        # Convert response data to XML
        response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<ClientIntegrationResponse>
    <DeviceID>{request.device_id}</DeviceID>
    <RequestUID>{request.request_uid}</RequestUID>
    <Function>{request.function_name}</Function>
    <FunctionVersion>{request.fucntion_version}</FunctionVersion>
    <ResponseUID>{response_uid}</ResponseUID>
    <Response>
        {self._dict_to_xml(response_data)}
    </Response>
</ClientIntegrationResponse>"""

        return response_xml

    def _dict_to_xml(self, data: dict, indent: int = 2) -> str:
        """Convert dictionary to XML string."""
        xml_parts = []
        spaces = " " * indent

        for key, value in data.items():
            if isinstance(value, dict):
                xml_parts.append(f"{spaces}<{key}>")
                xml_parts.append(self._dict_to_xml(value, indent + 2))
                xml_parts.append(f"{spaces}</{key}>")
            elif isinstance(value, list):
                xml_parts.append(f"{spaces}<{key}>")
                for item in value:
                    if isinstance(item, dict):
                        xml_parts.append(f"{spaces}  <Item>")
                        xml_parts.append(self._dict_to_xml(item, indent + 4))
                        xml_parts.append(f"{spaces}  </Item>")
                    else:
                        xml_parts.append(f"{spaces}  <Item>{item}</Item>")
                xml_parts.append(f"{spaces}</{key}>")
            else:
                xml_parts.append(f"{spaces}<{key}>{value}</{key}>")

        return "\n".join(xml_parts)

    def handle(self, request_data: bytes) -> str:
        """Handle incoming request.

        Args:
            request_data: The raw bytes of the request data.

        Returns:
            The XML string response.
        """
        try:
            xml_data = request_data.decode("utf-8")
            self._logger.info("Content length: %s characters", len(xml_data))
            self._logger.info("Content preview:\n%s...", xml_data[:300])

            # Parse XML request into dataclass
            request = self._parse_xml_request(xml_data)
            self._logger.info(
                "Parsed request - Function: %s, DeviceID: %s, RequestUID: %s",
                request.function_name,
                request.device_id,
                request.request_uid,
            )

            # Execute the requested function
            response_data = self._execute_function(request)
            self._logger.info(
                "Function %s executed successfully", request.function_name
            )

            # Create XML response
            response_xml = self._create_response_xml(request, response_data)
            self._logger.info("Response generated successfully")

            return response_xml

        except ET.ParseError as e:
            self._logger.error("XML Parse Error: %s", e)
            error_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<ClientIntegrationResponse>
    <Error>true</Error>
    <ErrorMessage>Invalid XML format: {e}</ErrorMessage>
    <ResponseUID>{str(uuid4()).upper()}</ResponseUID>
</ClientIntegrationResponse>"""
            return error_response

        except Exception as e:
            self._logger.error("Request processing error: %s", e)
            error_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<ClientIntegrationResponse>
    <Error>true</Error>
    <ErrorMessage>Processing error: {e}</ErrorMessage>
    <ResponseUID>{str(uuid4()).upper()}</ResponseUID>
</ClientIntegrationResponse>"""
            return error_response
