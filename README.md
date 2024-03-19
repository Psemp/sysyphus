# Sysyphus
![sisyphus got tired](https://raw.githubusercontent.com/Psemp/sysyphus/main/img/sysyphus_thumbnail.jpg)
## Introduction
`Sysyphus` is a Python package that simplifies access to the MetBull database for anyone interested in meteorite data. It's intended for scientists, educators, and meteorite enthusiasts who need an easier way to query, filter, and analyze information from one of the largest meteorite databases available.

Recognizing the difficulties often associated with handling large datasets, and the challenges resulting from a non uniform syntax, `Sysyphus` aims to make meteorite data more approachable and coherent.

With `Sysyphus`, users can focus more on their research questions and explorations, and less on the complexities of data retrieval and manipulation.

It encourages open science and community-driven improvements, making it a continually evolving tool that adapts to the needs of its users.


## Features
`Sysyphus` provides a robust set of features designed to streamline the exploration and analysis of meteorite data:

- Access to MetBull Data: Directly query and download the latest meteorite data from the MetBull database, ensuring you always have access to up-to-date information. The dataset used to perform searches is updated every first day of each month and can be found [On This Page](https://github.com/Psemp/sysyphus_notebooks/tree/main/datasets)
- Advanced Search Capabilities: Filter the vast MetBull dataset by various criteria, including name, type, fall country to find exactly what you're looking for with minimal effort.
- Data Enrichment: Enhance the raw data with additional computations, such as converting coordinates from DMS to decimal format, making it ready for analysis or mapping.
- Interactive Prompts: Simplify your data query process with user-friendly interactive prompts, guiding you through filtering options without needing to remember specific query syntax.
- Flexible Output Formats: Choose how you want to view your results, with options to display data as a pandas DataFrame for further analysis or a neatly formatted dictionary for quick reference.
- Meteorite Object Modeling: Transform search results into Python objects for more intuitive interaction and manipulation of meteorite data in your scripts or applications.
- Batch Request Management: Safely perform bulk data requests with built-in rate limiting to respect the MetBull server's resources while efficiently gathering the data you need.
- Customizable Data Display: Tailor the presentation of your search results with options to omit specific details or focus on particular attributes of interest.
- Open Source Collaboration: The package is 100% open source : browse, copy, fork, improve on it !

Sysyphus is continuously evolving, with new features and improvements added regularly based on user feedback and the latest developments in meteorite research. Stay tuned for future updates!

## Installation
The install requires python3.10 or newer (mainly because of pep604). If `python3 --version` < `3.10.XX`, consider updating either Anaconda or Python directly.

The [setup requirements (click me)](https://github.com/Psemp/sysyphus/blob/main/setup.py) are designed to be as light as possible and packages that are more often than not in most data driven projects.

**VIA PIP**
```bash
pip install sysyphus
```
*Conda release planned as well*

### <u>Updating Python Version</u>
<br>
<details>
  <summary>Click to expand</summary>

If your current Python version is below 3.10 and you wish to use Sysyphus, you will need to update your Python installation. Below are links to official guides for updating Python, whether you're using the standard Python installation or managing your Python versions with Anaconda.

#### For Standard Python Installation:
Visit [Python's official download page](https://www.python.org/downloads/) for the latest version and follow the instructions for your operating system. Make sure to download a version that is 3.10 or newer.

#### For Anaconda Users:
If you're using Anaconda to manage your Python environments, you can update Python within a specific conda environment by running:
```bash
conda update python
```
</details>

## Usage

Sysyphus is designed to simplify access to meteorite data from the MetBull database, providing an intuitive interface for querying, refining searches, performing detailed requests, and saving data.<br>
At its core is the Boulder class, which facilitates these operations with minimal setup.

Though Boulder offers a high-level abstraction for ease of use, Sysyphus is flexible.

Users can directly utilize its Meteorite class and other methods for more granular control or integration into broader projects.

### Typical use case : (more in depth in notebook I will try not to forget to upload)

```python
import sysyphus

boulder = sysyphus.Boulder()  # use_json=True by default

>>> cnx: OK
>>> remote content: Loaded

boulder.make_search()  # verbose_results=True by default

>>> Enter name to filter dataset (min. 2 chars):
<<< Catalina
>>> Enter numeric ID range (e.g., 100,200):
<<< 550,600 #  Order doesn't really matter, the script sorts it
>>> Refine search by fall country: 
<<< chile  # caps don't matter
>>> Refine results by types:
<<<   # search terms can be left blank
>>> # dataframe with the meteorites fitting the selection, head and tail if too long for default (pandas)

boulder.request_metbull(rate_limiter=25)  # max = 25, will auto lower to len(selection) if rate > len(selection), no useless threads
>>> # TQDM progress bar, ETA & stats

boulder.display_search(as_pandas=True)  # omit to ignore certain cols, as_pandas : True -> pd.Df, False : python Dict

>>> # displays the search results in the requested format with ignored cols if any

file_name = "met_search"
format = "csv"

boulder.save_search(filepath=file_name, file_format=format)
>>> file saved as csv at met_search  # extension added
```

## Advanced Features
*Cf. Notebook that i'll try not to forget and link here*

## Credits

Sysyphus is made possible thanks to the data provided by MetBull and the contributions from our community. <br>I appreciate every piece of input, code, or feedback I've received.

I am especially thankful to MetBull for allowing access to their meteorite data, which is essential for Sysyphus's functionality.

**While using Sysyphus, we encourage you to:**

- Be considerate of MetBull's resources by making requests responsibly.
- Adhere to any specified rate limits to help keep the service available for everyone.
- If you can, consider contributing to MetBull to enrich their data further.
- If you can spare a little time, tone down the rate limitation to a more conservative rate (4-8), this **will** be a bit slower but will ensure fair usage of the resources.

This project also relies on several third-party libraries, which enhance its features and usability. Thanks to the developers behind these tools for their invaluable work.

## License

Distributed under the MIT License. See [`LICENSE`](https://github.com/Psemp/sysyphus/blob/main/LICENSE) for more information.


## Contact

- Pierre Sempéré - pierre.sempere.01@gmail.com
- Project Link: [https://github.com/Psemp/sysyphus](https://github.com/Psemp/sysyphus)

## Acknowledgements

- [GitHub Copilot](https://copilot.github.com/) (tests)
- [AutoRegex](https://www.autoregex.xyz/) (most of the complex iterative regex filters)
- GPT4, for both the migraines and the helpful synthetic hand
- Image made using Dall-E inspired by a meme