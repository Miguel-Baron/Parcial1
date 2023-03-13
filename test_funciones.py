"""
Your module description
"""
from apps import download_html
from apps import f
from apps import f2

def test_scraping(mocker):
    mocker.patch("requests.get", return_value="0")
    html = download_html('https://casas.mitula.com.co/searchRE/nivel3-Chapinero/nivel2-Bogotá/nivel1-Cundinamarca/q-Bogotá-Chapinero')
    assert html == "0"
def test_scraping1(mocker):
    assert f() == 200
def test_scraping2(mocker):
    assert f2() == 200
    