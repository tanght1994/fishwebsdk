from django.http import JsonResponse as _JsonResponse


def JsonResponse(data=[], err_num=0, err_msg='', other_field=None):
    if data is None:
        data = []
    if not isinstance(data, list):
        data = [data]
    _data = {
        'err_num': int(err_num),
        'err_msg': str(err_msg),
        'data': data,
    }
    if isinstance(other_field, dict):
        _data.update(other_field)
    try:
        ret = _JsonResponse(data=_data, safe=False, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        ret = {'err_num': 1, 'err_msg': f'server json dump error, {str(e)}', 'data': []}
    return ret