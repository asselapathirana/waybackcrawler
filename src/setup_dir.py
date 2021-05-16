import pathlib
# create a directory structure for results
DIR_PAGES='../output/pages/'
DIR_KW   ='../output/keywords/'
DIR_GR   ='../output/graphics/'
DIR_PROC ='../output/processed/'


for dir_ in [DIR_PAGES, DIR_KW, DIR_GR, DIR_PROC]:
    pt=pathlib.Path(dir_)
    pt.mkdir(parents=True, exist_ok=True)