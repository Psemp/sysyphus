# sysyphus
Structured meteorite data access using MetBull: Query, filter, and analyze with ease.

# Notes (structure later) :
country list and types list obtained via the following snippet : 
```python

df = remote_load.get_remote_data(as_pd=True)

country_list = df["country"].unique().tolist()
types_list = df["type"].unique().tolist()

with open("sysyphus/utils/country_list.json", "w") as f:
    json.dump(country_list, f)

with open("sysyphus/utils/types_list.json", "w") as f:
    json.dump(type_list, f)
```

## Acknowledgements

This project has benefited greatly from the assistance of various tools. The unit tests were generated with the help of [GitHub Copilot](https://copilot.github.com/), an AI-powered code completion tool. Additionally, many of the regular expressions used throughout the codebase were created using [AutoRegex](https://www.autoregex.xyz/), a tool for automatically generating regular expressions. I express my gratitude to the developers of these tools for their contribution to the development process.