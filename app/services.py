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
