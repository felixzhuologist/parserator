#!/usr/bin/python
# -*- coding: utf-8 -*-

def template():

    return """\
import os
from training import train
import pycrfsuite
import warnings
from collections import OrderedDict
import parserator


class Parser(parserator.Parser):

    #  _____________________
    # |1. CONFIGURE LABELS! |
    # |_____________________| 
    #     (\__/) || 
    #     (•ㅅ•) || 
    #     / 　 づ
    LABELS = [] # The labels should be a list of strings

    TRAINING_DATA_DIR = os.path.split(os.path.abspath(__file__))[0] + '/../MODULENAME_data/labeled_xml'
    UNLABELED_DATA_DIR = os.path.split(os.path.abspath(__file__))[0] + '/../MODULENAME_data/unlabeled'

    #***************** OPTIONAL CONFIG ***************************************************
    # PARENT_LABEL  = [the XML tag for each labeled string]      default: 'TokenSequence'
    # GROUP_LABEL   = [the XML tag for a group of strings]       default: 'Collection'
    # NULL_LABEL    = [the null XML tag]                         default: 'Null'
    # MODEL_FILE    = [filename for the crfsuite settings file]  default: 'learned_settings.crfsuite'
    # MODEL_PATH    = [path for the crfsuite settings file]      default: os.path.split(os.path.abspath(__file__))[0] + '/' + MODEL_FILE
    #************************************************************************************

    #  _____________________
    # |2. CONFIGURE TOKENS! |
    # |_____________________| 
    #     (\__/) || 
    #     (•ㅅ•) || 
    #     / 　 づ
    def tokenize(self, raw_string):
        # this determines how any given string is split into its tokens
        # handle any punctuation you want to split on, as well as any punctuation to capture
        
        re_tokens = # re.compile( [REGEX HERE], re.VERBOSE | re.UNICODE)
        tokens = re_tokens.findall(raw_string)

        if not tokens :
            return []
        return tokens

    #  _______________________
    # |3. CONFIGURE FEATURES! |
    # |_______________________| 
    #     (\__/) || 
    #     (•ㅅ•) || 
    #     / 　 づ
    def tokens2features(self, tokens):
        # this should call tokenFeatures to get features for individual tokens,
        # as well as define any features that are dependent upon tokens before/after
        
        feature_sequence = [self.tokenFeatures(tokens[0])]
        previous_features = feature_sequence[-1].copy()

        for token in tokens[1:] :
            # set features for individual tokens (calling tokenFeatures)
            token_features = self.tokenFeatures(token)
            current_features = token_features.copy()

            # features for the features of adjacent tokens
            feature_sequence[-1]['next'] = current_features
            token_features['previous'] = previous_features        
            
            # DEFINE ANY OTHER FEATURES THAT ARE DEPENDENT UPON TOKENS BEFORE/AFTER
            # for example, a feature for whether a certain character has appeared previously in the token sequence
            
            feature_sequence.append(token_features)
            previous_features = current_features

        if len(feature_sequence) > 1 :
            # these are features for the tokens at the beginning and end of a string
            feature_sequence[0]['rawstring.start'] = True
            feature_sequence[-1]['rawstring.end'] = True
            feature_sequence[1]['previous']['rawstring.start'] = True
            feature_sequence[-2]['next']['rawstring.end'] = True

        else : 
            # a singleton feature, for if there is only one token in a string
            feature_sequence[0]['singleton'] = True

        return feature_sequence

    def tokenFeatures(self, token) :
        # this defines a dict of features for an individual token

        features = {   # DEFINE FEATURES HERE. some examples:
                        'length': len(token),
                        'case'  : casing(token),
                    }

        return features

    # define any other methods for features. this is an example to get the casing of a token
    def casing(self, token) :
        if token.isupper() :
            return 'upper'
        elif token.islower() :
            return 'lower' 
        elif token.istitle() :
            return 'title'
        elif token.isalpha() :
            return 'mixed'
        else :
            return False
"""
