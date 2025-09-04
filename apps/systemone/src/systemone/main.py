"""EPR System One Server.

Main server that listens on TCP port 407000 and handles XML requests.
"""

import logging
import socket
import sys
from logging import Logger
from socket import socket as Socket
from typing import Optional

from systemone import SystemOne


def setup_logging() -> logging.Logger:
    """Setup logging configuration for console and system logs."""
    # Create logger
    logger = logging.getLogger("epr_system_one")
    logger.setLevel(logging.INFO)

    # Create formatters
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # File handler for system logs
    file_handler = logging.FileHandler("/var/log/epr_system_one.log", mode="a")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


class EPRSystemOneServer:
    """EPR System One TCP Server."""

    def __init__(self, host: str, port: int = 407000) -> None:
        self.host = host
        self.port = port
        self.server_socket: Optional[Socket] = None
        self.running: bool = False
        self.logger: Logger = setup_logging()
        self.system_one: SystemOne = SystemOne()

    def start_server(self) -> None:
        """Start the EPR System One server."""
        try:
            self.server_socket = Socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)

            self.running = True
            self.logger.info(
                "EPR System One Server started on %s:%s", self.host, self.port
            )
            self.logger.info("Waiting for ClientIntegrationRequest messages...")
            self.logger.info("Press Ctrl+C to stop the server")

            while self.running:
                try:
                    client_socket, address = self.server_socket.accept()
                    self._handle_client(client_socket, address)
                except socket.error:
                    if self.running:
                        break

        except Exception as e:
            self.logger.error("Error starting server: %s", e)
        finally:
            self.stop_server()

    def _handle_client(self, client_socket: Socket, address: tuple) -> None:
        """Handle incoming client connection."""
        try:
            self.logger.info("New connection from %s", address)

            # Receive XML data
            data = b""
            while True:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                data += chunk

            if data:
                try:
                    # Process request through SystemOne handler
                    response_xml = self.system_one.handle(data)

                    # Send response back to client
                    client_socket.sendall(response_xml.encode("utf-8"))
                    self.logger.info("Response sent to %s", address)

                except Exception as e:
                    self.logger.error(
                        "Error processing request from %s: %s", address, e
                    )
                    error_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<ClientIntegrationResponse>
    <Error>true</Error>
    <ErrorMessage>Server error: {e}</ErrorMessage>
    <ResponseUID>ERROR-{address[0]}-{address[1]}</ResponseUID>
</ClientIntegrationResponse>"""
                    client_socket.sendall(error_response.encode("utf-8"))

            client_socket.close()
            self.logger.info("Connection from %s closed", address)

        except Exception as e:
            self.logger.error("Error handling client %s: %s", address, e)
            try:
                client_socket.close()
            except Exception:
                pass

    def stop_server(self) -> None:
        """Stop the EPR server."""
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
                self.logger.info("EPR System One Server stopped")
            except Exception:
                pass


def main() -> None:
    """Main function to run the EPR System One server."""
    print("EPR System One Server")
    print(
        "This server implements System One EPR functionality with XML-based communication."
    )
    print("Listening on port 407000 for ClientIntegrationRequest messages.")
    print("Logs are written to console and /var/log/epr_system_one.log\n")

    try:
        server = EPRSystemOneServer(host="0.0.0.0", port=407000)  # nosec
        server.start_server()
    except KeyboardInterrupt:
        print("\n\nServer interrupted by user")
    except Exception as e:
        print(f"\nServer error: {e}")


if __name__ == "__main__":
    main()
