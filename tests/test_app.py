import unittest

from app import app, redis_client


class TesteAplicacao(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health(self):
        resposta = self.client.get("/health")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json()["status"], "ok")

    def test_pagina_incrementa_contador(self):
        antes = int(redis_client.get("pequenojim:visitas") or 0)
        resposta = self.client.get("/")
        depois = int(redis_client.get("pequenojim:visitas"))

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(depois, antes + 1)
        self.assertIn(b"PequenoJim", resposta.data)

    def test_wallpaper_disponivel(self):
        resposta = self.client.get("/static/wallpaper_pequenojim.png")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.mimetype, "image/png")


if __name__ == "__main__":
    unittest.main()
