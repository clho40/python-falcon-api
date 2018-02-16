def isEmpty(data):
    for key,value in data.items():
        if not value:
            return key
    
    return None