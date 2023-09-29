from typing import List, Optional
from pydantic import BaseModel

class IA(BaseModel):
    id: int
    life: int

class Buff(BaseModel):
    lucky_unlucky: bool
    go_ryu: bool
    karin_gift: bool

class Zone(BaseModel):
    zone_id: int
    ias: Optional[List[IA]]
    triggers: Buff

class Status(BaseModel):
    life: int
    match_ia: int

class FindResponse(BaseModel):
    current_zone: Zone
    neighbours_zones: Optional[List[Zone]]
    status: Status

class StatusInfo(BaseModel):
    lucky_unlucky: int
    go_ryu: int
    life: int

class AttackResponse(BaseModel):
    attack_to: int
    match: str
    status_info: dict[int, StatusInfo]

class MoveResponse(BaseModel):
    to_zone: int
    match: str
    triggers: Buff

class DefendResponse(BaseModel):
    active: bool
    match_ia: int



###### TEST
#
#find_response_data = {
#    "current_zone": {
#        "zone_id": 10,
#        "ias": [{
#                "id": 9,
#                "life":1203
#            },
#            {
#                "id": 10,
#                "life":12
#            }],
#        "triggers": {
#            "lucky_unlucky": True,
#            "go_ryu": True,
#            "karin_gift": False
#        }},
#    "neighbours_zones":[{
#        "zone_id": 12,
#        "ias": [],
#        "triggers": {
#            "lucky_unlucky": True,
#            "go_ryu": True,
#            "karin_gift": False
#        }
#    }],
#    "status": {
#        "life": 200, 
#        "match_ia": 12 
#    }
#}
#
#
#response = FindResponse(**find_response_data)
#print(response.current_zone.triggers.go_ryu)
#print(response.model_dump())


#attack_response_data = {
#    'attack_to': 9, 
#    'match': '2', 
#    'status_info': {
#        '10': {
#            'lucky_unlucky': 0, 
#            'go_ryu': 0, 
#            'life': 200}, 
#        '9': {
#            'lucky_unlucky': 0, 
#            'go_ryu': 0, 
#            'life': 1191}
#    }
#}

#attack = AttackResponse(**attack_response_data)
#print(attack.attack_to)
#print(attack.status_info[10])
#print(attack.model_dump())


#move_response_data = {
#    "to_zone": "5",
#    "match": "2", 
#    "triggers" : {
#        "lucky_unlucky": False,
#        "go_ryu": False,
#        "karin_gift": False
#    }
#}

#move = MoveResponse(**move_response_data)
#print(attack.attack_to)
#print(attack.status_info[10])
#print(move.model_dump())


#defend_response_data = {
#    "active": "False", 
#    "match_ia":"11"
#}
#
#defend = DefendResponse(**defend_response_data)
#print(defend.model_dump())

