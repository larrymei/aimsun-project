### create a section of two lanes then implement this script

### Parameters:
### delta:
### length: block size
### intersize: intersection size
### m * n: m rows by n columns network
### c: cycle length
### L: number of lanes
### r: total red time
### qc: capacity for a lane
delta = 20
length = 200.0
intersize = 20.0
m = 5
n = 5
c = 120.0
L = 3
r = 12
qc = 1800.0


def Createonesection(inpoint, outpoint):
    newsection = target.clone()
    polyline = GKSystem.getSystem().newObject("GKPolyline", model)
    polyline.addPoint(inpoint)
    polyline.addPoint(outpoint)
    newsection.setPoints(polyline.getPoints())
    newlane = GKSectionLane()
    newsection.addLane(newlane)
    model.getGeoModel().add(target.getLayer(), newsection)
    return newsection


def Createintersectionarms(intersectionposition):
    intersectioninarms = [[[0 for x in range(4)] for x in range(n + 2)] for x in range(m + 2)]
    for i in range(m + 2):
        for j in range(n + 2):
            if j > 0 and i > 0 and i < m + 1:
                inpoint1 = GKPoint(intersectionposition[i][j].x - length - intersize, intersectionposition[i][j].y - 5)
                outpoint1 = GKPoint(intersectionposition[i][j].x - intersize, intersectionposition[i][j].y - 5)
                intersectioninarms[i][j][0] = Createonesection(inpoint1, outpoint1)
            if j > 0 and j < n + 1 and i > 0:
                inpoint3 = GKPoint(intersectionposition[i][j].x - 5, intersectionposition[i][j].y + length + intersize)
                outpoint3 = GKPoint(intersectionposition[i][j].x - 5, intersectionposition[i][j].y + intersize)
                intersectioninarms[i][j][1] = Createonesection(inpoint3, outpoint3)
            if j < n + 1 and i > 0 and i < m + 1:
                inpoint5 = GKPoint(intersectionposition[i][j].x + length + intersize, intersectionposition[i][j].y + 5)
                outpoint5 = GKPoint(intersectionposition[i][j].x + intersize, intersectionposition[i][j].y + 5)
                intersectioninarms[i][j][2] = Createonesection(inpoint5, outpoint5)
            if j > 0 and j < n + 1 and i < m + 1:
                inpoint7 = GKPoint(intersectionposition[i][j].x + 5, intersectionposition[i][j].y - length - intersize)
                outpoint7 = GKPoint(intersectionposition[i][j].x + 5, intersectionposition[i][j].y - intersize)
                intersectioninarms[i][j][3] = Createonesection(inpoint7, outpoint7)
    return intersectioninarms


