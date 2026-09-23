import sys
import datetime
# import argparse
import traceback
import random
# import psycopg2
# import psycopg2.extras
import time
from time import sleep
from optparse import OptionParser
import os

import pg8000
from pg8000.native import Connection

# Sostituzione di Tkinter con Kivy per Android
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.utils import platform

SCRIVI = False
# Gestione dei percorsi cross-platform (Windows vs Android)
if platform == 'win':
    HOMEPATH = os.environ.get('HOMEPATH', '')
    root_dir = os.path.join("C:", HOMEPATH, "Desktop", "log_bedge")
else:
    # Percorso sicuro per salvare file di log su Android
    from os.path import dirname
    root_dir = os.path.join(os.environ.get('ANDROID_PRIVATE_DATA', '.'), 'log_bedge')

if not os.path.exists(root_dir):
    try:
        os.makedirs(root_dir)
    except Exception:
        root_dir = "." # Fallback directory corrente

LOG_FILE = os.path.join(root_dir, 'log_%s.txt' % (datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")))



# def logga(msg_to_log,stampa=False,LOG_a=LOG_FILE):
#     current_datetime        = datetime.now().strftime( "%d/%m/%Y %H:%M:%S" )
#     message_with_datetime   = "%s : %s" % ( current_datetime, msg_to_log )
#     if stampa: print(message_with_datetime)
#     out_file = open( LOG_a, "a" )
#     out_file.write(  message_with_datetime + "\n" )
#     out_file.close()


class MyTimbra:
    idcheckin      = None
    ore_entrata    = None
    ore_uscita     = None
    ore_pranzo_exit= None
    ore_pranzo_in  = None

    MINUTI_entrata    = None
    MINUTI_uscita     = None
    MINUTI_pranzo_exit= None
    MINUTI_pranzo_in  = None

    def esegui_query(self,sql):

        self.db_cursor.execute(sql)
        record_aggiornati = self.db_cursor.rowcount
        print(sql)

        print (record_aggiornati)
        if record_aggiornati == 1:
            print('commit')
            if SCRIVI:
                print('SCRIVO')
#                 self.db_connection.commit()
        else:
            print('rollback')
            self.db_connection.rollback()



        if hasattr(self, 'db_cursor') and self.db_cursor:
            self.db_cursor.close()
            print("Cursore DB chiuso automaticamente.")
        if hasattr(self, 'db_connection') and self.db_connection:
            self.db_connection.close()
            print("Connessione DB chiusa automaticamente.")
        print('------------------------------------')

#         if not SCRIVI:   sleep(5)
#         sleep(5)




    def __init__( self ):
#         CONNECTION_STRING   = "dbname=presenze user=postgres password=postgres host=192.168.2.76 port=5432"
#         self.db_connection  = psycopg2.connect( CONNECTION_STRING )
#         self.db_cursor      = self.db_connection.cursor( cursor_factory=psycopg2.extras.DictCursor )

        self.db_connection = pg8000.connect(
            database="presenze",
            user="postgres",
            password="postgres",
            host="192.168.2.76",
            port=5432
        )
        self.db_cursor = self.db_connection.cursor()

        self.idcheckin      = None
        self.ore_entrata    = None
        self.ore_uscita     = None
        self.ore_pranzo_exit= None
        self.ore_pranzo_in  = None

        self.MINUTI_entrata    = None
        self.MINUTI_uscita     = None
        self.MINUTI_pranzo_exit= None
        self.MINUTI_pranzo_in  = None

        now = datetime.date.today()

        self.oggi = '%s/%s/%s'%(now.day,now.month,now.year)
        print(self.oggi)
        q_sel = """SELECT
                        idcheckin
                        ,day_checkin
                        ,checkin_time
                        ,checkout_time
                        , EXTRACT(HOUR FROM checkin_time)::integer as ore_entrata
                        , EXTRACT(MINUTE FROM checkin_time)::integer as minuti_entrata

                        , EXTRACT(HOUR FROM checkout_time)::integer as ore_uscita
                        , EXTRACT(MINUTE FROM checkout_time)::integer as minuti_uscita

                        , EXTRACT(HOUR FROM lunch_brake_start_time)::integer as ore_pranzo_exit
                        , EXTRACT(MINUTE FROM lunch_brake_start_time)::integer as minuti_pranzo_exit

                        , EXTRACT(HOUR FROM lunch_brake_end_time)::integer as ore_pranzo_in
                        , EXTRACT(MINUTE FROM lunch_brake_end_time)::integer as minuti_pranzo_in

                        from public.check_in where idpersona=1 and day_checkin='%s'"""%(self.oggi)

#         self.db_cursor.execute( query = q_sel )
        self.db_cursor.execute( q_sel )
        columns = [desc[0] for desc in self.db_cursor.description]
        rSet = [dict(zip(columns, row)) for row in self.db_cursor.fetchall()]
#         rSet = self.db_cursor.fetchall()
        if len(rSet) == 1:
            self.idcheckin      =   rSet[0]['idcheckin']
            self.ore_entrata    =   rSet[0]['ore_entrata']
            self.MINUTI_entrata =   rSet[0]['minuti_entrata']

            self.ore_uscita     =   rSet[0]['ore_uscita']
            self.MINUTI_uscita    =   rSet[0]['minuti_uscita']

            self.ore_pranzo_exit=   rSet[0]['ore_pranzo_exit']
            self.MINUTI_pranzo_exit=   rSet[0]['minuti_pranzo_exit']

            self.ore_pranzo_in  =   rSet[0]['ore_pranzo_in']
            self.MINUTI_pranzo_in  =   rSet[0]['minuti_pranzo_in']



        if self.idcheckin == None or self.ore_entrata == None or self.ore_uscita == None:
            print('ERRORE RECUPERO DATI')
#             sys.exit()


    def __del__(self):
        """Metodo distruttore: chiude automaticamente le connessioni quando l'oggetto viene eliminato"""
        try:
            # Verifica che il cursore esista e sia aperto prima di chiuderlo
            if hasattr(self, 'db_cursor') and self.db_cursor:
                self.db_cursor.close()
                print("Cursore DB chiuso automaticamente.")
        except Exception as e:
            print(f"Errore chiusura cursore: {e}")
        try:
            # Verifica che la connessione esista e sia aperta prima di chiuderla
            if hasattr(self, 'db_connection') and self.db_connection:
                self.db_connection.close()
                print("Connessione DB chiusa automaticamente.")
        except Exception as e:
            print(f"Errore chiusura connessione: {e}")

    def timbra_mattina(self):
        print('----------------    timbra_mattina --------------------')
        stringa_finale = self.ricalcola(self.ore_entrata,self.MINUTI_entrata,min=-2,max=2)
        print (stringa_finale)
        q_upd = "update public.check_in set checkin_ts='%s' where idpersona=1 and day_checkin='%s' and idcheckin=%s"%(stringa_finale,self.oggi,self.idcheckin)
        self.esegui_query(q_upd)

    def timbra_pranzo_exit(self):
        print('----------------    timbra_pranzo_exit --------------------')
        stringa_finale = self.ricalcola(self.ore_pranzo_exit,self.MINUTI_pranzo_exit)
        print (stringa_finale)
        q_upd = "update public.check_in set lunch_brake_start_ts='%s' where idpersona=1 and day_checkin='%s' and idcheckin=%s"%(stringa_finale,self.oggi,self.idcheckin)
        self.esegui_query(q_upd)

    def timbra_pranzo_in(self):
        print('----------------    timbra_pranzo_in --------------------')
        stringa_finale = self.ricalcola(self.ore_pranzo_in,self.MINUTI_pranzo_in)
        print (stringa_finale)
        q_upd = "update public.check_in set lunch_brake_end_ts='%s' where idpersona=1 and day_checkin='%s' and idcheckin=%s"%(stringa_finale,self.oggi,self.idcheckin)
        self.esegui_query(q_upd)

    def timbra_sera(self):
        print('----------------    timbra_sera --------------------')
        stringa_finale = self.ricalcola(self.ore_uscita,self.MINUTI_uscita)
        print(stringa_finale)
        q_upd = "update public.check_in set checkout_ts='%s' where idpersona=1 and day_checkin='%s' and idcheckin=%s"%(stringa_finale,self.oggi,self.idcheckin)
        self.esegui_query(q_upd)



    def ricalcola(self,ore,minuti,min=-1,max=4):
        print('###########')
        # 1. Stringa di partenza con l'orario
        orario_iniziale_str = "%s:%s:00:00"%(ore,minuti)
        oggi = datetime.datetime.today()
        # 3. Convertiamo l'orario iniziale inserendolo direttamente nella data di oggi
        orario_base = datetime.datetime.strptime(orario_iniziale_str + "000", "%H:%M:%S:%f").replace( year=oggi.year, month=oggi.month, day=oggi.day )
        # 4. Generiamo la variazione casuale in millisecondi (da -1 a +4 minuti)
        ms_minimo = min * 60 * 1000
        ms_massimo = max * 60 * 1000
        ms_casuali = random.randint(ms_minimo, ms_massimo)
        # 5. Modifichiamo l'orario di base
        orario_modificato = orario_base + datetime.timedelta(milliseconds=ms_casuali)
        # 6. Formattiamo l'output finale mantenendo le 6 cifre dei microsecondi (.960064)
        risultato = orario_modificato.strftime("%Y-%m-%d %H:%M:%S.%f")

        # Output di verifica
        return risultato


# --- INTERFACCIA GRAFICA KIVY ADATTA AD ANDROID ---
class TimbratriceApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scrivi_attivo = False
        # Creiamo subito il widget di testo in modo che sia disponibile
        # non appena sovrascriviamo lo stdout
        # Creiamo il widget di testo forzando il colore nero per i caratteri
        self.area_log = TextInput(
            readonly=True,
            font_name="Roboto",
            font_size='12sp',
            size_hint_y=1,
            foreground_color=[0, 0, 0, 1],       # <--- TESTO NERO
            background_color=[0.95, 0.95, 0.95, 1] # <--- SFONDO CHIARO
        )

        sys.stdout = ScrittoreKivy(self.area_log)
#         sys.stderr = ScrittoreKivy(self.area_log) # Intercettiamo anche eventuali errori di sistema

    def build(self):
        self.title = "Seleziona Azione"

        # Layout Principale Verticale
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Sezione Scrittura Reale
        main_layout.add_widget(Label(text="--- Opzioni di Scrittura ---", font_size='16sp', bold=True, size_hint_y=None, height=30))

        scrivi_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.cb_scrivi = CheckBox(size_hint_x=None, width=50)
        self.cb_scrivi.bind(active=self.on_checkbox_scrivi)
        scrivi_layout.add_widget(self.cb_scrivi)
        scrivi_layout.add_widget(Label(text="Attiva Scrittura Reale (SCRIVI)", halign='left', text_size=(None, None)))
        main_layout.add_widget(scrivi_layout)

        # Sezione Azioni
        main_layout.add_widget(Label(text="--- Seleziona Azione ---", font_size='16sp', bold=True, size_hint_y=None, height=30))

        # Bottoni Azione
        azioni = [
            ("m -- mattina", "m"),
            ("px -- pranzo_exit", "px"),
            ("pi -- pranzo_in", "pi"),
            ("s -- sera", "s")
        ]

        for testo, valore in azioni:
            btn = Button(text=testo, size_hint_y=None, height=50)
            btn.bind(on_release=lambda instance, val=valore: self.esegui_scelte(val))
            main_layout.add_widget(btn)

        # Area di Log dedicata ai print
        main_layout.add_widget(Label(text="--- Log di Esecuzione ---", font_size='14sp', bold=True, size_hint_y=None, height=25))
        main_layout.add_widget(self.area_log)

        return main_layout

    def on_checkbox_scrivi(self, checkbox, value):
        self.scrivi_attivo = value

    def esegui_scelte(self, action):
        global SCRIVI
        SCRIVI = self.scrivi_attivo
        print(f"SCRIVI: {SCRIVI}")
        print(f"Select: {action}")

        try:
            my_timbra = MyTimbra()
            if action == 'm':
                my_timbra.timbra_mattina()
            elif action == 'px':
                my_timbra.timbra_pranzo_exit()
            elif action == 'pi':
                my_timbra.timbra_pranzo_in()
            elif action == 's':
                my_timbra.timbra_sera()
        except Exception as e:
            print(f"[-] ERRORE DATABASE: {e}")
#             logga('%s' % traceback.format_exc())

        # Chiude l'applicazione dopo 4 secondi per lasciar leggere l'esito della query
        Clock.schedule_once(lambda dt: self.stop(), 10)


# Scrittore personalizzato per aggiornare la TextInput in modo immediato e sicuro
class ScrittoreKivy:
    def __init__(self, textinput_widget):
        self.widget = textinput_widget

    def write(self, string):
        # Usiamo Clock.schedule_once per eseguire l'aggiornamento in modo sicuro nel thread principale di Kivy
        Clock.schedule_once(lambda dt: self._append_text(string))

    def _append_text(self, string):
        # Aggiunge il testo alla fine
        self.widget.text += string
        # Forza lo scroll automatico verso il basso spostando il cursore
        self.widget.cursor = (0, len(self.widget.text))
        # Forza Kivy a ridisegnare la TextInput immediatamente
        self.widget.do_cursor_movement('cursor_home')
        self.widget.canvas.ask_update()

    def flush(self):
        pass


if __name__ == "__main__":
    try:
        TimbratriceApp().run()
    except Exception as e:
        print(f"[-] ERRORE NELL'ELABORAZIONE DEI DATI: {e}")
        print(traceback.format_exc())
#         logga('%s' % traceback.format_exc())