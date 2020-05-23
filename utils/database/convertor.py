from bson import ObjectId


def str2object_id(id_):
    if isinstance(id_, str):
        return ObjectId(id_)
    return id_


def object_id2str(id_):
    if isinstance(id_, str):
        return id_
    return str(id_)


def simplify_objects(obj):
    id_ = obj.get("_id")
    if id_ is None:
        return obj
    obj["_id"] = object_id2str(id_)
    return obj