def addturn(intersectioninarms, i, j, node, l_list, signals):
    # arm 0, through-moving
    turning = GKSystem.getSystem().newObject("GKTurning", model)
    turning.setConnection(intersectioninarms[i][j][0], intersectioninarms[i][j + 1][0])
    turning.setOriginLanes(3 - l_list[0], 2)
    turning.setDestinationLanes(0, 2)
    node.addTurning(turning, True, True)
    signals[0].addTurning(turning)
    # arm 0, left-turning
    if l_list[1] > 0:
        turning = GKSystem.getSystem().newObject("GKTurning", model)
        turning.setConnection(intersectioninarms[i][j][0], intersectioninarms[i - 1][j][3])
        turning.setOriginLanes(0, l_list[1] - 1)
        turning.setDestinationLanes(0, 2)
        node.addTurning(turning, True, True)
        signals[1].addTurning(turning)
    # arm 0, right-turning
    turning = GKSystem.getSystem().newObject("GKTurning", model)
    turning.setConnection(intersectioninarms[i][j][0], intersectioninarms[i + 1][j][1])
    turning.setOriginLanes(2, 2)
    turning.setDestinationLanes(0, 2)
    node.addTurning(turning, True, True)
    # arm 1, through-moving
    turning = GKSystem.getSystem().newObject("GKTurning", model)
    turning.setConnection(intersectioninarms[i][j][1], intersectioninarms[i + 1][j][1])
    turning.setOriginLanes(3 - l_list[2], 2)
    turning.setDestinationLanes(0, 2)
    node.addTurning(turning, True, True)
    signals[2].addTurning(turning)
    # arm 1, left-turning
    if l_list[3] > 0:
        turning = GKSystem.getSystem().newObject("GKTurning", model)
        turning.setConnection(intersectioninarms[i][j][1], intersectioninarms[i][j + 1][0])
        turning.setOriginLanes(0, l_list[3] - 1)
        turning.setDestinationLanes(0, 2)
        node.addTurning(turning, True, True)
        signals[3].addTurning(turning)
    # arm 1, right-turning
    turning = GKSystem.getSystem().newObject("GKTurning", model)
    turning.setConnection(intersectioninarms[i][j][1], intersectioninarms[i][j - 1][2])
    turning.setOriginLanes(2, 2)
    turning.setDestinationLanes(0, 2)
    node.addTurning(turning, True, True)
    # arm 2, through-moving
    turning = GKSystem.getSystem().newObject("GKTurning", model)
    turning.setConnection(intersectioninarms[i][j][2], intersectioninarms[i][j - 1][2])
    turning.setOriginLanes(3 - l_list[4], 2)
    turning.setDestinationLanes(0, 2)
    node.addTurning(turning, True, True)
    signals[0].addTurning(turning)
    # arm 2, left-turning
    if l_list[5] > 0:
        turning = GKSystem.getSystem().newObject("GKTurning", model)
        turning.setConnection(intersectioninarms[i][j][2], intersectioninarms[i + 1][j][1])
        turning.setOriginLanes(0, l_list[5] - 1)
        turning.setDestinationLanes(0, 2)
        node.addTurning(turning, True, True)
        signals[1].addTurning(turning)
    # arm 2, right-turning
    turning = GKSystem.getSystem().newObject("GKTurning", model)
    turning.setConnection(intersectioninarms[i][j][2], intersectioninarms[i - 1][j][3])
    turning.setOriginLanes(2, 2)
    turning.setDestinationLanes(0, 2)
    node.addTurning(turning, True, True)
    # arm 3, through-moving
    turning = GKSystem.getSystem().newObject("GKTurning", model)
    turning.setConnection(intersectioninarms[i][j][3], intersectioninarms[i - 1][j][3])
    turning.setOriginLanes(3 - l_list[6], 2)
    turning.setDestinationLanes(0, 2)
    node.addTurning(turning, True, True)
    signals[2].addTurning(turning)
    # arm 3, left-turning
    if l_list[7] > 0:
        turning = GKSystem.getSystem().newObject("GKTurning", model)
        turning.setConnection(intersectioninarms[i][j][3], intersectioninarms[i][j - 1][2])
        turning.setOriginLanes(0, l_list[7] - 1)
        turning.setDestinationLanes(0, 2)
        node.addTurning(turning, True, True)
        signals[3].addTurning(turning)
    # arm 3, right-turning
    turning = GKSystem.getSystem().newObject("GKTurning", model)
    turning.setConnection(intersectioninarms[i][j][3], intersectioninarms[i][j + 1][0])
    turning.setOriginLanes(2, 2)
    turning.setDestinationLanes(0, 2)
    node.addTurning(turning, True, True)


def CreateControlPlanSignals(node):
    signal_list = []
    for i in range(4):
        signal = GKSystem.getSystem().newObject("GKControlPlanSignal", model)
        signal_list.append(signal)
        node.addSignal(signal)
    return signal_list


def CreateControlPhase(controljunction, signals, g_list, yellow=3):
    b = 0
    n = len(g_list)
    for i in range(n):
        # grean
        phase = controljunction.createPhase()
        phase.addSignal(signals[i].getId())
        phase.setFrom(b)
        phase.setDuration(g_list[i])
        b += g_list[i]
        # intergreen
        phase = controljunction.createPhase()
        phase.setInterphase(True)
        phase.setFrom(b)
        phase.setDuration(yellow)
        b += yellow


def CreateControlPlan(only=False, name="Starting Configuration"):
    newControlPlan = GKSystem.getSystem().newObject("GKControlPlan", model)
    newControlPlan.setName(name)
    folderName = "GKModel::controlPlans"
    folder = model.getCreateRootFolder().findFolder(folderName)
    if folder == None:
        folder = GKSystem.getSystem().createFolder(model.getCreateRootFolder(), folderName)
    if only:
        for plan in folder.getContents().values():
            folder.remove(plan)
            if plan.canBeDeleted():
                cmd = plan.getDelCmd()
                model.getCommander().addCommand(cmd)
    folder.append(newControlPlan)
    return newControlPlan


def CreateControlJunction(node, controlplan):
    controljunction = controlplan.createControlJunction(node.getId())
    controljunction.setControlJunctionType(2)
    controljunction.setCycle(120)
    controljunction.setOffset(0)
    return controljunction


