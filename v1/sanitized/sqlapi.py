#!/usr/bin/python3
"""
    RESTful API to check user input
"""
from v1.sanitized import app_views
from flask import Flask, jsonify, request, make_response, abort
import operator


def check_op(input):
    """check the input containing a logical command
    return :
    -False (if there is no operator)
    -True (if there is no operator)
    """
    sqloperator = ["OR", "AND", "||"]
    ok = [a == b for a in sqloperator for b in input.upper().split()]
    if True in ok:
        return True
    return False


@app_views.route('/input', methods=['POST'], strict_slashes=False)
def get_users():
    """
    API for user input
    """
    mydict = {'=': operator.eq, '>': operator.gt, '<': operator.lt}
    check = ["--", ";", "\'", "\n", '"', ')', '(', "#", "\\*"]
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "payload" not in request.get_json():
        return make_response(jsonify({'error': 'Missing input'}), 400)
    input = request.get_json()["payload"]
    checkme = check_op(input)
    for i in input:
        if i in check:
            return make_response(jsonify({"result": "unsanitized"}), 406)
        if i in mydict and checkme:
            opindex = input.index(i)
            try:
                first = str(input[:opindex]).split()
                last = str(input[opindex + 1:]).split()
                rslt = mydict[i](first[len(first) - 1], last[0])
                if rslt:
                    return make_response(
                        jsonify({"result": "unsanitized"}), 406)
            except IndexError:
                pass
    return make_response(jsonify({"result": "sanitized"}), 200)
