import requests
from pprint import pprint

def get_finance() :

    #API KEY
    API_KEY = 'e890f865e3769d283e301acec04006e0'

    url = f"http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1"

    #API 요청 보내기
    response = requests.get(url).json()

    #날씨 데이터 출력하기
    #pprint(response)   
    return response

#key 값만 출력하기 (F06)
#for keys in response['result'].keys() ㅡ for 문으로 바꿀 필요가 없다. 이미 key만 모아서 list 로 반환
def make_dict_keys(response) : 
    keys = response['result'].keys()
    # pprint(keys)
    return keys

#key 값만 출력하기 (F07)
#for baseList in response['result']['baseList'] ㅡ for 문으로 바꿀 필요가 없다. 이미 key만 모아서 list 로 반환
def make_Baselist(response) :
    baseList = response['result']['baseList']
    # pprint(baseList)
    return baseList

# 다국어지원) 한국어로 변환한 새로운 딕셔너리 (F08)
# 리스트 안에 딕셔너리 넣는 방법
def make_optionList_kr(response) :

    optionList_en = response['result']['optionList']

    optionList_kr = []    
    for dict in optionList_en :
        dict_option = {} #리스트 하나 안에 여러 딕셔너리를 만들 것이기 떄문에 for 문 안에 넣어야 한다
        dict_option['금융상품코드'] = dict['fin_prdt_cd']
        dict_option['저축금리'] = dict['intr_rate']
        dict_option['저축기간'] = dict['save_trm']
        dict_option['저축금리유형'] = dict['intr_rate_type']
        dict_option['저축금리유형명'] = dict['intr_rate_type_nm']
        dict_option['최고 우대금리'] = dict['intr_rate2']
        optionList_kr.append(dict_option)

    pprint(optionList_kr)
    return optionList_kr

# 상품코드끼리 비교해서, 같은 상품코드끼리 회사와 상품명이 같은 딕셔너리로 묶기(F09)
# baseList 에서 fin_prdt_cd, kor_co_nm, fin_prdt_nm
# optionList에서 저축금리, 저축기간, 저축금리유형,저축금리유형명,최고우대금리 
# 금융상품코드(fin_prdt_cd) 기준으로 

def make_productList(baseList, optionList_kr) :

    # product_list = [] #상품정보 리스트  
    # for base_dict in baseList : #상품리스트 돌리기
    #     product_dict = {} #리스트 하나 안에 딕셔너리를 여러개 만들 것이기 때문에 for문 안에 만들어야 한다
    #     product_dict['금융회사명'] = base_dict['kor_co_nm'] #값은 가변형이기 때문에, 다른게 들어오면 덮어씌워지지만, 그때는 이미 새로운 딕셔너리가 만들어졌을 것이다
    #     product_dict['금융상품명'] = base_dict['fin_prdt_nm']

    #     product_dict['금리정보'] = [] #info_list를 만들어서 딕셔너리에 넣었는데, 딕셔너리를 먼저 만들고 키와 함꼐 
    #     for option_dict in optionList_kr : #옵션리스트 돌리기
    #         if base_dict['fin_prdt_cd'] == option_dict['금융상품코드'] : 
    #             product_dict['금리정보'].append(option_dict)
    #             option_copy = option_dict.copy()
    #             del option_copy['금융상품코드'] #금융상품코드 제거하기
    #     product_list.append(product_dict) #딕셔너리가 완성되면 전체리스트에 추가한다
    # pprint(product_list)

    product_list = [] #상품정보 리스트  
    for base_dict in baseList : #상품리스트 돌리기
        #딕셔너리를 여러개 만들 것이기 때문에 for문 안에 만들어야 한다
        info_list = [] #금리정보 리스트
        product_dict = { #상품정보 딕셔너리 
            '금리정보' : info_list,
            '금융상품명' : '',
            '금융회사명' : '',
        }
        for option_dict in optionList_kr : #옵션리스트 돌리기
            #상품 코드가 다르면 ㅡ 넘기기
            if base_dict['fin_prdt_cd'] != option_dict['금융상품코드'] : 
                continue
            #회사명이랑 상품명이 등록되지 않은 경우에 ㅡ 등록하기
            sameCompany = product_dict['금융회사명'] == base_dict['kor_co_nm']
            sameProduct = product_dict['금융상품명'] == base_dict['fin_prdt_nm']
            if not (sameCompany and sameProduct) :
                product_dict['금융회사명'] = base_dict['kor_co_nm'] #상품리스트에서 회사명 가져오기
                product_dict['금융상품명'] = base_dict['fin_prdt_nm'] #상품리스트에서 상품명 가져오기
            #금리정보 리스트에 옵션 딕셔너리 추가하기
            option_copy = option_dict.copy()
            del option_copy['금융상품코드'] #금융상품코드 제거하기
            product_dict['금리정보'].append(option_copy)
        #딕셔너리가 완성된 경우에 전체리스트에 추가한다
        product_list.append(product_dict)
    pprint(product_list)

# 함수 실행
response = get_finance()
# make_dict_keys(response) #06
baseList = make_Baselist(response) #07
optionList_kr = make_optionList_kr(response) #08
make_productList(baseList, optionList_kr) #09
