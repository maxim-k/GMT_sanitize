__author__ = 'maximkuleshov'

from collections import defaultdict
from ensemble_translator import ens


def super_strip(name):
    name = name.strip()
    name = '_'.join(name.split())
    return name


def remove_postfix(gene):
    gene = gene.split('.')[0]
    gene = gene.split('_')[0]
    return gene


def translate_ens(gene):
    if len(gene) > 10 and gene[0:3] == 'ENS':
        return ens(gene)
    return gene


def remove_excel_dates(term_genes):
    clean = []
    for gene in term_genes:
        if (len(gene.split('-')) == 2)and(gene.split('-')[0].isdigit())and(len(gene.split('-')[1])==3):
            pass
        else:
            clean.append(gene)
    return clean


def collapse_duplicate_genes(term_genes):
    term_genes = [translate_ens(remove_postfix(super_strip(gene))) for gene in term_genes]
    genes = set()
    for gene in term_genes:
        if gene:
            genes.add(gene)
    return sorted(list(genes))


def collapse_duplicate_terms(gmt_dict):
    """
    Think twice before use it. Sometimes duplicate terms have different genes.
    """
    for term in gmt_dict.keys():
        collapsed = set()
        if len(gmt_dict[term]) > 1:
            for termn in gmt_dict[term]:
                collapsed = collapsed.union(set(termn.strip().split('\t')))
            gmt_dict[term] = sorted(list(collapsed))
    return gmt_dict


def main():
    gmt = open('gmt_in/human_disease_filtered.gmt', 'r')
    gmt_clean = defaultdict(list)
    for line in gmt.readlines():
        term = super_strip(line.split('\t')[0])
        desc = line.split('\t')[1]
        genes = collapse_duplicate_genes(line.split('\t')[2:])
        genes = remove_excel_dates(genes)
        genes = '\t'.join(genes)
        gmt_clean[term].append(genes)
    gmt_clean = collapse_duplicate_terms(gmt_clean)
    gmt_clean = ['{0}\t\t{1}'.format(term, '\t'.join(gmt_clean[term])) for term in gmt_clean.keys()]
    gmt_clean_file = open('gmt_out/human_disease_filtered.gmt', 'w')
    gmt_clean_file.write('\n'.join(sorted(gmt_clean)))
    return None


if __name__ == '__main__':
    main()