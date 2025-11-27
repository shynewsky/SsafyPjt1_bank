import requests
from pprint import pprint

def get_weather() :

    #API KEY
    API_KEY = '2f7922c6ee918b5904d3a188767ced3f'

    #서울의 위도와 경도
    lat = 37.56
    lon = 126.97

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"

    #API 요청 보내기
    response = requests.get(url).json()

    #날씨 데이터 출력하기
    # pprint(response)   
    return response

#key 값만 출력하기 (F01)
#for key in response.keys(): dict_keys.append(key) 로 할 수 있지만, .keys() 자체가 dict_keys[] 라는 리스트를 만들어준다
def print_keys(response) : 
    key = response.keys() #key 자체가 리스트 자료형이 된다
    # print(key)

#key 값이 (main, weather) 인 데이터만 따로 구성 (F02)
def main_and_weather(response) :
    dict_main_weather = {}
    dict_main_weather['main'] = response['main']
    dict_main_weather['weather'] = response['weather']
    # pprint(dict_main_weather)
    return dict_main_weather

# 다국어지원) 한국어로 변환한 새로운 딕셔너리 (F03)
# dict_kr = { 기본 : { 체감온도 : response['main']['feels_like']}} 이런식으로 만들어도 되긴 하지만, 가독성이 떨어진다
def dict_to_korean(response) :
    dict_kr = {}
    dict_kr['기본'] = {}
    dict_kr['기본']['체감온도'] = response['main']['feels_like']
    dict_kr['기본']['지면기압'] = response['main']['grnd_level']
    dict_kr['기본']['습도'] = response['main']['humidity']
    dict_kr['기본']['압력'] = response['main']['pressure']
    dict_kr['기본']['해수면기압'] = response['main']['sea_level']
    dict_kr['기본']['온도'] = response['main']['temp']
    dict_kr['기본']['최고온도'] = response['main']['temp_max']
    dict_kr['기본']['최저온도'] = response['main']['temp_min']
    dict_kr['날씨'] = {}
    dict_kr['날씨']['요약'] = response['weather'][0]['description']
    dict_kr['날씨']['아이콘'] = response['weather'][0]['icon']
    dict_kr['날씨']['식별자'] = response['weather'][0]['id']
    dict_kr['날씨']['핵심'] = response['weather'][0]['main']
    #pprint(dict_kr)
    return dict_kr

# 화씨에서 섭씨로) (F04)
def add_celcius(dict_kr, response) :
    dict_kr['기본']['체감온도(섭씨)'] = round(response['main']['feels_like'] - 273.15, 2)
    dict_kr['기본']['온도(섭씨)'] = round(response['main']['temp'] - 273.15, 2)
    dict_kr['기본']['최고온도(섭씨)'] = round(response['main']['temp_max'] - 273.15, 2)
    dict_kr['기본']['최저온도(섭씨)'] = round(response['main']['temp_min'] - 273.15, 2)
    #pprint(dict_kr)
    return dict_kr

response = get_weather()
print_keys(response) #01
dict_main_weather = main_and_weather(response) #02
dict_kr = dict_to_korean(dict_main_weather) #03
dict_cel = add_celcius(dict_kr, response) #04
