import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from telegram_bot.process_messages.process_message import ProcessMessage
from telegram_bot.process_messages.utils import process_user_message


@csrf_exempt
@require_POST
def telegram_webhook(request):
    data = json.loads(request.body.decode('utf-8'))

    if 'message' in data:
        if data['message'].get('text'):
            message_data = process_user_message(data['message'])
            ProcessMessage(message_data=message_data).process_message()
    elif 'callback_query' in data:
        from_user_dict = data['callback_query']['from']
        message_data = process_user_message(
            message=data['callback_query']['message'],
            from_user_dict=from_user_dict
        )
        callback_query = data['callback_query']['data']
        ProcessMessage(
            message_data=message_data,
            callback_query_data=callback_query
        ).process_callback_query()

    return JsonResponse({'status': 'ok'})
