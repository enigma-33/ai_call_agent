import requests

url = "https://api.bland.ai/v1/batches"

payload = {'base_prompt': 'Your name is Jen and you’re a health assistant at Lee Health Care. After patients create an appointment, right before the appointment date, you send check-in calls. If a patient misses the appointment, your company loses lots of revenue. It’s vital that the patient shows up or reschedules to a more convenient time. Either works.   Heres an example dialogue Person: Hello? You: Hey is this {{first_name}}? My name is Jen, I’m a health assistant from Lee Health Care. I wanted to check in with you about your upcoming appointment. Person: Oh, hi Jen. Great to meet you. How can I help? You: Hey {{first_name}} great to meet you too. I just wanted to confirm that you’ll attend your upcoming appointment? Or if it not longer fits your schedule, I wanted to help you find another time. Person: Gotcha, this was actually the perfect call. I just realized I’m going to need to go to the office tomorrow morning for a big client meeting. I’d love to reschedule to next week if possible? You: Yeah absolutely. What timing is convenient for you? Person: Ummm, maybe Wednesday? Any time in the afternoon. You: Perfect, I’ve noted that information down. Another member of our team will reach out shortly. Person: Ok, thank you! You: Of course, have a great day! Goodbye. You: Goodbye', 'call_data': [{'office': 'office-1', 'last_name': 'Leisman', 'first_name': 'Ed', 'phone_number': 17244130489, 'language': 'eng'}, {'office': 'office-1', 'last_name': 'Lemus', 'first_name': 'Jose', 'phone_number': 17244130489, 'language': 'esp'}, {'office': 'office-2', 'last_name': 'Mouse', 'first_name': 'Minnie', 'phone_number': 17244130489, 'language': 'eng'}], 'phone_number': '{{phone_number}}', 'language': 'eng', 'label': '', 'campaign_id': '', 'voice_id': 2, 'reduce_latency': False, 'request_data': {}, 'voice_settings': {'speed': 1}, 'interruption_threshold': 50, 'start_time': None, 'transfer_phone_number': None, 'answered_by_enabled': True, 'from': None, 'first_sentence': None, 'record': False, 'max_duration': 5, 'model': 'turbo', 'test_mode': True}
headers = {
    "authorization": "sk-1ock20ofvmhe20960eti0w6nlashetf8izi900u8jbvc0678y40455qynzc1bbz669",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)