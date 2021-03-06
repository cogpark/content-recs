from os import remove
from tabnanny import check
import pandas as pd
from fuzzywuzzy import fuzz
from sentence_evaluator import SentenceEvaluator


class TitleEvalutor:

    def __init__(self): 
        self.titles_df = pd.read_csv('titles_urls.csv', usecols=['node_id', 'title','is_published','node_path'])
        print(f'Dataset size: {self.titles_df.shape}')
        # self.sample_df = self.titles_df[0:5000]
        self.se = SentenceEvaluator()
        return

    def evaluator(self, title, url, node_id):
        evaluation = {}

        evaluation['title'] = title
        evaluation['title_length'] = self.check_title_length(title)
        evaluation['title_matches'] = self.get_title_matches(title, url, node_id)
        evaluation['acronym_checker'] = self.acronym_checker(title)
        evaluation['trouble_words'] = self.se.get_trouble_words(title)
        evaluation['conjunctions'] = self.se.count_conjunctions(title, is_title=True)
        evaluation['noun_stacking'] = self.se.stacked_nouns(title)

        return evaluation

    '''RULES'''
    
    def check_title_length(self, title):
        """
        Checks the length of a title.

        """

        title_length = {}

        title_length['length'] = len(title)

        if title_length['length'] > 70:
            title_length['assessment'] = f'Keep titles under 70 characters. Google search previews will only display {title[0:70]}... .'

        elif title_length['length'] < 70:
            title_length['assessment'] = 'This title is a good length.'
        return title_length

    
    def get_title_matches(self, title, url, node_id):
        """
        Checks if the title is a close match for other titles on Mass.gov
        """
        if "https://" in url:
            url = url.replace("https://",'')
        # Remove the current page so we don't have to worry about returning it as a "match"
        remove_submitted_page_df = self.titles_df[self.titles_df['node_id'] != node_id]

        titles_list = list(remove_submitted_page_df['title'])
        watched_titles = []
        title_matches = {}

        # Build a data structure that includes the titles and paths of pages that are similar to the submitted one.
        # We could also do the title as the key and the url as the value
        

        for item in titles_list:
            # compare all the titles to the current page's title. Only keep the ones that are matches of 75 or higher.
            if fuzz.ratio(title.lower(),item.lower()) >= 75:
                watched_titles.append(item)

        # filter the data down to just the similar pages
        remove_submitted_page_df = remove_submitted_page_df[remove_submitted_page_df['title'].isin(watched_titles)]
        just_title_path = remove_submitted_page_df[['title','node_path']]

        similar_titles = dict(just_title_path.values)                
        
        #TODO Labor Market Information Statistics showed up once but then not again on subsequent searches for "labor market information" (the score is 81, and we changed the threshold from 70 to 75)
        #TODO maybe add stem match

        title_matches['total'] = len(similar_titles.keys())
        
        if  title_matches['total'] < 1:
            title_matches['assessment'] = 'This title is unique among Mass.gov page titles.'
        elif title_matches['total'] >= 1:
            title_matches['assessment'] = "Use a phrase that summarizes the purpose of the page using words your audience will know."

        title_matches['title_matches'] = similar_titles
        return title_matches

    def acronym_checker(self, title):
        """
        Checks for acronyms. Does not count capital letters inside parenthesis, as it assumes those are being spelled out elsewhee.
        """
        sequence_count = 0
        max_count = 0
        parens_flag = False

        for char in [i for i in title if i not in [',','.','"',"'"]]:
            if char == ')' and parens_flag is True:
                parens_flag = False
            elif char == '(':
                parens_flag = True
            
            if parens_flag is True:
                pass
            elif char.isupper():
                sequence_count += 1
            else:
                sequence_count = 0
            
            if sequence_count > max_count:
                max_count = sequence_count

        acronym_check = {'acronym_checker': max_count}

        if max_count > 1:
            acronym_check['assessment'] = 'It looks like your title has an acronym. To help users & search engines find your content, spell out the acronym or rewrite the title. You can include the acronym in parentheses, e.g. Labor Market Information (LMI).'
            # MassDEP Permitting & Reporting
        else:
            acronym_check['assessment'] = ''

        
        # print(f'Found sequence of {max_count} capital letters.')
        return acronym_check

    # from GSBS: noun stacking, trouble words, conjunction count > 2, noun/adjective pairs
    # check if title includes an org name
        



if __name__ == "__main__":
    tf = TitleEvalutor()
    
    x = tf.evaluator("you and me and us make three as well as coffee cup mug mug", "www.com.")
    print(x)

    