from amino_acid import amino_code, amino_code_r

class PdbInfo():
    '''Get residue infomation from pdb file. 
    '''

    def __init__(self, pdbname):
        self._pdbname = pdbname
        self._rawinfo = open(self._pdbname, 'r').readlines()
        self.get_seq()
        self.get_residue()
        self.get_missing_residue()

    def get_seq(self):
        self._seq = {}
        for rawline in self._rawinfo:
            if rawline.startswith('SEQRES'):
                tokens = rawline.strip().split()
                chain_id = tokens[2]
                res_3l = tuple(tokens[4:])
                res_1l = [amino_code[i] for i in res_3l]
                self.add_dict_data(self._seq, 'extend', chain_id, res_3l)

        # for i in self._seq.values():
        #     print(len(i))

    def get_missing_residue(self):
        self.missing_residue = {}
        record = False
        for rawline in self._rawinfo:
            if rawline.startswith('REMARK 465'):
                line = rawline.strip()
                if line.endswith('SSSEQI'):
                    record = True
                elif record:
                    res_name = line[15:18]
                    # res_name = tokens[2]
                    # chain_id = tokens[3]
                    chain_id = line[19]
                    res_seq = int(line[21:26])
                    self.add_dict_data(self.missing_residue, 'append', chain_id, (res_seq, res_name))

    def add_dict_data(self, d, func_type, chain_id, data):
        if chain_id not in d.keys():
            d[chain_id] = []
        getattr(d[chain_id], func_type)(data)

    def get_residue(self):
        self.residue = {}
        for rawline in self._rawinfo:
            if rawline.startswith('ATOM'):
                line = rawline.strip()
                atom_name = line[12:16].strip()
                if atom_name == 'CA':
                    res_name = line[17:21].strip()
                    res_seq = int(line[22:26])
                    chain_id = line[21]
                    self.add_dict_data(self.residue, 'append', chain_id, (res_seq, res_name))
                    # if chain_id not in self.residue.keys():
                    #     self.residue[chain_id] = []
                    # self.residue[chain_id].append([res_seq, res_name])
