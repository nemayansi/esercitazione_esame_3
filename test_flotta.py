import unittest
from prenotazioni import Flotta, Veicolo, VeicoloNonTrovato, DataNonAmmessa, Noleggio, ORIZZONTE_GIORNI
from datetime import date, timedelta
class TestFlotta(unittest.TestCase):
    def test_veicoli(self):
        flotta = Flotta()
        veicolo_a = Veicolo("A1", "Furgone", 3)
        veicolo_b = Veicolo("A1", "Furgone", 5)
        flotta.aggiungi_veicolo(veicolo_a)
        with self.assertRaises(ValueError):
            flotta.aggiungi_veicolo(veicolo_b)
        with self.assertRaises(VeicoloNonTrovato):
            flotta.veicolo("XX")
    def test_date_non_ammesse(self):
        giorno = date(2026, 11, 8)
        oggi = date(2026, 11, 18)
        flotta = Flotta()
        veicolo = Veicolo("A1", "Furgone", 3)
        flotta.aggiungi_veicolo(veicolo)
        noleggio = Noleggio("A1", giorno, "09:00", "12:00", "Giovanni", 1)
        with self.assertRaises(DataNonAmmessa):
            flotta.prenota(noleggio, oggi=oggi)
        noleggio = Noleggio("A1", oggi + timedelta(days=ORIZZONTE_GIORNI + 1), "09:00", "12:00", "Giovanni", 1)
        with self.assertRaises(DataNonAmmessa):
            flotta.prenota(noleggio, oggi=oggi)
        noleggio = Noleggio("A1", oggi, "09:00", "12:00", "Giovanni", 1)
        flotta.prenota(noleggio, oggi=oggi)
        noleggio = Noleggio("A1", oggi + timedelta(days=ORIZZONTE_GIORNI), "09:00", "12:00", "Giovanni", 1)
        flotta.prenota(noleggio, oggi=oggi)

