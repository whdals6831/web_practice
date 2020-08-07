import requests
from bs4 import BeautifulSoup
import json

def read_json() : 
    with open('./movie_data.json', 'r', encoding='UTF-8') as json_data:
        movie_data = json.load(json_data)
    return movie_data


def write_json(movie) :
    with open('./movie_data.json', 'w', encoding='UTF-8') as json_data:
        json.dump(movie, json_data, ensure_ascii=False, indent=4)


def movie_crawling() :
    URL = 'https://movie.naver.com/movie/running/current.nhn'

    movie_code_response = requests.get(URL)
    movie_code_soup = BeautifulSoup(movie_code_response.text, 'html.parser')
    current_movie_section = movie_code_soup.select('div[id=wrap] > div[id=container] > div[id=content] > div[class=article] > div[class=obj_section] > div[class=lst_wrap] > ul[class=lst_detail_t1] > li')
    
    movie_list = []

    for movie in current_movie_section :

        movie_data = {
            "title" : "",
            "code" : "",
        }

        a_tag = movie.select_one('dl > dt > a')
        movie_data['title'] = a_tag.contents[0]
        code = a_tag['href']
        equl_index = code.find('=')+1
        movie_data['code'] = code[equl_index:]
        
        movie_list.append(movie_data)

    movie = read_json()
    movie['movie_data'] = movie_list
    write_json(movie)

    
    # 영화의 리뷰와 평점 가져오기
    final_movie_data = read_json()['movie_data']

    headers = {
    'authority': 'movie.naver.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'iframe',
    'referer': 'https://movie.naver.com/movie/bi/mi/point.nhn?code=189069',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NNB=PGANISUE6ABF6; NaverSuggestUse=use%26unuse; NRTK=ag#20s_gr#4_ma#2_si#2_en#2_sp#2; NMUPOPEN=Y; _fbp=fb.1.1594628419149.131174204; MM_NEW=1; NFS=2; MM_NOW_COACH=1; _ga=GA1.1.1744766986.1594083824; _ga_4BKHBFKFK0=GS1.1.1596287156.1.1.1596287208.8; nid_inf=-1609332670; NID_AUT=pCn/Vr0ea5gcaffDsleurIGEnGf/aMzsSQa03u1Ta4slbzdMb2a6xkuP77Cjanfc; NID_JKL=PjO7+XmolDM+bUmewJkS/sUTFctdGTCHdqT3NEP1v1Q=; nx_ssl=2; NM_THUMB_PROMOTION_BLOCK=Y; NM_VIEWMODE_AUTO=basic; NID_SES=AAABeH62ENhM27RoPic7dxPffImoe7gfHcCPnGX94o6EnZDuu6m7SjZsHUZLUJyTqg/WdkoGy1ZELCJi4fcwb3BBUeB/kgDPVDIReJTzcJd1H3/mjXuDpKR1YEQ9HXssSmMM8Rw83IfLLbnsB6o63t9JuQ2ZmE+QTfMHWCSMzQs0Y66hnmiG5VdHCKPQjnU5ov5ol1n0eaXnOcHLERb7qGTxE98y0r8+mJFgiWuYf+4wZzUAtl5TxWffnM1r70EO8Fv7vpA6g/80oXt0renovdRkO7nkAHZwqYLAZGa2dDtHQR6nqAT2yGgPY7OPVVZhsQw7PjNLf4DDT3GBMstSesyTg8FQNRhLX+kCCNiqmWlu/mtsbBmAWfwyk7TwWjvKJvkckPIzgSSSg5wluZAnc/M7p3X9tD1F+oEEeGB/cml0qMWjYJRZ5unfLL07E371Zm0KJB1fdX60Yhk42eJ1oY5/jKoPsxHc8pXUPZLzrrUOdJKQlxotxkKcc/oRzgWiD61CHw==; JSESSIONID=106C2CC440C9271F3299476246D6EF00; csrf_token=76ba6295-3ddd-4ccd-8a24-a590cba6bfb3',
    }

    for movie in final_movie_data :
        movie_code = movie['code']

        params = (
            ('code', movie_code),
            ('type', 'after'),
            ('isActualPointWriteExecute', 'false'),
            ('isMileageSubscriptionAlready', 'false'),
            ('isMileageSubscriptionReject', 'false'),
        )

        response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', headers=headers, params=params)
        
        review_soup = BeautifulSoup(response.text, 'html.parser')

        review_list = review_soup.select('div.score_result > ul > li')

        i = 0
        for review_wrap in review_list :
            review_score = review_wrap.select_one(f'div.star_score > em').text

            if review_wrap.select_one(f'div.score_reple > p > span[id=_filtered_ment_{i}] > span[id=_unfold_ment{i}]') is None:
                review = review_wrap.select_one(f'div.score_reple > p > span[id=_filtered_ment_{i}]').text.strip()   
            else :
                review = review_wrap.select_one(f'div.score_reple > p > span[id=_filtered_ment_{i}] > span[id=_unfold_ment{i}] > a')['data-src']

            print(review_score, review)
            i += 1

movie_crawling()
        