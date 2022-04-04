from nltk import word_tokenize, pos_tag
import re
from collections import Counter 

class SentenceEvaluator:

    def __init__(self):
        return

    def run_prod_scoring(self, sentence, dev_rules=False):
        """
        Accepts a sentence and runs through every scoring method we have.
        Returns list with 3 items: The total score, a dictionary of individual scores, and a dictionary of assessment metadata. 

        """
        assessment, metadata = {}, {}

        length_assess = self.check_sentence_length(sentence)
        assessment['length_score'] = length_assess[0] 
        metadata['length'] = length_assess[1]

        trouble_words_assess = self.get_trouble_words(sentence)
        assessment['trouble_words_score'] = trouble_words_assess[0] 
        metadata['trouble_words'] = trouble_words_assess[1]

        prep_phrases = self.count_prepositional_phrases(sentence)
        assessment['prep_phrases_score'] = prep_phrases[0] 
        metadata['prep_phrases'] = prep_phrases[1]

        conjunctions = self.count_conjunctions(sentence)
        assessment['conjunctions_score'] = conjunctions[0] 
        metadata['conjunctions'] = conjunctions[1]

        # Actually noun AND adjective pairs
        npairs = self.noun_adj_pairs(sentence)
        assessment['noun_adj_pairs_score'] = npairs[0] 
        metadata['noun_adj_pairs'] = npairs[1]

        vpairs = self.verb_pairs(sentence)
        assessment['verb_pairs_score'] = vpairs[0] 
        metadata['verb_pairs'] = vpairs[1]

        stacked = self.stacked_nouns(sentence)
        assessment['stacked_nouns_score'] = stacked[0] 
        metadata['stacked_nouns'] = stacked[1]

        long_in_clauses = self.long_introductory_clause(sentence)
        assessment['long_intro_clause_score'] = long_in_clauses[0] 
        metadata['long_intro_clause'] = long_in_clauses[1]

        repeat_words = self.count_repeat_words(sentence)
        assessment['duplicate_words_score'] = repeat_words[0] 
        metadata['duplicate_words'] = repeat_words[1]

        count_to_be_verbs = self.count_to_be_verbs(sentence)
        assessment['to_be_score'] = count_to_be_verbs[0] 
        metadata['to_be_count'] = count_to_be_verbs[1]

        count_verbs = self.count_verbs(sentence)
        assessment['verb_count_score'] = count_verbs[0] 
        metadata['verb_count'] = count_verbs[1]

        total = sum(assessment.values())
        
        return [total, assessment, metadata]

    def count_to_be_verbs(self, sentence, print_reasons=False):
        score = 0
        to_bes = ['am', 'is', 'are', 'was', 'were', 'to be']
        count_to_bes = len([word for word in sentence.split() if word in to_bes])
        
        if print_reasons:
            print(f'Sentence was {sentence}. \n Found the following instances: {[word for word in sentence.split() if word in to_bes]}')
        if count_to_bes >= 3:
            score = count_to_bes * 2
        
        if print_reasons:
            print(f'return score: {score}, and number of "to bes": {count_to_bes}')
        return [score, count_to_bes]


    # does not look at stems, only at exact repeats
    def count_repeat_words(self, sentence, print_reasons=False):
        """
        Checks to see if the sentence contains repeat words (exact copies).

        Returns 1 point for each duplicate and an additional point for triplicates (or worse).
        """
        identify_pos = pos_tag((sentence.lower()).split())
        remove_filler_words = []

        score = 0

        for i in range(len(identify_pos)):
            #  	Coordinating conjunction , prepositions, determiners
            if identify_pos[i][1] not in ['DT', 'IN', 'TO', 'CC', 'WDT']:
                remove_filler_words.append(identify_pos[i][0])
        
        # Counter is a special type of dictionary that in which 
        # the key is some datum, and value is the number that of times that datum appears
        # in the dictionary
        word_counts = Counter(remove_filler_words)
        duplicates = [word for word in word_counts.items() if word[1] >= 2]

        if print_reasons:
            print(f'duplicates in this sentence: {duplicates}')

        if len(duplicates) > 3:
            score = score + len(duplicates)
        
        triplicates = [word for word in word_counts.items() if word[1] >= 3]
        
        if print_reasons:
            print(f'triplicated (or worse) words in this sentence: {triplicates}')

        if len(triplicates) > 0:
            score = score + len(triplicates)

        if print_reasons:
            print(f'returning score: {score} \n duplicate count {len(duplicates)} \n triplicate (or more) count: {len(triplicates)}')

        return [score, len(duplicates) + len(triplicates)]

    def check_sentence_length(self, sentence, print_reasons=False):
        """
        Checks the length of a sentence (string). Scores it 6 points if it's 
        50 words or longer, 3 if it's 25 or longer, else 0.

        Returns a list that includes the score and the sentence length.
        """
        sentence = sentence.split(' ')
        length = len(sentence)
        if length >= 50:
            score = 6
        elif length >= 25:
            score = 3
        else:
            score = 0
        if print_reasons:
            print(f"Sentence is {length} words long. Scoring it: {score}.")
        return [score, length]

    def get_trouble_words(self, sentence, print_reasons=False):
        """
        Runs through a list of "trouble" words and phrases that are nearly
        always redundant or bad.

        We add 2 points for each example we find.

        Returns a list whose first entry is the the score and second the number of trouble words/phrases found.
        """
        trouble_words = {}
        sentence = sentence.lower()
        points = 2
        score = 0
        
        look_for_these_phrases = ['rules and regulation', 'necessary and required','details and information','in your possession' ]

        for phrase in look_for_these_phrases:

            if phrase in sentence:
                score = score + points 
                trouble_words[f'{phrase}'] = True
            if print_reasons:
                print(f'Score after looking for "{phrase}": {score}')

        # these are special cases 

        if re.search('(have|has) the (capacity|capability|ability)', sentence):
            match = re.search('(have|has) the (capacity|capability|ability)', sentence)
            score = score + points
            # This gets us the phrase that the regex search caught
            trouble_words[f'{sentence[match.span()[0]: match.span()[1]]}']  = True
        if print_reasons:
            print(f'Score after looking for "have the ability/capacity/capability": {score}')
        
        if re.search('utiliz', sentence):
            match = re.search('utiliz', sentence)
            score = score + points 
            trouble_words[f'{sentence[match.span()[0]: match.span()[1]]}'] = True
        if print_reasons:
            print(f'Score after looking for "utilize (and variants)": {score}')

        # "manage* and operat*"
        if re.search('(manage[a-z]*) and (operat[a-z]*)', sentence):
            match = re.search('(manage[a-z]*) and (operat[a-z]*)', sentence)
            score = score + points
            trouble_words[f'{sentence[match.span()[0]: match.span()[1]]}'] = True
        if print_reasons:
            print(f'Score after looking for "manage and operate": {score}')

        if re.search('(across|throughout) the commonwealth', sentence):
            match = re.search('(across|throughout) the commonwealth', sentence)
            score = score + points
            trouble_words[f'{sentence[match.span()[0]: match.span()[1]]}'] = True
        if print_reasons:
            print(f'Score after looking for "across the commonwealth": {score}')

        trouble_words['score'] = score

        return trouble_words

    def count_prepositional_phrases(self, sentence, print_reasons=False):
        """
        Checks how many prepositional phrases are in 
        the sentence. If there are 3 or more, we score
        the sentence as a 6, else 0.

        Returns a list whose first entry is the the score and second the number of prepositional phrases.
        """
        if print_reasons: 
            print("Prepositional phrases:")

        sentence = sentence.lower()
        score = 0
        
        pp_indexes = []
        
        identify_pos = pos_tag(sentence.split())
        
            
        
        # Locate the indices of prepositions
        for i in range(len(identify_pos)):
            # Identify prepositions
            if identify_pos[i][1] == 'IN':
                pp_indexes.append(i)
            # Check if "to" is being used as a preposition or as part of an infinitive
            elif identify_pos[i][1] == 'TO':
                if identify_pos[i+1][1] != 'VB':
                    pp_indexes.append(i)
            ###if print_reasons:
                ###print(f"identified '{identify_pos[i][0]}' as a preposition.")
        
        
        
        # determine how far away each prepositional phrase is from the next one
        #pp_distances = [y - x for x, y in zip(pp_indexes, pp_indexes[1:])]
        #if print_reasons:
            #print(f"Words separating the beginning of each prepositional phrases: {pp_distances}")
        
        #stacked_pp_count = len([i for i in pp_distances if i <= 4])
        #if print_reasons:
            #print(f"Number of prepositions that are 4 or fewer words appart: {stacked_pp_count}")
        
        if len(pp_indexes) >= 4:
            # 1 point for every prep phrase past 3
            score = len(pp_indexes) - 3
    
        if score > 0:  
            if print_reasons:
                print(f'Prepositions are at the following indices: {pp_indexes} ')
                index_location = 0
                for item in identify_pos:
                    print(index_location, item)
                    index_location = index_location + 1
                

        return [score, len(pp_indexes)]

    def count_conjunctions(self, sentence, print_reasons=False, is_title=False):
        """
        Counts how many conjunctions are in a sentence. Scores
        it 5 if there are 4 or more, else 0. If we're evaluating a title, scores 5 if there are
        2 or more, else 0

        Returns a list whose first entry is the the score and second the number of conjunctions.
        """
        conjunctions = {}
        conj_list = []

        sentence = sentence.lower()
        score = 0
        
        identify_pos = pos_tag(sentence.split())
        
        for i in range(len(identify_pos)):
            # print(identify_pos[i])
            if identify_pos[i][1] == 'CC':
                conj_list.append(identify_pos[i][0])
                if print_reasons:
                    print(f'Found a conjunction: {identify_pos[i][0]}')     
        
        if "as well as" in sentence:
            conj_list.append("as well as")
            if print_reasons:
                print(f'Found {sentence.count("as well as")} instances of "as well as"')

        if is_title is True:
            score = 5 if len(conj_list) >= 2 else 0
        else:
            score = 5 if len(conj_list) >= 4 else 0

        conjunctions['score'] = score
        conjunctions['conjunctions'] = conj_list

        return conjunctions

    def noun_adj_pairs(self, sentence, print_reasons=False):
        """
        Counts how many times "noun and noun" and "adj. and adj." 
        constructions occur in a sentence. Score 1 point if a sentence
        contains 1, scores 3 if contains more than 1, else 0.

        Returns a list whose first entry is the the score and second the number of noun or adjectve pairs.
        """
        sentence = sentence.lower()
        # Catch commas so we don't add points for pairings that span list items, i.e.
        # "The carrots, peas, and soup"
        sentence = sentence.replace(',', ' <comma>')
        fingerprint = ''
        
        identify_pos = pos_tag(sentence.split())
        for i in range(len(identify_pos)):
            if identify_pos[i][1] in ['NN', 'NNP', 'NNS', 'VBG', 'JJ', 'JJR', 'JJS', 'VBN']:
                if "<comma>" not in identify_pos[i][0]:
                    fingerprint = fingerprint + 'N,'
                else:
                    fingerprint = fingerprint + "<comma>,"

            else:
                fingerprint = fingerprint  + identify_pos[i][1] + ','
        if print_reasons:
            print(f'Fingerprint after converting all nouns and adjectives to "N" : {fingerprint}')
        # print(fingerprint)     
        pairs_count = fingerprint.count('N,CC,N')
        if pairs_count == 0:
            score = 0
        elif pairs_count == 1:
            score = 1
        else:
            score = 3  

        if print_reasons:
            print(f'Number of pairs: {pairs_count}')
        return [score, pairs_count]

    def count_verbs(self, sentence, print_reasons=False):
        """
        Counts how many verbs appear in a sentence.
        in a sentence. Scores 1 point for the third verb, and 2 for 
        every verb past that.

        Returns a list whose first entry is the the score and second the number of verb pairs.
        """

        sentence = sentence.lower()
        verb_count = 0
        
        identify_pos = pos_tag(sentence.split())
        for i in range(len(identify_pos)):
            # print(identify_pos[i])
            if identify_pos[i][1] in ['VB','VBD', 'VBP', 'VBZ']:
                verb_count = verb_count + 1
                if print_reasons:
                    print(f'Adding "{identify_pos[i][0]}" to list of verbs.')
        
        score = verb_count - 2 if verb_count > 0 else 0

        if print_reasons:
            print(f'Found {verb_count} verbs.')
        
        return [score, verb_count]

    def verb_pairs(self, sentence):
        """
        Counts how many times "verb" and "verb" constructions occur 
        in a sentence. Score 1 point if a sentence contains 1, scores 3 
        if contains more than 1, else 0.

        Returns a list whose first entry is the the score and second the number of verb pairs.
        """
        sentence = sentence.lower()
        fingerprint = ''
        
        identify_pos = pos_tag(sentence.split())
        for i in range(len(identify_pos)):
            # print(identify_pos[i])
            if identify_pos[i][1] in ['VB','VBD', 'VBP', 'VBZ']:
                fingerprint = fingerprint + 'V,'
            else:
                fingerprint = fingerprint + identify_pos[i][1] + ','
        
        # print(fingerprint)
        
        pairs_count = fingerprint.count('V,CC,V')
        # print(pairs_count)
        
        if pairs_count == 0:
            score = 0
        elif pairs_count == 1:
            score = 1
        else:
            score = 3

        return [score, pairs_count]

    def stacked_nouns(self, sentence, print_reasons=False):
        """
        Counts how often sentences include constructions composed of
        many nouns in a row. Scores 2 if it finds 1 stack of nouns, 
        4 if it contains more than 1 stack, else 0.

        """

        fingerprint = ''
        
        identify_pos = pos_tag(sentence.split())
        print(identify_pos)
        for i in range(len(identify_pos)):
           
            if identify_pos[i][1] in ['NN', 'NNP', 'NNS', 'VBG', 'VBN']:
                fingerprint = fingerprint + 'N,'
            else:
                fingerprint = fingerprint  + identify_pos[i][1] + ','
        if print_reasons:
            print(fingerprint)
        # print(fingerprint)
        stack_count = fingerprint.count('N,N,N,N')
        
        if stack_count == 0:
            score = 0
        elif stack_count == 1:
            score = 2
        else:
            score = 4 
        
        return [score, stack_count]

    def long_introductory_clause(self, sentence, print_reasons=False):
        """
        Tries to identify how long a sentences introductory
        clause is. Scores 2 if the introductory clause is 10
        words or longer, else 0.

        Returns a list whose first entry is the the score and second the length of the introductory clause.
        """

        sentence = sentence.lower()
        identify_pos = pos_tag(sentence.split())
        
        intro_clause = []
        
        if identify_pos[0][1] != 'IN':
            # print("Sentence doesn't begin with a conjunction")
            score = 0
        else:
            for i in range(len(identify_pos)):
                # If the word doesn't include a comma, the introductory clause isn't over
                if ',' not in identify_pos[i][0]:
                    intro_clause.append(identify_pos[i][0])
                else:
                    intro_clause.append(identify_pos[i][0])
                    break
        if print_reasons:
            print(f'Identified intro clause as {intro_clause}, which is {len(intro_clause)} words long.')     
        if len(intro_clause) > 10:
            score = 2
        else:
            score = 0
        
        return [score, len(intro_clause)]
    
