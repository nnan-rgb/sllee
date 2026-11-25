
# =============================================
# =============================================
# 🌍 إعدادات البروكسي والبلد — عدّل هنا فقط
# =============================================

# ═══════════════════════════════════════════
# 🔀 البروكسي المحلي (socks_bridge.py يجب أن يعمل أولاً)
# ═══════════════════════════════════════════
# قائمة منافذ socks_bridge_multi (كل خيط يستخدم منفذًا مختلفًا)
LOCAL_PROXY_PORTS = [1337, 1338, 1339, 1340, 1341, 1342]

# البروكسي الافتراضي (يُستبدل في كل خيط)
LOCAL_PROXY = "socks5://127.0.0.1:1337"

# الحد الأقصى للخيوط النشطة في نفس الوقت
MAX_CONCURRENT_THREADS = 6

# ═══════════════════════════════════════════
# 🌍 البلد الحالي — غيّر القيمة فقط للتبديل
# ═══════════════════════════════════════════
#   "France"          → فرنسا (الافتراضي)
#   "Germany"         → ألمانيا
#   "United Kingdom"  → المملكة المتحدة
#   "United States"   → الولايات المتحدة
#   "Saudi Arabia"    → السعودية
#   "Japan"           → اليابان
#
# ⚠️ البروكسي السكني الحالي فرنسي.
#    تغيير البلد هنا بدون تغيير البروكسي = تناقض جغرافي.
TARGET_COUNTRY = "Germany"

# ═══════════════════════════════════════════
# 📚 قاموس البلدان — اللغة + التوقيت + العملة
# ═══════════════════════════════════════════
COUNTRY_PRESETS = {
    "France": {
        "language": "fr-FR",
        "languages": ["fr-FR", "fr", "en-US", "en"],
        "timezone": "Europe/Paris",
        "currency": "EUR",
    },
    "Germany": {
        "language": "de-DE",
        "languages": ["de-DE", "de", "en-US", "en"],
        "timezone": "Europe/Berlin",
        "currency": "EUR",
    },
    "United Kingdom": {
        "language": "en-GB",
        "languages": ["en-GB", "en", "fr-FR", "fr"],
        "timezone": "Europe/London",
        "currency": "GBP",
    },
    "United States": {
        "language": "en-US",
        "languages": ["en-US", "en", "es-US", "es"],
        "timezone": "America/New_York",
        "currency": "USD",
    },
    "Saudi Arabia": {
        "language": "ar-SA",
        "languages": ["ar-SA", "ar", "en-US", "en"],
        "timezone": "Asia/Riyadh",
        "currency": "SAR",
    },
    "Japan": {
        "language": "ja-JP",
        "languages": ["ja-JP", "ja", "en-US", "en"],
        "timezone": "Asia/Tokyo",
        "currency": "JPY",
    },
}

if TARGET_COUNTRY not in COUNTRY_PRESETS:
    raise ValueError(
        f"❌ البلد '{TARGET_COUNTRY}' غير موجود في COUNTRY_PRESETS.\n"
        f"   المتاح: {list(COUNTRY_PRESETS.keys())}"
    )

# =============================================
# 🖥️ استيراد المكتبات المتبقية
# =============================================

import subprocess
import threading
import time
import os
import random
import math
import ipaddress
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
from pyvirtualdisplay import Display
from google.colab import files

print("🚀 بدء تشغيل المتصفح المتخفي الذكي (نسخة النوافذ الموحدة slee_threads13)...")

# =============================================
# 🍪 كود إنشاء وتحقين الكوكيز (Python)
# =============================================

class FakeCookiesGenerator:
    def __init__(self):
        self.domains = [
            '.google.com', '.youtube.com', '.facebook.com', '.amazon.com', 
            '.twitter.com', '.instagram.com', '.linkedin.com', '.microsoft.com',
            '.apple.com', '.netflix.com', '.whatsapp.com', '.tiktok.com',
            '.reddit.com', '.pinterest.com', '.wordpress.com', '.blogger.com',
            '.github.com', '.stackoverflow.com', '.wikipedia.org', '.yahoo.com'
        ]
        
        self.cookie_names = [
            'sessionid', 'user_id', 'auth_token', 'csrf_token', 'refresh_token',
            'user_preferences', 'language', 'theme', 'last_visit', 'cart_items',
            'visited_pages', 'search_history', 'ad_id', 'tracking_id', 'ab_test',
            'utm_source', 'utm_medium', 'utm_campaign', 'gclid', 'fbclid',
            'remember_me', 'user_session', 'login_token', 'pref_lang', 'currency',
            'location', 'timezone', 'font_size', 'display_mode', 'notifications'
        ]
        
        self.cookie_values = [
            'true', 'false', '1', '0', 'yes', 'no', 'enabled', 'disabled',
            'light', 'dark', 'auto', 'ar', 'en', 'us', 'eu', 'sa', 'eg',
            'desktop', 'mobile', 'tablet', 'allowed', 'denied', 'accepted'
        ]

    def generate_fake_cookie(self, domain):
        """إنشاء كوكي وهمي عشوائي"""
        name = random.choice(self.cookie_names)
        
        if random.random() < 0.3:
            value = str(random.randint(100000, 999999999))
        elif random.random() < 0.5:
            value = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=random.randint(10, 50)))
        else:
            value = random.choice(self.cookie_values)
        
        cookie = {
            'name': name,
            'value': value,
            'domain': domain,
            'path': '/',
            'secure': random.choice([True, False]),
            'httpOnly': random.choice([True, False]),
            'sameSite': random.choice(['Strict', 'Lax', 'None']),
            'expiry': int(time.time()) + random.randint(3600, 31536000)
        }
        
        return cookie

    def generate_google_cookies(self):
        """إنشاء كوكيز خاصة بجوجل"""
        google_cookies = []
        
        google_specific = [
            {'name': 'NID', 'value': ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=160))},
            {'name': 'SID', 'value': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=50))},
            {'name': 'HSID', 'value': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=20))},
            {'name': 'SSID', 'value': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=30))},
            {'name': 'APISID', 'value': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=40))},
            {'name': 'SAPISID', 'value': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=40))},
            {'name': 'OGPC', 'value': random.choice(['1', '0'])},
            {'name': 'PREF', 'value': f'f1=50000000&f5=30000&al={random.choice(["ar", "en"])}'},
            {'name': 'CONSENT', 'value': f'YES+{random.randint(100, 999)}.{random.randint(100, 999)}'},
            {'name': 'AEC', 'value': ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=50))}
        ]
        
        for cookie_data in google_specific:
            cookie = {
                'name': cookie_data['name'],
                'value': cookie_data['value'],
                'domain': '.google.com',
                'path': '/',
                'secure': True,
                'httpOnly': random.choice([True, False]),
                'sameSite': 'None',
                'expiry': int(time.time()) + random.randint(2592000, 31536000)
            }
            google_cookies.append(cookie)
        
        return google_cookies

    def generate_facebook_cookies(self):
        """إنشاء كوكيز خاصة بفيسبوك"""
        facebook_cookies = []
        
        fb_specific = [
            {'name': 'sb', 'value': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=20))},
            {'name': 'fr', 'value': ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=100))},
            {'name': 'xs', 'value': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=30))},
            {'name': 'c_user', 'value': str(random.randint(1000000000, 9999999999))},
            {'name': 'datr', 'value': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=20))},
            {'name': 'presence', 'value': f'EDv3_{random.randint(1000000000, 9999999999)}'},
            {'name': 'wd', 'value': f'{random.randint(100, 999)}x{random.randint(100, 999)}'},
            {'name': 'locale', 'value': random.choice(['ar_AR', 'en_US'])},
        ]
        
        for cookie_data in fb_specific:
            cookie = {
                'name': cookie_data['name'],
                'value': cookie_data['value'],
                'domain': '.facebook.com',
                'path': '/',
                'secure': True,
                'httpOnly': True,
                'sameSite': 'None',
                'expiry': int(time.time()) + random.randint(86400, 2592000)
            }
            facebook_cookies.append(cookie)
        
        return facebook_cookies

    def generate_tracking_cookies(self):
        """إنشاء كوكيز التتبع والإعلانات"""
        tracking_cookies = []
        
        tracking_domains = [
            '.doubleclick.net', '.googleadservices.com', '.googlesyndication.com',
            '.facebook.com', '.fb.com', '.analytics.google.com'
        ]
        
        tracking_names = [
            'id', '_ga', '_gid', '_gat', '_gac', '_fbp', 'fbc'
        ]
        
        for domain in tracking_domains:
            for _ in range(random.randint(2, 5)):
                name = random.choice(tracking_names)
                if name.startswith('_ga'):
                    value = f"GA1.2.{random.randint(100000000, 999999999)}.{int(time.time())}"
                elif name in ['_fbp', 'fbc']:
                    value = f"fb.1.{int(time.time() * 1000)}.{random.randint(1000000000, 9999999999)}"
                else:
                    value = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=random.randint(10, 30)))
                
                cookie = {
                    'name': name,
                    'value': value,
                    'domain': domain,
                    'path': '/',
                    'secure': True,
                    'httpOnly': False,
                    'sameSite': 'None',
                    'expiry': int(time.time()) + random.randint(86400, 63072000)
                }
                tracking_cookies.append(cookie)
        
        return tracking_cookies

    def generate_mass_cookies(self, count=800):
        """إنشاء آلاف الكوكيز الوهمية"""
        all_cookies = []
        
        print(f"🍪 جاري إنشاء {count} كوكي وهمي...")
        
        all_cookies.extend(self.generate_google_cookies())
        all_cookies.extend(self.generate_facebook_cookies())
        all_cookies.extend(self.generate_tracking_cookies())
        
        remaining_count = count - len(all_cookies)
        for _ in range(remaining_count):
            domain = random.choice(self.domains)
            cookie = self.generate_fake_cookie(domain)
            all_cookies.append(cookie)
        
        random.shuffle(all_cookies)
        
        print(f"✅ تم إنشاء {len(all_cookies)} كوكي وهمي")
        return all_cookies

    def inject_cookies_to_browser(self, driver, cookies_list):
        """حقن الكوكيز المناسبة للموقع الحالي فقط"""
        print("🔄 جاري حقن الكوكيز المناسبة...")
        
        current_url = driver.current_url
        injected_count = 0
        skipped_count = 0
        
        # تعطيل الانتظار الضمني لتسريع العملية
        driver.implicitly_wait(0)
        
        for cookie in cookies_list:
            try:
                # الشرط الذهبي: نحقن فقط الكوكيز التي تطابق الدومين الحالي
                # مثلاً لو فاتح يوتيوب، لا تحاول حقن كوكيز فيسبوك
                if cookie['domain'] in current_url or 'google' in current_url and 'google' in cookie['domain']:
                    driver.add_cookie(cookie)
                    injected_count += 1
                else:
                    skipped_count += 1
                    
            except Exception:
                # تجاهل الأخطاء بصمت للحفاظ على السرعة
                continue
        
        # إعادة الانتظار الطبيعي
        driver.implicitly_wait(0)
        
        print(f"🎉 تم حقن {injected_count} كوكي (وتم تخطي {skipped_count} لعدم تطابق الدومين)")
        return injected_count, skipped_count

    def setup_fake_cookies(self, driver, cookie_count=800):
        """دالة رئيسية لإعداد الكوكيز الوهمية"""
        fake_cookies = self.generate_mass_cookies(cookie_count)
        
        driver.get("about:blank")
        
        injected, failed = self.inject_cookies_to_browser(driver, fake_cookies)
        
        print(f"🍪 تقرير الكوكيز: {injected} محقون, {failed} فاشل")
        
        return injected

# =============================================
# 🖥️ الفئة الرئيسية للمتصفح المتخفي (معدلة)
# =============================================

