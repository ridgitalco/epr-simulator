"""EPR System One Server.

Main server that listens on TCP port 40700 and handles XML requests.
"""

import logging
import signal
import socket
import sys
from logging import Logger
from socket import socket as Socket
from typing import Any, Optional

import typer
from systemone.systemone import SystemOne

app = typer.Typer(
    help="System One EPR Server",
    name="systemone",
    no_args_is_help=False,
)


def setup_logging() -> logging.Logger:
    """Setup logging configuration for console and system logs."""
    # Create logger
    logger = logging.getLogger("epr_system_one")
    logger.setLevel(logging.INFO)

    # Create formatters
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)

    return logger


class EPRSystemOneServer:
    """EPR System One TCP Server."""

    def __init__(self, host: str, port: int = 40700) -> None:
        self.host = host
        self.port = port
        self.server_socket: Optional[Socket] = None
        self.running: bool = False
        self.logger: Logger = setup_logging()
        self.system_one: SystemOne = SystemOne()

    def start_server(self) -> None:
        """Start the EPR System One server."""

        def signal_handler(signum: int, frame: Any) -> None:
            self.logger.info("Received signal %s, shutting down server...", signum)
            self.stop_server()

        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        try:
            self.server_socket = Socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.settimeout(1.0)
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
                except socket.timeout:

                    continue
                except socket.error as e:
                    if self.running:
                        self.logger.error("Socket error: %s", e)
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


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context, host: str = "0.0.0.0", port: int = 40700) -> None:  # nosec
    """Main function to run the EPR System One server."""
    typer.echo("EPR System One Server")
    typer.echo(
        "This server implements System One EPR functionality with XML-based communication."
    )
    typer.echo(f"Listening on port {port} for ClientIntegrationRequest messages.")

    try:
        server = EPRSystemOneServer(host=host, port=port)
        server.start_server()
    except KeyboardInterrupt:
        typer.echo("\n\nServer interrupted by user")
    except Exception as e:
        typer.echo(f"\nServer error: {e}")


if __name__ == "__main__":
    app()
    app()
