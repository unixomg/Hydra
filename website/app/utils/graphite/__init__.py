#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
from flask import current_app


def get_graphite_keys():
    try:
        r = requests.get("{}metrics/index.json".format(current_app.config.get("GRAPHITE_SERVER")))
        metrics = json.loads(r.content)
        ret = [m[m.index(".") + 1:] for m in metrics if not m.startswith("carbon")]
        return list(set(ret))
    except Exception, e:
        return []



#["carbon.agents.graphite-server-1-a.avgUpdateTime",
# "carbon.agents.graphite-server-1-a.blacklistMatches", 
#"carbon.agents.graphite-server-1-a.cache.bulk_queries", 
#"carbon.agents.graphite-server-1-a.cache.overflow", 
#"carbon.agents.graphite-server-1-a.cache.queries", 
#"carbon.agents.graphite-server-1-a.cache.queues", 
#"carbon.agents.graphite-server-1-a.cache.size", 
#"carbon.agents.graphite-server-1-a.committedPoints", 
#"carbon.agents.graphite-server-1-a.cpuUsage", 
#"carbon.agents.graphite-server-1-a.creates", 
#"carbon.agents.graphite-server-1-a.errors", 
#"carbon.agents.graphite-server-1-a.memUsage", 
#"carbon.agents.graphite-server-1-a.metricsReceived", 
#"carbon.agents.graphite-server-1-a.pointsPerUpdate", 
#"carbon.agents.graphite-server-1-a.updateOperations", 
#"carbon.agents.graphite-server-1-a.whitelistRejects", 
#"graphite-server-1.system.cpu.load1", 
#"graphite-server-1.system.cpu.load15", 
#"graphite-server-1.system.cpu.load5"]