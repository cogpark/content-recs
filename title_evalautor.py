import pandas as pd
from fuzzywuzzy import fuzz



class TitleEvalutor:

    def __init__(self): 
        titles_df = pd.read_csv('titles_urls.csv', usecols=['node_id', 'title','is_published','node_path'])
        self.sample_df = titles_df[0:1000]
        return

    # Rules
    
    def check_title_length(self, title):
        """
        Checks the length of a title.
        """
        length = len(title)
        if length > 70:
            reason = 'This title is longer than Google search previews allow'
        elif length < 70:
            pass
        
        return [length, reason]
    
    def get_title_matches(self, title):
        """
        Checks if the title is a close match for other titles on Mass.gov
        """
        print(self.sample_df)
        titles_list = list(self.sample_df['title'])
        similar_titles = {}
        for item in titles_list:
            if fuzz.ratio(title,item) > 50:
                similar_titles[item] = fuzz.ratio(title, item)
        
        print(similar_titles)


if __name__ == "__main__":
    tf = TitleEvalutor()
    
    tf.get_title_matches(title="grant recipients")