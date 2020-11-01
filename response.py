from flask import jsonify


class Response:
    def __init__(self):
        self.RESPONSE_STATUS = {
            'NORMAL': 200,
            'CREATE': 201,
            'BAD_REQUEST': 400,
            'UNAUTHORIZED': 401,
            'FORBIDDEN': 403,
            'NOT_FOUND': 404,
            'METHOD_NOT_ALLOWED' : 405,
            'NOT_ACCEPTABLE':406,
            'CONFLICT': 409,
            'TOO_MANY_REQUEST': 429,
            'INTERNAL_SERVER_ERROR': 500,  # Server
        }

        self.RESPONSE_MESSAGE = {value: key for key, value in self.RESPONSE_STATUS.items()}

    def __call__(self, status=200, message=0, data=None, unit_test=False):
        '''
            :param status: 상태
            :param message: 메시지
            :param data: 데이터

            :return jsonify(content)
        '''

        content = dict()

        if data:
            content['data'] = data

        content['message'] = self.RESPONSE_MESSAGE[self.RESPONSE_STATUS[status]]
        content['status'] = self.RESPONSE_STATUS[status]

        # unit test X
        if not unit_test:
            return jsonify(content)

        # unit test O
        elif unit_test:
            return content
