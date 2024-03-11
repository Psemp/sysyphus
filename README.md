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
