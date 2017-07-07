#!/usr/bin/env python
from bpsRest import *

#if you need aditional methods you can extend/overide the BPS class from bpsRest.py
class MY_BPS_REST(BPS):
    def saveAsNormalTest(self, name_, force, enableRequestPrints = False):
        service  = 'https://' + self.ipstr + '/api/v1/bps/workingmodel/operations/saveas'
        jheaders = {'content-type': 'application/json'}
        jdata = json.dumps({'name':name_, 'force': force})
        print jdata
        r = self.session.post(service, data=jdata, headers=jheaders, verify=False)
        if(enableRequestPrints):
            self.pretty_print_requests(r)
        print "For saveAs working model defined by json object %s , the resonse is: %s" %(r.json(), r.status_code)
    
    def viewNormalTest(self, enableRequestPrints = False):
        service  = 'https://' + self.ipstr + '/api/v1/bps/workingmodel/settings'
        jheaders = {'content-type': 'application/json'}
        r = self.session.get(service)
        if(enableRequestPrints):
            print "Working Model Config: \n %s"  % self.pretty_print_requests(r)
        print "For view working model %s" %r
        
    def stopTest(self, runid, enableRequestPrints = False):
        service = 'https://' + self.ipstr + '/api/v1/bps/tests/operations/stop'
        jheaders = {'content-type': 'application/json'}
        jdata = json.dumps({'testid':runid})
        r = self.session.post(service, data=jdata, headers=jheaders, verify=False)
        if(enableRequestPrints):
            self.pretty_print_requests(r)
        if(r.status_code == 200):
            print 'Test: [' + runid + '] has been successfully stopped.'
        else:
            print 'Some error occurred while cancelling the running test: [' + runid + ']: ' + self.pretty_print_requests(r)    

#creating a bps rest instance
bps = MY_BPS_REST('10.200.119.188', 'admin', 'admin')
# login
bps.login()
# showing current port reservation state
bps.portsState()
# reserving the ports.
bps.reservePorts(slot = 4, portList = [0,1], group = 1, force = True)

#set a pre-existent test as a wroking model
template = 'Clientside Strikes'
testModel  = 'REST %s' % template
bps.setNormalTest(template)
print "Mofifying %s existent template and saving as:  %s" % (template, testModel)
#bps.viewNormalTest( enableRequestPrints = True)
bps.modifyNormalTest(componentId = 'Security1', elementId = 'attackPlanIterations', Value=2)
bps.saveAsNormalTest(testModel, force = True)
# please note the runid generated. It will be used for many more functionalities
runid = bps.runTest(modelname = testModel,neighborhood = 'BreakingPoint Switching Jumbo Frames' , group = 1)
# showing progress and current statistics. Stop the test at 2% progress
progress = 0
while (progress < 2):
    progress = bps.getRTS(runid)
    time.sleep(1)
bps.stopTest(runid)
# showing the test result (Pass/Fail)
# a sleep is put here because we do not immediately get the test results.
# inserting a sleep to allow for the data to be stored in the database before retrieval
time.sleep(1)
bps.getTestResult(runid)
# logging out
bps.logout()
