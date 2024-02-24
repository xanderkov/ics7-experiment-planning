import math
import random
import queue
import numpy
from distributions import *
class Generator:
    def __init__(self, distribution_func, params):
        self.distribution_func = distribution_func
        self.params = params
        self.time = 0
        self.next = 0
        self.was_set = True
    def get_current(self):
        return self.time
    def set_next(self):
        self.time = self.next
        self.was_set = True
    def generate_next(self):
        if self.was_set:
            self.next = self.time + self.distribution_func(self.params)
            self.was_set = False
        return self.next
    def zero(self):
        self.time = 0
        self.next = 0
        was_set = False
class Handler:
    def __init__(self, distribution_func, params):
        self.distribution_func = distribution_func
        self.params = params
        self.busyTill = 0

    def generate(self):
        return self.distribution_func(self.params)
    
    def isBusy(self, curTime):
        return curTime < self.busyTill 
        
    def getBusy(self):
        return self.busyTill

    def setBusy(self, val):
        self.busyTill = val
        
class Queue:
    def __init__(self, length):
        self.queue = queue.Queue()
    def add(self, elem):
        self.queue.put(elem)
        return 0
    def empty(self):
        return self.queue.empty()
    def full(self):
        return False
    def rm(self):
        return self.queue.get()
    def size(self):
        return self.queue.qsize()
    
class Statistics():
    def __init__(self):
        self.reqs = []
        self.sm = 0
        self.hm = 0
        self.overfull = 0
        self.mt = 0
        
    def addRequest(self, r):
        self.reqs.append(r)
    def getRequests(self):
        return self.reqs
    
    def addSourceMiss(self):
        self.sm += 1
    def getSourceMiss(self):
        return self.sm

    def addHandleMiss(self):
        self.hm += 1
    def getHandleMiss(self):
        return self.hm

    def addOverfull(self):
        self.overfull += 1
    def getOverfull(self):
        return self.overfull
    def print(self):
        print("sm: {}, hm: {}, of: {}".format(self.sm, self.hm, self.overfull))
        for r in self.reqs:
            r.print()
    def setMaxTime(self, time):
        self.mt = time
    def getMaxTime(self):
        return self.mt
class Request:
    def __init__(self):
        self.ct = []
        self.sht = []
        self.ht = []
        self.handler = 0
    def getCreationTime(self):
        if len(self.ct) > 0:
            return self.ct[len(self.ct) - 1]
        else:
            return 0
    def getStartHandlingTime(self):
        if len(self.sht) > 0:
            return self.sht[len(self.sht) - 1]
        else:
            return 0
    def getHandlingTime(self):
        if len(self.ht) > 0:
            return self.ht[len(self.ht) - 1]
        else:
            return 0
    
    def setCreationTime(self, ct):
        self.ct.append(ct)
    def setStartHandlingTime(self, sht, pos = 0):
        self.sht.append(sht)
        self.handler = pos
    def setHandlingTime(self, ht):
        self.ht.append(ht)
    def print(self):
        print("ct: {}, sht: {}, ht: {}, handler: {}".format(self.ct, self.sht, self.ht, self.handler))

        
class ModelingGoverner:
    def __init__(self, tend, source_generators, handler_generators, queueSize):
        self.stats = Statistics()
        self.tend = tend
        self.source_generators = source_generators
        self.handler_generators = handler_generators
        self.queueSize = queueSize
    
    def getStatistics(self):
        return self.stats
    
    def getNextGeneratorEvent(self):
        pos = 0
        event = self.source_generators[pos].get_current()
        for i in range(len(self.source_generators)):
            if self.source_generators[i].get_current() < event:
                pos = i
                event = self.source_generators[pos].get_current()
        return (event, pos)

    def getNextHandlerEvent(self, nextGen, curTime):
        event = self.handler_generators[0].getBusy()
        for i in range(len(self.handler_generators)):
            if not self.handler_generators[i].isBusy(curTime):
                return nextGen
            if self.handler_generators[i].getBusy() < event:
                event = self.handler_generators[i].getBusy()

        return event 
    def updateHandlers(self, curTime):
        for i in range(len(self.handler_generators)):
            if self.handler_generators[i].getBusy() < curTime:
                self.handler_generators[i].setBusy(0)
    def event(self):
        self.stats = Statistics()
        tasks = 0
        for i in range(len(self.source_generators)):
            self.source_generators[i].zero()
            self.source_generators[i].generate_next()
            self.source_generators[i].set_next()
            
        t = 0
        q = Queue(self.queueSize)
        
        events = [0, 0]
        events[0], event_next_generator_pos = self.getNextGeneratorEvent()
        events[1] = events[0]
        min_event = 0
        it = 0
        count = 0
        while count < self.tend:
            it += 1
            min_event = numpy.argmin(events)
            if min_event == 0:
                r = Request()
                count += 1
                r.setCreationTime(self.source_generators[event_next_generator_pos].get_current())
                if q.full():
                    self.stats.addOverfull()
                else:
                    q.add(r)
                self.stats.addRequest(r)

                self.source_generators[event_next_generator_pos].generate_next()
                self.source_generators[event_next_generator_pos].set_next()
                events[0], event_next_generator_pos = self.getNextGeneratorEvent()
            elif min_event == 1:
                self.updateHandlers(events[1])
                for i in range(len(self.handler_generators)):
                    if not self.handler_generators[i].isBusy(events[1]) and not q.empty():
                        r = q.rm()
                        r.setStartHandlingTime(events[1], i)

                        htime = self.handler_generators[i].generate()
                        self.handler_generators[i].setBusy(r.getStartHandlingTime() + htime)
                    
                        r.setHandlingTime(htime)
                events[1] = self.getNextHandlerEvent(events[0], events[1])

        self.stats.setMaxTime(events[min_event])
                        
        return self.stats
                        
if __name__ == "__main__":                            
    source_generator1 = Generator(uniform_t, [8, 10])
    source_generator2 = Generator(uniform_t, [8, 10])
    source_generator3 = Generator(uniform_t, [8, 10])
    source_generator4 = Generator(uniform_t, [8, 10])
    handler_generator1 = Handler(exp_t, [0.01])
    handler_generator2 = Handler(exp_t, [0.01])
    handler_generator3 = Handler(exp_t, [0.01])
    handler_generator4 = Handler(exp_t, [0.01])
    gov = ModelingGoverner(100, [source_generator1], #, source_generator2, source_generator3, source_generator4],
                           [handler_generator1], 0) #, handler_generator2, handler_generator3, handler_generator4], 0)
    s = gov.event()
    s.print()
    print(s.getMaxTime(), len(s.getRequests()))


            
    
        
        
