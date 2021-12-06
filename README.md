CAN WE MEET
=============

> **음성기반 감정인식을 활용한 회의 및 자동 회의록 서비스**
2020.09~2020.12
세종대학교 소프트웨어학과 캡스톤디자인 프로젝트

***제 10회 세종대학교 창의 설계 경진대회 장려상 수상***
> 

## **설명**

감정을 이용한 회의 분석과 실시간 작성되는 자동 회의록을 통해 똑똑하고 선명한 협업을 돕는다. 음성 인식을 통해 자동으로 원격회의의 모든 것을 기록하며, 실시간 감정분석 인공지능이 전달하는 메시지로 회의 내 다채로운 소통을 가능케 한다.

1. **화상 회의 기능**
    
    2명 이상의 화상 회의가 가능하며 WebRTC를 사용한다. 이는 개방형 표준에서 작동하는 응용 프로그램에 실시간 통신 기능을 추가할 수 있게 하며 미디어 장치 접근이 가능하게 한다. Javascript API로 제공된다.
    
2. **회의록 자동 저장**
    
     회의록 자동 저장을 위해, 회의 중 실시간으로 들어오는 음성입력을 텍스트화하여 저장한다. 브러우저에서 기본으로 제공하는 Web Speech를 이용한다. 실시간으로 음성을 입력받아, 사용자 정보와 비교하여 데이터베이스에 저장한다. 데이터베이스에 저장한 후, socket을 이용하여 사용자의 현재 채팅창에 텍스트를 띄운다.
    
3. **음성기반 감정인식 모델 SER (Speech-Emotion-Recognition)**
    
     음성을 통해 감정을 인식하는 모델을 만든다. 컨볼루션 신경망을 통해 구축한다. 모델 구축이 완료되면, 해당 데이터의 Zero-Crossing Rate, Chroma_stft, MFCC, RMS value, MelSpectogram을 추출하여 모델을 학습시킨다. 
     
-------------
# Environment
## 개발환경
* Web Frontend: HTML5, CSS3, JavaScript, jQeury
* Web Backend: Python/Flask
* Database: MySQL
* STT(Speech-to-Text): Google Web Speech API, Socket IO
* Meeting API: Twilio

## Virtural Environment
* OS: Windows 10
* Python Version: 3.7
* Packages
  * Flask
  * pyngrok
  * twilio
  * gevent-websocket
  * Flask-SocketIO
  * PyAudio
  * Flask-SQLAlchemy
  * mysql-connector-Python

## Server Environment
* OS: Ubuntu18.06(linux)
* SSH Client: PuTTY
* Packages
  * mysql-server
  * Python3
  * dockcer
  * tensorflow
  
## Deep learning Environment
* Model: CNN, Convolutional Neural Network
* Type: Tensorflow SavedModel
* DataSet
  * 제공 데이터: 회의와 무관한 문장을 Happy, Sad, Angry, Neutral 4가지 감정으로 읽은 한국어 음성파일(600개)
  * 자체 데이터: 자체 제작한 회의 스크립트에 맞춰 4가지의 감정으로 분류하여 직젖ㅂ 음성 데이터 생성(약 300개)
* Libraries
  * librosa
  * sklearn
  * keras
  * tensorflow
 
 # Owner
 * 이정음
 * 김혜인
 * 윤소현
 * 최한나

# Video
https://drive.google.com/file/d/1DIZJXKk7bZVXJLCk7akwirp_tg4B7uSe/view?usp=sharing
