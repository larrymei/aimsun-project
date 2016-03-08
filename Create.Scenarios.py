### Create the network first using the first script
### Make the basic ODMatrix with externalId 999
### Make sure the routing problem has been solved, i.e. for the shortest path routing rule,
### using the function enlarging the cost of turning

### Parameters
### dr_l: demand range lower value
### dr_u: demand range upper value
### n_repli The number of Replications
dr_l = 5
dr_u = 9
n_repli = 3

def CreateTrafficDemand(only=True):
    folderName = "GKModel::trafficDemand"
    folder = model.getCreateRootFolder().findFolder(folderName)
    TrafficDemand = []
    if folder == None:
        folder = GKSystem.getSystem().createFolder(model.getCreateRootFolder(), folderName)    
    if only:
        for plan in folder.getContents().values():
            folder.remove(plan)
            if plan.canBeDeleted():
                cmd = plan.getDelCmd()
                model.getCommander().addCommand(cmd)

    ODMatrix = model.getCatalog().findObjectByExternalId('999')

    for i in range(dr_u+1-dr_l):
        TrafficDemand.append(GKSystem.getSystem().newObject("GKTrafficDemand", model))
        name = 'demand{0}'.format((i+dr_l)*10)
        TrafficDemand[i].setName(name)
        ScheduleDemandItem = GKScheduleDemandItem()
        ScheduleDemandItem.setFrom(0)
        ScheduleDemandItem.setDuration(3600*2)
        ScheduleDemandItem.setTrafficDemandItem(ODMatrix)
        ScheduleDemandItem.setFactor(str(100*(i+dr_l)))
        TrafficDemand[i].addToSchedule(ScheduleDemandItem)
        folder.append(TrafficDemand[i])
    return TrafficDemand


def getmatercontrolplan():
    folderName = "GKModel::masterControlPlans"
    folder = model.getCreateRootFolder().findFolder(folderName)
    ids = folder.getContents().keys()
    plan = model.getCatalog().find(ids[0])
    return plan


def setSCinput(newScenario):
    Scinput = newScenario.getInputData()
    Scinput.setTurnsStatistics(False)
    Scinput.setStatisticalInterval(GKTimeDuration(0,2,0))
    Scinput.setDetectionInterval(GKTimeDuration(0,2,0))
    return Scinput

def CreateScenarios(Demands):
    results = []
    folderName = "GKModel::top::scenarios"
    folder = model.getCreateRootFolder().findFolder(folderName)
    for i in range(dr_u+1-dr_l):
        name = "SC{0}".format((i+dr_l)*10)
        newScenario = GKSystem.getSystem().newObject("GKScenario", model)
        newScenario.setName(name)
        newScenario.setMasterControlPlan(getmatercontrolplan())
        newScenario.setDemand(Demands[i])
        newScenario.setInputData(setSCinput(newScenario))
        newExperiment = CreateExperiment()
        newAverage = CreateReplications(newExperiment,(i+dr_l)*10)
        newScenario.addExperiment(newExperiment)
        folder.append(newScenario)
        results.append(newAverage)
    return results


def CreateExperiment():

    newEx = GKSystem.getSystem().newObject("GKExperiment", model)
    newEx.setNbThreadsSim(2)
    newEx.setDataValueDoubleByID(GKExperiment.routeChoiceTypeAtt, 4)
    newEx.setDataValueDoubleByID(GKExperiment.maxRoutesAtt, 2)
    newEx.setDataValueDoubleByID(GKExperiment.maxRoutesToKeepAtt, 2)
    newEx.setDataValueDoubleByID(GKExperiment.initialSPTreesAtt, 2)
    newEx.setDataValueDoubleByID(GKExperiment.scaleFactorAtt, 10)
    return newEx

def CreateReplications(experiment,index):
    average = GKSystem.getSystem().newObject("GKExperimentResult",model)
    average.setExternalId(str(index))
    for i in range(n_repli):
        replication = (GKSystem.getSystem().newObject("GKReplication", model))
        replication.setExternalId(str(index+i+1))
        average.addReplication(replication)
        experiment.addReplication(replication)
    experiment.addReplication(average)
    return average

def Activate(results):
    module = GKSystem.getSystem().getPlugin( "GGetram" )
    for average in results:
        for replication in average.getReplications():
            module.simulateReplication(replication, GKReplication.eBatch, 0 )
        module.calculateResult(average)

TrafficDemands = CreateTrafficDemand(False)
results = CreateScenarios(TrafficDemands)
Activate(results)

model.getCommander().addCommand(None)
