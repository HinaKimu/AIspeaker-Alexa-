# -*- coding: utf-8 -*-
"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
from datetime import datetime
from libs.func import *
import requests
import random
import json
import boto3


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, card_content, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': card_content
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# ---------------Original Func Search-------------------------------------------


def start_search(intent, session):
    session_attributes = {}
    reprompt_text = None

    should_end_session = False

    if 'value' in intent['slots']['unumber']:
        unumber = intent['slots']['unumber']['value']
        params_unumber = {"unumber": unumber}
        search_key_unumber = unumber

    if 'value' in intent['slots']['nteam']:
        nteam = intent['slots']['nteam']['value']
        params_nteam = {"nteam": nteam}
        search_key_nteam = nteam


    else:
        # 喋らせたい文を作成
        speech_output = "検索条件を指定してもう一度話しかけてください"
        return build_response(session_attributes, build_speechlet_response(
            title="検索条件を指定してください", output=speech_output, card_content = "選手",reprompt_text=reprompt_text,
            should_end_session=should_end_session))

    s3 = boto3.client('s3')

    bucket_name = 'nifty-team-a'
    file_name = 'member/samplemember.json'

    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    body = response['Body'].read()

    bodystr = body.decode('utf-8')
    # lines = bodystr.split('\r\n')

    print(bodystr)

    rjson = json.loads(bodystr)

    # 喋らせたい文を作成
    speech_output = search_key_nteam + "のチームの背番号" + search_key_unumber + "の人は"\
                    + rjson["name"] + "です。" \
                    + "所属チームは"\
                    + rjson["current_team"] + "です。"\
                    + "関連のニュースとプロフィールどっちが知りたいですか?"

    session_attributes = {"player": rjson["name"]}


    return build_response(session_attributes, build_speechlet_response(
        "選手名", speech_output, speech_output, reprompt_text, should_end_session))

# --------------- Original Func news -------------------------------------------


def start_news(intent, session):
    session_attributes={"player": session['attributes']['player']}
    reprompt_text = None

    should_end_session = False

    if 'value' in intent['slots']['newsprofile']:
        judge = intent['slots']['newsprofile']['value']

    else:
        # 喋らせたい文を作成
        speech_output = "検索条件を指定してもう一度話しかけてください"
        return build_response(session_attributes, build_speechlet_response(
            title="検索条件を指定してください", output=speech_output, card_content = "選手", reprompt_text=reprompt_text,
            should_end_session=should_end_session))


    s3 = boto3.client('s3')

    bucket_name = 'nifty-team-a'

    file_name = 'hoge'

    if judge == "ニュース":
        file_name = 'news/samplenews.json'
    elif judge == "プロフィール":
        file_name = 'member/samplemember.json'

    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    body = response['Body'].read()

    bodystr = body.decode('utf-8')
    # lines = bodystr.split('\r\n')

    print(bodystr)

    rjson = json.loads(bodystr)

    print(session)

    card_content = ""
    if judge == "ニュース":
        speech_output = session['attributes']['player'] + "のニュースは次のようなものがあります"
        speech_output = rjson["warp_up"][random.randrange(3)]
        card_content = rjson["url"]

    elif judge == "プロフィール":
        speech_output = rjson["name"]+"選手" \
        +"誕生日は"+rjson["birthday"]\
        +"出身地は"+rjson["origin"]\
        +"身長は"+rjson["htight"]\
        +"体重は"+rjson["weight"]\
        +"現在の所属は"+rjson["current_team"]\
        +"ポジションは"+rjson["position"]\
        +"利き足は"+rjson["foot"]\
        +"です"
        card_content = speech_output

    return build_response(session_attributes, build_speechlet_response(
        judge, speech_output, card_content, reprompt_text, should_end_session))


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "検索するよ"

    speech_output = "こんにちは。チームと背番号でサッカー選手を検索するよ。"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "please prompt"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, "開始", reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "終了"
    r = requests.get("http://weather.livedoor.com/forecast/webservice/json/v1?city=130010")
    rjson = r.json()

    speech_output = "検索を終了します。" \
                    + rjson["forecasts"][1]["dateLabel"] + "の天気は" + rjson["forecasts"][1]["telop"] + "だよ。" \
                    + "また使ってね。"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, "終了", None, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # 起動時に分岐させたい場合は、ここに条件文をかく
    # 今回は固定で返却
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # 自作したインテント(インテントが増えた場合はここを追加)
    if intent_name == "PlayerSearchIntent":
        return start_search(intent, session)
    # 関連ニュースインテント
    if intent_name == "NewsProfileIntent":
        return start_news(intent, session)
    # 終了インテント(Amazon default)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    # 一致しない場合は例外を投げる
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler: 最初に呼び出される箇所 ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    # セッションを開始する場所
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    # 最初の条件分岐
    # 1. 起動リクエスト
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    # 2. インテントリクエスト(Developerで作成したやつ)
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    # 3. 終了リクエスト
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
