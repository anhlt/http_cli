# -*- coding: utf-8 -*-

"""Console script for http_cli."""
import sys
import click
from http_cli import app


@click.command()
def main(args=None):
    """Console script for http_cli."""
    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