def wait_for_local_bridge(host="127.0.0.1", port=1337, timeout=3):
    """يتأكد أن خادم socks_bridge.py يعمل"""
    import socket as _socket_module
    s = _socket_module.socket(_socket_module.AF_INET, _socket_module.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False


# =============================================
# 🎯 كلمات البحث عن أزرار الإغلاق (X)
# =============================================
X_KEYWORDS = [
    # رموز
    "×", "✕", "✗", "✖", "✘", "☒", "⨯",
    # إنجليزي
    "close", "dismiss", "skip", "cancel", "exit",
    # عربي
    "إغلاق", "اغلاق", "غلق", "إلغاء", "الغاء", "تخطي", "تخطّي", "رفض", "خروج",
    # فرنسي
    "fermer", "annuler", "quitter",
]

X_CLASS_HINTS = [
    "close", "dismiss", "ad-close", "ad_close", "close-ad", "close_ad",
    "popup-close", "popup_close", "modal-close", "modal_close",
    "btn-close", "btn_close", "close-btn", "close_btn",
]

X_ID_HINTS = [
    "close", "dismiss", "close-ad", "ad-close",
]


# 🔒 قفل عالمي لمنع تعارض Text file busy
_CHROME_LOCK = threading.Lock()

class UltimateStealthBrowser:
    def __init__(self):
        self.driver = None
        self.device_type = None
        self.visit_duration = 0
        self.display = None
        self.cookie_generator = FakeCookiesGenerator()
        self.selected_country = None
        self.selected_ip = None
        self.selected_language = None
        self.selected_timezone = None
        self.selected_currency = None
        self.thread_id = 0
        self.proxy_url = LOCAL_PROXY
        self._thread_temp_dir = None
        self._user_data_dir = None
        
    def choose_country_and_ip(self):
        """إعدادات البلد فقط — بدون IP lookup"""
        self.selected_country = TARGET_COUNTRY
        preset = COUNTRY_PRESETS[TARGET_COUNTRY]
        
        self.selected_language  = preset["language"]
        self.selected_languages = preset["languages"]
        self.selected_timezone  = preset["timezone"]
        self.selected_currency  = preset["currency"]
        self.selected_ip        = "hidden"  # لا نعرف IP، ولا نحتاج
        
        print(f"🌍 البلد: {self.selected_country}")
        print(f"🌐 اللغة: {self.selected_language}")
        print(f"⏰ التوقيت: {self.selected_timezone}")
        print(f"💶 العملة: {self.selected_currency}")
        
        return self.selected_country
    

    def _build_unified_ua_and_metadata(self):
        """بناء User-Agent و Client Hints موحدان بالكامل من device_profile"""
        p = getattr(self, "device_profile", None) or {}
        chrome_ver = p.get("chrome_version", "122.0.6187.0")
        major_ver = str(chrome_ver).split(".")[0]

        if p.get("type") == "phone" or self.device_type == "phone":
            android_ver = p.get("android_version", "14")
            model = p.get("model", "SM-G998B")
            ua = (
                f"Mozilla/5.0 (Linux; Android {android_ver}; {model}) "
                f"AppleWebKit/537.36 (KHTML, like Gecko) "
                f"Chrome/{chrome_ver} Mobile Safari/537.36"
            )
            brands = [
                {"brand": "Chromium", "version": major_ver},
                {"brand": "Google Chrome", "version": major_ver},
                {"brand": "Not=A?Brand", "version": "99"},
            ]
            full_brands = [
                {"brand": "Chromium", "version": chrome_ver},
                {"brand": "Google Chrome", "version": chrome_ver},
                {"brand": "Not=A?Brand", "version": "99"},
            ]
            metadata = {
                "brands": brands,
                "fullVersionList": full_brands,
                "platform": "Android",
                "platformVersion": str(android_ver),
                "architecture": p.get("architecture", "arm64"),
                "model": str(model),
                "mobile": True,
                "bitness": "64",
            }
            return ua, "Android", metadata
        else:
            win_ver = p.get("version", "Windows NT 10.0; Win64; x64")
            pt_ver = p.get("platform_version", "10.0.22621")
            ua = (
                f"Mozilla/5.0 ({win_ver}) "
                f"AppleWebKit/537.36 (KHTML, like Gecko) "
                f"Chrome/{chrome_ver} Safari/537.36"
            )
            brands = [
                {"brand": "Chromium", "version": major_ver},
                {"brand": "Google Chrome", "version": major_ver},
                {"brand": "Not(A:Brand", "version": "99"},
            ]
            full_brands = [
                {"brand": "Chromium", "version": chrome_ver},
                {"brand": "Google Chrome", "version": chrome_ver},
                {"brand": "Not(A:Brand", "version": "99"},
            ]
            metadata = {
                "brands": brands,
                "fullVersionList": full_brands,
                "platform": "Windows",
                "platformVersion": str(pt_ver),
                "architecture": "x86",
                "model": "",
                "mobile": False,
                "bitness": "64",
                "wow64": "WOW64" in str(win_ver),
            }
            return ua, "Windows", metadata

    def apply_cdp_override_to_current_driver(self):
        """تطبيق إعدادات الشبكة والسكربتات على الجلسة/النافذة الحالية"""
        if not self.driver:
            return
        try:
            ua, platform_name, metadata = self._build_unified_ua_and_metadata()
            self.driver.execute_cdp_cmd("Network.enable", {})
            self.driver.execute_cdp_cmd("Page.enable", {})
            self.driver.execute_cdp_cmd("Network.setUserAgentOverride", {
                "userAgent": ua,
                "acceptLanguage": self.selected_language or "en-US",
                "platform": platform_name,
                "userAgentMetadata": metadata,
            })
        except Exception:
            pass

    def enable_auto_attach_new_targets(self):
        """تفعيل الاكتشاف والإرفاق التلقائي لأي هدف/نافذة جديدة عبر CDP"""
        if not self.driver:
            return
        try:
            self.driver.execute_cdp_cmd("Target.setDiscoverTargets", {"discover": True})
            self.driver.execute_cdp_cmd("Target.setAutoAttach", {
                "autoAttach": True,
                "waitForDebuggerOnStart": False,
                "flatten": True,
            })
        except Exception:
            pass

    def sync_new_windows_with_stealth(self, known_handles=None):
        """رصد أي نافذة/صفحة مستقلة جديدة وحقن نفس الترويسة وسكربت التخفي فيها فوراً"""
        if not self.driver:
            return
        try:
            handles = list(self.driver.window_handles)
        except Exception:
            return

        if known_handles is None:
            known_handles = set()

        new_handles = [h for h in handles if h not in known_handles]
        if not new_handles:
            self.apply_cdp_override_to_current_driver()
            return

        original_handle = None
        try:
            original_handle = self.driver.current_window_handle
        except Exception:
            original_handle = handles[0] if handles else None

        scripts = self._build_stealth_scripts_list()
        ua, platform_name, metadata = self._build_unified_ua_and_metadata()

        for nh in new_handles:
            try:
                self.driver.switch_to.window(nh)
                self.driver.execute_cdp_cmd("Network.enable", {})
                self.driver.execute_cdp_cmd("Page.enable", {})
                self.driver.execute_cdp_cmd("Network.setUserAgentOverride", {
                    "userAgent": ua,
                    "acceptLanguage": self.selected_language or "en-US",
                    "platform": platform_name,
                    "userAgentMetadata": metadata,
                })
                for sc in scripts:
                    try:
                        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                            "source": sc
                        })
                    except Exception:
                        pass
                    try:
                        self.driver.execute_script(sc)
                    except Exception:
                        pass
                known_handles.add(nh)
            except Exception:
                continue

        if original_handle and original_handle in self.driver.window_handles:
            try:
                self.driver.switch_to.window(original_handle)
            except Exception:
                pass

    def choose_random_device(self):
        """اختيار عشوائي بين الهاتف والكمبيوتر وتثبيت بروفايل موحد لكل النوافذ والصفحات"""
        self.device_type = random.choice(["phone", "computer"])
        self.visit_duration = random.randint(10, 30)

        if self.device_type == "phone":
            manufacturers = [
                {"name": "Samsung", "models": ["SM-G998B", "SM-S928B", "SM-A546B", "SM-F946B"], "gpu": "Mali-G78"},
                {"name": "Xiaomi", "models": ["2211133G", "22071212AG", "2109119DG"], "gpu": "Adreno 660"},
                {"name": "OnePlus", "models": ["NE2215", "LE2125", "GM1917"], "gpu": "Adreno 660"},
                {"name": "Google", "models": ["GP4BC", "G9BQD", "G1MNW"], "gpu": "Mali-G78"},
            ]
            manuf = random.choice(manufacturers)
            ram = random.choice([6, 8, 12, 16])
            w, h = random.choice([(390, 844), (412, 915), (360, 800), (414, 736)])
            gpu = manuf["gpu"]
            vendor = "ARM" if "Mali" in gpu else "Qualcomm"
            self.device_profile = {
                "type": "phone",
                "manufacturer": manuf["name"],
                "model": random.choice(manuf["models"]),
                "gpu": gpu,
                "webgl_vendor": vendor,
                "webgl_renderer": gpu,
                "android_version": random.choice(["13", "14"]),
                "chrome_version": random.choice(["120.0.6099.0", "121.0.6147.0", "122.0.6187.0"]),
                "platform": "Android",
                "architecture": "arm64",
                "mobile": True,
                "ram": ram,
                "screen": {
                    "width": w,
                    "height": h,
                    "availWidth": w,
                    "availHeight": h - 36,
                    "pixelRatio": random.choice([2, 3]),
                },
                "audio": {
                    "sampleRate": random.choice([44100, 48000]),
                    "channelCount": 2,
                },
            }
        else:
            wins = [
                {"edition": "Windows 10", "version": "Windows NT 10.0; Win64; x64", "pt_ver": "10.0.19045"},
                {"edition": "Windows 11", "version": "Windows NT 10.0; Win64; x64", "pt_ver": "10.0.22621"},
            ]
            win = random.choice(wins)
            ram = random.choice([8, 16, 32])
            w, h = random.choice([(1920, 1080), (1366, 768), (1536, 864), (1440, 900)])
            gpu_choices = [
                ("NVIDIA Corporation", "NVIDIA GeForce RTX 3060"),
                ("NVIDIA Corporation", "NVIDIA GeForce RTX 4070"),
                ("AMD", "AMD Radeon RX 6700 XT"),
                ("Intel", "Intel Iris Xe Graphics"),
            ]
            g_vendor, g_renderer = random.choice(gpu_choices)
            self.device_profile = {
                "type": "computer",
                "edition": win["edition"],
                "version": win["version"],
                "platform_version": win["pt_ver"],
                "chrome_version": random.choice(["120.0.6099.0", "121.0.6147.0", "122.0.6187.0"]),
                "platform": "Windows",
                "mobile": False,
                "ram": ram,
                "webgl_vendor": g_vendor,
                "webgl_renderer": g_renderer,
                "screen": {
                    "width": w,
                    "height": h,
                    "availWidth": w - 40,
                    "availHeight": h - 60,
                    "pixelRatio": 1,
                },
                "audio": {
                    "sampleRate": random.choice([44100, 48000]),
                    "channelCount": 2,
                },
            }

        print(f"📱 الجهاز المختار: {self.device_type} ({self.device_profile.get('model') or self.device_profile.get('edition')})")
        print(f"⏰ مدة الزيارة: {self.visit_duration} ثانية")
        return self.device_type
    
    def setup_xvfb_display(self):
        """إعداد العرض الافتراضي بناءً على نوع الجهاز"""
        if self.device_type == "phone":
            phone_sizes = [(375, 667), (414, 736), (360, 640), (390, 844)]
            width, height = random.choice(phone_sizes)
        else:
            computer_sizes = [(1920, 1080), (1366, 768), (1536, 864), (1440, 900)]
            width, height = random.choice(computer_sizes)
        
        if self.display:
            self.display.stop()
            
        self.display = Display(visible=0, size=(width, height))
        self.display.start()
        
        print(f"🖥️  حجم العرض الافتراضي: {width}x{height}")
        return width, height
    
    def setup_driver(self):
        """إعداد المتصفح مع الإعدادات المتقدمة"""
        try:
            options = uc.ChromeOptions()
            
            # إضافة الخيارات الأساسية (بدون تكرار)
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--enable-webrtc-hide-local-ips-with-mdns")
            options.add_argument('--disable-infobars')
            options.add_argument('--disable-popup-blocking')
            
            # 🔀 توجيه كل الطلبات عبر الخادم المحلي
            options.add_argument(f'--proxy-server={self.proxy_url}')
            options.add_argument('--proxy-bypass-list=<-loopback>')
            
            # إعدادات إضافية للأداء
            options.add_argument('--disable-background-timer-throttling')
            options.add_argument('--disable-backgrounding-occluded-windows')
            options.add_argument('--disable-renderer-backgrounding')
            options.add_argument('--disable-logging')
            options.add_argument('--log-level=3')
            
            # 🚫 تعطيل optimizationguide + التحديثات + background networking
            options.add_argument('--disable-features=OptimizationGuideModelDownloading,OptimizationHints,OptimizationHintsFetching,OptimizationTargetPrediction,TranslateUI,BlinkGenPropertyTrees')
            options.add_argument('--disable-background-networking')
            options.add_argument('--disable-component-update')
            options.add_argument('--disable-component-extensions-with-background-pages')
            options.add_argument('--disable-sync')
            options.add_argument('--disable-default-apps')
            options.add_argument('--disable-client-side-phishing-detection')
            options.add_argument('--safebrowsing-disable-auto-update')
            options.add_argument('--no-first-run')
            options.add_argument('--no-default-browser-check')
            options.add_argument('--disable-domain-reliability')
            options.add_argument('--disable-breakpad')
            options.add_argument('--metrics-recording-only')
            options.add_argument('--disable-crash-reporter')
            
            # 🚫 حجب نطاقات التحديثات (لا تُحمّل شيئًا)
            options.add_argument(
                '--host-resolver-rules='
                'MAP *.gvt1.com 127.0.0.1, '
                'MAP *.gvt1.com:443 127.0.0.1, '
                'MAP *.googleusercontent.com 127.0.0.1, '
                'MAP edgedl.me.gvt1.com 127.0.0.1, '
                'MAP optimizationguide-pa.googleapis.com 127.0.0.1, '
                'MAP update.googleapis.com 127.0.0.1'
            )
            
            # إعدادات اللغة للواقعية
            if hasattr(self, 'selected_language') and self.selected_language:
                options.add_argument(f'--lang={self.selected_language}')
            
            print("🔧 جاري إعداد المتصفح مع الإعدادات المتقدمة...")
            
            # 🔒 عزل كامل: مجلد مؤقت خاص بكل خيط
            import shutil as _shutil, tempfile as _tempfile, uuid as _uuid
            
            # 1. مجلد مؤقت خاص بكل خيط
            self._thread_temp_dir = _tempfile.mkdtemp(
                prefix=f"uc_T{self.thread_id}_{_uuid.uuid4().hex[:8]}_"
            )
            print(f"🔒 [T{self.thread_id}] مجلد مؤقت: {self._thread_temp_dir}")
            
            # 2. user-data-dir فريد (يمنع تسريب الكوكيز/البصمة)
            self._user_data_dir = os.path.join(self._thread_temp_dir, "profile")
            os.makedirs(self._user_data_dir, exist_ok=True)
            options.add_argument(f"--user-data-dir={self._user_data_dir}")
            
            # 3. نسخة chromedriver خاصة بكل خيط
            _uc_path = os.path.join(self._thread_temp_dir, "chromedriver")
            _found = _shutil.which("chromedriver") or "/usr/local/bin/chromedriver"
            if os.path.exists(_found):
                _shutil.copy2(_found, _uc_path)
                os.chmod(_uc_path, 0o755)
                _driver_path = _uc_path
            else:
                _driver_path = None
            
            # 4. إنشاء المتصفح — داخل قفل عالمي + retry
            _max_attempts = 3
            for _attempt in range(_max_attempts):
                try:
                    with _CHROME_LOCK:
                        self.driver = uc.Chrome(
                            options=options,
                            use_subprocess=False,
                            version_main=156,
                            driver_executable_path=_driver_path,
                            user_data_dir=self._user_data_dir,
                        )
                    break  # نجح
                except Exception as _e:
                    _err_str = str(_e)
                    if "Text file busy" in _err_str and _attempt < _max_attempts - 1:
                        print(f"⚠️ [T{self.thread_id}] Text file busy — محاولة {_attempt+2}/{_max_attempts}")
                        time.sleep(2)
                        continue
                    raise
            
            # إضافة سكريبتات الحماية
            stealth_script = '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            '''
            
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': stealth_script
            })
            
            # 🌐 تفعيل حقن ترويسات الشبكة الحقيقية عبر CDP
            if hasattr(self, 'device_profile') and self.device_profile:
                self.driver.execute_cdp_cmd('Network.enable', {})
                p = self.device_profile
                chrome_ver = p["chrome_version"]
                major_ver = chrome_ver.split('.')[0]
                
                if p["type"] == "phone":
                    ua = f"Mozilla/5.0 (Linux; Android {p['android_version']}; {p['model']}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Mobile Safari/537.36"
                    metadata = {
                        "brands": [
                            {"brand": "Chromium", "version": major_ver},
                            {"brand": "Google Chrome", "version": major_ver},
                            {"brand": "Not=A?Brand", "version": "99"}
                        ],
                        "fullVersionList": [
                            {"brand": "Chromium", "version": chrome_ver},
                            {"brand": "Google Chrome", "version": chrome_ver},
                            {"brand": "Not=A?Brand", "version": "99"}
                        ],
                        "platform": "Android",
                        "platformVersion": p["android_version"],
                        "architecture": "arm64",
                        "model": p["model"],
                        "mobile": True,
                        "bitness": "64"
                    }
                else:
                    ua = f"Mozilla/5.0 ({p['version']}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Safari/537.36"
                    metadata = {
                        "brands": [
                            {"brand": "Chromium", "version": major_ver},
                            {"brand": "Google Chrome", "version": major_ver},
                            {"brand": "Not(A:Brand", "version": "99"}
                        ],
                        "fullVersionList": [
                            {"brand": "Chromium", "version": chrome_ver},
                            {"brand": "Google Chrome", "version": chrome_ver},
                            {"brand": "Not(A:Brand", "version": "99"}
                        ],
                        "platform": "Windows",
                        "platformVersion": p["platform_version"],
                        "architecture": "x86",
                        "model": "",
                        "mobile": False,
                        "bitness": "64",
                        "wow64": False
                    }
                
                self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                    "userAgent": ua,
                    "acceptLanguage": self.selected_language,
                    "platform": p["platform"],
                    "userAgentMetadata": metadata
                })
                print(f"🌐 تم فرض ترويسات الشبكة (CDP) لنظام: {p['platform']}")
            
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(0)
            
            print("✅ تم إعداد المتصفح المتخفي بنجاح")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في إعداد المتصفح: {e}")
            return False
    
    def _build_stealth_scripts_list(self):
        """بناء قائمة السكربتات المتقدمة الموحدة"""

        
        import json as _json
        _profile_json = _json.dumps(getattr(self, 'device_profile', {}))
        country_script = f"""
            window.__device_profile = {_profile_json};
            window.__stealth_config = {{
                country: "{self.selected_country}",
                ip: "{self.selected_ip}",
                language: "{self.selected_language}",
                timezone: "{self.selected_timezone}",
                currency: "{self.selected_currency}"
            }};
            console.log('🌍 تهيئة المتصفح مع إعدادات البلد والبروفايل الموحد:', window.__stealth_config.country);
        """
        
        if self.device_type == "phone":
            device_script = """(function() {
    'use strict';
    
    // =============================================
    // 🔧 استقبال البيانات من البايثون (الإضافة الجديدة)
    // =============================================
    
    const stealthConfig = window.__stealth_config || {
        country: "Saudi Arabia",
        ip: "188.48.125.34",
        language: "ar-SA",
        timezone: "Asia/Riyadh",
        currency: "SAR"
    };
    
    console.log('🌍 تهيئة الهاتف مع إعدادات البلد:', stealthConfig.country);
    
    // =============================================
    // 📱 إعدادات شركات وموديلات Android المتنوعة
    // =============================================
    
    const ANDROID_MANUFACTURERS = [
        {
            name: 'Samsung',
            models: [
                'SM-G998B', 'SM-S928B', 'SM-F946B', 'SM-A546B', 'SM-M536B',
                'SM-G781B', 'SM-A336B', 'SM-A217F', 'SM-A045F', 'SM-A146B'
            ],
            buildPrefix: 'samsung/',
            ramOptions: [8, 12, 16],
            gpuOptions: ['Mali-G78', 'Adreno 660', 'Mali-G68', 'Adreno 650'],
            architectures: ['arm64', 'arm']
        },
        {
            name: 'Xiaomi',
            models: [
                '2211133G', '22071212AG', '2109119DG', '21121119SG', '2203121G',
                '2107119DG', '2201123G', '21091116UG', '22081212UG', '2112123AG'
            ],
            buildPrefix: 'xiaomi/',
            ramOptions: [6, 8, 12, 16],
            gpuOptions: ['Adreno 660', 'Mali-G710', 'Adreno 650', 'Mali-G68'],
            architectures: ['arm64', 'arm']
        },
        {
            name: 'OnePlus',
            models: [
                'NE2215', 'LE2125', 'GM1917', 'HD1913', 'IN2015',
                'KB2005', 'DE2118', 'CPH2451', 'CPH2415', 'CPH2581'
            ],
            buildPrefix: 'OnePlus/',
            ramOptions: [8, 12, 16],
            gpuOptions: ['Adreno 660', 'Adreno 650', 'Adreno 640', 'Adreno 630'],
            architectures: ['arm64', 'arm']
        },
        {
            name: 'Google',
            models: [
                'GP4BC', 'G9BQD', 'G1MNW', 'GB7N6', 'GE2AE',
                'GPJ41', 'GZPF0', 'G1AZG', 'G9S9B', 'GQML3'
            ],
            buildPrefix: 'google/',
            ramOptions: [8, 12],
            gpuOptions: ['Mali-G78', 'Adreno 660', 'Mali-G77', 'Adreno 650'],
            architectures: ['arm64']
        },
        {
            name: 'OPPO',
            models: [
                'CPH2415', 'CPH2581', 'CPH2451', 'CPH2605', 'CPH2521',
                'CPH2505', 'CPH2449', 'CPH2467', 'CPH2601', 'CPH2611'
            ],
            buildPrefix: 'oppo/',
            ramOptions: [6, 8, 12],
            gpuOptions: ['Mali-G68', 'Adreno 619', 'Mali-G57', 'Adreno 610'],
            architectures: ['arm64', 'arm']
        },
        {
            name: 'Realme',
            models: [
                'RMX3708', 'RMX3687', 'RMX3663', 'RMX3612', 'RMX3624',
                'RMX3617', 'RMX3611', 'RMX3690', 'RMX3700', 'RMX3710'
            ],
            buildPrefix: 'realme/',
            ramOptions: [6, 8, 12],
            gpuOptions: ['Mali-G68', 'Adreno 619', 'PowerVR GE8320', 'Mali-G52'],
            architectures: ['arm64', 'arm']
        },
        {
            name: 'Vivo',
            models: [
                'V2318', 'V2303', 'V2314', 'V2309', 'V2313',
                'V2317', 'V2324', 'V2312', 'V2316', 'V2311'
            ],
            buildPrefix: 'vivo/',
            ramOptions: [8, 12, 16],
            gpuOptions: ['Adreno 660', 'Mali-G78', 'Adreno 650', 'Mali-G68'],
            architectures: ['arm64', 'arm']
        },
        {
            name: 'Huawei',
            models: [
                'NOH-NX9', 'TET-AN00', 'ABR-AL60', 'NCO-LX1', 'ANA-NX9',
                'JAD-AL50', 'LIO-AL00', 'ELS-NX9', 'MAR-LX1A', 'JNY-LX1'
            ],
            buildPrefix: 'HUAWEI/',
            ramOptions: [6, 8, 12],
            gpuOptions: ['Mali-G78', 'Mali-G76', 'Adreno 660', 'Mali-G57'],
            architectures: ['arm64', 'arm']
        },
        {
            name: 'Motorola',
            models: [
                'XT2401-5', 'XT2411-3', 'XT2421-1', 'XT2431-4', 'XT2441-2',
                'XT2451-6', 'XT2461-8', 'XT2471-7', 'XT2481-9', 'XT2491-5'
            ],
            buildPrefix: 'motorola/',
            ramOptions: [4, 6, 8],
            gpuOptions: ['Adreno 619', 'Adreno 610', 'PowerVR GE8320', 'Adreno 605'],
            architectures: ['arm64', 'arm']
        },
        {
            name: 'Tecno',
            models: [
                'TECNO-LC7', 'TECNO-KG7', 'TECNO-KG6', 'TECNO-KG5', 'TECNO-KG4',
                'TECNO-KG3', 'TECNO-KG2', 'TECNO-KG1', 'TECNO-KF7', 'TECNO-KF6'
            ],
            buildPrefix: 'TECNO/',
            ramOptions: [4, 6, 8],
            gpuOptions: ['PowerVR GE8320', 'Mali-G52', 'Mali-G57', 'Adreno 610'],
            architectures: ['arm64', 'arm']
        },
        {
            name: 'Infinix',
            models: [
                'INFINIX-X6825', 'INFINIX-X6823', 'INFINIX-X6821', 'INFINIX-X6815', 'INFINIX-X6813',
                'INFINIX-X6811', 'INFINIX-X6805', 'INFINIX-X6803', 'INFINIX-X6801', 'INFINIX-X6795'
            ],
            buildPrefix: 'Infinix/',
            ramOptions: [4, 6, 8],
            gpuOptions: ['PowerVR GE8320', 'Mali-G52', 'Mali-G57', 'Adreno 610'],
            architectures: ['arm64', 'arm']
        }
    ];
    
    // =============================================
    // 📱 إصدارات Android المختلفة
    // =============================================
    
    const ANDROID_VERSIONS = [
        {
            version: '14',
            apiLevel: '34',
            securityPatch: '2024-08-01',
            buildVersions: ['UP1A', 'UP1B', 'AP1A', 'AP2A'],
            chromeVersions: ['119.0.6045.0', '120.0.6099.0', '121.0.6147.0']
        },
        {
            version: '13',
            apiLevel: '33', 
            securityPatch: '2023-12-01',
            buildVersions: ['TP1A', 'TQ1A', 'TQ2A', 'TQ3A'],
            chromeVersions: ['113.0.5672.0', '114.0.5735.0', '115.0.5790.0']
        },
        {
            version: '12',
            apiLevel: '31',
            securityPatch: '2022-10-01',
            buildVersions: ['SP1A', 'SQ1A', 'SQ2A', 'SQ3A'],
            chromeVersions: ['107.0.5304.0', '108.0.5359.0', '109.0.5414.0']
        },
        {
            version: '11',
            apiLevel: '30',
            securityPatch: '2021-08-01', 
            buildVersions: ['RP1A', 'RQ1A', 'RQ2A', 'RQ3A'],
            chromeVersions: ['101.0.4951.0', '102.0.5005.0', '103.0.5060.0']
        },
        {
            version: '10',
            apiLevel: '29',
            securityPatch: '2020-05-01',
            buildVersions: ['QP1A', 'QQ1A', 'QQ2A', 'QQ3A'],
            chromeVersions: ['95.0.4638.0', '96.0.4664.0', '97.0.4692.0']
        }
    ];
    
    // =============================================
    // 📱 توليد أحجام شاشات الهواتف العشوائية
    // =============================================
    
    const generateRandomPhoneScreen = () => {
        const phoneScreenCategories = [
            { minW: 360, maxW: 420, minH: 640, maxH: 780, ratio: '19.5:9' },
            { minW: 420, maxW: 480, minH: 780, maxH: 900, ratio: '20:9' },
            { minW: 480, maxW: 550, minH: 900, maxH: 1200, ratio: '21:9' },
            { minW: 550, maxW: 600, minH: 1200, maxH: 1400, ratio: '22:9' },
            { minW: 600, maxW: 650, minH: 1400, maxH: 1600, ratio: '23:9' }
        ];
        
        const category = phoneScreenCategories[Math.floor(Math.random() * phoneScreenCategories.length)];
        
        const width = Math.floor(Math.random() * (category.maxW - category.minW + 1)) + category.minW;
        const height = Math.floor(Math.random() * (category.maxH - category.minH + 1)) + category.minH;
        
        return {
            width: width,
            height: height,
            availWidth: width - 10,
            availHeight: height - 50,
            pixelRatio: Math.random() < 0.7 ? 2 : 3,
            ratio: category.ratio,
            viewportWidth: width,
            viewportHeight: height
        };
    };
    
    const _scrP = (_dp.screen || { width: 390, height: 844, availWidth: 390, availHeight: 808, pixelRatio: 2 });
    const screenConfig = {
        width: _scrP.width,
        height: _scrP.height,
        availWidth: _scrP.availWidth,
        availHeight: _scrP.availHeight,
        pixelRatio: _scrP.pixelRatio,
        ratio: '19.5:9',
        viewportWidth: _scrP.width,
        viewportHeight: _scrP.height
    };
    
    // =============================================
    // 📱 اختيار عشوائي للجهاز والإصدار (معدل ليتوافق مع البلد)
    // =============================================
    
    const _dp = window.__device_profile || {};
    const selectedManufacturer = ANDROID_MANUFACTURERS.find(m => m.name === _dp.manufacturer) || ANDROID_MANUFACTURERS[0];
    const selectedModel = _dp.model || selectedManufacturer.models[0];
    const selectedAndroid = ANDROID_VERSIONS.find(v => v.version === _dp.android_version) || ANDROID_VERSIONS[0];
    const selectedBuild = selectedAndroid.buildVersions[Math.floor(Math.random() * selectedAndroid.buildVersions.length)];
    const selectedGPU = _dp.gpu || selectedManufacturer.gpuOptions[0];
    const selectedArchitecture = 'arm64';
    const selectedChromeVersion = _dp.chrome_version || selectedAndroid.chromeVersions[0];
    
    // =============================================
    // 📱 إعدادات الرامات المطلوبة (2-4-6-8-12-16-24)
    // =============================================
    
    const ALL_RAM_OPTIONS = [2, 4, 6, 8, 12, 16, 24];
    
    const getRandomRAM = (manufacturerRAMOptions) => {
        const availableRAM = ALL_RAM_OPTIONS.filter(ram => 
            manufacturerRAMOptions.includes(ram) || 
            (ram >= Math.min(...manufacturerRAMOptions) && ram <= Math.max(...manufacturerRAMOptions))
        );
        
        return availableRAM[Math.floor(Math.random() * availableRAM.length)];
    };
    
    const selectedRAM = _dp.ram || 8;
    
    // =============================================
    // 🔊 محاكاة Audio Context للهواتف
    // =============================================
    
    const simulateAudioContext = () => {
        const audioLatencies = ['balanced', 'interactive', 'playback'];
        const sampleRates = [44100, 48000];
        const channelCounts = [2, 6];
        
        return {
            sampleRate: sampleRates[Math.floor(Math.random() * sampleRates.length)],
            latencyHint: audioLatencies[Math.floor(Math.random() * audioLatencies.length)],
            channelCount: channelCounts[Math.floor(Math.random() * channelCounts.length)],
            maxChannelCount: 32,
            state: 'running'
        };
    };
    
    const audioConfig = {
        sampleRate: (_dp.audio && _dp.audio.sampleRate) || 48000,
        latencyHint: 'balanced',
        channelCount: (_dp.audio && _dp.audio.channelCount) || 2,
        maxChannelCount: 32,
        state: 'running'
    };
    
    // =============================================
    // 🎮 محاكاة WebGL Renderer للهواتف
    // =============================================
    
    const simulateWebGLRenderer = () => {
        const webglVendors = [
            { vendor: 'Qualcomm', renderer: `${selectedGPU}` },
            { vendor: 'ARM', renderer: `Mali-${selectedGPU.includes('Mali') ? selectedGPU : 'G78'}` },
            { vendor: 'Imagination Technologies', renderer: 'PowerVR GE8320' },
            { vendor: 'Google', renderer: 'SwiftShader' },
            { vendor: 'NVIDIA', renderer: 'Tegra' }
        ];
        
        const selectedWebGL = webglVendors[Math.floor(Math.random() * webglVendors.length)];
        
        return {
            vendor: selectedWebGL.vendor,
            renderer: selectedWebGL.renderer,
            version: 'OpenGL ES 3.2',
            shadingLanguageVersion: 'OpenGL ES GLSL ES 3.20',
            unmaskedVendor: selectedWebGL.vendor,
            unmaskedRenderer: selectedWebGL.renderer
        };
    };
    
    const webglConfig = {
        vendor: _dp.webgl_vendor || 'ARM',
        renderer: _dp.webgl_renderer || selectedGPU,
        version: 'OpenGL ES 3.2',
        shadingLanguageVersion: 'OpenGL ES GLSL ES 3.20',
        unmaskedVendor: _dp.webgl_vendor || 'ARM',
        unmaskedRenderer: _dp.webgl_renderer || selectedGPU
    };
    
    // =============================================
    // 🛡️ الحماية الأساسية من الاكتشاف
    // =============================================
    
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined,
        configurable: true,
        enumerable: true
    });
    
    delete navigator.__proto__.webdriver;
    delete window.chrome;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
    
    // =============================================
    // 🛡️ حماية WebRTC المتقدمة (الإضافة الجديدة)
    // =============================================
    
    const fakeRTCPeerConnection = function(configuration) {
        this.connectionState = 'connected';
        this.iceConnectionState = 'connected';
        this.getStats = () => Promise.resolve(new Map());
        this.getSenders = () => [];
        this.getReceivers = () => [];
        this.addTrack = () => {};
        this.removeTrack = () => {};
        this.createDataChannel = () => ({});
    };
    
    Object.defineProperty(window, 'RTCPeerConnection', {
        get: () => fakeRTCPeerConnection,
        configurable: false
    });
    
    Object.defineProperty(window, 'webkitRTCPeerConnection', {
        get: () => fakeRTCPeerConnection,
        configurable: false
    });
    
    // =============================================
    // 📱 إعدادات Media Devices للهواتف (الإضافة الجديدة)
    // =============================================
    
    const fakeMediaDevices = {
        getUserMedia: (constraints) => Promise.reject(new Error('Permission denied')),
        enumerateDevices: () => Promise.resolve([
            { kind: 'audioinput', deviceId: 'default', label: '', groupId: 'default' },
            { kind: 'videoinput', deviceId: 'default', label: '', groupId: 'default' }
        ]),
        getSupportedConstraints: () => ({
            width: true, height: true, aspectRatio: true, frameRate: true,
            facingMode: true, resizeMode: true, sampleRate: true,
            channelCount: true, volume: true, sampleSize: true,
            echoCancellation: true, autoGainControl: true, noiseSuppression: true
        })
    };
    
    Object.defineProperty(navigator, 'mediaDevices', {
        get: () => fakeMediaDevices,
        configurable: false
    });
    
    // =============================================
    // 📱 إعدادات Sensor APIs للهواتف (الإضافة الجديدة)
    // =============================================
    
    const fakeDeviceOrientationEvent = function(type, init) {
        this.type = type;
        this.alpha = init?.alpha || (Math.random() * 360);
        this.beta = init?.beta || (Math.random() * 180 - 90);
        this.gamma = init?.gamma || (Math.random() * 180 - 90);
        this.absolute = init?.absolute || false;
    };
    
    Object.defineProperty(window, 'DeviceOrientationEvent', {
        get: () => fakeDeviceOrientationEvent,
        configurable: false
    });
    
    Object.defineProperty(window, 'DeviceMotionEvent', {
        get: () => function(type, init) {
            this.type = type;
            this.acceleration = init?.acceleration || { x: 0, y: 0, z: 9.81 };
            this.accelerationIncludingGravity = init?.accelerationIncludingGravity || { x: 0, y: 0, z: 9.81 };
            this.rotationRate = init?.rotationRate || { alpha: 0, beta: 0, gamma: 0 };
            this.interval = init?.interval || 16;
        },
        configurable: false
    });
    
    // =============================================
    // 📱 تطبيق إعدادات Android النهائية
    // =============================================
    
    // 1. User Agent للهاتف Android
    Object.defineProperty(navigator, 'userAgent', {
        get: () => {
            const chromeVersion = selectedChromeVersion;
            const userAgents = [
                `Mozilla/5.0 (Linux; Android ${selectedAndroid.version}; ${selectedModel}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${chromeVersion} Mobile Safari/537.36`,
                `Mozilla/5.0 (Linux; Android ${selectedAndroid.version}; ${selectedModel}) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/${Math.floor(Math.random() * 10) + 20}.0 Chrome/115.0.0.0 Mobile Safari/537.36`,
                `Mozilla/5.0 (Linux; Android ${selectedAndroid.version}; ${selectedModel}; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/${chromeVersion} Mobile Safari/537.36`
            ];
            return userAgents[Math.floor(Math.random() * userAgents.length)];
        },
        configurable: false,
        enumerable: true
    });
    
    // 2. إعدادات النظام الأساسي
    Object.defineProperty(navigator, 'platform', {
        get: () => 'Linux armv8l',
        configurable: false,
        enumerable: true
    });
    
    // 3. إعدادات الشاشة للهاتف
    Object.defineProperty(screen, 'width', { 
        get: () => screenConfig.width,
        configurable: false
    });
    
    Object.defineProperty(screen, 'height', { 
        get: () => screenConfig.height,
        configurable: false
    });
    
    Object.defineProperty(screen, 'availWidth', { 
        get: () => screenConfig.availWidth,
        configurable: false
    });
    
    Object.defineProperty(screen, 'availHeight', { 
        get: () => screenConfig.availHeight,
        configurable: false
    });
    
    Object.defineProperty(screen, 'colorDepth', { 
        get: () => 24,
        configurable: false
    });
    
    Object.defineProperty(screen, 'pixelDepth', { 
        get: () => 24,
        configurable: false
    });
    
    // 4. إعدادات Pixel Ratio للهواتف
    Object.defineProperty(window, 'devicePixelRatio', {
        get: () => screenConfig.pixelRatio,
        configurable: false
    });
    
    // 5. إعدادات اللغة والمنطقة (معدلة لاستخدام بيانات البايثون)
    Object.defineProperty(navigator, 'language', {
        get: () => stealthConfig.language,
        configurable: false,
        enumerable: true
    });
    
    Object.defineProperty(navigator, 'languages', {
        get: () => [stealthConfig.language, "en-US", "en"],
        configurable: false,
        enumerable: true
    });
    
    Object.defineProperty(navigator, 'timezone', {
        get: () => stealthConfig.timezone,
        configurable: false
    });
    
    // 6. إعدادات الأجهزة للهواتف
    Object.defineProperty(navigator, 'hardwareConcurrency', {
        get: () => {
            const coresBasedOnRAM = {
                2: Math.floor(Math.random() * 2) + 2,
                4: Math.floor(Math.random() * 2) + 4,
                6: Math.floor(Math.random() * 2) + 6,
                8: Math.floor(Math.random() * 4) + 4,
                12: Math.floor(Math.random() * 4) + 6,
                16: Math.floor(Math.random() * 4) + 8,
                24: Math.floor(Math.random() * 6) + 10
            };
            return coresBasedOnRAM[selectedRAM] || 8;
        },
        configurable: false
    });
    
    Object.defineProperty(navigator, 'deviceMemory', {
        get: () => selectedRAM,
        configurable: false
    });
    
    Object.defineProperty(navigator, 'maxTouchPoints', {
        get: () => 10,
        configurable: false
    });
    
    // 7. إعدادات Network للهواتف (معدلة لتتوافق مع البلد)
    Object.defineProperty(navigator, 'connection', {
        get: () => {
            const country = stealthConfig.country;
            let downlink, rtt, effectiveType;
            
            if (country === "Saudi Arabia" || country === "Egypt" || country === "United Arab Emirates") {
                downlink = 15 + Math.random() * 25; // 15-40 Mbps
                rtt = 80 + Math.floor(Math.random() * 120); // 80-200ms
                effectiveType = Math.random() < 0.8 ? '4g' : '3g';
            } else if (country === "Japan" || country === "South Korea") {
                downlink = 40 + Math.random() * 60; // 40-100 Mbps
                rtt = 20 + Math.floor(Math.random() * 40); // 20-60ms
                effectiveType = '4g';
            } else {
                downlink = 20 + Math.random() * 40; // 20-60 Mbps
                rtt = 50 + Math.floor(Math.random() * 80); // 50-130ms
                effectiveType = Math.random() < 0.9 ? '4g' : '3g';
            }
            
            return {
                downlink: downlink,
                effectiveType: effectiveType,
                rtt: rtt,
                saveData: Math.random() < 0.2,
                type: Math.random() < 0.7 ? 'cellular' : 'wifi'
            };
        },
        configurable: false
    });
    
    // 8. إعدادات Client Hints المتقدمة (معدلة لتشمل بيانات جغرافية)
    Object.defineProperty(navigator, 'userAgentData', {
        get: () => {
            const brands = [
                { brand: "Chromium", version: selectedChromeVersion.split('.')[0] },
                { brand: "Google Chrome", version: selectedChromeVersion.split('.')[0] },
                { brand: "Android", version: selectedAndroid.version }
            ];
            
            return {
                brands: brands,
                mobile: true,
                platform: "Android",
                
                getHighEntropyValues: function(hints) {
                    return new Promise((resolve) => {
                        const result = {};
                        
                        hints.forEach(hint => {
                            switch (hint) {
                                case 'architecture':
                                    result.architecture = selectedArchitecture;
                                    break;
                                case 'bitness':
                                    result.bitness = selectedArchitecture === 'arm64' ? '64' : '32';
                                    break;
                                case 'model':
                                    result.model = selectedModel;
                                    break;
                                case 'platformVersion':
                                    result.platformVersion = selectedAndroid.version;
                                    break;
                                case 'fullVersionList':
                                    result.fullVersionList = brands;
                                    break;
                                case 'wow64':
                                    result.wow64 = selectedArchitecture === 'arm64' ? false : Math.random() < 0.3;
                                    break;
                                // إضافة بيانات جغرافية جديدة
                                case 'timezone':
                                    result.timezone = stealthConfig.timezone;
                                    break;
                                case 'country':
                                    result.country = stealthConfig.country;
                                    break;
                            }
                        });
                        
                        resolve(result);
                    });
                },
                
                toJSON: function() {
                    return {
                        brands: this.brands,
                        mobile: this.mobile,
                        platform: this.platform
                    };
                }
            };
        },
        configurable: false
    });
    
    // =============================================
    // 🌍 محاكاة HTTP Headers المتقدمة (الإضافة الجديدة)
    // =============================================
    
    const originalSend = XMLHttpRequest.prototype.send;
    const originalOpen = XMLHttpRequest.prototype.open;
    const originalFetch = window.fetch;
    
    XMLHttpRequest.prototype.open = function(...args) {
        this._url = args[1];
        return originalOpen.apply(this, args);
    };
    
    XMLHttpRequest.prototype.send = function(...args) {
        // إضافة الترويسات الجغرافية المتقدمة
        if (this._url && !this._url.includes('chrome-extension')) {
            
            // Client Hints headers
            this.setRequestHeader('Sec-CH-UA', `"Chromium";v="${selectedChromeVersion.split('.')[0]}", "Google Chrome";v="${selectedChromeVersion.split('.')[0]}", "Not=A?Brand";v="99"`);
            this.setRequestHeader('Sec-CH-UA-Mobile', '?1');
            this.setRequestHeader('Sec-CH-UA-Platform', '"Android"');
            this.setRequestHeader('Sec-CH-UA-Platform-Version', `"${selectedAndroid.version}"`);
            this.setRequestHeader('Sec-CH-UA-Model', `"${selectedModel}"`);
            this.setRequestHeader('Device-Memory', selectedRAM.toString());
            this.setRequestHeader('DPR', screenConfig.pixelRatio.toString());
            this.setRequestHeader('Viewport-Width', screenConfig.viewportWidth.toString());
            this.setRequestHeader('Width', Math.floor(screenConfig.width * 0.8).toString());
        }
        
        return originalSend.apply(this, args);
    };
    
    // تعديل fetch API أيضاً
    window.fetch = function(...args) {
        const [resource, init = {}] = args;
        
        const newInit = {
            ...init,
            headers: {
                ...init.headers,
                'Sec-CH-UA': `"Chromium";v="${selectedChromeVersion.split('.')[0]}", "Google Chrome";v="${selectedChromeVersion.split('.')[0]}", "Android";v="${selectedAndroid.version}"`,
                'Sec-CH-UA-Mobile': '?1',
                'Sec-CH-UA-Platform': '"Android"'
            }
        };
        
        return originalFetch(resource, newInit);
    };
    
    // =============================================
    // 🎨 الحماية المتقدمة للـCanvas وWebGL
    // =============================================
    
    const originalGetContext = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function(contextType, ...args) {
        const context = originalGetContext.call(this, contextType, ...args);
        
        if (contextType === '2d') {
            const originalGetImageData = context.getImageData;
            context.getImageData = function(...getImageDataArgs) {
                try {
                    const imageData = originalGetImageData.apply(this, getImageDataArgs);
                    for (let i = 0; i < imageData.data.length; i += 4) {
                        if (Math.random() < 0.01) {
                            imageData.data[i] += Math.floor(Math.random() * 3) - 1;
                            imageData.data[i + 1] += Math.floor(Math.random() * 3) - 1;
                            imageData.data[i + 2] += Math.floor(Math.random() * 3) - 1;
                        }
                    }
                    return imageData;
                } catch (e) {
                    return null;
                }
            };
        } else if (contextType === 'webgl' || contextType === 'webgl2') {
            const originalGetParameter = context.getParameter;
            context.getParameter = function(parameter) {
                switch (parameter) {
                    case context.VENDOR:
                        return webglConfig.vendor;
                    case context.RENDERER:
                        return webglConfig.renderer;
                    case context.VERSION:
                        return webglConfig.version;
                    case context.SHADING_LANGUAGE_VERSION:
                        return webglConfig.shadingLanguageVersion;
                    case 37445: // UNMASKED_VENDOR_WEBGL
                        return webglConfig.unmaskedVendor;
                    case 37446: // UNMASKED_RENDERER_WEBGL
                        return webglConfig.unmaskedRenderer;
                    default:
                        return originalGetParameter.call(this, parameter);
                }
            };
        }
        
        return context;
    };
    
    // =============================================
    // 🔊 تزوير Audio Context المتقدم
    // =============================================
    
    const originalAudioContext = window.AudioContext || window.webkitAudioContext;
    if (originalAudioContext) {
        window.AudioContext = function() {
            const audioContext = new originalAudioContext();
            
            Object.defineProperty(audioContext, 'sampleRate', {
                get: () => audioConfig.sampleRate,
                configurable: false
            });
            
            const originalCreateAnalyser = audioContext.createAnalyser;
            audioContext.createAnalyser = function() {
                const analyser = originalCreateAnalyser.call(this);
                Object.defineProperty(analyser, 'frequencyBinCount', {
                    get: () => 1024,
                    configurable: false
                });
                return analyser;
            };
            
            return audioContext;
        };
        
        window.AudioContext.prototype = originalAudioContext.prototype;
    }
    
    // =============================================
    // 🧹 تنظيف الجلسات السابقة
    // =============================================
    
    const clearPreviousSessions = () => {
        try {
            if (window.localStorage) window.localStorage.clear();
            if (window.sessionStorage) window.sessionStorage.clear();
            if (window.indexedDB) {
                window.indexedDB.databases().then(databases => {
                    databases.forEach(db => {
                        if (db.name) window.indexedDB.deleteDatabase(db.name);
                    });
                }).catch(() => {});
            }
            console.log('🧹 تم تنظيف الجلسات السابقة');
        } catch (e) {}
    };
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', clearPreviousSessions);
    } else {
        clearPreviousSessions();
    }
    
    // =============================================
    // 📱 معلومات التفعيل النهائية
    // =============================================
    
    console.log('📱 Android Phone Stealth - ULTIMATE EDITION WITH GEO-LOCATION');
    console.log('🌍 البلد: ' + stealthConfig.country);
    console.log('📡 IP: ' + stealthConfig.ip);
    console.log('🌐 اللغة: ' + stealthConfig.language);
    console.log('⏰ التوقيت: ' + stealthConfig.timezone);
    console.log('📱 الجهاز: ' + selectedManufacturer.name + ' ' + selectedModel);
    console.log('🤖 Android: ' + selectedAndroid.version);
    console.log('📐 الشاشة: ' + screenConfig.width + 'x' + screenConfig.height);
    console.log('💾 الرام: ' + selectedRAM + 'GB');
    console.log('🔒 الحماية: WebRTC + Media + Sensors + Headers');
    
    // علامات نجاح التحميل
    window.__android_phone_stealth_geo_ultimate = true;
    window.__stealth_config_applied = stealthConfig;
    window.__session_cleaned = true;
    
})();"""
        else:
            device_script =  """(function() {
    'use strict';
    
    // =============================================
    // 🔧 استقبال البيانات من البايثون (الإضافة الجديدة)
    // =============================================
    
    const stealthConfig = window.__stealth_config || {
        country: "United States",
        ip: "192.168.1.100",
        language: "en-US",
        timezone: "America/New_York",
        currency: "USD"
    };
    
    console.log('🌍 تهيئة الكمبيوتر مع إعدادات البلد:', stealthConfig.country);
    
    // =============================================
    // 🖥️ إعدادات أنظمة Windows المحدثة
    // =============================================
    
    const WINDOWS_VERSIONS = [
        {
            version: 'Windows NT 10.0; Win64; x64',
            build: '19045',
            edition: 'Windows 10',
            platformVersion: '10.0.19045'
        },
        {
            version: 'Windows NT 10.0; WOW64',
            build: '19045',
            edition: 'Windows 10',
            platformVersion: '10.0.19045'
        },
        {
            version: 'Windows NT 10.0',
            build: '19045',
            edition: 'Windows 10',
            platformVersion: '10.0.19045'
        },
        {
            version: 'Windows NT 10.0; Win64; x64',
            build: '22621',
            edition: 'Windows 11',
            platformVersion: '10.0.22621'
        },
        {
            version: 'Windows NT 10.0; WOW64',
            build: '22621',
            edition: 'Windows 11',
            platformVersion: '10.0.22621'
        },
        {
            version: 'Windows NT 6.3; Win64; x64',
            build: '9600',
            edition: 'Windows 8.1',
            platformVersion: '6.3.9600'
        },
        {
            version: 'Windows NT 6.3; WOW64',
            build: '9600',
            edition: 'Windows 8.1',
            platformVersion: '6.3.9600'
        },
        {
            version: 'Windows NT 6.3',
            build: '9600',
            edition: 'Windows 8.1',
            platformVersion: '6.3.9600'
        },
        {
            version: 'Windows NT 6.2; Win64; x64',
            build: '9200',
            edition: 'Windows 8',
            platformVersion: '6.2.9200'
        },
        {
            version: 'Windows NT 6.2; WOW64',
            build: '9200',
            edition: 'Windows 8',
            platformVersion: '6.2.9200'
        },
        {
            version: 'Windows NT 6.2',
            build: '9200',
            edition: 'Windows 8',
            platformVersion: '6.2.9200'
        },
        {
            version: 'Windows NT 6.1; Win64; x64',
            build: '7601',
            edition: 'Windows 7',
            platformVersion: '6.1.7601'
        },
        {
            version: 'Windows NT 6.1; WOW64',
            build: '7601',
            edition: 'Windows 7',
            platformVersion: '6.1.7601'
        },
        {
            version: 'Windows NT 6.1',
            build: '7601',
            edition: 'Windows 7',
            platformVersion: '6.1.7601'
        }
    ];
    
    // =============================================
    // 🎮 إعدادات كروت الشاشة للكمبيوتر
    // =============================================
    
    const GPU_CONFIGS = [
        {
            vendor: 'NVIDIA Corporation',
            renderers: [
                'NVIDIA GeForce RTX 4090', 'NVIDIA GeForce RTX 4080', 'NVIDIA GeForce RTX 4070 Ti',
                'NVIDIA GeForce RTX 4070', 'NVIDIA GeForce RTX 4060 Ti', 'NVIDIA GeForce RTX 4060',
                'NVIDIA GeForce RTX 3090 Ti', 'NVIDIA GeForce RTX 3090', 'NVIDIA GeForce RTX 3080 Ti',
                'NVIDIA GeForce RTX 3080', 'NVIDIA GeForce RTX 3070 Ti', 'NVIDIA GeForce RTX 3070',
                'NVIDIA GeForce RTX 3060 Ti', 'NVIDIA GeForce RTX 3060', 'NVIDIA GeForce GTX 1660 Ti',
                'NVIDIA GeForce GTX 1660 Super', 'NVIDIA GeForce GTX 1660', 'NVIDIA GeForce GTX 1650 Super'
            ]
        },
        {
            vendor: 'AMD',
            renderers: [
                'AMD Radeon RX 7900 XTX', 'AMD Radeon RX 7900 XT', 'AMD Radeon RX 7800 XT',
                'AMD Radeon RX 7700 XT', 'AMD Radeon RX 7600', 'AMD Radeon RX 6950 XT',
                'AMD Radeon RX 6900 XT', 'AMD Radeon RX 6800 XT', 'AMD Radeon RX 6800',
                'AMD Radeon RX 6700 XT', 'AMD Radeon RX 6650 XT', 'AMD Radeon RX 6600 XT',
                'AMD Radeon RX 6600', 'AMD Radeon RX 5700 XT', 'AMD Radeon RX 5700',
                'AMD Radeon RX 5600 XT', 'AMD Radeon RX 5500 XT'
            ]
        },
        {
            vendor: 'Intel',
            renderers: [
                'Intel Arc A770', 'Intel Arc A750', 'Intel Arc A580',
                'Intel Arc A380', 'Intel Iris Xe Graphics', 'Intel UHD Graphics 770',
                'Intel UHD Graphics 750', 'Intel UHD Graphics 730', 'Intel UHD Graphics 630'
            ]
        }
    ];
    
    // =============================================
    // 🖥️ توليد أحجام شاشات عشوائية واقعية
    // =============================================
    
    const generateRandomScreenSize = () => {
        const screenCategories = [
            { minW: 1280, maxW: 1440, minH: 720, maxH: 900, type: 'HD' },
            { minW: 1440, maxW: 1920, minH: 900, maxH: 1080, type: 'FHD' },
            { minW: 1920, maxW: 2560, minH: 1080, maxH: 1440, type: 'QHD' },
            { minW: 2560, maxW: 3840, minH: 1080, maxH: 1600, type: 'UWQHD' },
            { minW: 3840, maxW: 5120, minH: 2160, maxH: 2880, type: '4K' }
        ];
        
        const category = screenCategories[Math.floor(Math.random() * screenCategories.length)];
        
        const width = Math.floor(Math.random() * (category.maxW - category.minW + 1)) + category.minW;
        const height = Math.floor(Math.random() * (category.maxH - category.minH + 1)) + category.minH;
        
        return {
            width: width,
            height: height,
            availWidth: width - Math.floor(Math.random() * 50 + 50),
            availHeight: height - Math.floor(Math.random() * 100 + 100),
            type: category.type,
            pixelRatio: Math.random() < 0.8 ? 1 : (Math.random() < 0.5 ? 1.25 : 1.5),
            viewportWidth: width,
            viewportHeight: height
        };
    };
    
    const _scrC = (_dp.screen || { width: 1920, height: 1080, availWidth: 1880, availHeight: 1020, pixelRatio: 1 });
    const screenConfig = {
        width: _scrC.width,
        height: _scrC.height,
        availWidth: _scrC.availWidth,
        availHeight: _scrC.availHeight,
        type: 'FHD',
        pixelRatio: _scrC.pixelRatio,
        viewportWidth: _scrC.width,
        viewportHeight: _scrC.height
    };
    
    // =============================================
    // 🖥️ إعدادات الذاكرة العشوائية (RAM)
    // =============================================
    
    const WINDOWS_RAM_OPTIONS = [4, 8, 12, 16, 24, 32, 64];
    const selectedRAM = _dp.ram || 16;
    
    // =============================================
    // 🎨 توليد قائمة الخطوط للكمبيوتر
    // =============================================
    
    const generateComputerFonts = () => {
        const windowsCoreFonts = [
            'Arial', 'Arial Black', 'Bahnschrift', 'Calibri', 'Cambria',
            'Cambria Math', 'Candara', 'Comic Sans MS', 'Consolas', 'Constantia',
            'Corbel', 'Courier New', 'Ebrima', 'Franklin Gothic Medium', 'Gabriola',
            'Gadugi', 'Georgia', 'Impact', 'Javanese Text', 'Leelawadee UI',
            'Lucida Console', 'Lucida Sans Unicode', 'Malgun Gothic', 'Microsoft Himalaya',
            'Microsoft JhengHei', 'Microsoft New Tai Lue', 'Microsoft PhagsPa',
            'Microsoft Sans Serif', 'Microsoft Tai Le', 'Microsoft YaHei',
            'Microsoft Yi Baiti', 'MingLiU-ExtB', 'Mongolian Baiti', 'MS Gothic',
            'MV Boli', 'Myanmar Text', 'Nirmala UI', 'Palatino Linotype',
            'Segoe MDL2 Assets', 'Segoe Print', 'Segoe Script', 'Segoe UI',
            'Segoe UI Historic', 'Segoe UI Emoji', 'Segoe UI Symbol', 'SimSun',
            'Sitka', 'Sylfaen', 'Symbol', 'Tahoma', 'Times New Roman',
            'Trebuchet MS', 'Verdana', 'Webdings', 'Wingdings', 'Yu Gothic'
        ];
        
        const additionalFonts = [
            'Roboto', 'Open Sans', 'Lato', 'Montserrat', 'Oswald',
            'Source Sans Pro', 'Raleway', 'PT Sans', 'Noto Sans', 'Ubuntu',
            'Playfair Display', 'Merriweather', 'Fira Sans', 'Roboto Condensed'
        ];
        
        const allFonts = [...windowsCoreFonts, ...additionalFonts];
        
        const fontCount = Math.floor(Math.random() * 20) + 30;
        const selectedFonts = [];
        
        for (let i = 0; i < fontCount; i++) {
            const randomFont = allFonts[Math.floor(Math.random() * allFonts.length)];
            if (!selectedFonts.includes(randomFont)) {
                selectedFonts.push(randomFont);
            }
        }
        
        return selectedFonts.sort();
    };
    
    // =============================================
    // 🎮 محاكاة WebGL Renderer للكمبيوتر
    // =============================================
    
    const simulateComputerWebGL = () => {
        const selectedGPUConfig = GPU_CONFIGS[Math.floor(Math.random() * GPU_CONFIGS.length)];
        const selectedRenderer = selectedGPUConfig.renderers[Math.floor(Math.random() * selectedGPUConfig.renderers.length)];
        
        const webglVersions = [
            'WebGL 1.0 (OpenGL ES 2.0 Chromium)',
            'WebGL 2.0 (OpenGL ES 3.0 Chromium)',
            'WebGL 1.0 (OpenGL ES 2.0)',
            'WebGL 2.0 (OpenGL ES 3.0)'
        ];
        
        const glslVersions = [
            'WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)',
            'WebGL GLSL ES 2.0 (OpenGL ES GLSL ES 2.0 Chromium)',
            'WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0)',
            'WebGL GLSL ES 2.0 (OpenGL ES GLSL ES 2.0)'
        ];
        
        return {
            vendor: selectedGPUConfig.vendor,
            renderer: selectedRenderer,
            version: webglVersions[Math.floor(Math.random() * webglVersions.length)],
            shadingLanguageVersion: glslVersions[Math.floor(Math.random() * glslVersions.length)],
            unmaskedVendor: selectedGPUConfig.vendor,
            unmaskedRenderer: selectedRenderer
        };
    };
    
    const webglConfig = {
        vendor: _dp.webgl_vendor || 'NVIDIA Corporation',
        renderer: _dp.webgl_renderer || 'NVIDIA GeForce RTX 3060',
        version: 'WebGL 2.0 (OpenGL ES 3.0 Chromium)',
        shadingLanguageVersion: 'WebGL GLSL ES 2.0 (OpenGL ES GLSL ES 2.0 Chromium)',
        unmaskedVendor: _dp.webgl_vendor || 'NVIDIA Corporation',
        unmaskedRenderer: _dp.webgl_renderer || 'NVIDIA GeForce RTX 3060'
    };
    
    // =============================================
    // 🔊 محاكاة Audio Context للكمبيوتر
    // =============================================
    
    const simulateComputerAudioContext = () => {
        const audioDevices = [
            { name: 'Realtek High Definition Audio', manufacturer: 'Realtek' },
            { name: 'NVIDIA High Definition Audio', manufacturer: 'NVIDIA' },
            { name: 'AMD High Definition Audio', manufacturer: 'AMD' },
            { name: 'Conexant SmartAudio HD', manufacturer: 'Conexant' },
            { name: 'Logitech G Pro X', manufacturer: 'Logitech' },
            { name: 'SteelSeries Sonar', manufacturer: 'SteelSeries' },
            { name: 'HyperX Cloud II', manufacturer: 'HyperX' }
        ];
        
        const selectedDevice = audioDevices[Math.floor(Math.random() * audioDevices.length)];
        const sampleRates = [44100, 48000, 96000, 192000];
        const channelCounts = [2, 6, 8];
        
        return {
            sampleRate: sampleRates[Math.floor(Math.random() * sampleRates.length)],
            latencyHint: 'interactive',
            channelCount: channelCounts[Math.floor(Math.random() * channelCounts.length)],
            maxChannelCount: 32,
            state: 'running',
            deviceName: selectedDevice.name,
            manufacturer: selectedDevice.manufacturer
        };
    };
    
    const audioConfig = {
        sampleRate: (_dp.audio && _dp.audio.sampleRate) || 48000,
        latencyHint: 'interactive',
        channelCount: (_dp.audio && _dp.audio.channelCount) || 2,
        maxChannelCount: 32,
        state: 'running',
        deviceName: 'Realtek High Definition Audio',
        manufacturer: 'Realtek'
    };
    
    // =============================================
    // 🔧 محاكاة Client Hints للكمبيوتر
    // =============================================
    
    const generateComputerClientHints = () => {
        const chromeVersions = [
            '119.0.6045.0', '120.0.6099.0', '121.0.6147.0', 
            '122.0.6187.0', '123.0.6223.0', '124.0.6255.0'
        ];
        
        const _dp = window.__device_profile || {};
        const selectedChromeVersion = _dp.chrome_version || chromeVersions[0];
        const selectedWindows = WINDOWS_VERSIONS.find(w => w.platformVersion === _dp.platform_version && w.version.includes('x64')) || WINDOWS_VERSIONS[0];
        
        const brands = [
            { brand: "Chromium", version: selectedChromeVersion.split('.')[0] },
            { brand: "Google Chrome", version: selectedChromeVersion.split('.')[0] },
            { brand: "Not(A:Brand", version: "99" }
        ];
        
        const lowEntropyHints = {
            brands: brands,
            mobile: false,
            platform: "Windows"
        };
        
        const highEntropyHints = {
            architecture: "x86",
            bitness: selectedWindows.version.includes('x64') ? "64" : "32",
            model: "",
            platformVersion: selectedWindows.platformVersion,
            fullVersionList: brands,
            wow64: selectedWindows.version.includes('WOW64') ? true : false
        };
        
        return {
            lowEntropy: lowEntropyHints,
            highEntropy: highEntropyHints,
            chromeVersion: selectedChromeVersion,
            windowsVersion: selectedWindows
        };
    };
    
    const clientHintsConfig = generateComputerClientHints();
    const selectedWindows = clientHintsConfig.windowsVersion;
    
    // =============================================
    // 🛡️ الحماية الأساسية من الاكتشاف
    // =============================================
    
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined,
        configurable: true,
        enumerable: true
    });
    
    delete navigator.__proto__.webdriver;
    delete window.chrome;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
    
    // =============================================
    // 🛡️ حماية WebRTC المتقدمة للكمبيوتر (الإضافة الجديدة)
    // =============================================
    
    const fakeRTCPeerConnection = function(configuration) {
        this.connectionState = 'connected';
        this.iceConnectionState = 'connected';
        this.getStats = () => Promise.resolve(new Map());
        this.getSenders = () => [];
        this.getReceivers = () => [];
        this.addTrack = () => {};
        this.removeTrack = () => {};
        this.createDataChannel = () => ({});
        this.close = () => {};
    };
    
    Object.defineProperty(window, 'RTCPeerConnection', {
        get: () => fakeRTCPeerConnection,
        configurable: false
    });
    
    Object.defineProperty(window, 'webkitRTCPeerConnection', {
        get: () => fakeRTCPeerConnection,
        configurable: false
    });
    
    // =============================================
    // 🖥️ إعدادات Performance API للكمبيوتر (الإضافة الجديدة)
    // =============================================
    
    const originalNow = performance.now;
    performance.now = function() {
        return originalNow.call(performance) + Math.random() * 10;
    };
    
    const originalGetEntries = performance.getEntries;
    performance.getEntries = function() {
        const entries = originalGetEntries.call(performance);
        return entries.map(entry => {
            if (entry.entryType === 'navigation') {
                return {
                    ...entry,
                    domContentLoadedEventEnd: entry.domContentLoadedEventEnd + Math.random() * 50,
                    loadEventEnd: entry.loadEventEnd + Math.random() * 100
                };
            }
            return entry;
        });
    };
    
    // =============================================
    // 🖥️ إعدادات Browser Plugins للكمبيوتر (الإضافة الجديدة)
    // =============================================
    
    const fakePlugin = function(name, filename, description) {
        this.name = name;
        this.filename = filename;
        this.description = description;
        this.length = 1;
        this[0] = { type: "application/x-google-chrome-pdf" };
    };
    
    Object.defineProperty(navigator, 'plugins', {
        get: () => [
            new fakePlugin('Chrome PDF Plugin', 'internal-pdf-viewer', 'Portable Document Format'),
            new fakePlugin('Chrome PDF Viewer', 'mhjfbmdgcfjbbpaeojofohoefgiehjai', 'Portable Document Format'),
            new fakePlugin('Native Client', 'internal-nacl-plugin', 'Native Client Executable')
        ],
        configurable: false,
        enumerable: true
    });
    
    // =============================================
    // 🖥️ تطبيق إعدادات الكمبيوتر النهائية
    // =============================================
    
    // 1. User Agent عشوائي لنظام Windows
    Object.defineProperty(navigator, 'userAgent', {
        get: () => {
            const WINDOWS_USER_AGENTS = [
                `Mozilla/5.0 (${selectedWindows.version}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${clientHintsConfig.chromeVersion} Safari/537.36`,
                `Mozilla/5.0 (${selectedWindows.version}; rv:${Math.floor(Math.random() * 20) + 100}.0) Gecko/20100101 Firefox/${Math.floor(Math.random() * 20) + 100}.0`,
                `Mozilla/5.0 (${selectedWindows.version}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${clientHintsConfig.chromeVersion} Safari/537.36 Edg/${clientHintsConfig.chromeVersion}`
            ];
            return WINDOWS_USER_AGENTS[Math.floor(Math.random() * WINDOWS_USER_AGENTS.length)];
        },
        configurable: false,
        enumerable: true
    });
    
    // 2. إعدادات النظام الأساسي
    Object.defineProperty(navigator, 'platform', {
        get: () => 'Win32',
        configurable: false,
        enumerable: true
    });
    
    Object.defineProperty(navigator, 'oscpu', {
        get: () => selectedWindows.version.split(';')[0],
        configurable: false
    });
    
    // 3. إعدادات الشاشة العشوائية
    Object.defineProperty(screen, 'width', { 
        get: () => screenConfig.width,
        configurable: false
    });
    
    Object.defineProperty(screen, 'height', { 
        get: () => screenConfig.height,
        configurable: false
    });
    
    Object.defineProperty(screen, 'availWidth', { 
        get: () => screenConfig.availWidth,
        configurable: false
    });
    
    Object.defineProperty(screen, 'availHeight', { 
        get: () => screenConfig.availHeight,
        configurable: false
    });
    
    Object.defineProperty(screen, 'colorDepth', { 
        get: () => 24,
        configurable: false
    });
    
    Object.defineProperty(screen, 'pixelDepth', { 
        get: () => 24,
        configurable: false
    });
    
    // 4. إعدادات Pixel Ratio للكمبيوتر
    Object.defineProperty(window, 'devicePixelRatio', {
        get: () => screenConfig.pixelRatio,
        configurable: false
    });
    
    // 5. إعدادات اللغة والمنطقة المتقدمة (معدلة لاستخدام بيانات البايثون)
    Object.defineProperty(navigator, 'language', {
        get: () => stealthConfig.language,
        configurable: false,
        enumerable: true
    });
    
    Object.defineProperty(navigator, 'languages', {
        get: () => [stealthConfig.language, "en-US", "en"],
        configurable: false,
        enumerable: true
    });
    
    Object.defineProperty(navigator, 'timezone', {
        get: () => stealthConfig.timezone,
        configurable: false
    });
    
    // 6. إعدادات الأجهزة المحسنة
    Object.defineProperty(navigator, 'hardwareConcurrency', {
        get: () => {
            const coresBasedOnRAM = {
                4: Math.floor(Math.random() * 2) + 2,
                8: Math.floor(Math.random() * 4) + 4,
                12: Math.floor(Math.random() * 4) + 6,
                16: Math.floor(Math.random() * 6) + 8,
                24: Math.floor(Math.random() * 6) + 8,
                32: Math.floor(Math.random() * 8) + 12,
                64: Math.floor(Math.random() * 12) + 16
            };
            return coresBasedOnRAM[selectedRAM] || 8;
        },
        configurable: false
    });
    
    Object.defineProperty(navigator, 'deviceMemory', {
        get: () => selectedRAM,
        configurable: false
    });
    
    Object.defineProperty(navigator, 'maxTouchPoints', {
        get: () => 0,
        configurable: false
    });
    
    // 7. إعدادات Network للكمبيوتر (معدلة لتتوافق مع البلد)
    Object.defineProperty(navigator, 'connection', {
        get: () => {
            const country = stealthConfig.country;
            let downlink, rtt;
            
            if (country === "United States" || country === "Germany" || country === "Japan") {
                downlink = 80 + Math.random() * 120; // 80-200 Mbps
                rtt = 15 + Math.floor(Math.random() * 25); // 15-40ms
            } else if (country === "Saudi Arabia" || country === "Egypt" || country === "UAE") {
                downlink = 40 + Math.random() * 60; // 40-100 Mbps
                rtt = 30 + Math.floor(Math.random() * 50); // 30-80ms
            } else {
                downlink = 50 + Math.random() * 80; // 50-130 Mbps
                rtt = 20 + Math.floor(Math.random() * 40); // 20-60ms
            }
            
            return {
                downlink: downlink,
                effectiveType: '4g',
                rtt: rtt,
                saveData: false,
                type: 'wifi'
            };
        },
        configurable: false
    });
    
    // 8. إعدادات Client Hints للكمبيوتر (معدلة لتشمل بيانات جغرافية)
    Object.defineProperty(navigator, 'userAgentData', {
        get: () => ({
            brands: clientHintsConfig.lowEntropy.brands,
            mobile: clientHintsConfig.lowEntropy.mobile,
            platform: clientHintsConfig.lowEntropy.platform,
            
            getHighEntropyValues: function(hints) {
                return new Promise((resolve) => {
                    const result = {};
                    
                    hints.forEach(hint => {
                        switch (hint) {
                            case 'architecture':
                                result.architecture = clientHintsConfig.highEntropy.architecture;
                                break;
                            case 'bitness':
                                result.bitness = clientHintsConfig.highEntropy.bitness;
                                break;
                            case 'model':
                                result.model = clientHintsConfig.highEntropy.model;
                                break;
                            case 'platformVersion':
                                result.platformVersion = clientHintsConfig.highEntropy.platformVersion;
                                break;
                            case 'fullVersionList':
                                result.fullVersionList = clientHintsConfig.highEntropy.fullVersionList;
                                break;
                            case 'wow64':
                                result.wow64 = clientHintsConfig.highEntropy.wow64;
                                break;
                            // إضافة بيانات جغرافية جديدة
                            case 'timezone':
                                result.timezone = stealthConfig.timezone;
                                break;
                            case 'country':
                                result.country = stealthConfig.country;
                                break;
                        }
                    });
                    
                    resolve(result);
                });
            },
            
            toJSON: function() {
                return {
                    brands: this.brands,
                    mobile: this.mobile,
                    platform: this.platform
                };
            }
        }),
        configurable: false
    });
    
    // =============================================
    // 🌍 محاكاة HTTP Headers المتقدمة للكمبيوتر (الإضافة الجديدة)
    // =============================================
    
    const originalSend = XMLHttpRequest.prototype.send;
    const originalOpen = XMLHttpRequest.prototype.open;
    const originalFetch = window.fetch;
    
    XMLHttpRequest.prototype.open = function(...args) {
        this._url = args[1];
        return originalOpen.apply(this, args);
    };
    
    XMLHttpRequest.prototype.send = function(...args) {
        // إضافة الترويسات الجغرافية المتقدمة
        if (this._url && !this._url.includes('chrome-extension')) {
            
            // Client Hints headers
            this.setRequestHeader('Sec-CH-UA', `"Chromium";v="${clientHintsConfig.chromeVersion.split('.')[0]}", "Google Chrome";v="${clientHintsConfig.chromeVersion.split('.')[0]}", "Not(A:Brand";v="99"`);
            this.setRequestHeader('Sec-CH-UA-Mobile', '?0');
            this.setRequestHeader('Sec-CH-UA-Platform', '"Windows"');
            this.setRequestHeader('Sec-CH-UA-Platform-Version', `"${clientHintsConfig.highEntropy.platformVersion}"`);
            this.setRequestHeader('Device-Memory', selectedRAM.toString());
            this.setRequestHeader('DPR', screenConfig.pixelRatio.toString());
            this.setRequestHeader('Viewport-Width', screenConfig.viewportWidth.toString());
            this.setRequestHeader('Width', Math.floor(screenConfig.width * 0.8).toString());
        }
        
        return originalSend.apply(this, args);
    };
    
    // تعديل fetch API أيضاً
    window.fetch = function(...args) {
        const [resource, init = {}] = args;
        
        const newInit = {
            ...init,
            headers: {
                ...init.headers,
                'Sec-CH-UA': `"Chromium";v="${clientHintsConfig.chromeVersion.split('.')[0]}", "Google Chrome";v="${clientHintsConfig.chromeVersion.split('.')[0]}", "Not(A:Brand";v="99"`,
                'Sec-CH-UA-Mobile': '?0',
                'Sec-CH-UA-Platform': '"Windows"'
            }
        };
        
        return originalFetch(resource, newInit);
    };
    
    // =============================================
    // 🎮 الحماية المتقدمة للـCanvas وWebGL
    // =============================================
    
    const originalGetContext = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function(contextType, ...args) {
        const context = originalGetContext.call(this, contextType, ...args);
        
        if (contextType === '2d') {
            const originalGetImageData = context.getImageData;
            context.getImageData = function(...getImageDataArgs) {
                try {
                    const imageData = originalGetImageData.apply(this, getImageDataArgs);
                    for (let i = 0; i < imageData.data.length; i += 4) {
                        if (Math.random() < 0.01) {
                            imageData.data[i] += Math.floor(Math.random() * 3) - 1;
                            imageData.data[i + 1] += Math.floor(Math.random() * 3) - 1;
                            imageData.data[i + 2] += Math.floor(Math.random() * 3) - 1;
                        }
                    }
                    return imageData;
                } catch (e) {
                    return null;
                }
            };
        } else if (contextType === 'webgl' || contextType === 'webgl2') {
            const originalGetParameter = context.getParameter;
            context.getParameter = function(parameter) {
                switch (parameter) {
                    case context.VENDOR:
                        return webglConfig.vendor;
                    case context.RENDERER:
                        return webglConfig.renderer;
                    case context.VERSION:
                        return webglConfig.version;
                    case context.SHADING_LANGUAGE_VERSION:
                        return webglConfig.shadingLanguageVersion;
                    case 37445: // UNMASKED_VENDOR_WEBGL
                        return webglConfig.unmaskedVendor;
                    case 37446: // UNMASKED_RENDERER_WEBGL
                        return webglConfig.unmaskedRenderer;
                    default:
                        return originalGetParameter.call(this, parameter);
                }
            };
            
            const originalGetSupportedExtensions = context.getSupportedExtensions;
            context.getSupportedExtensions = function() {
                const extensions = originalGetSupportedExtensions.call(this) || [];
                return [...extensions, 'WEBGL_debug_renderer_info', 'EXT_texture_filter_anisotropic'];
            };
        }
        
        return context;
    };
    
    // =============================================
    // 🔊 تزوير Audio Context المتقدم للكمبيوتر
    // =============================================
    
    const originalAudioContext = window.AudioContext || window.webkitAudioContext;
    if (originalAudioContext) {
        window.AudioContext = function() {
            const audioContext = new originalAudioContext();
            
            Object.defineProperty(audioContext, 'sampleRate', {
                get: () => audioConfig.sampleRate,
                configurable: false
            });
            
            const originalGetOutputTimestamp = audioContext.getOutputTimestamp;
            audioContext.getOutputTimestamp = function() {
                const contextTime = audioContext.currentTime;
                const performanceTime = performance.now();
                return {
                    contextTime: contextTime,
                    performanceTime: performanceTime
                };
            };
            
            const originalCreateAnalyser = audioContext.createAnalyser;
            audioContext.createAnalyser = function() {
                const analyser = originalCreateAnalyser.call(this);
                
                Object.defineProperty(analyser, 'frequencyBinCount', {
                    get: () => 2048,
                    configurable: false
                });
                
                Object.defineProperty(analyser, 'fftSize', {
                    get: () => 4096,
                    set: function(value) {},
                    configurable: false
                });
                
                return analyser;
            };
            
            return audioContext;
        };
        
        window.AudioContext.prototype = originalAudioContext.prototype;
    }
    
    // =============================================
    // 🧹 تنظيف الجلسات السابقة
    // =============================================
    
    const clearPreviousSessions = () => {
        try {
            if (window.localStorage) window.localStorage.clear();
            if (window.sessionStorage) window.sessionStorage.clear();
            if (window.indexedDB) {
                window.indexedDB.databases().then(databases => {
                    databases.forEach(db => {
                        if (db.name) window.indexedDB.deleteDatabase(db.name);
                    });
                }).catch(() => {});
            }
            if (navigator.serviceWorker) {
                navigator.serviceWorker.getRegistrations().then(registrations => {
                    registrations.forEach(registration => {
                        registration.unregister();
                    });
                });
            }
            console.log('🧹 تم تنظيف جلسات الكمبيوتر السابقة');
        } catch (e) {}
    };
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', clearPreviousSessions);
    } else {
        clearPreviousSessions();
    }
    
    // =============================================
    // 🎯 معلومات التفعيل النهائية
    // =============================================
    
    console.log('🖥️ Windows Computer Stealth - ULTIMATE EDITION WITH GEO-LOCATION');
    console.log('🌍 البلد: ' + stealthConfig.country);
    console.log('📡 IP: ' + stealthConfig.ip);
    console.log('🌐 اللغة: ' + stealthConfig.language);
    console.log('⏰ التوقيت: ' + stealthConfig.timezone);
    console.log('📺 الشاشة: ' + screenConfig.width + 'x' + screenConfig.height + ' (' + screenConfig.type + ')');
    console.log('💻 العتاد: ' + navigator.hardwareConcurrency + ' نواة, ' + selectedRAM + 'GB رام');
    console.log('🖥️ النظام: ' + selectedWindows.edition + ' ' + selectedWindows.build);
    console.log('🎮 كرت الشاشة: ' + webglConfig.vendor + ' - ' + webglConfig.renderer);
    console.log('🔒 الحماية: WebRTC + Performance + Plugins + Headers');
    
    // علامات نجاح التحميل
    window.__windows_computer_stealth_geo_ultimate = true;
    window.__stealth_config_applied = stealthConfig;
    window.__session_cleaned = true;
    
})();"""
        
        touch_script = """(function() {
    'use strict';
    
    // =============================================
    // 👆 محاكاة اللمس المتقدمة للهواتف
    // =============================================
    
    class AdvancedTouchSimulator {
        constructor() {
            this.touchPoints = [];
            this.isTouching = false;
            this.lastTouchTime = 0;
            this.touchCooldown = 100; // منع اللمسات المتكررة بسرعة
        }
        
        generateTouchEvent(type, touches, target) {
            const event = new TouchEvent(type, {
                bubbles: true,
                cancelable: true,
                composed: true,
                touches: touches,
                targetTouches: touches,
                changedTouches: touches
            });
            
            // إضافة خصائص إضافية للواقعية
            Object.defineProperties(event, {
                'scale': { value: 1.0 },
                'rotation': { value: 0.0 },
                'altitudeAngle': { value: Math.PI / 2 },
                'azimuthAngle': { value: 0.0 },
                'touchType': { value: 'direct' }
            });
            
            return event;
        }
        
        createTouch(point, target) {
            return new Touch({
                identifier: Date.now() + Math.random(),
                target: target,
                clientX: point.x,
                clientY: point.y,
                screenX: point.x + window.screenX,
                screenY: point.y + window.screenY,
                pageX: point.x + window.pageXOffset,
                pageY: point.y + window.pageYOffset,
                radiusX: 10 + Math.random() * 10,
                radiusY: 10 + Math.random() * 10,
                rotationAngle: Math.random() * 360,
                force: 0.5 + Math.random() * 0.5
            });
        }
        
        getRandomElement() {
            const selectors = [
                'button', 'a', 'input', 'textarea', 'select',
                'div[onclick]', 'span[onclick]', 'li[onclick]',
                '[role="button"]', '[tabindex]', '.btn', '.button',
                'h1', 'h2', 'h3', 'p', 'span', 'div',
                'ytm-compact-video-renderer', 
                'ytm-item-section-renderer', 
                '.video-title', 
                '.media-item-thumbnail-container',
                '#player-control-container',
                '[class*="renderer"]'
            ];
            
            const elements = [];
            
            // البحث في document الرئيسي
            selectors.forEach(selector => {
                try {
                    const found = document.querySelectorAll(selector);
                    found.forEach(el => {
                        if (this.isTappableElement(el)) {
                            elements.push(el);
                        }
                    });
                } catch (e) {}
            });
            
            // البحث في iframes (نفس الأصل فقط)
            try {
                const iframes = document.querySelectorAll('iframe');
                iframes.forEach(iframe => {
                    try {
                        const iDoc = iframe.contentDocument || iframe.contentWindow.document;
                        if (!iDoc) return;
                        selectors.forEach(selector => {
                            try {
                                const found = iDoc.querySelectorAll(selector);
                                found.forEach(el => {
                                    if (this.isTappableElement(el)) {
                                        elements.push(el);
                                    }
                                });
                            } catch (e) {}
                        });
                    } catch (e) {}
                });
            } catch (e) {}
            
            // ✅ Fallback: إذا لم نجد شيئًا، نجرب elementFromPoint في نقاط عشوائية
            if (elements.length === 0) {
                console.log('⚠️ لم نجد عناصر بـ CSS — نجرب elementFromPoint');
                for (let i = 0; i < 20; i++) {
                    const x = Math.random() * window.innerWidth;
                    const y = Math.random() * window.innerHeight;
                    try {
                        const el = document.elementFromPoint(x, y);
                        if (el && this.isTappableElement(el)) {
                            elements.push(el);
                        }
                    } catch (e) {}
                }
            }
            
            console.log(`🔍 عدد العناصر المكتشفة: ${elements.length}`);
            
            return elements.length > 0 ? elements[Math.floor(Math.random() * elements.length)] : null;
        }
        
        isTappableElement(element) {
            if (!element) return false;
            
            // تجاهل العناصر غير المرئية تمامًا
            const style = window.getComputedStyle(element);
            if (style.display === 'none' || style.visibility === 'hidden') return false;
            if (style.pointerEvents === 'none') return false;
            if (style.opacity === '0') return false;
            
            const rect = element.getBoundingClientRect();
            if (rect.width < 10 || rect.height < 10) return false;
            
            // نسمح بالعناصر خارج الشاشة قليلاً (مرونة أكبر)
            // نتحقق فقط أنها ليست بعيدة جدًا
            const margin = 200;  // هامش إضافي
            if (rect.bottom < -margin) return false;
            if (rect.top > window.innerHeight + margin) return false;
            if (rect.right < -margin) return false;
            if (rect.left > window.innerWidth + margin) return false;
            
            return true;
        }
        
        getElementCenter(element) {
            const rect = element.getBoundingClientRect();
            return {
                x: rect.left + rect.width / 2,
                y: rect.top + rect.height / 2
            };
        }
        
        addRandomOffset(point, maxOffset = 20) {
            return {
                x: point.x + (Math.random() * maxOffset * 2 - maxOffset),
                y: point.y + (Math.random() * maxOffset * 2 - maxOffset)
            };
        }
        
        async simulateTap(element = null) {
            const now = Date.now();
            if (now - this.lastTouchTime < this.touchCooldown) {
                return false;
            }
            
            if (!element) {
                element = this.getRandomElement();
                if (!element) {
                    console.log('👆 لم نجد عنصرًا — نلمس نقطة عشوائية في الشاشة');
                    // fallback: لمس نقطة عشوائية
                    const randX = Math.random() * window.innerWidth;
                    const randY = Math.random() * window.innerHeight;
                    const fallbackEl = document.elementFromPoint(randX, randY) || document.body;
                    if (!fallbackEl) return false;
                    element = fallbackEl;
                }
            }
            
            try {
                const center = this.getElementCenter(element);
                const touchPoint = this.addRandomOffset(center);
                const touch = this.createTouch(touchPoint, element);
                
                this.simulateTouchSequence([touch], element);
                
                this.lastTouchTime = now;
                console.log(`👆 تم محاكاة لمس على: ${element.tagName}.${Array.from(element.classList).join('.')}`);
                return true;
                
            } catch (error) {
                console.log('👆 خطأ في محاكاة اللمس:', error);
                return false;
            }
        }
        
        simulateTouchSequence(touches, target) {
            // touchstart
            const startEvent = this.generateTouchEvent('touchstart', touches, target);
            target.dispatchEvent(startEvent);
            
            // touchend بعد تأخير بسيط
            setTimeout(() => {
                const endEvent = this.generateTouchEvent('touchend', [], target);
                target.dispatchEvent(endEvent);
                
                // click event للتوافق
                setTimeout(() => {
                    const clickEvent = new MouseEvent('click', {
                        bubbles: true,
                        cancelable: true,
                        view: window
                    });
                    target.dispatchEvent(clickEvent);
                }, 10);
            }, 50 + Math.random() * 100);
        }
        
        async simulateSwipe(startX, startY, endX, endY, duration = 500) {
            const steps = 10;
            const stepDelay = duration / steps;
            
            const startTouch = this.createTouch({ x: startX, y: startY }, document.elementFromPoint(startX, startY));
            
            // بدء اللمس
            const startEvent = this.generateTouchEvent('touchstart', [startTouch], document.elementFromPoint(startX, startY));
            document.dispatchEvent(startEvent);
            
            // حركة السحب
            for (let i = 1; i <= steps; i++) {
                await this.delay(stepDelay);
                
                const progress = i / steps;
                const currentX = startX + (endX - startX) * progress;
                const currentY = startY + (endY - startY) * progress;
                
                const moveTouch = this.createTouch({ x: currentX, y: currentY }, document.elementFromPoint(currentX, currentY));
                const moveEvent = this.generateTouchEvent('touchmove', [moveTouch], document);
                document.dispatchEvent(moveEvent);
            }
            
            // نهاية اللمس
            await this.delay(stepDelay);
            const endTouch = this.createTouch({ x: endX, y: endY }, document.elementFromPoint(endX, endY));
            const endEvent = this.generateTouchEvent('touchend', [], document);
            document.dispatchEvent(endEvent);
            
            console.log("👆 تم محاكاة سحب من (" + startX + "," + startY + ") إلى (" + endX + "," + endY + ")");
        }
        
        async simulatePinchZoom(centerX, centerY, startDistance, endDistance, duration = 600) {
            const steps = 12;
            const stepDelay = duration / steps;
            
            const startTouch1 = this.createTouch(
                { x: centerX - startDistance / 2, y: centerY }, 
                document.elementFromPoint(centerX - startDistance / 2, centerY)
            );
            const startTouch2 = this.createTouch(
                { x: centerX + startDistance / 2, y: centerY }, 
                document.elementFromPoint(centerX + startDistance / 2, centerY)
            );
            
            // بدء اللمس بنقطتين
            const startEvent = this.generateTouchEvent('touchstart', [startTouch1, startTouch2], document);
            document.dispatchEvent(startEvent);
            
            // حركة التكبير/التصغير
            for (let i = 1; i <= steps; i++) {
                await this.delay(stepDelay);
                
                const progress = i / steps;
                const currentDistance = startDistance + (endDistance - startDistance) * progress;
                
                const moveTouch1 = this.createTouch(
                    { x: centerX - currentDistance / 2, y: centerY }, 
                    document.elementFromPoint(centerX - currentDistance / 2, centerY)
                );
                const moveTouch2 = this.createTouch(
                    { x: centerX + currentDistance / 2, y: centerY }, 
                    document.elementFromPoint(centerX + currentDistance / 2, centerY)
                );
                
                const moveEvent = this.generateTouchEvent('touchmove', [moveTouch1, moveTouch2], document);
                document.dispatchEvent(moveEvent);
            }
            
            // نهاية اللمس
            await this.delay(stepDelay);
            const endEvent = this.generateTouchEvent('touchend', [], document);
            document.dispatchEvent(endEvent);
            
            console.log("👆 تم محاكاة تكبير/تصغير حول (" + centerX + "," + centerY + ")");
        }
        
        async simulateScroll(direction = 'down', distance = 300, duration = 800) {
            const viewportWidth = window.innerWidth;
            const viewportHeight = window.innerHeight;
            
            let startX, startY, endX, endY;
            
            switch (direction) {
                case 'down':
                    startX = viewportWidth / 2;
                    startY = viewportHeight * 0.7;
                    endX = startX;
                    endY = startY - distance;
                    break;
                case 'up':
                    startX = viewportWidth / 2;
                    startY = viewportHeight * 0.3;
                    endX = startX;
                    endY = startY + distance;
                    break;
                case 'left':
                    startX = viewportWidth * 0.7;
                    startY = viewportHeight / 2;
                    endX = startX - distance;
                    endY = startY;
                    break;
                case 'right':
                    startX = viewportWidth * 0.3;
                    startY = viewportHeight / 2;
                    endX = startX + distance;
                    endY = startY;
                    break;
                default:
                    startX = viewportWidth / 2;
                    startY = viewportHeight * 0.7;
                    endX = startX;
                    endY = startY - distance;
            }
            
            await this.simulateSwipe(startX, startY, endX, endY, duration);
        }
        
        async performRandomTouchActions(count = 3) {
            console.log("👆 بدء " + count + " إجراء لمس عشوائي...");
            
            let successCount = 0;
            
            for (let i = 0; i < count; i++) {
                const actionType = Math.random();
                let result = false;
                
                try {
                    if (actionType < 0.6) {
                        // لمس عادي (60%)
                        result = await this.simulateTap();
                    } else if (actionType < 0.8) {
                        // سحب (20%)
                        const startX = Math.random() * window.innerWidth * 0.8 + window.innerWidth * 0.1;
                        const startY = Math.random() * window.innerHeight * 0.8 + window.innerHeight * 0.1;
                        const endX = startX + (Math.random() * 200 - 100);
                        const endY = startY + (Math.random() * 200 - 100);
                        await this.simulateSwipe(startX, startY, endX, endY);
                        result = true;
                    } else {
                        // scroll (20%)
                        const directions = ['up', 'down', 'left', 'right'];
                        const direction = directions[Math.floor(Math.random() * directions.length)];
                        await this.simulateScroll(direction);
                        result = true;
                    }
                    
                    if (result) successCount++;
                } catch (e) {
                    console.log('👆 خطأ في إجراء ' + i + ':', e);
                }
                
                // تأخير بين الإجراءات
                await this.delay(1000 + Math.random() * 2000);
            }
            
            console.log('👆 اكتملت الإجراءات: ' + successCount + '/' + count + ' نجحت');
            return successCount > 0;
        }
        
        delay(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }
    }
    
    // إنشاء المحاكي وتعريضه globally
    window.touchSimulator = new AdvancedTouchSimulator();
    
    console.log('👆 محاكي اللمس المتقدم جاهز للاستخدام');
    console.log('👆 الأوامر المتاحة:');
    console.log('   - touchSimulator.simulateTap(element)');
    console.log('   - touchSimulator.simulateSwipe(startX, startY, endX, endY)');
    console.log('   - touchSimulator.simulateScroll(direction)');
    console.log('   - touchSimulator.performRandomTouchActions(count)');
    
})();
"""if self.device_type == "phone" else None
        
        
        combined_script = country_script + "\n" + device_script
        
        # نضع السكربت المدمج في القائمة
        scripts = [combined_script]
        
        
        if touch_script:
            scripts.append(touch_script)
        

        return scripts

    def load_advanced_scripts(self):
        """تحميل السكريبتات المتقدمة للتهرب من الكشف وتفعيل تتبع الأهداف الجديدة"""
        self.enable_auto_attach_new_targets()
        self.apply_cdp_override_to_current_driver()
        scripts = self._build_stealth_scripts_list()
        for i, script in enumerate(scripts):
            try:
                self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                    'source': script
                })
                print(f"✅ تم تحميل السكريبت المدمج {i+1} بنجاح")
            except Exception as e:
                print(f"⚠️ تحذير في تحميل السكريبت {i+1}: {e}")

                
    def handle_cookie_policy(self):
        """التعامل مع سياسة ملفات الارتباط بسرعة"""
        try:
            # تقليل وقت الانتظار إلى 1 ثانية فقط أثناء البحث السريع
            self.driver.implicitly_wait(1)
            
            cookie_selectors = [
                'button[aria-label*="Agree"]', 'button[aria-label*="Accept"]',
                '#L2AGLb', '.tHlp8d',  # أزرار جوجل ويوتيوب الشهيرة
                'button.VfPpkd-LgbsSe', 
                '//button[contains(text(), "Accept")]', 
                '//button[contains(text(), "Agree")]',
                '//button[contains(text(), "قبول")]',
                '//button[contains(text(), "موافق")]'
            ]
            
            print("🍪 فحص سريع لسياسة ملفات الارتباط...")
            
            for selector in cookie_selectors:
                try:
                    elements = []
                    if selector.startswith('//'):
                        elements = self.driver.find_elements(By.XPATH, selector)
                    else:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    if elements and elements[0].is_displayed():
                        print(f"🍪 تم العثور على الزر، جاري النقر...")
                        self.driver.execute_script("arguments[0].click();", elements[0])
                        print("✅ تم قبول السياسة")
                        self.driver.implicitly_wait(0) # إعادة الوقت الأصلي
                        return True
                except:
                    continue
            
            self.driver.implicitly_wait(0) # إعادة الوقت الأصلي في حال لم يجد شيء
            print("ℹ️ لم تظهر نافذة منبثقة")
            return False
            
        except Exception as error:
            self.driver.implicitly_wait(0)
            return False
            
        except Exception as error:
            print(f"⚠️ خطأ في التعامل مع سياسة ملفات الارتباط: {error}")
            return False     
    
    def setup_cookies(self):
        """إعداد الكوكيز الوهمية"""
        try:
            print("🍪 جاري إعداد الكوكيز الوهمية...")
            cookies_injected = self.cookie_generator.setup_fake_cookies(self.driver, 800)
            print(f"✅ تم إعداد {cookies_injected} كوكي وهمي")
            return True
        except Exception as e:
            print(f"❌ خطأ في إعداد الكوكيز: {e}")
            return False
    
    def schedule_movements_during_visit(self):
        """جدولة الحركات خلال فترة الزيارة"""
        start_time = time.time()
        end_time = start_time + self.visit_duration
        
        if self.device_type == "phone":
            num_touches = random.randint(2, 3)
            movements = []
            
            for i in range(num_touches):
                movement_time = start_time + random.uniform(1, self.visit_duration - 5)
                movements.append(("touch", movement_time))
                
        else:
            num_movements = random.randint(4, 10)
            movements = []
            
            for i in range(num_movements):
                movement_time = start_time + random.uniform(1, self.visit_duration - 3)
                movements.append(("mouse", movement_time))
        
        movements.sort(key=lambda x: x[1])
        
        # طباعة الجدول الزمني المتوقع للمستخدم
        print(f"\n📅 === جدول الحركات ({len(movements)} أحداث) ===")
        base_start = movements[0][1] if movements else start_time
        for i, (m_type, m_time) in enumerate(movements):
            offset = m_time - start_time
            print(f"   {i+1}. {m_type} - بعد {offset:.1f} ثانية")
        print("======================================\n")
        
        return movements
    
    def execute_phone_touches(self):
        """تنفيذ لمسات للهاتف مع انتظار حقيقي للانتهاء"""
        try:
            self.driver.set_script_timeout(30)
            
            # فحص أولاً إن كان الكائن موجودًا
            exists = self.driver.execute_script(
                "return typeof window.touchSimulator !== 'undefined';"
            )
            
            if not exists:
                # محاولة إعادة حقن السكريبت
                print("⚠️ touchSimulator غير موجود — نحاول إعادة حقنه...")
                try:
                    self.driver.execute_script("""
                        if (typeof AdvancedTouchSimulator === 'undefined') {
                            console.log('⚠️ AdvancedTouchSimulator class missing');
                        }
                    """)
                except:
                    pass
                print("❌ فشل: touchSimulator غير معرّف في الصفحة الحالية")
                return
            
            touches_executed = self.driver.execute_async_script("""
                var callback = arguments[arguments.length - 1];
                
                if (window.touchSimulator) {
                    window.touchSimulator.performRandomTouchActions(1)
                        .then((success) => {
                            callback(success);
                        })
                        .catch((err) => {
                            console.error("Touch Error:", err);
                            callback(false);
                        });
                } else {
                    console.log("TouchSimulator object not found!");
                    callback(false);
                }
            """)
            
            if touches_executed:
                print("👆 تم تنفيذ لمسات الهاتف بنجاح")
            else:
                print("⚠️ لم تنجح أي محاولة لمس (تظهر رسالة تفصيلية في console)")
                
        except Exception as e:
            print(f"❌ خطأ في نظام اللمس: {e}")
    
    def execute_computer_movements(self):
        """تنفيذ حركة ماوس واحدة — مع timeout 8s"""
        import threading as _th
        
        try:
            elements = self.find_interactive_elements()
            if not elements:
                return
            
            target_element = random.choice(elements)
            movements = self.generate_smart_movements(target_element)
            
            if movements:
                movement = movements[0]
                
                # 🆕 تشغيل الحركة في thread مع timeout
                _done = [False]
                def _run():
                    try:
                        self.execute_smart_mouse_movement(movement)
                        _done[0] = True
                    except:
                        pass
                
                t = _th.Thread(target=_run, daemon=True)
                t.start()
                t.join(timeout=8)  # ← 8 ثوانٍ كحد أقصى
                
                if not t.is_alive():
                    print(f"✅ تم تنفيذ حركة {movement['type']} على عنصر واحد")
                else:
                    print(f"⚠️ حركة {movement['type']} تجاوزت 8s — تخطي")
                    return
                
                # نقرة عشوائية نادرة (20%)
                if random.random() < 0.2:
                    try:
                        _done2 = [False]
                        def _click():
                            try:
                                ActionChains(self.driver).move_to_element(target_element).click().perform()
                                _done2[0] = True
                            except:
                                pass
                        t2 = _th.Thread(target=_click, daemon=True)
                        t2.start()
                        t2.join(timeout=5)
                        if _done2[0]:
                            print("🖱️ تم النقر (Click) أيضاً")
                    except:
                        pass
            
        except Exception as e:
            print(f"❌ خطأ في الحركة: {e}")
    
    def find_interactive_elements(self):
        """مسح واحد بـ XPATH — سريع"""
        try:
            els = self.driver.find_elements(
                By.XPATH,
                "//button | //a | //input | //*[@role='button'] | //*[@tabindex]"
            )
        except Exception:
            return []
        
        result = []
        for el in els:
            try:
                if el.is_displayed() and el.is_enabled():
                    result.append(el)
                    if len(result) >= 15:
                        break
            except Exception:
                pass
        
        return result
    
    def generate_smart_movements(self, target_element):
        """توليد حركات ذكية تستهدف عنصر معين"""
        movements = []
        # إزالة الحركة المكررة رقم 8 - أصبحت 5 حركات فقط
        movement_types = ['spiral_in', 'spiral_out', 'figure_eight', 'wave', 'zigzag']
        
        for _ in range(random.randint(1, 2)):
            movement = {
                'type': random.choice(movement_types),
                'target_element': target_element,
                'complexity': random.choice(['simple', 'medium']),
                'speed': random.choice(['medium', 'fast'])
            }
            movements.append(movement)
        
        return movements

    def execute_smart_mouse_movement(self, movement):
        """تنفيذ حركة ماوس ذكية — مع timeout وحماية"""
        try:
            element = movement['target_element']
            center = self.get_element_center_safe(element)
            if not center:
                return
            
            center_x, center_y = center
            
            # 1. الانتقال الأولي للعنصر (بـ try/except)
            try:
                ActionChains(self.driver).move_to_element(element).perform()
            except:
                pass
            
            # 2. الآن الحركة الذكية
            actions = ActionChains(self.driver)
            
            if movement['type'] == 'spiral_in':
                self.spiral_in_movement(actions, center_x, center_y, movement)
            elif movement['type'] == 'spiral_out':
                self.spiral_out_movement(actions, center_x, center_y, movement)
            elif movement['type'] == 'figure_eight':
                self.figure_eight_movement(actions, center_x, center_y, movement)
            elif movement['type'] == 'wave':
                self.wave_movement(actions, center_x, center_y, movement)
            elif movement['type'] == 'zigzag':
                self.zigzag_movement(actions, center_x, center_y, movement)
            
            print(f"✅ تم تنفيذ حركة {movement['type']}")
            
        except Exception as e:
            print(f"⚠️ خطأ في الحركة الذكية: {e}")

    # =============================================
    # 🎯 دوال الحركات الذكية (بدون التكرار)
    # =============================================

    def _safe_move_by_offset(self, dx, dy, pause=0.03):
        """حركة ماوس آمنة — perform فوري + timeout داخلي"""
        try:
            act = ActionChains(self.driver)
            act.move_by_offset(int(dx), int(dy))
            act.pause(pause)
            act.perform()
        except Exception:
            # إذا فشلت الحركة، لا نكسر الحلقة
            pass
    
    def get_element_center_safe(self, element):
        """مركز العنصر — مع قيم افتراضية عند الفشل"""
        try:
            center = self.get_element_center(element)
            if center:
                cx, cy = center
                try:
                    vw = self.driver.execute_script("return window.innerWidth;")
                    vh = self.driver.execute_script("return window.innerHeight;")
                except:
                    vw, vh = 1366, 768
                cx = max(20, min(vw - 20, cx))
                cy = max(20, min(vh - 20, cy))
                return cx, cy
            return None
        except:
            return None
    
    def spiral_in_movement(self, actions, center_x, center_y, movement):
        """حركة لولبية للداخل — perform بعد كل خطوة + حدود"""
        radius = random.randint(80, 150)
        steps = 8  # ← قللنا من 15 لـ 8 (أخف)
        
        # حدود الشاشة (مع هامش 20px)
        try:
            vw = self.driver.execute_script("return window.innerWidth;")
            vh = self.driver.execute_script("return window.innerHeight;")
        except:
            vw, vh = 1366, 768
        margin = 20
        
        prev_x, prev_y = center_x, center_y
        
        for i in range(steps):
            t = i / steps
            current_radius = radius * (1 - t)
            angle = 4 * math.pi * t
            
            x = center_x + current_radius * math.cos(angle)
            y = center_y + current_radius * math.sin(angle)
            
            # تثبيت داخل الشاشة
            x = max(margin, min(vw - margin, x))
            y = max(margin, min(vh - margin, y))
            
            move_x = x - prev_x
            move_y = y - prev_y
            
            # تخطي الحركات الصغيرة جدًا
            if abs(move_x) < 1 and abs(move_y) < 1:
                continue
            
            try:
                self._safe_move_by_offset(move_x, move_y, 0.03)
            except:
                pass
            
            prev_x, prev_y = x, y

    def spiral_out_movement(self, actions, center_x, center_y, movement):
        """حركة لولبية للخارج — perform بعد كل خطوة + حدود"""
        radius = random.randint(40, 100)
        steps = 8  # ← قللنا
        
        try:
            vw = self.driver.execute_script("return window.innerWidth;")
            vh = self.driver.execute_script("return window.innerHeight;")
        except:
            vw, vh = 1366, 768
        margin = 20
        
        prev_x, prev_y = center_x, center_y
        
        for i in range(steps):
            t = i / steps
            current_radius = radius * t
            angle = 4 * math.pi * t
            
            x = center_x + current_radius * math.cos(angle)
            y = center_y + current_radius * math.sin(angle)
            
            x = max(margin, min(vw - margin, x))
            y = max(margin, min(vh - margin, y))
            
            move_x = x - prev_x
            move_y = y - prev_y
            
            if abs(move_x) < 1 and abs(move_y) < 1:
                continue
            
            try:
                self._safe_move_by_offset(move_x, move_y, 0.03)
            except:
                pass
            
            prev_x, prev_y = x, y

    def figure_eight_movement(self, actions, center_x, center_y, movement):
        """حركة على شكل رقم 8 — perform بعد كل خطوة"""
        scale = random.randint(60, 120)
        steps = 10  # ← قللنا من 20
        
        try:
            vw = self.driver.execute_script("return window.innerWidth;")
            vh = self.driver.execute_script("return window.innerHeight;")
        except:
            vw, vh = 1366, 768
        margin = 20
        
        prev_x, prev_y = center_x, center_y
        
        for i in range(steps):
            t = 2 * math.pi * i / steps
            x = center_x + scale * math.sin(t) / (1 + math.cos(t)**2)
            y = center_y + scale * math.sin(t) * math.cos(t) / (1 + math.cos(t)**2)
            
            x = max(margin, min(vw - margin, x))
            y = max(margin, min(vh - margin, y))
            
            move_x = x - prev_x
            move_y = y - prev_y
            
            if abs(move_x) < 1 and abs(move_y) < 1:
                continue
            
            try:
                self._safe_move_by_offset(move_x, move_y, 0.03)
            except:
                pass
            
            prev_x, prev_y = x, y

    def wave_movement(self, actions, center_x, center_y, movement):
        """حركة موجية — perform بعد كل خطوة"""
        amplitude = random.randint(50, 100)
        frequency = random.randint(2, 4)
        steps = 10  # ← قللنا
        
        try:
            vw = self.driver.execute_script("return window.innerWidth;")
            vh = self.driver.execute_script("return window.innerHeight;")
        except:
            vw, vh = 1366, 768
        margin = 20
        
        prev_x, prev_y = center_x, center_y
        
        for i in range(steps):
            t = 2 * math.pi * i / steps
            x = center_x + amplitude * math.cos(frequency * t)
            y = center_y + amplitude * math.sin(t)
            
            x = max(margin, min(vw - margin, x))
            y = max(margin, min(vh - margin, y))
            
            move_x = x - prev_x
            move_y = y - prev_y
            
            if abs(move_x) < 1 and abs(move_y) < 1:
                continue
            
            try:
                self._safe_move_by_offset(move_x, move_y, 0.03)
            except:
                pass
            
            prev_x, prev_y = x, y

    def zigzag_movement(self, actions, center_x, center_y, movement):
        """حركة متعرجة — perform بعد كل خطوة"""
        amplitude = random.randint(60, 120)
        segments = random.randint(2, 4)  # ← قللنا
        steps = 8  # ← قللنا
        steps_per_segment = max(2, steps // segments)
        
        try:
            vw = self.driver.execute_script("return window.innerWidth;")
            vh = self.driver.execute_script("return window.innerHeight;")
        except:
            vw, vh = 1366, 768
        margin = 20
        
        prev_x, prev_y = center_x, center_y
        
        for segment in range(segments):
            for i in range(steps_per_segment):
                t = i / steps_per_segment
                direction = 1 if segment % 2 == 0 else -1
                
                x = center_x + amplitude * direction * (1 - 2 * t)
                y = center_y + amplitude * (segment / segments - 0.5)
                
                x = max(margin, min(vw - margin, x))
                y = max(margin, min(vh - margin, y))
                
                move_x = x - prev_x
                move_y = y - prev_y
                
                if abs(move_x) < 1 and abs(move_y) < 1:
                    continue
                
                try:
                    self._safe_move_by_offset(move_x, move_y, 0.03)
                except:
                    pass
                
                prev_x, prev_y = x, y

    def get_element_center(self, element):
        """الحصول على مركز العنصر"""
        try:
            location = element.location
            size = element.size
            center_x = location['x'] + size['width'] / 2
            center_y = location['y'] + size['height'] / 2
            return center_x, center_y
        except:
            return None

    # ═══════════════════════════════════════════════════════
    # 🆕 نظام النقر على الأزرار (إضافة)
    # ═══════════════════════════════════════════════════════
    
    def ask_user_for_buttons(self):
        """يسأل المستخدم عن الأزرار قبل فتح المتصفح"""
        print("\n" + "=" * 60)
        print("🔘 إعداد الأزرار — أدخل الكلمات كما تظهر في الموقع")
        print("=" * 60)
        
        while True:
            try:
                count_str = input("كم عدد الأزرار التي تريد النقر عليها؟ ").strip()
                count = int(count_str)
                if count <= 0:
                    print("⚠️ يجب أن يكون العدد 1 على الأقل")
                    continue
                if count > 10:
                    print("⚠️ الحد الأقصى 10 أزرار")
                    continue
                break
            except ValueError:
                print("⚠️ أدخل رقمًا صحيحًا")
        
        keywords = []
        for i in range(1, count + 1):
            while True:
                kw = input(f"اكتب كلمة الزر {i}: ").strip()
                if kw:
                    keywords.append(kw)
                    break
                print("⚠️ الكلمة فارغة — أعد الإدخال")
        
        print(f"\n✅ تم حفظ {len(keywords)} زر: {keywords}")
        print("=" * 60 + "\n")
        
        return keywords
    
    def _find_x_button(self, max_results=3):
        """يبحث عن زر إغلاق X شاملًا. يُرجع قائمة بالعناصر المرشحة"""
        found = []
        
        # 1. البحث بالنص المرئي (الرموز)
        symbol_xpath = (
            "//*[self::button or self::span or self::div or self::a or self::i]"
            "["
            "contains(text(), '×') or contains(text(), '✕') or "
            "contains(text(), '✗') or contains(text(), '✖') or "
            "contains(text(), '✘') or contains(text(), '☒') or "
            "normalize-space(text())='X' or normalize-space(text())='x'"
            "]"
        )
        try:
            for el in self.driver.find_elements(By.XPATH, symbol_xpath):
                if self._is_valid_clickable(el):
                    found.append(el)
        except:
            pass
        
        # 2. البحث بالكلمات (إنجليزي/عربي/فرنسي)
        for kw in X_KEYWORDS:
            if len(found) >= max_results:
                break
            if kw in ["×", "✕", "✗", "✖", "✘", "☒", "⨯"]:
                continue  # رموز — بحثنا عنها
            xpaths = [
                f"//*[self::button or self::a or self::span or self::div]"
                f"[contains(translate(normalize-space(text()), "
                f"'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
                f"'{kw.lower()}')]",
                f"//*[@aria-label and "
                f"contains(translate(@aria-label, "
                f"'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
                f"'{kw.lower()}')]",
                f"//*[@title and "
                f"contains(translate(@title, "
                f"'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
                f"'{kw.lower()}')]",
            ]
            for xp in xpaths:
                try:
                    for el in self.driver.find_elements(By.XPATH, xp):
                        if self._is_valid_clickable(el):
                            found.append(el)
                            if len(found) >= max_results:
                                break
                except:
                    pass
        
        # 3. البحث بـ class أو id يشير إلى close
        for hint in X_CLASS_HINTS + X_ID_HINTS:
            if len(found) >= max_results:
                break
            xpaths = [
                f"//*[contains(@class, '{hint}')]",
                f"//*[contains(@id, '{hint}')]",
            ]
            for xp in xpaths:
                try:
                    for el in self.driver.find_elements(By.XPATH, xp):
                        if self._is_valid_clickable(el):
                            # تأكد أنه صغير (زر فعلي وليس قسم)
                            try:
                                size = el.size
                                if size['width'] < 200 and size['height'] < 200:
                                    found.append(el)
                                    if len(found) >= max_results:
                                        break
                            except:
                                pass
                except:
                    pass
        
        # إزالة التكرار
        unique = []
        seen = set()
        for el in found:
            try:
                eid = el.id
                if eid not in seen:
                    seen.add(eid)
                    unique.append(el)
            except:
                pass
        
        return unique[:max_results]
    
    def _is_valid_clickable(self, element):
        """يتحقق أن العنصر قابل للنقر ومرئي"""
        try:
            if not element.is_displayed() or not element.is_enabled():
                return False
            size = element.size
            if size['width'] < 5 or size['height'] < 5:
                return False
            # تأكد أن العنصر ليس body
            tag = element.tag_name.lower()
            if tag in ('body', 'html'):
                return False
            return True
        except:
            return False
    
    def close_ad_if_present(self):
        """يفحص ويغلق الإعلانات (3 محاولات)"""
        for attempt in range(3):
            buttons = self._find_x_button(max_results=1)
            if not buttons:
                if attempt == 0:
                    return False  # لا يوجد إعلان
                break
            
            element = buttons[0]
            
            # تحريك الماوس أولاً (للكمبيوتر فقط)
            if self.device_type == "computer":
                try:
                    actions = ActionChains(self.driver)
                    actions.move_to_element(element)
                    actions.pause(random.uniform(0.2, 0.5))
                    actions.perform()
                except:
                    pass
            
            # النقر حسب نوع الجهاز
            try:
                if self.device_type == "phone":
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});",
                        element
                    )
                    time.sleep(0.3)
                    self.driver.execute_script(
                        "if (window.touchSimulator) {"
                        "  window.touchSimulator.simulateTap(arguments[0]);"
                        "} else {"
                        "  arguments[0].click();"
                        "}",
                        element
                    )
                else:
                    try:
                        element.click()
                    except:
                        self.driver.execute_script("arguments[0].click();", element)
                
                print(f"🚫 تم إغلاق إعلان (محاولة {attempt + 1})")
                time.sleep(0.5)
            except Exception as e:
                # لا نُطبع تفاصيل — نتجاهل
                break
        
        self.sync_new_windows_with_stealth()
        return True
    
    def find_button_by_keyword(self, keyword, timeout=10, debug=False):
        """يبحث عن الزر بالكلمة بشكل ذكي مع الانتظار الديناميكي ودعم تجاهل الأخطاء"""
        kw = keyword.strip()
        kw_lower = kw.lower()
        
        xpaths = [
            f"//button[normalize-space(text())='{kw}']",
            f"//a[normalize-space(text())='{kw}']",
            f"//*[normalize-space(text())='{kw}']",
            f"//button[contains(., '{kw}')]",
            f"//a[contains(., '{kw}')]",
            f"//*[@role='button' and contains(., '{kw}')]",
            f"//*[@aria-label and contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{kw_lower}')]",
            f"//*[@title and contains(translate(@title, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{kw_lower}')]",
            f"//input[@type='submit' or @type='button'][contains(@value, '{kw}')]",
        ]
        
        xpaths.append(
            f"//*[contains(translate(normalize-space(text()), 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ', 'abcdefghijklmnopqrstuvwxyzàâäéèêëîïôöùûüç'), '{kw_lower}')]"
        )
        
        end_time = time.time() + timeout
        while time.time() < end_time:
            for xp in xpaths:
                try:
                    elements = self.driver.find_elements(By.XPATH, xp)
                    for el in elements:
                        if self._is_valid_clickable(el):
                            print(f"🎯 تم العثور على الزر بنجاح عبر البحث: '{kw}'")
                            return el
                except:
                    continue
            time.sleep(0.5)
        
        if debug:
            print(f"⚠️ Debug: لم يتم العثور على العنصر '{kw}' حتى بعد انتهاء المهلة.")
        return None

    def click_element_natural(self, element):
        """ينقر بشكل طبيعي مع التأكد من إزاحة العنصر وإظهاره على الشاشة ومزامنة أي نافذة جديدة بنفس التخفي"""
        known_handles = set()
        try:
            known_handles = set(self.driver.window_handles)
        except Exception:
            known_handles = set()

        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                element
            )
            time.sleep(random.uniform(0.5, 1.0))
            
            if self.device_type == "phone":
                try:
                    self.driver.execute_script(
                        "if (window.touchSimulator) { window.touchSimulator.simulateTap(arguments[0]); } else { arguments[0].click(); }",
                        element
                    )
                except:
                    element.click()
            else:
                try:
                    ActionChains(self.driver).move_to_element(element).pause(0.2).click().perform()
                except:
                    try:
                        element.click()
                    except:
                        self.driver.execute_script("arguments[0].click();", element)
            
            time.sleep(0.4)
            self.sync_new_windows_with_stealth(known_handles)
            return True
        except Exception as e:
            print(f"⚠️ فشل النقر الطبيعي، جاري محاولة النقر عبر JavaScript مباشرة: {e}")
            try:
                self.driver.execute_script("arguments[0].click();", element)
                return True
            except Exception as js_err:
                print(f"❌ فشل النقر النهائي: {js_err}")
                return False

    def do_one_movement(self):
        """ينفذ حركة قصيرة واحدة (من نفس مجموعة الحركات)"""
        try:
            if self.device_type == "phone":
                self.execute_phone_touches()
            else:
                self.execute_computer_movements()
        except Exception as e:
            print(f"⚠️ خطأ في الحركة: {e}")
    
    def dynamic_visit_loop(self, buttons):
        """الحلقة الديناميكية الرئيسية — تنسّق الحركات والنقرات"""
        visit_start = time.time()
        visit_deadline = visit_start + self.visit_duration
        
        button_index = 0
        total_buttons = len(buttons)
        
        # وقت النقرة الأولى: بعد 3-6 ثواني من بداية الزيارة
        next_click_at = visit_start + random.uniform(3, 6)
        
        cycle = 0
        while True:
            cycle += 1
            now = time.time()
            
            # 🆕 فحص: هل Chrome مغلق؟
            try:
                _ = self.driver.current_url
            except Exception as _e:
                print(f"\n⚠️ Chrome مغلق ({type(_e).__name__}) — إنهاء الحلقة")
                break
            
            print(f"\n🔄 دورة {cycle} — الوقت المنقضي: {now - visit_start:.1f}s")
            
            # ═══════════════════════════════════
            # هل حان وقت النقرة؟
            # ═══════════════════════════════════
            if button_index < total_buttons and now >= next_click_at:
                keyword = buttons[button_index]
                print(f"\n🎯 حان وقت الزر {button_index + 1}/{total_buttons}: '{keyword}'")
                
                # 1. حركة قصيرة قبل النقرة
                print("🎬 حركة قصيرة قبل النقرة...")
                self.do_one_movement()
                
                # 2. فحص X
                print("🔍 فحص إعلان...")
                self.close_ad_if_present()
                
                # 3. البحث عن الزر
                print(f"🔍 البحث عن '{keyword}'...")
                element = self.find_button_by_keyword(keyword)
                
                # 🆕 إذا لم نجد، فعّل debug
                if element is None:
                    print(f"⚠️ لم أجد '{keyword}' — تفعيل DEBUG")
                    element = self.find_button_by_keyword(keyword, debug=True)
                
                # 🆕 انتظار ديناميكي: 5 محاولات × 1s
                if element is None:
                    print(f"⏳ انتظار ديناميكي للزر '{keyword}' (5s)...")
                    for _try in range(5):
                        time.sleep(1)
                        element = self.find_button_by_keyword(keyword)
                        if element is not None:
                            print(f"✅ وجدت الزر بعد {_try + 1}s")
                            break
                    
                    if element is not None:
                        pass  # وُجد بعد الانتظار
                    else:
                        # ⛔ توقف كلي
                        print(f"\n{'=' * 60}")
                        print(f"❌ لم أجد الزر: '{keyword}' بعد 5 محاولات")
                        print(f"   يتم إيقاف الكود بالكامل")
                        print(f"{'=' * 60}")
                        raise RuntimeError(f"BUTTON_NOT_FOUND:{keyword}")
                
                # 4. النقر
                print(f"👆 النقر على '{keyword}'...")
                if not self.click_element_natural(element):
                    raise RuntimeError(f"CLICK_FAILED:{keyword}")
                
                print(f"✅ تم النقر على '{keyword}'")
                
                # 5. انتظار 6-20 ثانية
                wait_time = random.uniform(6, 20)
                print(f"⏳ انتظار {wait_time:.1f}s بعد النقرة...")
                time.sleep(wait_time)
                
                # 6. فحص X بعد النقرة
                print("🔍 فحص إعلان بعد النقرة...")
                self.close_ad_if_present()
                
                # 7. استعد للزر التالي
                button_index += 1
                if button_index < total_buttons:
                    next_click_at = time.time() + random.uniform(2, 5)
                    print(f"➡️ الزر التالي بعد {next_click_at - time.time():.1f}s")
                else:
                    print("🎉 اكتملت كل الأزرار!")
                    next_click_at = float('inf')
                
                continue
            
            # ═══════════════════════════════════
            # هل انتهت الجلسة؟
            # ═══════════════════════════════════
            all_buttons_done = (button_index >= total_buttons)
            visit_expired = (now >= visit_deadline)
            
            # 🆕 WATCHDOG
            hard_deadline = visit_start + self.visit_duration + 90
            if now >= hard_deadline:
                print(f"\n⚠️ WATCHDOG: تجاوز {self.visit_duration + 90:.0f}s — خروج")
                break
            
            if all_buttons_done and visit_expired:
                print(f"\n✅ اكتمل الوقت + كل الأزرار")
                break
            
            # ═══════════════════════════════════
            # حركة عادية
            # ═══════════════════════════════════
            print(f"🎬 حركة عشوائية...")
            self.do_one_movement()
            
            # فحص X بعد الحركة (اختياري)
            self.close_ad_if_present()
            
            # انتظار قصير بين الحركات
            gap = random.uniform(1.5, 4)
            print(f"⏸️ فاصل {gap:.1f}s")
            time.sleep(gap)
        
        print(f"\n{'=' * 60}")
        print(f"✅ اكتملت الحلقة الديناميكية ({cycle} دورة)")
        print(f"{'=' * 60}\n")
    
    def clean_session(self):
        """تنظيف الجلسة — مع فحص driver"""
        print("🧹 جاري تنظيف الجلسة...")
        
        # فحص: هل driver مغلق؟
        if self.driver is None:
            print("ℹ️ driver مغلق مسبقًا")
            return
        
        try:
            _ = self.driver.current_url
        except Exception:
            print("ℹ️ driver مغلق — تخطي التنظيف")
            return
        
        try:
            self.driver.execute_script("""
                localStorage.clear();
                sessionStorage.clear();
            """)
            
            self.driver.delete_all_cookies()
            
            print("✅ تم تنظيف الجلسة بالكامل")
            
        except Exception as e:
            print(f"⚠️ تحذير في التنظيف: {e}")
    
    def visit_website(self, url, thread_id=0, proxy_url=None, user_buttons=None):
        """زيارة الموقع — thread_id لعرض [T#]، proxy_url للخيط"""
        self.thread_id = thread_id
        self.proxy_url = proxy_url if proxy_url else LOCAL_PROXY
        tag = f"[T{thread_id}] "
        
        # حماية: إن لم تُمرّر أزرار، استخدم قائمة فارغة
        if user_buttons is None:
            user_buttons = []
        """زيارة الموقع مع التنفيذ الذكي للحركات"""
        try:
            print(f"🌐 {tag}جاري زيارة الموقع: {url}")
            
            # 0. التأكد من الخادم المحلي
            if not wait_for_local_bridge():
                raise RuntimeError(
                    "❌ خادم SOCKS5 المحلي لا يعمل على 127.0.0.1:1337\n"
                    "   شغّل socks_bridge.py أولاً في خلية منفصلة."
                )
            print(f"✅ {tag}الخادم المحلي يستجيب")
            
            # 1. البلد الثابت + IP من البروكسي
            self.choose_country_and_ip()
            
            # 2. اختيار الجهاز عشوائياً
            self.choose_random_device()
            
            # 3. إعداد العرض الافتراضي
            self.setup_xvfb_display()
            
            # 5. إعداد المتصفح
            if not self.setup_driver():
                return False
            
            # 6. تحميل السكريبتات المتقدمة
            self.load_advanced_scripts()
            
            # 7. (تخطي setup_cookies — متصفح نظيف)
            #    Adsterra تضع كوكيزها بنفسها عند الزيارة
            
            # 8. زيارة الموقع
            start_time = time.time()
            self.driver.get(url)
            
            # انتظار ثابت 5s مرة واحدة فقط (بدل implicitly_wait)
            print(f"⏳ {tag}انتظار 5s لتحميل العناصر...")
            time.sleep(5)
            
            print(f"✅ {tag}تم تحميل الصفحة بنجاح")
            
            cookie_handled = self.handle_cookie_policy()
            if cookie_handled:
                print("✅ تم قبول سياسة ملفات الارتباط بنجاح")
            else:
                print("ℹ️ لا بانر كوكيز (طبيعي)")
            
            # 🆕 انتظار قصير لـ Adsterra ليضع كوكيزه
            time.sleep(1)
            print("ℹ️ Adsterra ستضع كوكيزها بنفسها (متصفح نظيف)")
                        
            # 9. 🆕 الحلقة الديناميكية — تنسّق الحركات + النقرات
            self.dynamic_visit_loop(user_buttons)
            
            # 10. تنظيف الجلسة بعد الانتهاء
            self.clean_session()
            
            return True
            
        except Exception as e:
            print(f"❌ خطأ في زيارة الموقع: {e}")
            return False
    
    def close(self):
        """إغلاق وحذف — مع timeouts لمنع التعليق"""
        import shutil as _sh
        import threading as _th
        tid = getattr(self, 'thread_id', '?')
        
        # ─────────────────────────────────────
        # 1. driver.quit() في thread مع timeout 10s
        # ─────────────────────────────────────
        if self.driver:
            def _safe_quit():
                try:
                    self.driver.quit()
                except:
                    pass
            
            t_quit = _th.Thread(target=_safe_quit, daemon=True)
            t_quit.start()
            t_quit.join(timeout=10)
            
            if t_quit.is_alive():
                print(f"⚠️ [T{tid}] quit() علق > 10s — نتجاهله")
            else:
                print(f"🔒 [T{tid}] Chrome مغلق")
        
        self.driver = None
        
        # ─────────────────────────────────────
        # 2. pkill (timeout 3s)
        # ─────────────────────────────────────
        try:
            if getattr(self, '_thread_temp_dir', None):
                import subprocess as _sp
                _sp.run(["pkill", "-9", "-f", self._thread_temp_dir],
                        capture_output=True, timeout=3)
        except:
            pass
        
        # ─────────────────────────────────────
        # 3. حذف user-data-dir
        # ─────────────────────────────────────
        try:
            if getattr(self, '_user_data_dir', None) and os.path.exists(self._user_data_dir):
                _sh.rmtree(self._user_data_dir, ignore_errors=True)
                print(f"🗑️  [T{tid}] حُذف profile")
        except:
            pass
        
        # ─────────────────────────────────────
        # 4. حذف temp dir
        # ─────────────────────────────────────
        try:
            if getattr(self, '_thread_temp_dir', None) and os.path.exists(self._thread_temp_dir):
                _sh.rmtree(self._thread_temp_dir, ignore_errors=True)
                print(f"🗑️  [T{tid}] حُذف temp")
        except:
            pass
        
        # ─────────────────────────────────────
        # 5. Xvfb.stop() في thread مع timeout 5s
        # ─────────────────────────────────────
        try:
            if self.display:
                def _safe_stop():
                    try:
                        self.display.stop()
                    except:
                        pass
                
                t_disp = _th.Thread(target=_safe_stop, daemon=True)
                t_disp.start()
                t_disp.join(timeout=5)
                
                self.display = None
                print(f"🔒 [T{tid}] Xvfb مغلق")
        except:
            pass
        
        print(f"✅ [T{tid}] اكتمل الإغلاق")

