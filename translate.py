"""
    Here we will use the Amazon Translate to translate the text from one language to another.
"""

import boto3

translate_client = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)


def translate_text(text_to_translate, source_language_code, target_language_code):
    result = translate_client.translate_text(Text=text_to_translate, SourceLanguageCode=source_language_code,
                                             TargetLanguageCode=target_language_code)

    return result.get('TranslatedText')
