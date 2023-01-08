import sys
import os
import string
from collections import Counter

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def get_tokens(text):
    tokens = text.split()
    normalized_tokens = []
    for token in tokens:
        normalized_token = token.lower().strip(string.punctuation)
        if normalized_token:
            normalized_tokens.append(normalized_token)
    return normalized_tokens

def get_levenshtein_distance(s1, s2):
    if not s1: return len(s2)
    if not s2: return len(s1)
    if s1[0] == s2[0]:
        return get_levenshtein_distance(s1[1:], s2[1:])
    else:
        return 1 + min(
            get_levenshtein_distance(s1[1:], s2),
            get_levenshtein_distance(s1, s2[1:]),
            get_levenshtein_distance(s1[1:], s2[1:])
        )

def compare(filename1, filename2):
    text1 = read_file(filename1)
    text2 = read_file(filename2)
    tokens1 = get_tokens(text1)
    tokens2 = get_tokens(text2)
    distance = get_levenshtein_distance(tokens1, tokens2)
    max_distance = max(len(tokens1), len(tokens2))
    similarity = 1 - distance / max_distance
    return similarity

def read_pairs(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        pairs = []
        for line in lines:
            pair = tuple(line.strip().split(','))
            pairs.append(pair)
        return pairs

def write_similarities(pairs, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as f:
        for pair in pairs:
            similarity = compare(*pair)
            f.write(f'{pair[0]},{pair[1]},{similarity}\n')

def main():
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    pairs = read_pairs(input_filename)
    write_similarities(pairs, output_filename)

if __name__ == '__main__':
    main()