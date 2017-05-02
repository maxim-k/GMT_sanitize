__author__ = 'maximkuleshov'

from string import punctuation
from ensemble_translator import ens


def super_strip(name):
    name = name.strip()
    name = '_'.join(name.split())
    return name


def remove_postfix(gene):
    gene = gene.split('.')[0]
    gene = gene.split('_')[0]
    return gene


def check_name(gene):
    # If gene name is Ensembl id
    if len(gene) > 10 and gene[0:3] == 'ENS':
        if not ens(gene):
            print('{0} is non-translating Ensamble id'.format(gene))
        return ens(gene)
    # If gene name is numerical
    if gene.isdigit():
        print('{0} is numerical'.format(gene))
        return None
    if (len(gene) == 5)and(gene[0].isdigit())and(gene[1] == '-'):
        print('{0} is date'.format(gene))
    # If gene name contains special characters
    wrong_chars = set(gene).intersection(punctuation)
    if wrong_chars:
        if (len(wrong_chars) == 1)and(list(wrong_chars)[0] != '-'):
            return None
    return gene


def check_term_name(term):
    intersect = set(term).intersection(punctuation)
    if (len(intersect) > 0)and(intersect - {'.', ',', '_', '-', '(', ')', '&'}):
        pass
        # print(term)
    return None


def find_duplicate_terms(gmt):
    terms_list = []
    for line in gmt:
        term = line.split('\t')[0]
        term = super_strip(term)
        terms_list.append(term)

    terms = set()
    for term in terms_list:
        if term in terms:
            print('{0} is duplicate'.format(term))
        terms.add(term)
    if len(terms_list) != len(terms):
        print('Found {0} duplicates\n\n\n'.format(len(terms_list) - len(terms)))
    return None


def find_duplicate_genes(term, term_genes):
    term_genes = [remove_postfix(super_strip(gene)) for gene in term_genes]
    genes = set()
    for gene in term_genes:
        if gene in genes:
            print('{0} is duplicate'.format(gene))
        check = check_name(gene)
        if check:
            genes.add(gene)
    if len(term_genes) != len(genes):
        print('Found {0} duplicates in term {1}'.format(len(term_genes) - len(genes), term))
    return None


def main():
    gmt = open('gmt_in/human_disease_filtered.gmt', 'r').readlines()
    find_duplicate_terms(gmt)

    for line in gmt:
        term = super_strip(line.split('\t')[0])
        check_term_name(term)
        genes = line.split('\t')[2:]
        find_duplicate_genes(term, genes)
    return None


if __name__ == '__main__':
    main()