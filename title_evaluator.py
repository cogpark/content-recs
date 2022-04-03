import pandas as pd
from fuzzywuzzy import fuzz
from sentence_evaluator import SentenceEvaluator


class TitleEvalutor:

    def __init__(self): 
        self.titles_df = pd.read_csv('titles_urls.csv', usecols=['node_id', 'title','is_published','node_path'])
        self.sample_df = self.titles_df[0:5000]
        #self.evaluator = SentenceEvaluator()
        return

    def evaluator(self, title):
        evaluation = {}

        evaluation['title'] = title
        evaluation['title_length'] = self.check_title_length(title)
        evaluation['title_matches'] = self.get_title_matches(title)
        evaluation['acronym_checker'] = self.acronym_checker(title)

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

    
    def get_title_matches(self, title):
        """
        Checks if the title is a close match for other titles on Mass.gov
        """
        # TODO Also get links and return those too
        titles_list = list(self.titles_df['title'])
        title_matches = {}
        similar_titles = {}

        for item in titles_list:
            if fuzz.ratio(title,item) > 75:
                similar_titles[item] = fuzz.ratio(title.lower(), item.lower())
        
        #TODO Labor Market Information Statistics showed up once but then not again on subsequent searches for "labor market information" (the score is 81, and we changed the threshold from 70 to 75)
        #TODO maybe add stem match

        title_matches['total'] = len(similar_titles.keys())
        print(similar_titles)
        
        if  title_matches['total'] < 1:
            title_matches['assessment'] = 'This title is unique among Mass.gov page titles.'
        elif title_matches['total'] >= 1:
            title_matches['assessment'] = "There are other pages with titles like this on Mass.gov. Use a phrase that summarizes the purpose of the page as succinctly as possible using words your audience will know."

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

        



if __name__ == "__main__":
    tf = TitleEvalutor()
    
    tf.get_title_matches(title="Natural Gas Industry")