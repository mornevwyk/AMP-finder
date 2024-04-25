from Bio import SeqIO
import pandas as pd
from PyBioMed.Pyprotein import CalculateAAComposition, CalculateDipeptideComposition, CalculateCTD, GetAPseudoAAC
from sklearn.feature_selection import VarianceThreshold
import urllib.request

url_file_name = [
    ["https://raw.githubusercontent.com/dataprofessor/AMP/main/train_po.fasta", "train_data/train_po.fasta"],
    ["https://raw.githubusercontent.com/dataprofessor/AMP/main/train_ne.fasta", "train_data/train_ne.fasta"],
    ["https://raw.githubusercontent.com/dataprofessor/AMP/main/test_ne.fasta", "test_data/test_ne.fasta"],
    ["https://raw.githubusercontent.com/dataprofessor/AMP/main/test_po.fasta", "test_data/test_po.fasta"]
]

def import_data():
    for url, file_name in url_file_name:
        urllib.request.urlretrieve(url, file_name)

def parse_sequences(file_in):
    parse = SeqIO.parse(file_in, "fasta")
    sequences = []
    for seq in parse:
        sequences.append(str(seq.seq))

    return sequences



def prep_data(seq_po, seq_ne, feature_fun = [], verbose=False):
    '''
        Prepares the data for the model. Gets the features for each feature_fun from each sequence in deq_po and deq_ne and adds the activity feature as 1 to seq_po and 0 to seq_ne. Returns a concatenated dataframe with all the data features.
    '''
    out = []
    
    for seq in seq_po:
        seq_features = {}
        for func in feature_fun:
            seq_features |= func(seq)
        seq_features |= {'activity': 1}
        out.append(seq_features)
    
    for seq in seq_ne:
        seq_features = {}
        for func in feature_fun:
            seq_features |= func(seq)
        seq_features |= {'activity': 0}
        out.append(seq_features)

    if verbose:
        print(f"Extraced {len(out[0])} features from {len(out)} sequences")

    return pd.DataFrame(out)

def pseudoAAC(seq):
    return GetAPseudoAAC(seq, 1)

def select_features(data):
    fs = VarianceThreshold(threshold=0.1)
    fs.fit(data)
    return fs.get_support()


def filter_features(data, feature_bool):
    return data.loc[:, feature_bool]



def encode_aa(seq, max_len):
    dic = {'A':1, 'R':2, 'N':3, 'D':4, 'C':5, 'E':6, 'Q':7, 'H':8, 'I':9, 'L':10, 'K':11, 'M':12, 'F':13, 'P':14, 'S':15, 'T':16, 'W':17, 'Y':18, 'V':19, 'G':20}
    encode = []
    for i in range(max_len):
        e = [0]*20
        if i < len(seq):
            pos = dic[str(seq[i])]
            e[pos-1] = 1
        encode.append(e)
    return {'code':encode}


