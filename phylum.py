from typing import Dict, List
import requests, json


BASE_URL = "http://104.236.127.116:8080/"

def sign_in() -> str or None:
    data = {
        'firstName': 'Joey',
        'lastName': 'David',
        'email': 'joeyfakeemail@gmail.com',
        'handle': 'doey',
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    rsp = requests.put(BASE_URL+'start',data=data,headers=headers)

    if rsp.ok:
        data = json.loads(rsp.text)
        token = data['message']
        return token
    return None

def search(data: Dict) -> str:
    result = search_recurs(data['haystack'], data['needle'])
    return result['name']

def search_recurs(node: Dict, value: int):

    if node is None or node['data'] == value:
        return node
    
    if node['data'] < value:
        return search_recurs(node['right_child'], value)
    
    return search_recurs(node['left_child'], value)

def count(data: Dict) -> int:
    result = count_recurs(data)
    return result

def count_recurs(node: Dict) -> int:
    if node == None:
        return 0
    
    return 1 + count_recurs(node['left_child']) + count_recurs(node['right_child'])

def largest(data: Dict) -> str:
    result = largest_recurs(data)
    result_node = search_recurs(data, result)
    return result_node['name']

def largest_recurs(node: Dict) -> int:
    # Base case
    if (node == None):
        return float('-inf')
  
    # Return maximum of 3 values:
    # 1) Root's data 2) Max in Left Subtree
    # 3) Max in right subtree
    res = node['data']
    lres = largest_recurs(node['left_child'])
    rres = largest_recurs(node['right_child'])
    if (lres > res):
        res = lres
    if (rres > res):
        res = rres
    return res

def sort(data: List):
    new_data = data
    new_data.sort()
    return new_data

def divisible(data: Dict):
    value = data['value']
    candidates = data['candidates']

    result = []
    for candidate in candidates:
        if candidate % value == 0:
            result.append(1)
        else:
            result.append(0)

    return result

TASK_TYPES = {
    'search': search,
    'count': count,
    'largest': largest,
    'sort': sort,
    'divisible': divisible,
}

def real_data(token: str) -> Dict or None:
    rsp = requests.get(BASE_URL+'tasks', headers={'Auth':token})

    if rsp.ok:
        data: Dict = json.loads(rsp.text)
        return data
    return None

def test_data() -> Dict:
    data = {
        'search_task': {
            'type': 'search',
            'data': {
                "needle": 1004,
                "haystack": {
                    "name": "a", "data": 1002,
                    "left_child": {
                        "name": "b", "data": 1003, "left_child": None, "right_child": None},
                    "right_child":
                        {"name": "c", "data": 1004, "left_child": None, "right_child": None}
                }
            }
        },
        'count_task': {
            'type': 'count',
            'data': {
                "name": "a", "data": 1002, "left_child":
                {"name": "b", "data": 1003, "left_child": None, "right_child": None},
                "right_child":
                {"name": "c", "data": 1004, "left_child": None, "right_child": None}
            }
        },
        'sort_task': {
            'type': 'sort',
            'data': [13, 5, 8, 4, 10, 9]
        },
        'largest_task': {
            'type': 'largest',
            'data': {
                "name": "a", "data": 1002, "left_child":
                {"name": "b", "data": 1003, "left_child": None, "right_child": None},
                "right_child":
                {"name": "c", "data": 1004, "left_child": None, "right_child": None}
            }
        },
        'divisible_task': {
            'type': 'divisible',
            'data': {
                'value': 10,
                'candidates': [5, 10, 15, 20, 25, 30]
            }
        },
    }
    return data

def main():
    REAL_DATA = True

    if REAL_DATA:
        token = sign_in()
        if token:
            data = real_data(token)

            if data:
                results = {}
                for key, value in data.items():
                    chal_func = TASK_TYPES.get(value['type'])
                    if chal_func:
                        result = chal_func(value['data'])
                        results[key] = result
                rsp2 = requests.post(BASE_URL+'results',headers={'Auth':token},data=json.dumps(results))
                data2 = json.loads(rsp2.text)
                print(data2)
    else:
        data = test_data()

        results = {}
        for key, value in data.items():
            chal_func = TASK_TYPES.get(value['type'])
            result = chal_func(value['data'])
            if result:
                results[key] = result
        print(results)
        
main()