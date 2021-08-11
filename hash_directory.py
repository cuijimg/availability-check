import hashlib
import pathlib
import pandas as pd
from typing import Optional


def setup(path: pathlib.Path) -> bool:
    """
    This function sets up the hash directory in the given path.
    If necessary, it creates the path (but nor recursively) and then sets up the 256 folders.

    If there are already the correct folders, nothing is done. If there are incorrect folders, I quit.

    :param path: The path to the root of the policy folder.
    :return: A boolen indicating success.
    """
    if not path.exists():
        try:
            path.mkdir()
        except Exception as err:
            print(err)
            return False

    # check if all files exist.
    folders_expected = [format(i, '#04x')[2:4] for i in range(256)]
    folders_given = [g.name for g in path.glob('*')]
    if all([f in folders_given for f in folders_expected]):
        return True
    if len(folders_given) != 0:
        print("Bad folder structure given")
        return False
    for f in folders_expected:
        tp = path / f
        tp.mkdir()
    return True


def store(path: pathlib.Path, id: str, dat: pd.DataFrame) -> bool:
    """
    A simple function storing the dataframe in the path library.

    :param path: The path to the root of the policy folder.
    :param id: The id of the current dataframe. From it the name and folder is derived.
    :param dat: The dataframe that should be saved.
    :return: A boolean indicating success.
    """

    try:
        folder = hashlib.sha256(id.encode()).hexdigest()[0:2]
        file_path = path / folder / f'{id}.csv'
        dat.to_csv(file_path)
        return True
    except Exception as err:
        return False


def read(path, id) -> Optional[pd.DataFrame]:
    """
    Read a dataframe from a hash directory. The id must be exactly the same used to store the frame!

    :param path: The path to the root of the policy folder.
    :param id: The id of the current dataframe. From it the namne and the folder is derived.
    :return: The dataframe read in, None on failure.
    """

    try:
        folder = hashlib.sha256(id.encode()).hexdigest()[0:2]
        file_path = path / folder / f'{id}.csv'
        dat = pd.read_csv(file_path)
        return dat
    except Exception as err:
        print(err)
        return None