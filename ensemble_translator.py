__author__ = 'maximkuleshov'

ensp_f = open('translation/ENSP.tsv', 'r').readlines()
ensp_d = dict()
for line in ensp_f:
    gene, id = line.strip().split()
    ensp_d[id] = gene

ensg_f = open('translation/ENSG.tsv', 'r').readlines()
ensg_d = dict()
for line in ensg_f:
    gene, id = line.strip().split()
    ensg_d[id] = gene


enst_f = open('translation/ENST.tsv', 'r').readlines()
enst_d = dict()
for line in enst_f:
    gene, id = line.strip().split()
    enst_d[id] = gene


def ens(gene):
    if gene[0:4] == 'ENSP':
        return ensp_d.get(gene)
    if gene[0:4] == 'ENSG':
        return ensg_d.get(gene)
    if gene[0:4] == 'ENST':
        return ensp_d.get(gene)
    return gene


def main():
    return None


if __name__ == '__main__':
    main()