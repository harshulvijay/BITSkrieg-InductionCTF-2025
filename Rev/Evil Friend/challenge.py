#!/bin/env python3

import argparse
import os
import tempfile
import zipfile
from cryptography.fernet import Fernet

SECRET_KEY_SHHH = "NDiqrH3MkCWrjN103C9KvnhlGGssLbujK0km5tZxan4="


def parse_cli_args():
    parser = argparse.ArgumentParser(
        description="Encrypt your data with our magical tooling. ™️  (Outputs a ZIP.)"
    )
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        type=str,
        help="File to encrypt",
    )
    parser.add_argument(
        "-a",
        "--add",
        required=False,
        type=str,
        help="File to add to the ZIP archive",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        type=str,
        help="Output file",
    )
    parser.add_help = True
    args = parser.parse_args()
    return args


def encrypt_data(data: bytes) -> bytes:
    f = Fernet(SECRET_KEY_SHHH)
    return f.encrypt(data)


def create_archive(name: str, files: list[tuple[str, str]]):
    zf = zipfile.ZipFile(name, "w")

    for file, filename in files:
        if len(filename) > 0:
            zf.write(file, filename)
        else:
            zf.write(file, os.path.basename(file))
    zf.close()


def main(args: argparse.Namespace):
    file = open(args.input, "rb")
    file_contents = file.read()
    encrypted = encrypt_data(file_contents)
    orig_input_name = file.name
    file.close()

    tfile = tempfile.NamedTemporaryFile(mode="wb", delete=True)
    tfile.write(encrypted)
    tfile.flush()

    if args.add:
        create_archive(args.output, [(tfile.name, orig_input_name), (args.add, "")])
    else:
        create_archive(args.output, [(tfile.name, orig_input_name)])

    print("encrypted data successfully!")
    tfile.close()


if __name__ == "__main__":
    args = parse_cli_args()
    main(args)