def AddNode(intersectioninarms, i, j, controlplan):
    newnode = GKSystem.getSystem().newObject("GKNode", model)
    newnode.setYellowBox(True)
    model.getGeoModel().add(target.getLayer(), newnode)
    signals = CreateControlPlanSignals(newnode)
    l_list = getoptimalsetting(i, j)[1]
    g_list = getoptimalsetting(i, j)[3]

    addturn(intersectioninarms, i, j, newnode, l_list, signals)
    controljunction = CreateControlJunction(newnode, controlplan)
    CreateControlPhase(controljunction, signals, g_list, 3)


def CreateNodes(intersectioninarms, controlplan):
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            AddNode(intersectioninarms, i, j, controlplan)


def CreateMasterControlPlan(ControlPlan, only=True, name="Starting Configuration"):
    MasterControlPlan = GKSystem.getSystem().newObject("GKMasterControlPlan", model)
    MasterControlPlan.setName(name)
    ScheduleMasterControlPlanItem = GKScheduleMasterControlPlanItem()
    ScheduleMasterControlPlanItem.setFrom(0)
    ScheduleMasterControlPlanItem.setDuration(3600)
    ScheduleMasterControlPlanItem.setZone(1)
    ScheduleMasterControlPlanItem.setControlPlan(ControlPlan)
    MasterControlPlan.addToSchedule(ScheduleMasterControlPlanItem)
    folderName = "GKModel::masterControlPlans"
    folder = model.getCreateRootFolder().findFolder(folderName)
    if folder == None:
        folder = GKSystem.getSystem().createFolder(model.getCreateRootFolder(), folderName)
    if only:
        for plan in folder.getContents().values():
            folder.remove(plan)
            if plan.canBeDeleted():
                cmd = plan.getDelCmd()
                model.getCommander().addCommand(cmd)
    folder.append(MasterControlPlan)
    return MasterControlPlan


def CreateTrafficDemand(ODMatrix, only=True, name="TestDemand"):
    TrafficDemand = GKSystem.getSystem().newObject("GKTrafficDemand", model)
    TrafficDemand.setName(name)
    ScheduleDemandItem = GKScheduleDemandItem()
    ScheduleDemandItem.setFrom(0)
    ScheduleDemandItem.setDuration(3600)
    ScheduleDemandItem.setTrafficDemandItem(ODMatrix)
    TrafficDemand.addToSchedule(ScheduleDemandItem)
    folderName = "GKModel::trafficDemand"
    folder = model.getCreateRootFolder().findFolder(folderName)
    if folder == None:
        folder = GKSystem.getSystem().createFolder(model.getCreateRootFolder(), folderName)
    if only:
        for plan in folder.getContents().values():
            folder.remove(plan)
            if plan.canBeDeleted():
                cmd = plan.getDelCmd()
                model.getCommander().addCommand(cmd)
    folder.append(TrafficDemand)
    return TrafficDemand


def CreateCenConnection(centroid, link, to=True):
    ### To means connection from centroid to link
    CenConnection = GKSystem.getSystem().newObject("GKCenConnection", model)
    if to:
        CenConnection.setConnectionType(2)
    else:
        CenConnection.setConnectionType(1)
    CenConnection.setConnectionObject(link)
    centroid.addConnection(CenConnection)


def CreateConnections(centroid, i, j, intersectioninarms):
    ### Use index 0,0 of intersectioninarims, top-left centroid index is 1,1
    # connection from centroid to link
    CreateCenConnection(centroid, intersectioninarms[i][j - 1][2], True)
    CreateCenConnection(centroid, intersectioninarms[i - 1][j][3], True)
    CreateCenConnection(centroid, intersectioninarms[i][j + 1][0], True)
    CreateCenConnection(centroid, intersectioninarms[i + 1][j][1], True)
    # connection from link to centroid
    for k in range(4):
        CreateCenConnection(centroid, intersectioninarms[i][j][k], False)


def CreateCentroid(position):
    Centroid = GKSystem.getSystem().newObject("GKCentroid", model)
    Centroid.setFromPosition(position)
    Centroid.setConsideredPercentages(0)
    Centroid.setUseInMatrix(True)
    model.getGeoModel().add(target.getLayer(), Centroid)
    return Centroid


def CreateCentroids(intersectionposition, intersectioninarms):
    centroids = [[0 for x in range(n)] for y in range(m)]
    for i in range(m):
        for j in range(n):
            point = intersectionposition[i + 1][j + 1]
            point.x += intersize
            point.y += intersize
            centroids[i][j] = CreateCentroid(point)
            CreateConnections(centroids[i][j], i + 1, j + 1, intersectioninarms)
    return centroids


