
from ruamel.yaml.scalarstring import LiteralScalarString

def m2d_exclude(obj, *args):
    model_dict = obj.to_mongo().to_dict()
    if args:
        list(map(model_dict.pop, list(args)))
    if "_id" in model_dict.keys():
        model_dict["_id"] = str(model_dict["_id"])
    return model_dict


def m2d_fields(obj, *args):
    model_dict = obj.to_mongo().to_dict()
    if args:
        fields = [i for i in model_dict.keys() if i not in list(args)]
        list(map(model_dict.pop, fields))
    if "_id" in model_dict.keys():
        model_dict["_id"] = str(model_dict["_id"])
    return model_dict

def render(example):
    text = example['text']
    example['text'] = LiteralScalarString(text + "\n")
    return example

def example2dict(examples):
    example_trans = {}
    for example in examples:
        intent = example.get('intent')
        entities = example.get('entities')
        text = example.get('text')
        str2list = list(text)
        if len(entities):
            entities = sorted(entities, key=lambda e: e['end'], reverse=True)
        for entity in entities:
            if text[entity['start']:entity["end"]] == entity["value"]:
                str2list.insert(entity["end"], ']({})'.format(entity["type"]))
                str2list.insert(entity["start"], '[')
            else:
                str2list.insert(entity["end"], "]" + json.dumps({"entity": entity['type'], "value": entity['value']}))
                str2list.insert(entity["start"], '[')
        # example['text'] = ''.join(str2list)
        if intent not in example_trans:
            example_trans[intent] = {"intent": intent,
                                     "examples": [{"text": LiteralScalarString(''.join(str2list) + "\n")}]}
        else:
            example_trans[intent]["examples"].append({"text": LiteralScalarString(''.join(str2list) + "\n")})
    return example_trans

def all_subclasses(cls):
    """Returns all known (imported) subclasses of a class."""
    return cls.__subclasses__() + [
        g for s in cls.__subclasses__() for g in all_subclasses(s)
    ]