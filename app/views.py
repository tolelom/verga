from django.shortcuts import render, redirect, get_object_or_404
from .forms import BirthChartForm
import requests
from google import genai
from google.genai import types
from decouple import config
from .models import BirthChart, VargaChart
from .utils.image_utils import svg_to_png

def index(request):
    """메인 페이지: 개인 정보 입력"""
    if request.method == 'POST':
        form = BirthChartForm(request.POST)
        if form.is_valid():
            chart = form.save(commit=False)
            # TODO: 실제 Geocoding API 연동하여 위도/경도/시간대 설정
            chart.latitude  = 37.5665
            chart.longitude = 126.9780
            chart.timezone  = 9.0
            chart.save()
            return redirect('varga_charts', birth_chart_id=chart.id)
    else:
        form = BirthChartForm()
    return render(request, 'app/index.html', {'form': form})



# app/views.py

from django.shortcuts import render, get_object_or_404
from .models import BirthChart
from .services import AstrologyService

def varga_charts(request, birth_chart_id):
    """베르가 차트 목록 페이지 (SVG URL 전용)"""
    # 1. BirthChart 인스턴스 가져오기
    birth_chart = get_object_or_404(BirthChart, id=birth_chart_id)


    varga_charts = VargaChart.objects.filter(birth_chart=birth_chart)

    # 2. API 호출용 birth_data 구성 (D2 등 모든 차트에 공통)
    birth_data = {
        'year':              birth_chart.birth_date.year,
        'month':             birth_chart.birth_date.month,
        'date':              birth_chart.birth_date.day,
        'hours':             birth_chart.birth_time.hour,
        'minutes':           birth_chart.birth_time.minute,
        'seconds':           0,
        'latitude':          birth_chart.latitude,
        'longitude':         birth_chart.longitude,
        'timezone':          birth_chart.timezone,
        'observation_point': 'topocentric',  # 최상위 필드
        'language':          'en',            # 최상위 필드
    }

    astrology = AstrologyService()

    if not varga_charts.exists():
        # --- 첫 방문: primitive JSON과 SVG URL 호출, DB에 저장 ---
        primitive = astrology.get_varga_svg_urls(birth_data)
        svg_urls  = astrology.get_varga_svg_urls(birth_data)

        for chart_type, chart_data in primitive.items():
            VargaChart.objects.create(
                birth_chart=birth_chart,
                chart_type=chart_type,
                chart_data=chart_data,
                svg_url=svg_urls.get(chart_type)
            )

        # 저장된 차트 다시 조회
        varga_charts = VargaChart.objects.filter(birth_chart=birth_chart)
    else:
        # --- 재방문: DB에 저장된 svg_url 사용 ---
        # svg_url은 VargaChart.svg_url 필드에 이미 저장되어 있음
        svg_urls = { vc.chart_type: vc.svg_url for vc in varga_charts }

    # 4. 템플릿에 primitive 차트 목록과 SVG URL 전달
    return render(request, 'app/varga_charts.html', {
        'birth_chart': birth_chart,
        'varga_charts': varga_charts,
        'svg_urls': svg_urls,
    })


# Gemini Client 설정 (최상단)
client = genai.Client(api_key=config('GEMINI_API_KEY'))

def chart_interpretation(request, birth_chart_id, chart_type):
    # …BirthChart, VargaChart 조회 생략…

    # SVG 다운로드
    resp = requests.get(varga_charts.svg_url)
    resp.raise_for_status()
    svg_text = resp.text

    # SVG → PNG 바이트 변환
    png_data = svg_to_png(svg_text)

    # 프롬프트 및 멀티모달 파트 구성
    prompt_text = (
        f"아래 베르가 차트({chart_type})를 분석하여\n"
        "1) 주요 행성 배치 설명\n"
        "2) 삶의 특정 영역 예측\n"
        "3) 조언 및 권고사항\n"
        "한국어로 친근하게 서술해주세요."
    )
    parts = [
        types.Part.from_text(text=prompt_text),
        types.Part.from_bytes(data=png_data, mime_type="image/png"),
    ]

    # Gemini 호출
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=parts
    )
    interpretation = response.text

    return render(request, 'app/chart_interpretation.html', {
        'birth_chart':    birth_chart,
        'chart_type':     chart_type,
        'svg_url':        varga_charts.svg_url,
        'interpretation': interpretation,
    })