import sys
from src.main import main
from pytest import MonkeyPatch


def test_main():
    with MonkeyPatch().context() as mp:
        mp.setattr(
            sys,
            "argv",
            [
                sys.argv[0],
                "-uf",
                "customer_data/GRI_2017_2020.xlsx",
                "-rf",
                "temp/Metadata2017_2020.xlsx",
                "-d",
                "temp/",
            ],
        )

        main()
