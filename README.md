# oisubset

oisubset == "o"pen "i"mages dataset + "subset".


This is a tool for generating subset of [Open Images Dataset V4](https://storage.googleapis.com/openimages/web/index.html).
The original dataset has 600 object classes on 1.74M images.
You can generate a subset, that contains specified classes.
For example, `Human Face` only dataset can be generated.


## Requirments

- Python 3.5 or later
- Original Open Images Dataset files

## Usage

### Installation

```
$ git clone git@github.com:LeapMind/oisubset.git
$ cd oisubset
$ pip install -r requirements.txt
```

### Generation

First, [copy](https://github.com/LeapMind/oisubset/blob/master/config/template.yml) config file to anywhere you want.
Then edit `target_classes` and some pathes.
You can choice multiple classes.


Then execute

```
$ python oisubset/main.py -c path/to/your/config.yml
```

## Development

### Test

not yet...

### CI

not yet...
