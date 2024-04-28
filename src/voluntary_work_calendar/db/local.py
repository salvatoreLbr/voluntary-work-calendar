from pathlib import Path
import streamlit as st


def create_input_path(test: bool) -> Path:
    input_path = Path("input_csv") if not test else Path("test_input_csv")
    if not input_path.exists():
        input_path.mkdir()
    return input_path


def exist_file(path: Path) -> bool:
    if not path.exists():
        text = "!!! following path not exist: {}".format(path)
        print(text)
        return False
    return True

