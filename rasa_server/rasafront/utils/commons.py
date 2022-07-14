from pathlib import Path
from typing import Any, Dict, List, Optional, Text, Type, Union
from ruamel import yaml as yaml
from ruamel.yaml import RoundTripRepresenter, YAMLError
from ruamel.yaml.constructor import DuplicateKeyError, BaseConstructor, ScalarNode


YAML_VERSION = (1, 2)
DEFAULT_ENCODING = "utf-8"


def _is_ascii(text: Text) -> bool:
    return all(ord(character) < 128 for character in text)


def read_file(filename: Union[Text, Path], encoding: Text = DEFAULT_ENCODING) -> Any:
    """Read text from a file."""

    with open(filename, encoding=encoding) as f:
        return f.read()


def read_yaml(content: Text, reader_type: Union[Text, List[Text]] = "safe") -> Any:
    """Parses yaml from a text.
    Args:
        content: A text containing yaml content.
        reader_type: Reader type to use. By default "safe" will be used.
    Raises:
        ruamel.yaml.parser.ParserError: If there was an error when parsing the YAML.
    """
    if _is_ascii(content):
        # Required to make sure emojis are correctly parsed
        content = (
            content.encode("utf-8")
                .decode("raw_unicode_escape")
                .encode("utf-16", "surrogatepass")
                .decode("utf-16")
        )

    yaml_parser = yaml.YAML(typ=reader_type)
    yaml_parser.version = YAML_VERSION
    yaml_parser.preserve_quotes = True

    return yaml_parser.load(content) or {}


def read_yaml_file(filename: Union[Text, Path]) -> Union[List[Any], Dict[Text, Any]]:
    """Parses a yaml file.
    Raises an exception if the content of the file can not be parsed as YAML.
    Args:
        filename: The path to the file which should be read.
    Returns:
        Parsed content of the file.
    """
    return read_yaml(read_file(filename, DEFAULT_ENCODING))


if __name__ == "__main__":
    from pprint import pprint
    import sys
    d = read_yaml_file("../Chapter03/config.yml")
    # yamler = yaml.YAML()
    # yy = yamler.dump(d,stream=sys.stdout)
    # pprint(yy)
    import yaml
    y = yaml.safe_dump(d, default_flow_style=False)
    print(y)