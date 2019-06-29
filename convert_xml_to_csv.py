import glob
import xml.etree.ElementTree as ET
import re
import pandas as pd

pictures = glob.glob("annotations/*.xml")
bigdf = pd.DataFrame()
for picture in pictures:
    filename = ''
    tree = ET.parse(picture)
    root = tree.getroot()
    conv = {'filename': [], 'xmin': [], 'xmax': [], 'ymin': [], 'ymax': []}
    for child in root:
        name = ''
        xmin = ''
        xmax = ''
        ymin = ''
        ymax = ''
        if child.tag == 'filename':
            filename = child.text
        if child.tag == 'object':
            cell = str(ET.tostring(child))
            name = re.search('<name>\w+', cell).group(0)[6:]
            xmin = int(re.search('<xmin>\d+', cell).group(0)[6:])
            xmax = int(re.search('<xmax>\d+', cell).group(0)[6:])
            ymin = int(re.search('<ymin>\d+', cell).group(0)[6:])
            ymax = int(re.search('<ymax>\d+', cell).group(0)[6:])
            conv['filename'].append(f'annotations/{filename}')
            conv['xmin'].append(xmin)
            conv['xmax'].append(xmax)
            conv['ymin'].append(ymin)
            conv['ymax'].append(ymax)
    df = pd.DataFrame(conv)
    bigdf = bigdf.append(df, ignore_index=True)
bigdf.to_csv('annotations.csv')
