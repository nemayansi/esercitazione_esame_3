import unittest
from prenotazioni import Flotta, Veicolo, VeicoloNonTrovato, DataNonAmmessa, Noleggio, ORIZZONTE_GIORNI, NoleggioNonTrovato
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
    def test_id(self):
        giorno = date(2026, 11, 20)
        oggi = date(2026, 11, 18)
        flotta = Flotta()
        veicolo = Veicolo("A1", "Furgone", 3)
        flotta.aggiungi_veicolo(veicolo)
        noleggio_a = Noleggio("A1", giorno, "09:00", "12:00", "Giovanni", 1)
        prima = flotta.prenota(noleggio_a, oggi)
        noleggio_b = Noleggio("A1", giorno, "12:00", "14:00", "Giovanni", 1)
        seconda = flotta.prenota(noleggio_b, oggi)
        flotta.cancella(prima)
        noleggio_c = Noleggio("A1", giorno, "14:00", "14:30", "Giovanni", 1)
        terza = flotta.prenota(noleggio_c, oggi)
        self.assertEqual(prima, 1)
        self.assertEqual(seconda, 2)
        self.assertEqual(terza, 3)
    def test_id_inesistenti(self):
        flotta = Flotta()
        with self.assertRaises(NoleggioNonTrovato):
            flotta.noleggio("x")
        with self.assertRaises(NoleggioNonTrovato):
            flotta.cancella("x")    
    def test_noleggi_del_giorno(self):
        giorno = date(2026, 11, 20)
        oggi = date(2026, 11, 18)
        flotta = Flotta()
        veicolo_a = Veicolo("A1", "Furgone", 3)
        flotta.aggiungi_veicolo(veicolo_a)
        veicolo_b = Veicolo("A2", "Furgone", 3)
        flotta.aggiungi_veicolo(veicolo_b)
        noleggio_b = Noleggio("A2", giorno, "12:00", "14:00", "Giovanni", 1)
        flotta.prenota(noleggio_b, oggi)
        noleggio_a = Noleggio("A1", giorno, "09:00", "12:00", "Giovanni", 1)
        flotta.prenota(noleggio_a, oggi)
        tutti = flotta.noleggi_del_giorno(giorno)
        filtrati = flotta.noleggi_del_giorno(giorno, "A1")
        self.assertEqual([x.id for x in tutti], [2, 1])
        self.assertEqual([x.id for x in filtrati], [2])
       