"""EPR E.M.I.S Server."""

import typer

app = typer.Typer(
    help="E.M.I.S EPR Server",
    name="emis",
    no_args_is_help=False,
)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Main function to run the EPR E.M.I.S server."""
    typer.echo("EPR E.M.I.S Server")
    typer.echo(
        "This server implements E.M.I.S EPR functionality with XML-based communication."
    )


if __name__ == "__main__":
    app()
