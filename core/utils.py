def to_dict_with_relation_ids(obj, relation_name: str):

    result = {c.key: getattr(obj, c.key) for c in obj.__table__.columns}

    relation_objs = getattr(obj, relation_name, [])
    if relation_objs:
        pk_field = list(relation_objs[0].__table__.primary_key.columns)[0].key
        result[f"{relation_name}_ids"] = [getattr(rel, pk_field) for rel in relation_objs]
    else:
        result[f"{relation_name}_ids"] = []

    return result
