# datasource/mapping_config.py
MAPPING_CONFIG = {
    'accounts': {
        'UserID': ['user_id', 'UserID', 'identifier'],
        'Nick': ['nick', 'Nick', 'nickname', 'Nickname'],
        'FaceUrl': ['face_url', 'faceUrl', 'avatar', 'Avatar']
    },
    # 添加其他映射配置，如 'groups' 和 'group_members'
    'groups':{
        'GroupId':['imGroupId'],
        'Owner_Account':['ownerUserImId'],
        'Type':['imGroupType'],
        'Name':['groupName'],
        'FaceUrl':['faceUrl'],
        'MaxMemberCount':['maxMemberCount'],
        'ApplyJoinOption':['applyJoinMethod']
    }
}
