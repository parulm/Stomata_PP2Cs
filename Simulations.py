import boolean2
from boolean2 import util
import json

text = file('rules_reduced.booleannet').read()
repeat = 4500
steps = 50
print len(text)


def runSimulations(knockouts=True):
    print "starting Simulations"
    data = {}
    #use the following set of targets if running the simulation for the reduced model
    #targets = ['NOGC1', 'PLDdel', 'InsP3', 'nitrocGMP', 'CIS', 'Actin', 'AnionEM', 'K_efflux', 'PP2CA', 'H2O_Efflux', 'DAG', 'NO', 'pHc', 'PEPC', 'HAB1', 'PA', 
    #'PLDa', 'PLC', 'PI3P5K', 'OST1', 'SLAH3', 'ABA', 'H_ATPase', 'Malate', 'KOUT', 'Depolarization', 'QUAC1', 'CaIM', 'TCTP', 'AtRAC1', 'SPHK12', 'Ca_ATPase', 
    #'CPKa', 'CPKb', 'ABI2', 'Microtubule_Depolymerization', 'Ca', 'ABI1', 'NIA12', 'MPK', 'RCARs', 'VATPase', 'Vacuolar_Acidification', 'ROP11', 'RBOH', 'KEV', 
    #'GHR1', 'SLAC1', 'WT']
    
    #use the following set of targets when running the simulation for the full model
    #targets = ['CPK321', 'H_ATPase', 'NOGC1', 'ABA', 'Microtubule_Depolymerization', 'Depolarization', 'InsP3', 'SPHK12', 'ABH1', 'InsP6', 'CIS', 'AnionEM', 
    #'GAPC12', 'K_efflux', 'H2O_Efflux', 'VPPase', 'PP2CA', 'MRP5', 'CPK23', 'Vacuolar_Acidification', 'DAG', 'ROP11', 'NO', 'pHc', 'PIP', 'PEPC', 'nitrocGMP', 
    #'HAB1', 'DAGK', 'PLDdel', 'PC', 'CPK6', 'PA', 'PLDa', 'PLC', 'PI3P5K', 'ROS', 'AtRAC1', 'OST1', 'cGMP', 'Ca2_ATPase', 'GCR1', 'RCN1', 'QUAC1', 'S1P', 
    #'Malate', 'KOUT', 'NADPH', 'MPK912', 'KEV', 'SCAB1', 'CaIM', 'TCTP', 'VATPase', 'GPA1', 'PtdIns35P2', 'GTP', 'GEF', 'ARP_Complex', 'PtdInsP4', 'Sph', 
    #'ABI1', 'NIA12', 'ADPRc', 'RCARs', 'PtdInsP3', 'Nitrite', 'ABI2', 'SPP1', 'RBOH', 'Actin_Reorganization', 'ERA1', 'NtSyp121', 'Ca2', 'GHR1', 'cADPR', 
    #'SLAH3', 'SLAC1', 'WT', 'PtdIns45P2']
    
    for target in targets:
    	print 'Processing target', target
        if knockouts is True:
            mtext = boolean2.modify_states(text=text, turnoff=target)
            fname = 'results_KO.json'
        else:
            mtext = boolean2.modify_states(text=text, turnon=target)
            fname = 'results_CA.json'
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
    #set knockouts = True for KO of each node in the list targets
    #set knockouts = False for CA of each node in the list targets
    runSimulations(knockouts=True)
