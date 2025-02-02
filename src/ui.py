import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from threading import Thread
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from config import driver
from bot import startPostingAds
from helpers import getAdsData
import time
import random
import json
import os

class FacebookBotUI:
    def __init__(self, master):
        self.master = master
        master.title("Facebook Auto Poster Pro")
        master.geometry("1000x700")
        master.configure(bg='#f0f2f5')
        
        # Variables de instancia
        self.email_entry = None
        self.pass_entry = None
        self.ads_list = getAdsData()
        self.running = False
        self.credentials_file = os.path.join(os.path.dirname(__file__), 'data', 'credentials.json')
        
        self.setup_ui()
        self.load_settings()
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.master, bg='#ffffff')
        main_frame.pack(expand=True, fill='both', padx=25, pady=25)
        
        # Encabezado con logo
        header = tk.Frame(main_frame, bg='#1877f2', height=100)
        header.pack(fill='x', pady=(0, 25))
        tk.Label(header, text="🚀 Facebook Auto Poster Pro", font=('Helvetica', 22, 'bold'), 
                bg='#1877f2', fg='white').pack(pady=25)
        
        # Panel de configuración
        config_frame = tk.LabelFrame(main_frame, text=" Configuración de Cuenta ", 
                                   font=('Arial', 12, 'bold'), bg='#ffffff')
        config_frame.pack(fill='x', pady=10)
        
        # Campos de entrada
        self.email_entry = self.create_input_field(config_frame, "Correo electrónico:", 0)
        self.pass_entry = self.create_input_field(config_frame, "Contraseña:", 1, show='•')
        
        # Recordar usuario
        self.remember_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(config_frame, text="Recordar credenciales", variable=self.remember_var,
                      style='TCheckbutton', cursor='hand2').grid(row=2, column=1, pady=8, sticky='w')
        
        # Panel de control
        control_frame = tk.Frame(main_frame, bg='#ffffff')
        control_frame.pack(fill='x', pady=15)
        
        self.start_btn = ttk.Button(control_frame, text="▶ Iniciar Publicación", 
                                  command=self.start_bot_thread, style='Accent.TButton')
        self.start_btn.pack(side='left', padx=12)
        
        self.stop_btn = ttk.Button(control_frame, text="⏹ Detener", 
                                 command=self.stop_bot, state='disabled')
        self.stop_btn.pack(side='left', padx=12)
        
        # Consola de estado
        console_frame = tk.LabelFrame(main_frame, text=" Registro de Actividad ", 
                                    font=('Arial', 12, 'bold'), bg='#ffffff')
        console_frame.pack(fill='both', expand=True)
        
        self.console = scrolledtext.ScrolledText(console_frame, wrap=tk.WORD, 
                                                font=('Consolas', 10), height=12)
        self.console.pack(fill='both', expand=True, padx=5, pady=5)
        self.console.tag_config('error', foreground='red')
        self.console.tag_config('success', foreground='green')
        
        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, orient='horizontal', 
                                      length=450, mode='determinate')
        self.progress.pack(pady=15)
        
        # Estadísticas
        stats_frame = tk.Frame(main_frame, bg='#ffffff')
        stats_frame.pack(fill='x')
        
        self.stats_label = tk.Label(stats_frame, text="Anuncios publicados: 0 | Pendientes: 0", 
                                  font=('Arial', 10), bg='#ffffff')
        self.stats_label.pack()
        
        self.set_styles()

    def create_input_field(self, parent, label, row, show=None):
        """Crea campos de entrada con estilo moderno"""
        tk.Label(parent, text=label, font=('Arial', 11), 
                bg='#ffffff').grid(row=row, column=0, padx=12, pady=6, sticky='e')
        entry = ttk.Entry(parent, show=show, font=('Arial', 11), width=35)
        entry.grid(row=row, column=1, padx=12, pady=6, sticky='w')
        return entry

    def set_styles(self):
        """Configura los estilos visuales"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Botones principales
        style.configure('Accent.TButton', font=('Arial', 12, 'bold'), 
                      padding=10, foreground='white', background='#1877f2')
        style.map('Accent.TButton', background=[('active', '#166fe5'), ('disabled', '#a8c7fa')])
        
        # Checkboxes
        style.configure('TCheckbutton', background='#ffffff', font=('Arial', 10))
        
        # Barra de progreso
        style.configure('Horizontal.TProgressbar', troughcolor='#e4e6eb', 
                       thickness=22, troughrelief='flat')

    def start_bot_thread(self):
        """Inicia el proceso en un hilo separado"""
        if not self.running:
            self.save_settings()
            self.running = True
            Thread(target=self.run_bot, daemon=True).start()
            self.start_btn['state'] = 'disabled'
            self.stop_btn['state'] = 'normal'

    def stop_bot(self):
        """Detiene la ejecución del bot"""
        self.running = False
        self.update_console("⏹ Proceso detenido por el usuario", 'error')
        self.start_btn['state'] = 'normal'
        self.stop_btn['state'] = 'disabled'

    def run_bot(self):
        """Ejecuta el flujo principal del bot"""
        try:
            self.progress['value'] = 0
            total_ads = len(self.ads_list)
            self.progress['maximum'] = total_ads
            self.update_stats(0, total_ads)
            
            self.update_console("🔑 Iniciando sesión en Facebook...")
            if not self.login():
                return
                
            self.update_console(f"📢 Iniciando publicación de {total_ads} anuncios...")
            
            for index, ad in enumerate(self.ads_list):
                if not self.running:
                    break
                
                self.update_console(f"📄 Procesando anuncio: {ad['title']}")
                startPostingAds(ad, self.human_action)
                self.progress['value'] = index + 1
                self.update_stats(index + 1, total_ads - index - 1)
                self.random_delay(15, 25)  # Espera entre anuncios
                
            self.update_console("✅ Proceso completado con éxito!" if self.running 
                              else "⏹ Proceso interrumpido", 'success')
            
        except Exception as e:
            self.update_console(f"❌ Error crítico: {str(e)}", 'error')
            messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")
            
        finally:
            self.running = False
            self.start_btn['state'] = 'normal'
            self.stop_btn['state'] = 'disabled'

    def login(self):
        """Maneja el proceso de inicio de sesión"""
        try:
            email = self.email_entry.get()
            password = self.pass_entry.get()
            
            if not email or not password:
                raise ValueError("Debe completar todos los campos")
                
            driver.get('https://www.facebook.com')
            
            # Escribir credenciales de forma humana
            self.human_type(driver.find_element(By.ID, 'email'), email)
            self.random_delay(1, 2)
            self.human_type(driver.find_element(By.ID, 'pass'), password)
            self.random_delay(1, 2)
            
            # Hacer clic en el botón de login
            login_btn = driver.find_element(By.XPATH, "//button[@name='login']")
            self.human_click(login_btn)
            
            self.random_delay(5, 8)
            self.update_console("🔓 Sesión iniciada correctamente", 'success')
            return True
            
        except Exception as e:
            self.update_console(f"❌ Error de autenticación: {str(e)}", 'error')
            self.running = False
            return False

    def human_action(self, element, text=None):
        """Realiza acciones humanizadas"""
        if text:
            self.human_type(element, text)
        else:
            self.human_click(element)

    def human_type(self, element, text):
        """Escribe texto con patrones humanos"""
        for char in text:
            element.send_keys(char)
            self.random_delay(0.1, 0.4)
            if random.random() < 0.05:  # 5% de probabilidad de error
                element.send_keys(Keys.BACKSPACE)
                self.random_delay(0.2, 0.5)
                element.send_keys(char)

    def human_click(self, element):
        """Simula un clic humano"""
        ActionChains(driver)\
            .move_to_element(element)\
            .pause(random.uniform(0.2, 0.5))\
            .click()\
            .perform()
        self.random_delay(0.5, 1.2)

    def random_delay(self, min_t, max_t=None):
        """Genera una espera aleatoria"""
        delay = random.uniform(min_t, max_t if max_t else min_t * 1.5)
        time.sleep(delay)

    def update_console(self, message, tag=None):
        """Actualiza la consola de registro"""
        self.console.configure(state='normal')
        self.console.insert('end', f"[{time.strftime('%H:%M:%S')}] {message}\n", tag)
        self.console.configure(state='disabled')
        self.console.see('end')
        self.master.update_idletasks()

    def update_stats(self, published, remaining):
        """Actualiza las estadísticas"""
        self.stats_label.config(text=f"Publicados: {published} | Pendientes: {remaining}")

    def load_settings(self):
        """Carga las credenciales guardadas"""
        try:
            if os.path.exists(self.credentials_file):
                with open(self.credentials_file, 'r') as f:
                    data = json.load(f)
                    self.email_entry.insert(0, data['email'])
                    self.pass_entry.insert(0, data['password'])
                    self.remember_var.set(data['remember'])
        except Exception as e:
            self.update_console(f"⚠️ Error cargando credenciales: {str(e)}", 'error')

    def save_settings(self):
        """Guarda las credenciales si está marcado 'Recordar'"""
        if self.remember_var.get():
            try:
                data = {
                    'email': self.email_entry.get(),
                    'password': self.pass_entry.get(),
                    'remember': True
                }
                os.makedirs(os.path.dirname(self.credentials_file), exist_ok=True)
                with open(self.credentials_file, 'w') as f:
                    json.dump(data, f)
            except Exception as e:
                self.update_console(f"⚠️ Error guardando credenciales: {str(e)}", 'error')

    def on_close(self):
        """Maneja el cierre de la ventana"""
        self.save_settings()
        self.master.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = FacebookBotUI(root)
    root.mainloop()