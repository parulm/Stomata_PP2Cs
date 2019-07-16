import boolean2
from boolean2 import util
import json

text = file('ABANewDraft.txt').read()
repeat = 2500
steps = 50
print len(text)


def runSimulations(knockouts=True):
    print "starting Simulations"
    data = {}
    targets = ['Actin', 'WT']
    #targets = ['SPHK12', 'RCARs', 'TCTP', 'OST1', 'PA', 'PLDa', 'Microtubule_Depolymerization', 'NOGC1', 'pHc', 'ROP11', 'ABI2', 'H_ATPase', 'PP2CA', 'AtRAC1', 'ABI1', 'GPA1', 'CaIM']
    #targets = ['SPHK12', 'HAB1', 'ABI1', 'ABI2', 'NIA12', 'CPKb', 'InsP3', 'NOGC1', 'VATPase', 'NO', 'ROP11', 'PP2CA', 'NOGC1', 'QUAC1', 'PLC', 'PLDa', 'PI3P5K', 'CIS', 'nitrocGMP', 
    #			'SLAH3', 'Vacuolar_Acidification', 'pHc', 'CaIM', 'MPK', 'GHR1', 'SLAC1', 'RBOH', 'PA', 'Actin', 'PLDdel', 'Microtubule_Depolymerization', 'K_efflux', 
    #			'KOUT', 'OST1', 'RCARs', 'Ca']
    print len(targets)
    #ntext = boolean2.modify_states(text=text, turnon='ABA')
    #text = ntext
    for target in targets:
    	print 'Processing target', target
        if knockouts is True:
            mtext = boolean2.modify_states(text=text, turnoff=target)
            fname = 'knockouts_actin.json'
        else:
            mtext = boolean2.modify_states(text=text, turnon=target)
            fname = 'WT_actin.json'
        model = boolean2.Model(mode='async', text=mtext)
        coll = util.Collector()
        for i in xrange(repeat):
            model.initialize(missing=util.randbool)
            model.iterate(steps=steps)
            coll.collect(states=model.states, nodes='Closure')
        data[target] = {'Timesteps': coll.get_averages(normalize=True)}
        data[target]['Closure AUC'] = sum(data[target]['Timesteps']['Closure'])
    with open(fname, 'w') as fp:
        json.dump(data, fp)

if __name__ == '__main__':
    runSimulations(knockouts=True)
    #pass
