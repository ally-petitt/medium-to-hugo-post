# Medium Blog to Hugo Blog
This repository contains a script `medium-to-hugo-post.py` that, when paired with [medium-to-markdown](https://github.com/smrfeld/medium-to-markdown), enables automated migration from Medium blog posts to Hugo posts.

This is ideal for those who have created their own medium blogs and are looking to transition to hosting on a personal website.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Technical Details](#technical-details)
4. [Limitations](#limitations)


## Installation

Installing this Python script requires minimal setup.

```
git clone https://github.com/ally-petitt/medium-to-hugo-post
cd medium-to-hugo-post
pip install -r requirements.txt
```


## Usage

The overall usage involves 2 main steps: converting your Medium blog posts to markdown and converting the markdown files to Hugo posts.

### Converting Medium Blogs to Markdown
Creating usable input for this script requires a few preparatory steps, which can be found [here](https://github.com/smrfeld/medium-to-markdown/blob/main/README.md). A brief overview is the following:

1. Request a copy of your data from your Medium account.
2. Download the data (it should be sent to you email address at the time of writing) and unzip it.
3. Locate the `posts` directory of the unzipped data.

Now, you can convert the posts to markdown with [medium-to-markdown](https://github.com/smrfeld/medium-to-markdown).

```
git clone https://github.com/smrfeld/medium-to-markdown
cd medium-to-markdown
python run.py convert --posts-dir <PATH_TO_POSTS> --output-dir <DESIRED_OUTPUT_DIRECTORY>
```

Remember the output directory used since it will be required as input for `medium-to-hugo-post.py`.


### Converting the Markdown Files to Hugo Posts

The primary difference between the markdown files and a Hugo posts contain additional metadata in the header and the images and their captions require further formatting. More on this in the [Technical Details](#technical-details) section.

The general usage of `medium-to-hugo-post.py` is as follows:

```
python3 ./medium-to-hugo-post.py --md-dir <PREVIOUS_OUPUT_DIRECTORY>/md --posts-dir <POSTS_DIRECTORY_OF_HUGO_APP>
```

Note that the "PREVIOUS_OUPUT_DIRECTORY" is the output directory from the previous step and POSTS_DIRECTORY_OF_HUGO_APP is the `contents/posts` directory that can be found from the base of your Hugo app.

This program will write the Hugo-compatible posts to the posts directory of your Hugo app, which you can see the results of by running a local instance of the Hugo development server from the root directory of your Hugo website.

```
hugo server -D
```

### Command Line Arguments

The `-h` flag can be used to show the help menu which describes the parameters taken by the program.

```
python ./medium-to-hugo-post.py -h
usage: medium-to-hugo-post.py [-h] --md-dir MD_DIR [--posts-dir POSTS_DIR]

Convert markdown files into a Hugo-compatible post

options:
  -h, --help            show this help message and exit
  --md-dir MD_DIR       md directory from medium-to-markdown output folder
  --posts-dir POSTS_DIR
                        posts directory of Hugo application where the converted files will be stored

```


## Technical Details

The script `medium-to-hugo-post.py` accomplishes a 2 main steps that complete the transition of Medium exports from markdown to one that is ideal for a Hugo post:

1. Prepends post metadata into markdown file.
    * Hugo expects a prologue containing the title, date, and draft status of each post, which is not included by default in the markdown files exported by `medium-to-markdown`.

2. Converts image tags and their subtexts into markdown.
    * The images and their subtexts from Medium exports were not converted to markdown by the `medium-to-markdown` parser, so they did not show up. This scripts fixes that formatting so that the images are transferred.


### Limitations
This is not a perfect toolchain. Generalized regular expressions are used to parse image `src` and `alt` tags, so these values may be inappropriately trunucated if an edge case is reached in the expression such as an escaped quote in an "alt" tag.

Additionally, at the time of writing, the converted image tags still reference the images hosted on Medium, so deleting your Medium blog will result in broken images on your Hugo application. 