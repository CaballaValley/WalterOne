from typing import List, Optional
from pydantic import BaseModel

from walterplayers.constants import Role

class ActiveBuff(BaseModel):
    ''' Active Buff for a player '''
    go_ryu: int
    lucky_unlucky: int

class IA(BaseModel):
    ''' Current ia information '''
    id: int
    life: int
    role: Role
    buff: ActiveBuff

class Buff(BaseModel):
    ''' Buffos for one zone. '''
    lucky_unlucky: bool
    go_ryu: bool
    karin_gift: bool

class Zone(BaseModel):
    ''' Zone information '''
    zone_id: int
    ias: Optional[List[IA]]
    triggers: Buff

class Status(BaseModel):
    ''' Status for your player '''
    buff: ActiveBuff
    life: int
    match_ia: int
    role: Role

class FindResponse(BaseModel):
    ''' Response for find resquest '''
    current_zone: Zone
    neighbours_zones: Optional[List[Zone]]
    status: Status

class StatusInfo(BaseModel):
    ''' Status info '''
    lucky_unlucky: int
    go_ryu: int
    life: int

class AttackResponse(BaseModel):
    ''' Response for attack resquest '''
    attack_to: int
    match: str
    status_info: dict[int, StatusInfo]

class MoveResponse(BaseModel):
    ''' Response for move resquest '''
    to_zone: int
    match: str
    triggers: Buff

class DefendResponse(BaseModel):
    ''' Response for defend resquest '''
    active: bool
    match_ia: int
