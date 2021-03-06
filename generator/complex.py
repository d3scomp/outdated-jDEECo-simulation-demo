import collections
import ast
from simple import *


def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el
            

def generate2AreasPlayground(density, cellSize,  areaSizeX, areaSizeY, margin, scale, prefix, ipCount):
    sizeX = 2*cellSize*areaSizeX + 3*margin*cellSize
    sizeY = cellSize*areaSizeY + 2*margin*cellSize
    f = open(prefix + 'site.cfg', 'w') 
    print>>f, sizeX, sizeY
    f.close()
    f = open(prefix + 'component.cfg', 'w') 
    f.close()
    fig = figure()
    area = fig.add_subplot(111, aspect='equal')
    area.set_xlim(0, sizeX*scale)
    area.set_ylim(0, sizeY*scale)
    
    
    
    
    
    savefig(prefix + "cfg.png")
    if __name__ == '__main__':
        show()
    close()
    
    

            
def generateComplexRandomConfigWithOutsiders(areaSize, extSize, scale, teamDistribution, outsideTeams, leadersDistribution, membersDistribution, othersDistribution, prefix, ipCount):
    f = open(prefix + 'site.cfg', 'w') 
    sizeX = areaSize*len(teamDistribution)*2
    sizeY = areaSize*1.5
    print>>f, sizeX, sizeY
    f.close()
    f = open(prefix + 'component.cfg', 'w') 
    f.close()
    fig = figure()
    area = fig.add_subplot(111, aspect='equal')
    area.set_xlim(0, sizeX*scale)
    area.set_ylim(0, sizeY*scale)
    diff = (sizeX - areaSize*(len(teamDistribution)))/(len(teamDistribution) + 1)
    offset = 0
    areas = []
    for i in range(0, len(teamDistribution)):
        coordX = diff*(i+1) + areaSize*i
        coordY = (sizeY - areaSize)/2
        areas.append([coordX, coordY, areaSize, areaSize])
        generateSimpleConfig("a", str(i), coordX, coordY, areaSize, extSize, scale, teamDistribution[i], leadersDistribution[i], membersDistribution[i], othersDistribution[i], prefix, ipCount[i], offset, area)
        offset = offset + sum(flatten([leadersDistribution[i], membersDistribution[i], othersDistribution[i]]))
    
    if outsideTeams:
        generateNonArealTeams(outsideTeams, sizeX, sizeY, scale, areas, leadersDistribution[len(leadersDistribution)-1], membersDistribution[len(membersDistribution)-1], othersDistribution[len(othersDistribution)-1], prefix, ipCount[len(ipCount)-1], offset, area)
    
    savefig(prefix + "cfg.png")
    if __name__ == '__main__':
        show()
    close()

def generateComplexRandomConfig(areaSize, extSize, scale, teamDistribution, leadersDistribution, membersDistribution, othersDistribution, prefix, ipCount):
    f = open(prefix + 'site.cfg', 'w') 
    sizeX = areaSize*len(teamDistribution)*3*scale
    sizeY = areaSize*len(teamDistribution)*3*scale
    print>>f, sizeX, sizeY
    f.close()
    f = open(prefix + 'component.cfg', 'w') 
    f.close()
    fig = figure()
    area = fig.add_subplot(111, aspect='equal')
    area.set_xlim(0, sizeX)
    area.set_ylim(0, sizeY)
    diff = extSize - areaSize
    offset = 0;
    for i in range(0, len(teamDistribution)):
        generateSimpleConfig("a", str(i), diff+(i+1)*areaSize*2, diff+(i+1)*areaSize*2, areaSize, extSize, scale, teamDistribution[i], leadersDistribution[i], membersDistribution[i], othersDistribution[i], prefix, ipCount[i], offset, area)
        offset = offset + sum(flatten([leadersDistribution[i], membersDistribution[i], othersDistribution[i]]))
    savefig(prefix + "cfg.png")
    if __name__ == '__main__':
        show()
    close()
# call this as python gen_for_gossip_eval.py -l <num leaders> -m <num members> -o <num others>
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-l", "--leaders", dest="numLeaders",
                      help="leaders distribution")
    parser.add_option("-m", "--members", dest="numMembers",
                      help="members distribution")
    parser.add_option("-o", "--others", dest="numOthers",
                      help="others distribution")
    parser.add_option("-p", "--path", dest="prefix",
                      help="output file prefix (including path)")
    parser.add_option("-i", "--ip", dest="ip",
                      help="ip enabled nodes distribution")
    (options, args) = parser.parse_args()
    
    prefix = ''
    numLeaders = [[1,1], [0,1]]
    numMembers = [[5,1], [1,5]]
    numOthers = [5, 5]
    ip = [5,5]
    
    if options.numLeaders is not None:
        numLeaders = list(ast.literal_eval(options.numLeaders))
    if options.numMembers is not None:
        numMembers = list(ast.literal_eval(options.numMembers))
    if options.numOthers is not None:
        numOthers = list(ast.literal_eval(options.numOthers))
    if options.ip is not None:
        ip = list(ast.literal_eval(options.ip))
    if options.prefix is not None:
        prefix = options.prefix
    #generateComplexRandomConfig(100, 120, 10, [range(0, 2), range(0, 1)], numLeaders, numMembers, numOthers, prefix, ip)
    generateComplexRandomConfigWithOutsiders(
                                            100, #area size 
                                            0, #external area size 
                                            10, #scale
                                            [[0, 1], [0, 2]], # distribution of teams
                                            [3], # outside teams
                                            [[1, 1, 0, 0], [1, 0, 1, 0], [0, 0, 0, 1]], # distribution of leaders 
                                            [[9, 9, 0, 0], [9, 0, 9, 0], [0, 0, 0, 100]], # distribution of members 
                                            [0, 0, 0], # distribution of others 
                                            '', 
                                            [2, 2, 2], # distribution of IP-enabled nodes
                                            )
    
    