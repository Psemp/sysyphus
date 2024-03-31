import json
import sysyphus

from time import perf_counter


def get_uniques(boulder: sysyphus.Boulder) -> None:
    """
    Get unique countries and types from the boulder object and save them to a json file.

    Args:
    - boulder: sysyphus.Boulder object
    """

    unique_countries = boulder.sy_df["country"].unique().tolist()
    unique_types = boulder.sy_df["type"].unique().tolist()

    unique_types = [str(mtype).lower().strip() for mtype in unique_types]
    unique_countries = [str(country).lower().strip() for country in unique_countries]

    with open("sysyphus/utils/country_validation.json", "w") as f:
        json.dump(unique_countries, f)

    with open("sysyphus/utils/type_validation.json", "w") as f:
        json.dump(unique_types, f)


if __name__ == "__main__":
    print("Getting unique countries and types...")
    t_zero = perf_counter()
    boulder = sysyphus.Boulder()
    get_uniques(boulder)

    print(f"Time taken: {perf_counter() - t_zero:.2f} seconds")
