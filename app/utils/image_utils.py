# app/utils/image_utils.py

from svglib.svglib import svg2rlg
from reportlab.graphics.renderPM import drawToPIL
from PIL import Image
import io

def svg_to_png(svg_content: str) -> bytes:
    """
    순수 Python: svglib + ReportLab + Pillow를 이용해 SVG → PNG 바이트 변환

    Args:
        svg_content: SVG XML 문자열
    Returns:
        PNG 이미지의 바이트
    """
    # 1) SVG 문자열을 ReportLab Drawing 객체로 변환
    drawing = svg2rlg(io.StringIO(svg_content))

    # 2) ReportLab의 drawToPIL로 PIL.Image 생성 (configPIL로 Pillow 사용 강제)
    pil_img = drawToPIL(
        drawing,
        dpi=300,
        configPIL={'usePIL': True, 'transparent': True}
    )

    # 3) PNG로 메모리 저장
    buf = io.BytesIO()
    pil_img.save(buf, format='PNG')
    return buf.getvalue()
