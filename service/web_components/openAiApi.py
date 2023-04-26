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
       # apiK = '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'
        data = request.get_json()
        prompt = data['prompt']
        temp = data['temp']
        print(prompt)
        print(temp)

        openai.api_key = apiKey

        completion = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
            {"role": "user", "content": prompt}
          ]
        )

        print(completion.choices[0].message)



        # you can get the request args by request.args.get('argName')
        arg1 = request.args.get('arg1')
        # you can reutrn a dict, it will be converted to json automatically
        return {'status': 'ok', 'arg1': arg1}