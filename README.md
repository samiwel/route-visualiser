# route-visualiser

An utility for visualising routes through eQ survey runner surveys as a
connected graph of nodes and edges.

## Usage

### Install the dependencies

This project relies on [Graphviz](http://www.graphviz.org/).

Ubuntu Linux:

```
sudo apt-get install graphviz

```

on Mac:

```
brew install graphviz
```

### Install Python dependencies

1. Create a virtualenv based on Python 3.

2. Install the dependencies using `pip`

```
pip install -r requirements.txt
```

## Run the utility

```
python routviz.py <schema.json> <output_filename>
```

## Screenshot

![Screenshot](./screenshot.png)