def CreateODMatrix(CentroidConfiguration, centroids, name="New OD Matrix"):
    ODMatrix = GKSystem.getSystem().newObject("GKODMatrix", model)
    ODMatrix.setName(name)
    ODMatrix.setCentroidConfiguration(CentroidConfiguration)
    for i in range(m):
        for j in range(n):
            for u in range(m):
                for v in range(n):
                    if i != u or j != v:
                        ODMatrix.setTrips(centroids[i][j], centroids[u][v], delta)
    CentroidConfiguration.addODMatrix(ODMatrix)
    ODMatrix.setEnableStore(True)
    car = model.getCatalog().find(53)
    userclass = GKUserClass.createUserClass(model, car, None)
    ODMatrix.setUserClass(userclass)
    return ODMatrix


def CreateCentroidConfiguration(centroids, only=False):
    CentroidConfiguration = GKSystem.getSystem().newObject("GKCentroidConfiguration", model)
    CentroidConfiguration.activate()
    folderName = "GKModel::centroidsConf"
    folder = model.getCreateRootFolder().findFolder(folderName)
    if folder == None:
        folder = GKSystem.getSystem().createFolder(model.getCreateRootFolder(), folderName)
    if only:
        for plan in folder.getContents().values():
            folder.remove(plan)
            if plan.canBeDeleted():
                cmd = plan.getDelCmd()
                model.getCommander().addCommand(cmd)
    folder.append(CentroidConfiguration)
    for i in range(m):
        for j in range(n):
            CentroidConfiguration.addCentroid(centroids[i][j])
    return CentroidConfiguration


def getoptimalsetting(i, j):
    k = delta
    q1 = (j - 1) * (n - j + 1) * m * k - (j - 1) * (i - 1) * k
    q3 = (i - 1) * (m - i + 1) * n * k - (i - 1) * (n - j) * k
    q5 = j * (n - j) * m * k - (m - i) * (n - j) * k
    q7 = i * (m - i) * n * k - (m - i) * (j - 1) * k
    q2 = (j - 1) * (i - 1) * k
    q4 = (i - 1) * (n - j) * k
    q6 = (m - i) * (n - j) * k
    q8 = (m - i) * (j - 1) * k
    minlambda = 99999
    minl1 = 0
    minl3 = 0
    minl5 = 0
    minl7 = 0
    lambda_list = [0, 0, 0, 0]
    for l1 in range(1, L + 1):
        l2 = L - l1 + 0.0001
        for l3 in range(1, L + 1):
            l4 = L - l3 + 0.0001
            for l5 in range(1, L + 1):
                l6 = L - l5 + 0.0001
                for l7 in range(1, L + 1):
                    l8 = L - l7 + 0.0001
                    lambda_list[0] = max(q1 / qc / l1, q5 / qc / l5)
                    lambda_list[1] = max(q2 / qc / l2, q6 / qc / l6)
                    lambda_list[2] = max(q3 / qc / l3, q7 / qc / l7)
                    lambda_list[3] = max(q4 / qc / l4, q8 / qc / l8)
                    sumlambda = sum(lambda_list)
                    if sumlambda < minlambda:
                        minlambda = sumlambda
                        minl1 = l1
                        minl3 = l3
                        minl5 = l5
                        minl7 = l7
                        minlambda_list = lambda_list[:]
    minl_list = [minl1, L - minl1, minl3, L - minl3, minl5, L - minl5, minl7, L - minl7]
    q_list = [q1, q2, q3, q4, q5, q6, q7, q8]
    cc = c - r
    g_list = [int(round(x / minlambda * cc)) for x in minlambda_list]
    return minlambda, minl_list, q_list, g_list



intersectionposition = [[0 for x in range(n + 2)] for x in range(m + 2)]

for i in range(m + 2):
    for j in range(n + 2):
        intersectionposition[i][j] = GKPoint()
        intersectionposition[i][j].set(j * (length + 2 * intersize), -i * (length + 2 * intersize), 0)

ControlPlan = CreateControlPlan(True, "test control")
MasterControlPlan = CreateMasterControlPlan(ControlPlan)
intersectioninarms = Createintersectionarms(intersectionposition)
CreateNodes(intersectioninarms, ControlPlan)
Centroids = CreateCentroids(intersectionposition, intersectioninarms)
CentroidConfiguration = CreateCentroidConfiguration(Centroids, True)
ODMatrix = CreateODMatrix(CentroidConfiguration, Centroids)
CreateTrafficDemand(ODMatrix)
model.getCommander().addCommand(None)