# 6. التشغيل الرئيسي
def main():
    print("=" * 60)
    print("🚀 المتصفح المتخفي الذكي - نسخة متعددة الخيوط")
    print("=" * 60)
    print(f"🌍 البلد: {TARGET_COUNTRY}")
    print(f"🔀 المنافذ: {LOCAL_PROXY_PORTS}")
    print(f"⚙️  الحد الأقصى للخيوط: {MAX_CONCURRENT_THREADS}")
    print("=" * 60)
    
    TARGET_URL = "https://moho-dhpmsx5n.manus.space"
    
    # ═══════════════════════════════════════════════
    # 1. إدخال الأزرار (مرة واحدة لكل الخيوط)
    # ═══════════════════════════════════════════════
    print("\n" + "=" * 60)
    print("🔘 إعداد الأزرار المشتركة")
    print("=" * 60)
    
    while True:
        try:
            count = int(input("كم عدد الأزرار؟ ").strip())
            if 1 <= count <= 10:
                break
            print("⚠️ العدد بين 1 و 10")
        except ValueError:
            print("⚠️ أدخل رقمًا صحيحًا")
    
    user_buttons = []
    for i in range(1, count + 1):
        while True:
            kw = input(f"اكتب كلمة الزر {i}: ").strip()
            if kw:
                user_buttons.append(kw)
                break
            print("⚠️ الكلمة فارغة")
    
    print(f"✅ الأزرار: {user_buttons}")
    
    # ═══════════════════════════════════════════════
    # 2. إدخال عدد الخيوط
    # ═══════════════════════════════════════════════
    print("\n" + "=" * 60)
    print("🧵 إعداد الخيوط")
    print("=" * 60)
    
    while True:
        try:
            total_threads = int(input("كم عدد الخيوط الكلي؟ ").strip())
            if total_threads >= 1:
                break
            print("⚠️ على الأقل خيط واحد")
        except ValueError:
            print("⚠️ أدخل رقمًا صحيحًا")
    
    print(f"✅ {total_threads} خيط إجمالي")
    print(f"   الحد الأقصى النشط: {MAX_CONCURRENT_THREADS}")
    print(f"   الفاصل بين كل خيط: 2-10s")
    print("=" * 60 + "\n")
    
    # ═══════════════════════════════════════════════
    # 3. نظام إدارة الخيوط
    # ═══════════════════════════════════════════════
    
    queue_lock   = threading.Lock()
    active_lock  = threading.Lock()
    queue        = list(range(total_threads))
    active_count = [0]   # list للسماح بالتعديل داخل الدوال
    results      = {}
    
    def launch_next():
        """يُطلق الخيط التالي إن أمكن"""
        with queue_lock:
            if not queue:
                return False
            idx = queue.pop(0)
        
        with active_lock:
            active_count[0] += 1
        
        t = threading.Thread(
            target=worker,
            args=(idx,),
            daemon=False,
            name=f"T{idx}"
        )
        t.start()
        return True
    
    def worker(idx):
        """الخيط الفعلي"""
        # الفاصل 2-10s (ما عدا أول 6 خيوط)
        # نتحقق: هل هذا الخيط من أول MAX_CONCURRENT_THREADS؟
        # الحل: نمرر is_initial كـ بارامتر
        # سنستخدم منطق: أول 6 خيوط (idx < 6) تبدأ فورًا
        if idx >= MAX_CONCURRENT_THREADS:
            delay = random.uniform(2, 10)
            print(f"⏸️  [T{idx}] انتظار {delay:.1f}s قبل البدء...")
            time.sleep(delay)
        
        proxy_port = LOCAL_PROXY_PORTS[idx % len(LOCAL_PROXY_PORTS)]
        proxy_url  = f"socks5://127.0.0.1:{proxy_port}"
        
        print("\n" + "═" * 60)
        print(f"🌐 [T{idx}] بدء الخيط — منفذ {proxy_port}")
        print("═" * 60)
        
        browser = UltimateStealthBrowser()
        ip_info = None
        success = False
        
        try:
            success = browser.visit_website(
                TARGET_URL,
                thread_id=idx,
                proxy_url=proxy_url,
                user_buttons=user_buttons
            )
            # نحاول استخراج IP من browser
            if hasattr(browser, "selected_ip"):
                ip_info = browser.selected_ip
            results[idx] = {"success": success, "ip": ip_info}
        except RuntimeError as e:
            if "BUTTON_NOT_FOUND" in str(e):
                keyword = str(e).split(":", 1)[1] if ":" in str(e) else "?"
                print(f"\n🛑 [T{idx}] لم يُعثر على الزر: '{keyword}'")
            elif "CLICK_FAILED" in str(e):
                keyword = str(e).split(":", 1)[1] if ":" in str(e) else "?"
                print(f"\n🛑 [T{idx}] فشل النقر على: '{keyword}'")
            else:
                print(f"\n❌ [T{idx}] RuntimeError: {e}")
            results[idx] = {"success": False, "ip": ip_info, "error": str(e)}
        except Exception as e:
            print(f"\n❌ [T{idx}] خطأ عام: {e}")
            results[idx] = {"success": False, "ip": ip_info, "error": str(e)}
        finally:
            try:
                browser.close()
            except:
                pass
            
            print("═" * 60)
            print(f"✅ [T{idx}] انتهى الخيط — IP: {ip_info if ip_info else 'غير معروف'}")
            print("═" * 60 + "\n")
            
            with active_lock:
                active_count[0] -= 1
            
            # أطلق الخيط التالي
            launch_next()
    
    # ═══════════════════════════════════════════════
    # 4. الإطلاق الأولي (6 خيوط تبدأ فورًا)
    # ═══════════════════════════════════════════════
    
    print("🚀 الإطلاق الأولي...")
    for _ in range(min(MAX_CONCURRENT_THREADS, total_threads)):
        launch_next()
    
    # ═══════════════════════════════════════════════
    # 5. انتظار كل الخيوط
    # ═══════════════════════════════════════════════
    
    print("\n⏳ في انتظار انتهاء جميع الخيوط...")
    while True:
        time.sleep(2)
        with queue_lock:
            q_empty = len(queue) == 0
        with active_lock:
            a_count = active_count[0]
        if q_empty and a_count == 0:
            break
    
    # ═══════════════════════════════════════════════
    # 6. الملخص
    # ═══════════════════════════════════════════════
    
    print("\n" + "=" * 60)
    print("📊 الملخص النهائي")
    print("=" * 60)
    
    success_count = sum(1 for r in results.values() if r.get("success"))
    fail_count    = len(results) - success_count
    
    print(f"   نجحت  : {success_count}/{len(results)}")
    print(f"   فشلت  : {fail_count}/{len(results)}")
    print("\n   تفاصيل كل خيط:")
    for idx in sorted(results.keys()):
        r = results[idx]
        status = "✅" if r.get("success") else "❌"
        ip     = r.get("ip", "?")
        print(f"   {status} [T{idx}] IP: {ip}")
    
    print("=" * 60)


if __name__ == "__main__":
    main()