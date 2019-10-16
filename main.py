#!/usr/bin/env python
# coding: utf-8

# # ONS Trade in goods: country-by-commodity, imports and exports
# 
# This data is split into two distributions, one for imports and the other for exports:
# 
# https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/datasets/uktradecountrybycommodityimports
# 
# and
# 
# https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/datasets/uktradecountrybycommodityexports   

# In[3]:


from gssutils import *


# In[4]:


def run_script(s):
    get_ipython().run_line_magic('run', '"$s"')
    return table

observations = pd.concat(
    run_script(s) for s in ['exports.ipynb', 'imports.ipynb']
).drop_duplicates()


# In[5]:


from pathlib import Path
import numpy as np
out = Path('out')
out.mkdir(exist_ok=True)
slice_size = 100000

for i in np.arange(len(observations) // slice_size):
    dest_file = out / f'observations_{i:04}.csv'
    observations.iloc[i * slice_size : i * slice_size + slice_size - 1].to_csv(dest_file, index=False)


# Fix up title and description as we're combining the data into one Data Cube dataset

# In[6]:


from gssutils.metadata import THEME
scraper.dataset.family = 'Trade'
scraper.dataset.theme = THEME['business-industry-trade-energy']
scraper.dataset.title = scraper.dataset.title.replace('imports', 'imports and exports')
scraper.dataset.comment = scraper.dataset.comment.replace('import', 'import and export')

scraper.dataset


# In[9]:


with open(out / 'dataset.trig', 'wb') as metadata:
     metadata.write(scraper.generate_trig())
        
csvw = CSVWMetadata('https://gss-cogs.github.io/ref_trade/')
csvw.create(out / 'observations_0000.csv', out / 'observations.csv-schema.json')


# In[ ]:



