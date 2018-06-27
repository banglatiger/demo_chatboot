#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

train=True

chatbot = ChatBot(
    "Experto_cruceros",

    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database_uri='mongodb://root:root@ds153710.mlab.com:53710/mothership',
    database='mothership',
    
    input_adapter="chatterbot.input.TerminalAdapter",
    
    output_adapter="chatterbot.output.OutputAdapter",
    output_format="text",

    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
            "response_selection_method": "chatterbot.response_selection.get_most_frequent_response"
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.51,
            'default_response': 'Disculpa, no te he entendido bien, sólo soy experto en viajes. ¿Puedes ser más específico?.'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'Quiero reservar un crucero',
            'output_text': 'Puedes reservarlo ahora en: https://www.logitravel.com/cruceros/'
        },
    ],
    
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    
    read_only=True,
)

DEFAULT_SESSION_ID = chatbot.default_conversation_id

if train:
    chatbot.set_trainer(ChatterBotCorpusTrainer)
    chatbot.train("./corpus_oxxo.yml")


while True:
    input_statement = chatbot.input.process_input_statement()
    statement, response = chatbot.generate_response(input_statement, DEFAULT_SESSION_ID)
    print("\n%s\n\n" % response)