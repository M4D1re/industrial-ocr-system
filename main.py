import sys

from app.bootstrap import Bootstrap


def main() -> None:
    bootstrap = Bootstrap()

    exit_code = bootstrap.run()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()