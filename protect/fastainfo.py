class FastaInfo():
    '''
    Get sequence infomation from fasta file.
    '''
    def __init__(self, fastaname):
        self._fastaname = fastaname
        self._rawinfo = open(self._fastaname, 'r').readlines()
        self.get_seq()

    def get_seq(self):
        self.seq = []
        seq = ''
        for rawline in self._rawinfo:
            line = rawline.strip()
            if len(line) == 0:
                continue
            if line.startswith('>'):
                if len(seq) != 0:
                    self.seq.append(seq)
                    seq = ''
            else:
                seq += line
        if len(seq) != 0:
            self.seq.append(seq)