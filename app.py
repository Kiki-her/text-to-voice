import os
from google.cloud import texttospeech

import io
import streamlit as st

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = dotenv_path

def synthesize_speech(text, lang='日本語', gender='defalut'):
    gender_type = {
        'defalut': texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED,
        'male': texttospeech.SsmlVoiceGender.MALE,
        'female': texttospeech.SsmlVoiceGender.FEMALE,
        'neutral': texttospeech.SsmlVoiceGender.NEUTRAL,
        'デフォルト': texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED,
        '男性': texttospeech.SsmlVoiceGender.MALE,
        '女性': texttospeech.SsmlVoiceGender.FEMALE,
        'ニュートラル': texttospeech.SsmlVoiceGender.NEUTRAL,
    }
    lang_code = {
        'English': 'en-US',
        '日本語': 'ja-JP'
    }

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=lang_code[lang], ssml_gender=gender_type[gender]
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response

page_lang = st.radio("Lang", ["日本語", "English"])

if page_lang == "日本語":
    st.title('音声出力アプリ')

    st.markdown('### データ準備')

    input_option = st.selectbox(
        '入力データの選択',
        ('直接入力', 'テキストファイル')
    )
    input_data = None

    if input_option == '直接入力':
        input_data = st.text_area('こちらにテキストを入力してください。', 'Cloud Speech-to-Text用のサンプル文になります。')
    else:
        uploaded_file = st.file_uploader('テキストファイルをアップロードしてください。', ['txt'])    
        if uploaded_file is not None:
            content = uploaded_file.read()
            input_data = content.decode()

    if input_data is not None:
        st.write('入力データ')
        st.write(input_data)
        st.markdown('### パラメータ設定')
        st.subheader('言語と話者の性別選択')

        lang = st.selectbox(
            '言語を選択してください',
            ('日本語', 'English')
        )
        gender = st.selectbox(
            '話者の性別を選択してください',
            ('デフォルト', '男性', '女性', 'ニュートラル')
        )
        st.markdown('### 音声合成')
        st.write('こちらの文章で音声ファイルの生成を行いますか？')
        if st.button('開始'):
            comment = st.empty()
            comment.write('音声出力を開始します')
            response = synthesize_speech(input_data, lang=lang, gender=gender)
            st.audio(response.audio_content)
            comment.write('完了しました🎉🎉')
else:
    st.title('Audio output App')

    st.markdown('### Data prep')

    input_option = st.selectbox(
        'Select of input data',
        ('Direct input', 'Upload txt file')
    )
    input_data = None

    if input_option == 'Direct input':
        input_data = st.text_area('Please enter your text here.', 'This is sample text for Cloud Speech-to-Text.')
    else:
        uploaded_file = st.file_uploader('Please upload txt file.', ['txt'])    
        if uploaded_file is not None:
            content = uploaded_file.read()
            input_data = content.decode()

    if input_data is not None:
        st.write('Input data')
        st.write(input_data)
        st.markdown('### Parameter Setting')
        st.subheader('Language and speaker gender selection')

        lang = st.selectbox(
            'Pleace select language',
            ('English', '日本語')
        )
        gender = st.selectbox(
            'Pleace select speaker gender',
            ('default', 'male', 'female', 'neutral')
        )
        st.markdown('### Speech synthesis')
        st.write('Would you like to generate an audio file with this text?')
        if st.button('Start'):
            comment = st.empty()
            comment.write('Start audio output')
            response = synthesize_speech(input_data, lang=lang, gender=gender)
            st.audio(response.audio_content)
            comment.write('Completed🎉🎉')