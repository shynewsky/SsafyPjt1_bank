# 🌤️ 날씨  
---

## OpenWeather API 사용하는 방법
- `import requests`  : 서버에게 요청할 수 있는 라이브러리를 불러온다  
- `from pprint import pprint` : pretty print 기능을 불러온다  
- `API_KEY =`  → API 를 가져온 다음에  
- `https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}`  
  → 이 링크를 f-string 으로 작성해서 채울 수 있도록  
- `lat = 37.56`, `lon = 126.97`  → 서울의 위도와 경도를 설정해준다  
- `response = requests.get(url).json()`  
  → 조립한 링크를 가져오도록 요청을 하고 `.json()` 으로 json 에서 dict 형식으로 변환한다  
- `return response`  → 추후 response 정보를 사용할 수 있도록 dict 전체를 반환한다  

---

## 딕셔너리에서 key 값 추출하기
```python
key_list = []
for key in response :
    key_list.append(key)
print(key_list)
```
- 처음에 for 문과 list 를 사용해서 key 를 추출하고 담았었다

```python
key = response.keys()
print(key)
```
- 하지만 `keys()` 함수를 사용하면, dict 자료형에서 key 만 뽑아서 리스트로 반환해준다  
- 그래서 따로 리스트를 사용할 필요도, `for`을 사용할 필요도 없다  
- 특이한건 key를 추출하면 자동으로 `dict_keys` 라는 리스트 명으로 출력된다는 것이다  

---

## 한국어로 된 키의 딕셔너리 만들기
```
https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}&lang=kr
```
- 처음에는 URL을 수정해서 한국어로 바꿔야 하는 것인 줄 알았다  
- API 사이트에서 옵션을 찾아봤고 `kr`을 시도했지만, '맑음' 하나만 한국어로 나왔다  
- 다른 사람들 하는 것을 찾아봤더니, 한국어 키를 갖는 딕셔너리를 직접 만드는 것 같았다  

---

## 가독성 좋게 딕셔너리 선언하기

이전 방식:
```python
dict_main_weather = {
    'main' : response['main']
    'weather' : response['weather']
}
```

개선한 방식:
```python
dict_main_weather = {}
dict_main_weather['main'] = response['main']
dict_main_weather['weather'] = response['weather']
```

- 빈 딕셔너리를 선언하고, 키를 만들면서 값을 넣는 것이 더 가독성이 좋아보였다

---

## 화씨에서 섭씨로 바꿔서 추가하기
```python
dict_kr['기본']['체감온도(섭씨)'] = response['main']['feels_like'] - 273.15
```

- 부동소수점으로 인해 무한소수로 나오는 문제가 생겼다  
- 그래서 `round( , 2)` 함수를 사용해서 소수점 2자리까지 반올림하였다

```python
dict_kr['기본']['체감온도(섭씨)'] = round(response['main']['feels_like'] - 273.15, 2)
```

---

# 💸 금융  
---

- 대부분 코드 구성이 '날씨' 프로젝트와 많이 비슷했다

---

## 리스트 안에 딕셔너리 넣기 구조
```python
리스트 선언 = []
for 문으로 리스트 순회
    딕셔너리 선언 = {}
    딕셔너리 채워넣기
    리스트에.append(딕셔너리 추가하기)
```

- 리스트 하나 안에 딕셔너리 여러개 안에 리스트 하나 안에 딕셔너리 여러개 넣는 구조에서 틀렸다  
- 위에 작성한 구조를 눈치채고 사용했으면 좋았을텐데, `for`문 밖에 딕셔너리를 선언해서 오래 헤맸다  

---

## 중첩 구조 예시
```python
큰 리스트 선언 = []
for 문으로 큰 리스트 순회
    큰 딕셔너리 선언 = {}
    큰 딕셔너리 채워넣기

    큰 딕셔너리에 작은 리스트 선언 = []
    for 문으로 작은 리스트 순회
        작은 딕셔너리 선언 = {}
        작은 딕셔너리 채워넣기
```

---

## del 키워드 실수

- 딕셔너리에서 `'금융상품코드'` 를 빼야했는데, 새로운 딕셔너리를 만드는 대신 `del`을 사용해봤다  
- `del`은 변수, 리스트 요소, 딕셔너리 키, 객체 자체 등을 삭제하는 키워드이다  
- 메모리에서 삭제하거나 이름 바인드를 끊는데에 사용된다  
- 딕셔너리 키를 삭제하면 자동으로 값도 함께 사라진다  

---

## 루프 중 키 삭제 문제
```python
for base_dict in baseList:
    for option_dict in optionList_kr:
        del option_dict['금융상품코드']  # 여기서 오류 발생 가능
```

- `optionList_kr`의 모든 딕셔너리에서 `'금융상품코드'`가 사라진 상태에서 다시 `del` 하려고 해서 문제가 생김  

해결 방법:
```python
option_copy = option_dict.copy()
del option_copy['금융상품코드']
```

- 루프를 도는 원본 `option_dict`은 유지하고, 복사한 딕셔너리에서만 삭제
