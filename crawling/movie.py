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

    response = requests.get(URL)

    soup = BeautifulSoup(response.text, 'html.parser')

    current_movie_section = soup.select('div[id=wrap] > div[id=container] > div[id=content] > div[class=article] > div[class=obj_section] > div[class=lst_wrap] > ul[class=lst_detail_t1] > li')

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

        
        movie = read_json()

        movie_title_list = []

        for movie_dict in movie['movie_data'] :
             movie_title_list.append(movie_dict['title'])
        
        if movie_data['title'] not in movie_title_list :
            movie['movie_data'].append(movie_data)

        write_json(movie)


movie_crawling()
        