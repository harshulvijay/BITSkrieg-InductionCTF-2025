# [rev] python-rev &mdash; Write Up

## Figuring out what this thing is

If we run `strings` on the challenge binary, we see some Python-related strings. But `file` reports this as a `ELF 64-bit LSB executable`.

A quick Google search for `compiled python elf32`, or even more targeted `python to elf 64 bit lsb`, says something about PyInstaller.

## Unpacking the binary

The given binary is a PyInstaller binary. We can use [PyInstxtractor](https://github.com/extremecoders-re/pyinstxtractor) to get the `pyc` files.

## Getting the Python source

We can use [pycdc](https://github.com/zrax/pycdc) on `challenge.pyc` to get the program's source code.

```bash
$ pycdc challenge.pyc
# Source Generated with Decompyle++
# File: challenge.pyc (Python 3.10)
```

```python
import argparse
import os
import tempfile
import zipfile
from cryptography.fernet import Fernet
SECRET_KEY_SHHH = 'NDiqrH3MkCWrjN103C9KvnhlGGssLbujK0km5tZxan4='

def parse_cli_args():
    parser = argparse.ArgumentParser('Encrypt your data with our magical tooling. ™️  (Outputs a ZIP.)', **('description',))
    parser.add_argument('-i', '--input', True, str, 'File to encrypt', **('required', 'type', 'help'))
    parser.add_argument('-a', '--add', False, str, 'File to add to the ZIP archive', **('required', 'type', 'help'))
    parser.add_argument('-o', '--output', True, str, 'Output file', **('required', 'type', 'help'))
    parser.add_help = True
    args = parser.parse_args()
    return args


def encrypt_data(data = None):
    f = Fernet(SECRET_KEY_SHHH)
    return f.encrypt(data)


def create_archive(name = None, files = None):
    zf = zipfile.ZipFile(name, 'w')
    for file, filename in files:
        if len(filename) > 0:
            zf.write(file, filename)
            continue
        zf.write(file, os.path.basename(file))
    zf.close()


def main(args = None):
    file = open(args.input, 'rb')
    file_contents = file.read()
    encrypted = encrypt_data(file_contents)
    orig_input_name = file.name
    file.close()
    tfile = tempfile.NamedTemporaryFile('wb', True, **('mode', 'delete'))
    tfile.write(encrypted)
    tfile.flush()
    if args.add:
        create_archive(args.output, [
            (tfile.name, orig_input_name),
            (args.add, '')])
    else:
        create_archive(args.output, [
            (tfile.name, orig_input_name)])
    print('encrypted data successfully!')
    tfile.close()

if __name__ == '__main__':
    args = parse_cli_args()
    main(args)
    return None
```

## Analysing the source code

Looking at the CLI tool's source, we can see that it encrypts the file passed via the `-i` argument, writes it to a temporary file and adds that file to the ZIP archive at a path set by the `-o` argument, alongside any file passed via `-a` (but those ones are unencrypted). We can also see a Fernet key called `SECRET_KEY_SHHH` defined at the top of the file, which is used to encrypt the data.

## Solving the challenge

On extracting the ZIP archive and looking at `important.txt`, we see some encrypted data. If we decode that using Fernet decryption with `SECRET_KEY_SHHH`, we get the flag `InductionCTF{zipp3d_it_l0ck3d_it_but_f0rg0t_to_h1de_the_k3y}`.
