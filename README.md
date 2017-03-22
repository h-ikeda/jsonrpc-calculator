Available at https://nameless-falls-59671.herokuapp.com/ !
# JSONRPC Calculator
Python version|Build status|Code coverage
:-:|---|---
2.7.11|[![CircleCI](https://circleci.com/gh/1stop-st/jsonrpc-calculator.svg?style=svg)](https://circleci.com/gh/1stop-st/jsonrpc-calculator)|[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/6f01fe311425497bb25fc51022ab0461)](https://www.codacy.com/app/1stop-st/jsonrpc-calculator?utm_source=github.com&utm_medium=referral&utm_content=1stop-st/jsonrpc-calculator&utm_campaign=Badge_Coverage)
3.5.3|[![](https://codeship.com/projects/d34410c0-e145-0134-2aa0-3a335c5eb36d/status?branch=master)](https://app.codeship.com/projects/205458)|[![codecov](https://codecov.io/gh/1stop-st/jsonrpc-calculator/branch/master/graph/badge.svg)](https://codecov.io/gh/1stop-st/jsonrpc-calculator)
3.6.0|[![Codefresh build status]( https://g.codefresh.io/api/badges/build?repoOwner=1stop-st&repoName=jsonrpc-calculator&branch=master&pipelineName=jsonrpc-calculator&accountName=h-ikeda&type=cf-1)]( https://g.codefresh.io/repositories/1stop-st/jsonrpc-calculator/builds?filter=trigger:build;branch:master;service:58b7cceba5addb0100a9fe0d~jsonrpc-calculator)|[![Coverage Status](https://coveralls.io/repos/github/1stop-st/jsonrpc-calculator/badge.svg?branch=master)](https://coveralls.io/github/1stop-st/jsonrpc-calculator?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6f01fe311425497bb25fc51022ab0461)](https://www.codacy.com/app/h-ikeda/jsonrpc-calculator?utm_source=github.com&utm_medium=referral&utm_content=1stop-st/jsonrpc-calculator&utm_campaign=badger)
## Overview
This program runs on wsgi server, recieves json requests compatible with jsonrpc, and responds processed values.
## Usage
POST your data model formatted with JSONRPC, and it returns the analyzed response as a JSONRPC response.

POST:
```json
{
    "jsonrpc": "2.0",
    "id": "id string",
    "method": "method string",
    "params": ["object or array"]
}
```
Response:
```json
{
    "jsonrpc": "2.0",
    "id": "id string",
    "result": "analyzed result"
}
```
or on error:
```json
{
    "jsonrpc": "2.0",
    "id": "id string",
    "error": {
        "code": -32000,
        "message": "error message"
    }
}
```
### Methods
#### frame.calculate
##### Discription
Analyze frame structure's node displacements.
##### Params
```json
{
    "model": {
        "nodes": {
            "id": 0,
            "x": 0,
            "y": 0,
            "z": 0
        },
        "lines": {
        
        },
        "sections": {
        
        },
        "materials": {
        
        }
        "boundaries": {
        
        },
        "nodeLoads": {
        
        }
    }
}
```
##### Result
```json
{
    "displacements": {
        "node_id": {
            "x": 0,
            "y": 0,
            "z": 0
        }
    }
}
```
#### frame_calculate
##### Discription
Analyze frame structure's node displacements.
##### Params
```json
{
    "frameModel": {
        "nodes": {
            "id": 0,
            "x": 0,
            "y": 0,
            "z": 0
        },
        "lines": {
        
        },
        "boundaries": {
        
        },
        "nodeLoads": {
        
        }
    }
}
```
##### Result
```json
{
    "displacements": {
        "node_id": {
            "x": 0,
            "y": 0,
            "z": 0
        }
    }
}
```
## Contribution
Writing now...
