import reportlab
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from foodgram.settings import MEDIA_ROOT, SITE_NAME


def pdf_generate(text, response):
    """Функция генерации PDF-файла налету."""
    reportlab.rl_config.TTFSearchPath.append(str(MEDIA_ROOT) + '/fonts')
    pdfmetrics.registerFont(TTFont('Open Sans', 'opensans.ttf'))
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='Top Recipe',
        fontName='Open Sans',
        fontSize=15,
        leading=20,
        backColor=colors.blueviolet,
        textColor=colors.white,
        alignment=TA_CENTER)
    )
    styles.add(ParagraphStyle(
        name='Ingredient',
        fontName='Open Sans',
        fontSize=10,
        textColor=colors.black,
        alignment=TA_LEFT)
    )
    styles.add(ParagraphStyle(
        name='Info',
        fontName='Open Sans',
        fontSize=9,
        textColor=colors.silver,
        alignment=TA_LEFT)
    )

    pdf = SimpleDocTemplate(
        response,
        title=f'Список рецептов с сайта {SITE_NAME}',
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )
    pdf_generate = []
    text_title = 'Ингридиенты:'
    text_info = f'Этот список был сгенерирован на сайте <b>{SITE_NAME}</b>'
    pdf_generate.append(Paragraph(text_info, styles['Ingredient']))
    pdf_generate.append(Spacer(1, 1))
    pdf_generate.append(Paragraph(text_title, styles['Top Recipe']))
    pdf_generate.append(Spacer(1, 24))
    pdf_generate.append(Paragraph(text, styles['Ingredient']))
    pdf.build(pdf_generate)

    return response
