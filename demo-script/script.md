# 00: Setup

## Create two users
Thais can be done in gitlab or keycloak directly.

### cramakri:
  - First Name: Chandrasekhar
  - Last Name: Ramakrishnan
  - email: cramakri@ethz.ch
  - Avatar: From Gravatar

Log in as cramakri and set an ssh key.

### ableuler:
  - First Name: Andreas
  - Last Name: Bleuler
  - email: andreas.bleuler@sdsc.ethz.ch
  - Avatar: From Gravatar

## Create Project

Log into Gitlab as cramakri.

- Create the project ```weather-zh``` in Gitlab under the cramakri namespace. Make the project public and add `ableuler` as a ```Developer``` on the project.
- Add the description

    An investigation into weather trends in Zürich, Switzerland.

- Set the tags to the following: linear models, python, weather
- Star the project as cramakri
- Set the Project > Settings > CI/CD > General pipeline settings to "Enable Auto DevOps"

## Prepare Work

Switch to user ableuler to create the following Kus:

### Ku: Data Reader

    Title: Data Reader
    Desc: Implement code to read the data

### Ku: Preprocess Data

    Title: Preprocess Data
    Text: Convert values to deviation from monthly mean

Switch back to user cramakri for the rest of the script.

# 01: Initialize

## Import data

```
mkdir weather-zh
renga init weather-zh
cd weather-zh
renga dataset create zh
renga dataset add zh http://www.meteoschweiz.admin.ch/product/output/climate-data/homogenous-monthly-data-processing/data/homog_mo_SMA.txt
```

## Add Readme

The text is in ```commits/01/README.md```.

## Commit / Push

```
git remote add origin ssh://git@gitlab.renga.build:5022/cramakri/weather-zh.git

git add .
git commit -m"Added readme"
git push --set-upstream origin master
```

# 02: Implement Reader

Locally:
- Copy the python package, jupyter notebook and updated readme from ```commits/02``` into the repo.
- Install the package by running ```pip install -e src/python/weather-ch``` in the root of the repo
- Add the new files to git, commit with message "Work on Ku Data Reader", and push to server

In UI:
- Go to Ku 1 (Data Reader), add a comment referencing the notebook: ```See ![GettingStarted](notebooks/GettingStarted.ipynb) for an example on how to use the reading code.```
- Mark Ku 1 as closed

# 03: Preprocess Data

Locally:
- Copy the updated python package and jupyter notebook from ```commits/03``` into the repo.
- Add the new files to git and commit with message "Work on Ku Preprocess Data" and push to server
- Run the command:
```
renga run python -m weather_ch preprocess data/zh/homog_mo_SMA.txt data/zh/standardized.csv
```
- Push updates to server

In UI:
- Go to Ku 2 (Preprocess Data), add a comment referencing the notebook: ```See ![PreprocessData](notebooks/PreprocessData.ipynb) for the result of preprocessing the data.```
- Mark Ku 2 as closed

# 04: Analyze Data

Create the following Ku:

### Ku: Analyze Data

    Title: Analyze Data
    Text: Analyze data to understand weather trends

Locally:
- Copy the updated jupyter notebooks from ```commits/04``` into the repo.
- Add the new files to git and commit with message "Work on Ku Analyze Data"
- Push updates to server

In UI:
- Go to Ku 3 (Analyze Data), add a comment referencing the notebook: ```See ![Analysis](notebooks/Analysis.ipynb) for some thoughts on the analysis.```


# Live Demo

1. Make another weather project that will just show some limited functionality

```
mkdir weather-ch-demo
cd weather-ch-demo
renga init --no-external-storage
renga dataset create zh
renga dataset add zh http://www.meteoschweiz.admin.ch/product/output/climate-data/homogenous-monthly-data-processing/data/homog_mo_SMA.txt
```

2. show the directory structure and the data

```
tree
head -n 30 data/zh/homog_mo_SMA.txt
```

3. remove the header

```
tail -n +27 data/zh/homog_mo_SMA.txt | less
renga run tail -n +27 data/zh/homog_mo_SMA.txt > data/zh/no-header.txt
```

4. show the logs

```
git log --oneline
renga log data/zh/no-header.txt
```


5. start a notebook
```
import pandas

data = pd.read_table('../data/zh/no-header.txt', sep='\s+')
```

6. make a readmee

7. Create the project on the server

8. add git remote and push

9. show the project on the Renga UI / then switch the the more complete
`weather-ch` project to show other functionality
