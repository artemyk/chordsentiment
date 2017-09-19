notes     = ['A','B','C','D','E','F','G']
flats     = [n+'b' for n in notes]
sharps    = [n+'#' for n in notes]
all_notes = notes + flats + sharps

sfx2type = {}
sfx2type['']     = 'major'
sfx2type['M']    = 'major'
sfx2type['maj']  = 'major'
sfx2type['m']    = 'minor'
sfx2type['min']  = 'minor'
sfx2type['+']    = 'aug'
sfx2type['aug']  = 'aug'
sfx2type['o']    = 'dim'
sfx2type['dim']  = 'dim'
sfx2type['5']    = 'power'
sfx2type['M6']   = 'major6'
sfx2type['maj6'] = 'major6'
sfx2type['m6']   = 'minor6'
sfx2type['min6'] = 'minor6'
sfx2type['7']    = 'dom7'
sfx2type['dom7'] = 'dom7'
sfx2type['M7']   = 'major7'
sfx2type['maj7'] = 'major7'
sfx2type['m7']   = 'minor7'
sfx2type['min7'] = 'minor7'
sfx2type['+7']   = 'aug7'
sfx2type['aug7'] = 'aug7'
sfx2type['o7']   = 'dim7'
sfx2type['dim7'] = 'dim7'

std_names = {'major':'', 'minor':'m','aug':'aug','dim':'dim',
             'power':'5',
             'major6':'6','minor6':'m6',
             'dom7':'7','major7':'M7','minor7':'m7','aug7':'aug7','dim7':'dim7',
             'INVALID':'INVALID'}

lookup_stdnames = {}
lookup_roots    = {}
lookup_cats     = {}
for root in (sharps + flats + notes):
    for catsfx, cat in sfx2type.items():
        for k in (root+catsfx, root+catsfx+'*'):
            lookup_stdnames[k] = root + std_names[cat]
            lookup_roots[k]    = root
            lookup_cats[k]     = cat


"""
def chord_root_and_type(chord):
    return lookup_rootcats.get(chord, ('INVALID','INVALID'))

def chord_root_and_type(chord):
    if chord == 'INVALID' or not isinstance(chord, str):
        return 'INVALID', 'INVALID'

    root = None
    for n in (sharps + flats + notes):
        if chord.startswith(n):
            root = n
            break

    if root is None:
        return 'INVALID', 'INVALID'

    sfx = chord[len(root):]
    if len(sfx)>=1 and sfx[-1] == '*':
        sfx = sfx[:-1]

    if sfx not in sfx2type:
        return 'INVALID', 'INVALID'
    else:
        return root, sfx2type[sfx]

def chord2root(chord):
    return lookup_roots.get(chord, 'INVALID')
    #return chord_root_and_type(chord)[0]
def chord2type(chord):
    return lookup_cats.get(chord, 'INVALID')
    #return chord_root_and_type(chord)[1]
def stdname(chord):
    root, cat = chord_root_and_type(chord)
    if root == 'INVALID': 
        return 'INVALID'
    return root + std_names[cat]
"""

if __name__ == '__main__':

    to_test = ['Amin','Am','AM','A*','A7*','A#aug','BbM7', 'GM','Gmaj7','G5', 'blah','INVALID']

    for t in to_test:

        print('Chord %5s mapped to root=%2s, type=%6s, stdname=%5s' %
              (t, lookup_roots.get(t,'INVALID'), lookup_cats.get(t,'INVALID'), lookup_stdnames.get(t,'INVALID')))
