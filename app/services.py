import requests
import google.generativeai as genai
from decouple import config
from datetime import datetime


class AstrologyService:
    def __init__(self):
        self.api_key = config('ASTROLOGY_API_KEY')
        self.base_url = 'https://json.freeastrologyapi.com'
        self.headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }
        # SVG URL 전용 매핑
        self.svg_url_map = {\
            'D2': 'd2-chart-url',
            'D3': 'd3-chart-url',
            'D7': 'd7-chart-url',
            'D9': 'd9-chart-url',
            'D10': 'd10-chart-url',
            'D12': 'd12-chart-url',
        }

    def get_varga_svg_urls(self, birth_data):
        """SVG URL 차트를 가져오는 메서드"""
        urls = {}
        for chart_type, endpoint in self.svg_url_map.items():
            resp = requests.post(
                f"{self.base_url}/{endpoint}",
                json=birth_data,
                headers=self.headers
            )
            data = resp.json()
            print(data)  # {'statusCode':200,'output':'https://…'}
            if resp.status_code == 200:
                # 'url' 대신 'output' 키에서 꺼내기
                urls[chart_type] = data.get('output')
            else:
                print(f"{chart_type} SVG URL 호출 실패: {resp.status_code}")
        return urls


class GeminiService:
    def __init__(self):
        genai.configure(api_key=config('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro')

    def interpret_varga_chart(self, chart_type, chart_data, birth_info):
        """베르가 차트를 해석하는 메서드"""
        prompt = f"""
        당신은 베다 점성술 전문가입니다. 다음 {chart_type} 베르가 차트를 해석해주세요:

        출생 정보:
        - 이름: {birth_info.get('name')}
        - 출생일: {birth_info.get('birth_date')}
        - 출생시간: {birth_info.get('birth_time')}
        - 출생지: {birth_info.get('birth_location')}

        차트 데이터:
        {chart_data}

        다음 사항들을 포함하여 자세히 해석해주세요:
        1. 이 차트의 의미와 중요성
        2. 주요 행성 배치의 의미
        3. 삶의 특정 영역에 대한 예측
        4. 조언과 권고사항

        한국어로 친근하고 이해하기 쉽게 설명해주세요.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"해석 중 오류가 발생했습니다: {str(e)}"




# from google import genai
# from google.genai import types
#
# api_key = "AIzaSyDYJqHq7nvmIYFXS2e2R49cQTgRy6MH-As"  # 본인 API키 입력
# image_path = "C:/Users/98kim/Downloads/Chart_1752505954503.png"  # 여기에 로컬 PNG 파일 경로 입력
#
# # PNG 파일을 바이너리로 읽기
# with open(image_path, "rb") as f:
#     image_bytes = f.read()
#
# # Gemini API 클라이언트 초기화
# client = genai.Client(api_key=api_key)
#
# # 이미지 파트 생성 (MIME 타입은 반드시 'image/png')
# image_part = types.Part.from_bytes(
#     data=image_bytes,
#     mime_type="image/png"
# )
#
# # API 호출 (프롬프트와 이미지 함께 전달)
# resp = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents=[
#         "이 이미지를 설명해줘. hora d2 chart 이미지야",
#         image_part
#     ]
# )
#
# print(resp.text)
