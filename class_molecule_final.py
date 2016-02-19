import re   # regexp knihovna


class Molecule(object):
           
    def __init__(self, vzorec):
        self.vzorec = vzorec
        
        self.slovnik = {}
        
        # právě jedno velký písmeno + 0 nebo 1 malý písmeno + 0-mnoho čísel ve dvou skupinách (1)(2)
        pattern = re.compile(r"([A-Z][a-z]?)([0-9]*)")
                        
        # pattern.finditer(vzorec) - iterátor nad nalezenými shodami regexpu
        for match in pattern.finditer(vzorec): # každej match je objekt, na kterým se dají volat různý metody
            # vkládání do slovníku => 1 pokud je match-objekt.group(2) prázdný, pokud není prázdný, tak jeho obsah
            self.slovnik[match.group(1)] = 1 if len(match.group(2)) == 0 else int(match.group(2))

        #print(self.slovnik)
        
        # sós: http://www.ciaaw.org/atomic-weights.htm
        self.mw_dict = {'Mt': False, 'Fe': 55.845, 'Es': False, 'Hg': 200.592, 'Fm': False, 'Fl': False, 'Fr': False, 'Lr': False,
                'Rf': False, 'Re': 186.207, 'He': 4.002602, 'Au': 196.966569, 'Uup': False, 'No': False, 'Lv': False,
                'Pa': 231.03588, 'Yb': 173.045, 'Se': 78.971, 'V': 50.9415, 'C': 12.0096, 'Sn': 118.71, 'Ga': 69.723, 'Rn': False,
                'Bk': False, 'Tb': 158.92535, 'Lu': 174.9668, 'La': 138.90547, 'Sb': 121.76, 'Bi': 208.9804, 'Db': False, 'Gd': 157.25,
                'Cr': 51.9961, 'Eu': 151.964, 'Zn': 65.38, 'Y': 88.90584, 'Ce': 140.116, 'Cl': 35.446, 'I': 126.90447, 'Ac': False,
                'Na': 22.98976928, 'Tm': 168.93422, 'Si': 28.084, 'Ho': 164.93033, 'Cs': 132.90545196, 'Co': 58.933194, 'Ca': 40.078,
                'Xe': 131.293, 'O': 15.99903, 'Bh': False, 'Te': 127.6, 'Pr': 140.90766, 'In': 114.818, 'Rb': 85.4678, 'N': 14.00643,
                'Mn': 54.938044, 'Ti': 47.867, 'Rg': False, 'Cu': 63.546, 'B': 10.806, 'K': 39.0983, 'Tl': 204.382, 'Hf': 178.49,
                'W': 183.84, 'Sc': 44.955908, 'Ni': 58.6934, 'S': 32.059, 'Sr': 87.62, 'Pb': 207.2, 'Mg': 24.304, 'Er': 167.259,
                'Ir': 192.217, 'Tc': False, 'Sm': 150.36, 'Pu': False, 'Mo': 95.95, 'Zr': 91.224, 'Uut': False, 'At': False, 'Rh': 102.9055,
                'Hs': False, 'Ar': 39.948, 'H': 1.00784, 'Ds': False, 'As': 74.921595, 'Cn': False, 'Uuo': False, 'Al': 26.9815385,
                'Md': False, 'Cm': False, 'U': 238.02891, 'Ag': 107.8682, 'Nd': 144.242, 'Cf': False, 'Uus': False, 'Dy': 162.5, 'Am': False,
                'Os': 190.23, 'Po': False, 'Nb': 92.90637, 'Ru': 101.07, 'Kr': 83.798, 'Br': 79.901, 'Sg': False, 'P': 30.973761998,
                'Ra': False, 'Li': 6.938, 'Pm': False, 'Pt': 195.084, 'Cd': 112.414, 'F': 18.998403163, 'Ta' : 180.94788, 'Th': 232.0377,
                'Ne': 20.1797, 'Ba': 137.327, 'Pd': 106.42, 'Ge': 72.63, 'Be': 9.0121831, 'Np': False}
    
        
    
    def atom_count(self, prvek=""):
        # není definován prvek, vrať součet všech atomů
        if prvek == "":
            counter = 0
            for i in self.slovnik:
                counter += self.slovnik[i]
            return counter
        # vrať počet výskytů prvku
        elif prvek in self.slovnik:
            return self.slovnik[prvek]
        
        # prvek není ve slovníku/vzorci, vrať 0
        elif prvek not in self.slovnik:
            print(prvek + " not in the summary formula.")
            return 0
    
    def summary_formula(self):
        return self.vzorec
    
    def molecular_weight(self):
        vzorec_mw = 0
        for atom in self.slovnik:
            #print("a: ", atom)
            mol_weight = self.mw_dict[atom]
            #print("mw: ", mol_weight)
            # False počítá jako nulu, ale je asi dobrý dát uživatelovi vědět
            if mol_weight == False:
                print("Unknown molecular weight (" + atom + "), counting as 0.")
            
            # přičítání molekulární hmotnosti
            vzorec_mw += mol_weight * self.slovnik[atom]
            #print("vzorec_mw", vzorec_mw)
        return vzorec_mw
            
            
            
mol = Molecule("H2O")
print("voda")
print(mol.atom_count())
print(mol.atom_count("H"))
print(mol.atom_count("O"))
print(mol.molecular_weight())
print(mol.summary_formula())
print()
print()
print("methionine")
methionine = Molecule("C5H11NO2S")
print(methionine.summary_formula())
print(methionine.atom_count())
print(methionine.atom_count("N"))
print(methionine.atom_count("Cl"))
print(methionine.molecular_weight())


