from . import *
import os
import openai


class openAiApi(Component):

    def __init__(self, env: Environment):
        super().__init__(env, '/api/openAiApi', 'openAiApi', ['GET', 'POST'])
        self.env = env

    # when frontend request this api, this function will be called
    def view(self):
        apiKey = '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'

        data = request.get_json()
        prompt = data['prompt']
        temp = data['temp']
        temp = float(temp)
        print(prompt)
        print(temp)

        openai.api_key = apiKey

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temp
        )

        message = completion.choices[0].message.content

        return {'status': 'ok', 'text': message}
