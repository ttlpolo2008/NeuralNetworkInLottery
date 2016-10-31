import random
import httplib
from StringIO import StringIO
import json
import time
import sys
import numpy as np
import itertools as its

def load_csv(file_name, headers, delimiter):
    import csv
    with open(file_name, 'rb') as csv_file:
        spamreader = csv.reader(csv_file, delimiter=delimiter, quotechar='|')
        data = []
        # read header
        data = [[str for str in next(spamreader)]]
        for row in spamreader:
            # check format
            # TODO: create object
            line = [int(str) for str in row]
            data.append(line)
        return data


def export_csv(file_name, headers, delimiter, data):
    import csv
    with open(file_name, 'wb') as csv_file:
        spamwriter = csv.writer(csv_file, delimiter=delimiter)
        spamwriter.writerow(headers)
        # validate ROW
        # write to file
        for idx, ln in enumerate(data):
            line = [idx + 1]
            line = line + [item for item in ln]
            spamwriter.writerow(line)

def calc_entropy(probabs):
    if isinstance(probabs, (np.ndarray, np.generic)):
        probabs_transpose = np.transpose(probabs)
        log_probabs = np.log(probabs_transpose)
        return np.sum(-np.dot(probabs, log_probabs)) / len(probabs)
    return 0.0

def combination(n, k):
    return list(its.combinations(xrange(1, n + 1), k))

def send_request_to_randomdotorg(n, min_r, max_r):
    conn = httplib.HTTPSConnection("api.random.org")
    request_body = {"jsonrpc":"2.0",
                    "method":"generateIntegers",
                    "params":{"apiKey":"e12737be-f964-46cf-ab73-ebec83f63643",
                              "n":n,
                              "min":min_r,
                              "max":max_r,
                              "replacement": False,
                              "base": 10},
                    "id":random.randint(1, 1000000)}
    conn.request("GET", "/json-rpc/1/invoke", body=json.dumps(request_body))
#     conn.request("GET", "https://www.random.org/integers/?num=10&min=1&max=6&col=1&base=10&format=plain&rnd=new")
    response = conn.getresponse()
    data = response.read()
    print data

if __name__ == '__main__':
    probabs = np.array([[0.8, 0.9, 0.5]])
    n = 10
    k = 4
    export_csv('test_csv.csv', ['index','1st', '2nd', '3rd', '4th'], ',', combination(n, k))
    data = load_csv('test_csv.csv', ['index','1st', '2nd', '3rd', '4th'], ',')
    send_request_to_randomdotorg(6, 1, 45)
    sys.exit(calc_entropy(probabs))


