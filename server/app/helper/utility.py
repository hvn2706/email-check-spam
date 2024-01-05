import re
import numpy as np
from bs4 import BeautifulSoup


def convert_str_to_camel(snake_str):
    parts = snake_str.split('_')
    return parts[0] + ''.join(x.title() for x in parts[1:])


def clean(text):
    sms = re.sub('[^a-zA-Z]', ' ', text)  # Replacing all non-alphabetic characters with a space
    sms = sms.lower()  # converting to lowercase
    if sms == '':
        sms = np.nan
    return sms


def remove_tags(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")
    
    for tmp_data in soup(['style', 'script']):
        # Remove tags
        tmp_data.decompose()
    
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)
