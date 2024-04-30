#####################################################################
# 
# Author:       Ally Petitt
#
# Description:  Python script to convert the markdown parsed by the 
#               tool https://github.com/smrfeld/medium-to-markdown
#               to something usable by Hugo for migrating from 
#               Medium to a personal hugo site.
#
# Date:         4/29/2024
#
#####################################################################

import argparse, os, re

def img_tag_to_md(tag:str, isFigcaption:bool=False) -> str:
    """
    Turns img and figcaption tags into markdown!
    """

    if isFigcaption:
        # not a perfect regex, but it works well enough for this use case
        caption = re.findall(f'>([a-z1-9][^<]*)', tag, re.IGNORECASE)
        if caption: md_format = f'*{caption[0]}*\n'
        else: md_format = ''
    else:
        # we care about 2 things when parsing an image tag: alt text and the src
        
        try: 
        # i know this isn't DRY- the goal of this script isn't full optimization
        
            src = re.findall(r' src="(.*?)"', tag, re.IGNORECASE)[0] # assume this exists or return nothing
            alt = re.findall(r' alt="(.*?)"', tag, re.IGNORECASE)

            if alt: alt = alt[0]
            else: alt = ''
            # combine the alt and src into markdown
            md_format = f"![{alt}]({src})"
        except Exception as e:
            print(f"Had an error while parsing the img tag: {e}")
            md_format = ""

    return md_format


def convert_post(metadata: dict, fpath, out_dir: str) -> None:
    """
    Adds appropriate metadata to post, reformats images and figcaptions
    to markdown, and removes the duplicate title of the post.
    """

    file_content = ""
    dest_file = os.path.join(out_dir, metadata["filename"])

    with open(fpath, 'r') as original:
        for i, line in enumerate(original.readlines()):

            # don't duplicate the title
            if i == metadata['title_offset'] or i == metadata['title_offset'] + 1:
                continue
            # read original file and modify the file_content variable to 
            # contain valid markdown image references
            elif line[:5].lower() == "<img ":
                file_content += img_tag_to_md(line)
            elif line[:12].lower() == "<figcaption ":
                file_content += img_tag_to_md(line, isFigcaption=True)
            else:
                file_content += line
    
    
    with open(dest_file, 'w') as new:
        # write prologue to a hugo post
        new.write(f"+++\ntitle = '{metadata['title']}'\n" + 
                f"date = {metadata['date']}\ndraft = false\n+++\n")

        new.write(file_content)



def extract_post_metadata(fpath: str) -> dict:
    """
    This function finds the name of the article, which is the first 
    occurance of a heading underlined by the repeated character "=".
    Then, it writes a copy of it to the destination directory without 
    the title to avoid a duplicate name.
    """

    # to make a post, we'll need the date and the title
    # date is easy - it's formatted in the name of the md file
    post_date = fname[:10]
    post_title = ""
    post_title_offset = -1 # if this is still -1 by the end, we know a title wasn't found

    # we can look for the first markdown heading to find the title
    with open(fpath, 'r') as f:
        lines = f.readlines()
        prev_len = 0

        for i, line in enumerate(lines):
            prev_line = lines[i-1]
            if i == 0:
                continue # first line can't contain '=' since those go beneath the title

            if line.strip() == '=' * (len(prev_line) - 1):
                post_title = prev_line.strip()
                post_title_offset = i-1
                break

            prev_len = len(line)
    

    return {"date":post_date, 
            "title": post_title,
            "title_offset": post_title_offset}

    



if __name__ == "__main__":
    """
    Collect user arguments and parse the md files for 
    """

    parser = argparse.ArgumentParser(description='Convert markdown files into a Hugo-compatible post')

    parser.add_argument('--md-dir', type=str, required=True,
                    help='md directory from medium-to-markdown output folder')
    parser.add_argument('--posts-dir', default='content/posts', type=str, required=False,
                    help='posts directory of Hugo application where the converted files will be stored')
    

    args = parser.parse_args()
    in_dir, out_dir = args.md_dir, args.posts_dir
    

    # convert 1 file at a time
    for fname in os.listdir(in_dir):
        fpath = os.path.join(in_dir, fname)
        # We'll collect the data that is needed to create a formatted post
        # The post date is formatted in the md file name by the medium-to-markdown tool
        
        # 1. Extract post metadata
        metadata = extract_post_metadata(fpath)
        metadata["filename"] = fname # we'll reuse existing pathname

        # 2. Combine the metadata and the post to make something formatted for Hugo
        convert_post(metadata, fpath, out_dir)
        


