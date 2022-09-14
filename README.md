# Aiven Interview Project

The purpose of this project is to write a coding exercise for my 2022 interview with Aiven. Hooray!

Let's talk about the journey:

* v0 - The Zillow Bathtub Project: turns out getting Zillow to programmatically do what I want in order to surface the data I need to do this was more than the whole exercise. Harrumph! This is being migrated to a different project For A Later Time where I'll focusly solely on making the scraper work. Thus, no spoilers for any of the context for what this means.
* v1 - Go on Kaggle and get some NYC Bus Data, load it into Aiven's postgres offering and use Aiven's Grafana offering to build some dashboards. Drawback: this is a no-code solution to a coding exercise, so that won't do!
* v2 - The Final Version: go on Kaggle, find a JSON data set, and use Aiven's OpenSearch offering via command line.


# The Data: Steam Data Via Kaggle

I am using a 640 MB dataset from Kaggle to do this project: [Steam Data by Souyama](https://www.kaggle.com/datasets/souyama/steam-dataset).

## The Upload

Hit a few snags with this, as the Python Opensearch library doesn't appear to be fully compatible with Python3. Since Python2 is EOL, switching tactics to Golang. I made a note about the Python library as that might be worth a deeper analysis and (re-)?opening one of their tickets on this issue.