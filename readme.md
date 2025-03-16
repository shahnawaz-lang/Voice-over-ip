# ISDN Parser

## Overview

The ISDN Parser is a Python-based tool designed to parse ISDN messages. It reads configuration from a `config.ini` file and processes ISDN messages, dial peers, and call information from a text file. The parsed data is then outputted in a structured format.

## Features

- Parses ISDN messages, dial peers, and call information.
- Configurable logging through `config.ini`.
- Command-line interface for parsing files and searching specific call details.

## Requirements

- Python 3.9 or higher
- Pydantic
- TextFSM

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/shahnawaz-lang/voice-over-ip/isdn_parser.git
    cd isdn_parser
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv .venv
    source .venv/bin/activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```


### Usage
To parse an ISDN message file, use the following command:
```sh
python -m isdn_parser.cli -f path/to/your/file.txt
```
#### Options
```
-f, --file: Path to the text file containing ISDN messages.
-s, --search: Enable the search flag.
-cgn, --calling: Specify the calling number.
-cdn, --called: Specify the called number.
-ca, --cause: Specify the cause code.
```
#### Example
```sh
python -m isdn_parser.cli -f path/to/your/file.txt -s -cgn 1234567890 -cdn 0987654321 -ca 16
```


