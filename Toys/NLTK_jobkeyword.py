import pandas as pd
import numpy as np
import nltk
import matplotlib.pyplot as plt

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from collections import Counter

source = pd.read_excel(r'C:\Users\chaot\Documents\Projects\NLTK_bankjob\Bankjobs.xlsx', engine='openpyxl')


# Check for non-string values in Responsibilities column
non_string_responsibilities = source.loc[~source['Responsibilities'].apply(isinstance, args=(str,))]

# Remove non-string values from dataframe
source = source.loc[source['Responsibilities'].apply(isinstance, args=(str,))]


source['Responsibilities'] = source['Responsibilities'].str.lower()
source['Requirements'] = source['Requirements'].str.lower()

source['Responsibilities'] = source['Responsibilities'].apply(word_tokenize)
source['Requirements'] = source['Requirements'].apply(word_tokenize)

stop_words = set(stopwords.words('english'))
source['Responsibilities'] = source['Responsibilities'].apply(lambda x: [word for word, pos in pos_tag(x) if pos.startswith('NN') and word not in stop_words and word.isalnum()])
source['Requirements'] = source['Requirements'].apply(lambda x: [word for word, pos in pos_tag(x) if pos.startswith('NN') and word not in stop_words and word.isalnum()])

responsibilities_words = [word for sublist in source['Responsibilities'].tolist() for word in sublist]
requirements_words = [word for sublist in source['Requirements'].tolist() for word in sublist]

responsibilities_word_counts = Counter(responsibilities_words)
requirements_word_counts = Counter(requirements_words)

most_common_responsibilities_words = responsibilities_word_counts.most_common(30)
most_common_requirements_words = requirements_word_counts.most_common(30)


# the number of non-IT jobs out of the entire sample
num_nonit_jobs = source['IT'].value_counts()['n']
num_entire_jobs = len(source)

print('In the sample, there are ',num_entire_jobs, 'jobs in total and amongst them there are', num_nonit_jobs,'non-IT jobs.')

print('\n','Here are the most common words in responsibility sections:', most_common_responsibilities_words)
print('\n','Here are the most common words in requirement sections:',most_common_requirements_words)



# Create my own list of jargon

def count_jargon(jargon_list, word_list):
    jargon_counts = Counter(word for word in word_list if word in jargon_list)
    return jargon_counts

it_jargons = ['computing', 'engineering', 'science', 'stem', 'statistics','spss','sas', 'programming', 'analytics', 'quant', 'api', 'integration', 'server', 'backend', 'dataframe', 'powerbi',
             'visualization', 'sql', 'python', 'vba', 'architecture', 'architect', 'c#', 'c++', 'warehousing', 'bloomberg', 'reuters', 'dataset', 'mining', 'cloud', 
             'computing', 'infrastructure', 'systems', 'ledger', 'blockchain', 'slack', 'automation', 'pandas', 'numpy', 'html', 'css', 'javascript', 'react', 
             'angular', 'vue', 'jquery', 'php', 'ruby', 'node.js', 'django', 'flask', 'express.js', 'asp', 'mysql',
             'digital', 'system', 'mongodb', 'oracle', 'postgresql', 'pbi','tableau']

nonit_jargons = ['attitude', 'teamwork', 'relationship', 'initiative', 'passion', 'willingness', 'spirit', 'mindset', 'ownership', 'discipline', 'customer', 'people', 'punctuality', 
                 'pressure', 'interpersonal', 'time management', 'communication', 'stakeholders', 'modeling', 'valuation','accounting','corporate', 'actuary', 
                 'marketing', 'strategy', 'sustainability','esg','consulting', 'compliance', 'investment', 'sales', 'budget', 'planning','wealth','ifrs', 'gaap']


# Let's see what keywords occur in both IT and non-IT positions

responsibilities_itskills = source['Responsibilities'].apply(lambda x: count_jargon(it_jargons, x)).sum()
requirements_itskills = source['Requirements'].apply(lambda x: count_jargon(it_jargons, x)).sum()
responsibilities_nonitskills = source['Responsibilities'].apply(lambda x: count_jargon(nonit_jargons, x)).sum()
requirements_nonitskills = source['Requirements'].apply(lambda x: count_jargon(nonit_jargons, x)).sum()

print('\nIn responsibility sections, we have this many IT related keywords: ', responsibilities_itskills)
print('\nIn responsibility sections, we have this many non-IT related keywords: ', responsibilities_nonitskills)
print('\nIn requirement sections, we have this many IT related keywords: ', requirements_itskills)
print('\nIn requirement sections, we have this many non-IT related keywords: ', requirements_nonitskills)





# Filter non-IT positions with more than 1 IT keyword in responsibilities or requirements
nonit_positions = source[source['IT'] == 'n']

responsibilities_withit= nonit_positions[(nonit_positions['Responsibilities'].apply(lambda x: sum(1 for word in x if word in it_jargons)) >= 1)]

requirements_withit= nonit_positions[(nonit_positions['Requirements'].apply(lambda x: sum(1 for word in x if word in it_jargons)) >= 1)]


num_responsibilities_withit = len(responsibilities_withit)
num_requirements_withit = len(requirements_withit)
num_nonit_positions = len(nonit_positions)

percentage_nonit_responsibilities_with_it_keywords = 100 * num_responsibilities_withit / num_nonit_positions
percentage_nonit_requirements_with_it_keywords = 100 * num_requirements_withit / num_nonit_positions


print('\nOut of', num_nonit_positions, 'non-IT positions,',
      num_responsibilities_withit, '(', round(percentage_nonit_responsibilities_with_it_keywords, 2),
      '%) have more than one IT keywords in their responsibilities.')

print('\nOut of', num_nonit_positions, 'non-IT positions,',
      num_requirements_withit, '(', round(percentage_nonit_requirements_with_it_keywords, 2),
      '%) have more than one IT keywords in their requirements.')


# Create a new column called 'Num_IT_Keywords'
source['Num_IT_Resp'] = source.apply(lambda row: sum(1 for word in row['Responsibilities'] if word in it_jargons), axis=1)
source['Num_IT_Reqm'] = source.apply(lambda row: sum(1 for word in row['Requirements'] if word in it_jargons), axis=1)


non_IT_positions = source[source['IT']=='n']
num1 = len(non_IT_positions[non_IT_positions['Num_IT_Resp'] != 0])
print(non_IT_positions[non_IT_positions['Num_IT_Resp'] != 0])




fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# plot first histogram on first subplot
axes[0].hist(non_IT_positions['Num_IT_Resp'], bins=4)
axes[0].set_title('Number of IT Responses')

# plot second histogram on second subplot
axes[1].hist(non_IT_positions['Num_IT_Reqm'], bins=4)
axes[1].set_title('Number of IT Requirements')

plt.show()