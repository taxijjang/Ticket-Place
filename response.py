from flask import jsonify

class Response:
    RESPONSE_STATUS = {
        'NORMAL': 200,
        'BAD_REQUEST': 400,
        'UNAUTHORIZED': 401,
        'FORBIDDEN': 403,
        'NOT_FOUND': 404,  # Server
        'TOO_MANY_REQUEST': 429,
        'INTERNAL_SERVER_ERROR': 500,  # Server
    }

    RESPONSE_MESSAGE = {
        'NORMAL': 0,  # 정상
        'NOT_FOUND': 404,
    }

    def __call__(self, status='NORMAL', message='NORMAL', data=None):
        '''
        :param status: 상태
        :param message: 메시지
        :param data: 데이터

        :return jsonify(content)
        '''

        content = dict()
        content['status'] = self.RESPONSE_STATUS[status]
        content['message'] = self.RESPONSE_MESSAGE[message]

        if data:
            content['data'] = data

        return jsonify(content)
