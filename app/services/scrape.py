"""
Instagram Selenium Scraper - Function-Based Version
Scrapes multiple hashtags and creates separate CSV files for each
Credentials loaded from .env file
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random
import pandas as pd
from datetime import datetime
import json
import os
from dotenv import load_dotenv
import ollama
from bs4 import BeautifulSoup
from app.utils.cerebras_ai import init_cerebras , process_with_cerebras
from app.db.leads_repo import save_leads
from typing import List

# ============================================================================
# BROWSER SETUP FUNCTIONS
# ============================================================================

def create_chrome_options(headless=False, profile_dir="ig_session"):
    options = Options()

    # Persist session
    options.add_argument(f"--user-data-dir={os.path.abspath(profile_dir)}")

    # Anti-detection
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )

    if headless:
        options.add_argument('--headless=new')

    return options

def reset_session(profile_dir="ig_session"):
    if os.path.exists(profile_dir):
        print("♻️ Resetting corrupted Instagram session")
        import shutil
        shutil.rmtree(profile_dir)

def initialize_driver(headless=False):
    print("🚀 Starting browser with persisted session...")
    options = create_chrome_options(headless=headless)
    driver = webdriver.Chrome(options=options)

    driver.execute_cdp_cmd(
        'Page.addScriptToEvaluateOnNewDocument',
        {'source': "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"}
    )

    return driver


def check_ollama_connection(model_name):
    """Check if Ollama is running and accessible"""
    print(f"🤖 Initializing Ollama with model: {model_name}")
    try:
        ollama.list()
        return True
    except Exception as e:
        print("⚠️  Cannot connect to Ollama! Make sure Ollama is running.")
        print("   Command:  ollama serve")
        print(f"   And pull model:  ollama pull {model_name}")
        return False


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def human_delay(min_sec=2, max_sec=5):
    """Add random human-like delay"""
    time.sleep(random.uniform(min_sec, max_sec))


def slow_type(element, text):
    """Type text slowly to simulate human typing"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))


# ============================================================================
# AUTHENTICATION FUNCTIONS
# ============================================================================


def find_first_element(driver, wait, selectors):
    """Try multiple selectors and return the first that works"""
    for by, value in selectors:
        try:
            return wait.until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            continue
    return None


def click_if_exists(driver, selectors):
    for by, value in selectors:
        try:
            driver.find_element(by, value).click()
            return True
        except:
            continue
    return False


def login_to_instagram(driver, username, password, timeout=15):
    print("📱 Opening Instagram...")
    driver.get("https://www.instagram.com/")
    wait = WebDriverWait(driver, timeout)
    time.sleep(3)

    # -------------------------------
    # 1. Handle cookies (all variants)
    # -------------------------------
    click_if_exists(driver, [
        (By.XPATH, "//button[contains(text(),'Allow')]"),
        (By.XPATH, "//button[contains(text(),'Accept')]"),
        (By.XPATH, "//button[contains(text(),'Only allow essential')]"),
        (By.XPATH, "//button[contains(text(),'Decline')]"),
    ])

    print("🔐 Attempting login...")

    # -------------------------------
    # 2. Username field (fallbacks)
    # -------------------------------
    username_input = find_first_element(driver, wait, [
        (By.NAME, "username"),
        (By.NAME, "email"),
        (By.XPATH, "//input[@aria-label='Phone number, username, or email']"),
        (By.XPATH, "//input[contains(@placeholder,'username')]"),
        (By.XPATH, "//input[contains(@name,'user')]"),
    ])

    if not username_input:
        raise Exception("❌ Username input not found")

    username_input.clear()
    slow_type(username_input, username)
    time.sleep(1)

    # -------------------------------
    # 3. Password field (fallbacks)
    # -------------------------------
    password_input = find_first_element(driver, wait, [
        (By.NAME, "password"),
        (By.NAME, "pass"),
        (By.XPATH, "//input[@aria-label='Password']"),
        (By.XPATH, "//input[@type='password']"),
    ])

    if not password_input:
        raise Exception("❌ Password input not found")

    password_input.clear()
    slow_type(password_input, password)

    # -------------------------------
    # 4. Login button (fallbacks)
    # -------------------------------
    clicked = click_if_exists(driver, [
        (By.XPATH, "//button[@type='submit']"),
        (By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div[1]/div/div[3]/div/div/div/div/div/div/div/div/div[2]/form/div/div[1]/div/div[3]/div/div"),
        (By.XPATH, "//button/div[text()='Log in']/parent::button"),
        (By.XPATH, "//button[contains(text(),'Log in')]"),
    ])

    if not clicked:
        raise Exception("❌ Login button not found")

    # -------------------------------
    # 5. Confirm login success
    # -------------------------------
    try:
        wait.until(
            EC.any_of(
                EC.url_contains("/accounts/"),
                EC.url_contains("/challenge/"),
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']")),
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'/direct')]")),
            )
        )
        print("✅ Login successful!")
        return True

    except TimeoutException:
        print("⚠️ Login may require verification or failed")
        return False


# ============================================================================
# HTML EXTRACTION FUNCTIONS
# ============================================================================

def extract_profile_html(driver, username):
    """Extract HTML content from Instagram profile"""
    try:
        url = f"https://www.instagram.com/{username}/"
        driver.get(url)
        human_delay(3, 5)
        
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "header")))
        
        # Try specific section first, fallback to header
        try:
            section_xpath = "/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div[2]/section/main/div/div/header"
            section_element = wait.until(
                EC.presence_of_element_located((By.XPATH, section_xpath))
            )
            html_content = section_element.get_attribute('innerHTML')
            print(f"  ✓ Extracted HTML for @{username} ({len(html_content)} chars)")
            return html_content
        except:
            header_element = driver.find_element(By.TAG_NAME, "header")
            html_content = header_element.get_attribute('innerHTML')
            print(f"  ✓ Extracted header HTML for @{username} ({len(html_content)} chars)")
            return html_content
            
    except Exception as e:
        print(f"  ✗ Error extracting HTML for {username}: {e}")
        return None


def clean_html_keep_links(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Remove script/style/noscript
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    for tag in soup.find_all(True):
        if tag.name == "a":
            # Keep ONLY href
            href = tag.get("href")
            tag.attrs = {}
            if href:
                tag["href"] = href
        else:
            tag.unwrap()  # remove tag, keep text

    cleaned_html = " ".join(str(soup).split())
    return cleaned_html


# ============================================================================
# AI PROCESSING FUNCTIONS
# ============================================================================

def  process_with_ollama(html_content, username, model_name):
    """Process HTML content with Ollama AI to extract structured data"""
    if not model_name:
        print("  ⚠️  Ollama not available, skipping AI processing")
        return None
    
    time.sleep(2)
    
    try:
        prompt = f"""
Extract Instagram profile information from the text below.

Rules:
- Followers / Following / Posts are numbers
- Bio is all descriptive text
- Website must be a real business website
- Ignore Threads and Instagram internal links
- ONLY extract actual business websites (company websites, e-commerce stores, landing pages, portfolios)
- EXCLUDE all social media links like: Facebook, Twitter/X, LinkedIn, TikTok, YouTube, Pinterest, Snapchat, Telegram, etc.
- INCLUDE WhatsApp links/numbers separately in the "whatsapp" field, NOT in website
- If multiple URLs exist, prioritize the main business website
- Common website patterns: company.com, mybrand.com, shop.example.com, www.business.co

TEXT:
{html_content}

Return ONLY valid JSON:
{{
  "followers_count": number or null,
  "following_count": number or null,
  "posts_count": number or null,
  "bio": string or null,
  "website": string or null,
  "email": string or null,
  "phone": string or null,
  "whatsapp": string or null,
  "is_verified": boolean,
  "is_business": boolean,
  "category": string or null,
  "full_name": string or null
}}
""".strip()

        print(f"  🤖 Processing @{username} with Ollama ({model_name})...")
        
        response = ollama.generate(
            model=model_name,
            prompt=prompt,
            options={
                "temperature": 0.0,
                "num_predict": 800,
            }
        )
        
        response_text = response['response'].strip()
        
        # Clean markdown/code fences
        if response_text.startswith("```"):
            parts = response_text.split("```")
            if len(parts) >= 3:
                response_text = parts[1].strip()
            elif len(parts) == 2:
                response_text = parts[1].strip()
        
        if response_text.lower().startswith("json"):
            response_text = response_text[4:].strip()
        
        extracted_data = json.loads(response_text)
        print(f"  ✓ Ollama extraction successful for @{username}")
        return extracted_data
        
    except json.JSONDecodeError:
        print("  ✗ Invalid JSON returned from Ollama")
        print("   Raw response was:")
        print(response_text[:800] + "..." if len(response_text) > 800 else response_text)
        return None
    except Exception as e:
        print(f"  ✗ Ollama processing error: {e}")
        return None


# ============================================================================
# PROFILE SCRAPING FUNCTIONS
# ============================================================================

def create_profile_data_dict(username, ai_data=None):
    """Create profile data dictionary with safe defaults"""
    profile_data = {
        'username': username,
        'profile_url': f"https://www.instagram.com/{username}/",
        'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    if ai_data:
        followers = ai_data.get('followers_count') or 0
        following = ai_data.get('following_count') or 0
        posts = ai_data.get('posts_count') or 0
        
        profile_data.update({
            'followers': followers,
            'following': following,
            'posts': posts,
            'bio': ai_data.get('bio') or '',
            'website': ai_data.get('website') or '',
            'email': ai_data.get('email') or '',
            'phone': ai_data.get('phone') or '',
            'whatsapp': ai_data.get('whatsapp') or '',
            'is_verified': ai_data.get('is_verified') is True,
            'is_business': ai_data.get('is_business') is True,
            'category': ai_data.get('category') or '',
            'full_name': ai_data.get('full_name') or ''
        })
    else:
        # Fallback defaults
        profile_data.update({
            'followers': 0,
            'following': 0,
            'posts': 0,
            'bio': '',
            'website': '',
            'email': '',
            'phone': '',
            'whatsapp': '',
            'is_verified': False,
            'is_business': False,
            'category': '',
            'full_name': ''
        })
    
    return profile_data


def scrape_profile(driver, username, model, ollama_model):
    """Scrape a single Instagram profile"""
    try:
        print(f"\n📊 Scraping @{username}...")
        
        # Extract HTML
        html_content = extract_profile_html(driver, username)
        if not html_content:
            return None
        
        # Clean HTML
        cleaned_content = clean_html_keep_links(html_content)
        
        if model:
            # Process with Cerebras
            ai_data = process_with_cerebras(cleaned_content, username, model)
        else:
            # Process with AI
            ai_data = process_with_ollama(cleaned_content, username, ollama_model)
        
        # Create profile data
        profile_data = create_profile_data_dict(username, ai_data)
        
        # Print results
        if ai_data:
            print(f"  ✅ @{username}: {profile_data['followers']:,} followers")
            if profile_data['email']:
                print(f"     📧 Email: {profile_data['email']}")
            if profile_data['phone']:
                print(f"     📱 Phone: {profile_data['phone']}")
            if profile_data['whatsapp']:
                print(f"     💬 WhatsApp: {profile_data['whatsapp']}")
        else:
            print(f"  ⚠️ @{username}: No AI data → using defaults")
        
        return profile_data
        
    except Exception as e:
        print(f"  ✗ Error scraping {username}: {e}")
        return None


def scrape_multiple_profiles(driver, usernames, model, ollama_model, delay_range=(5, 10)):
    """Scrape multiple Instagram profiles with delays"""
    results = []
    for username in usernames:
        data = scrape_profile(driver, username, model, ollama_model)
        if data:
            results.append(data)
        time.sleep(random.randint(*delay_range))
    return results


# ============================================================================
# HASHTAG SEARCH FUNCTIONS
# ============================================================================

def scroll_page(driver, scrolls=3):
    """Scroll page multiple times to load more content"""
    for i in range(scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"  📜 Scrolling... ({i+1}/{scrolls})")
        human_delay(2, 3)


def extract_username_from_post(driver):
    """Extract username from opened post modal"""
    try:
        wait = WebDriverWait(driver, 10)
        profile_xpath = (
            "/html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[1]/div/div[1]/span/span/span/div/div/a/div/span"
        )
        
        profile_elem = wait.until(
            EC.presence_of_element_located((By.XPATH, profile_xpath))
        )
        
        username = profile_elem.text.strip()
        print(f"    👤 Extracted username: @{username}")
        return username
    except:
        return None


def close_post_modal(driver):
    """Close the post modal dialog"""
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[6]/div[1]/div/div[2]/div")
            )
        ).click()
        human_delay(2, 3)
        return True
    except:
        try:
            driver.find_element(By.CSS_SELECTOR, "svg[aria-label='Close']").click()
            human_delay(1, 2)
            return True
        except:
            return False


def search_hashtag(driver, hashtag, max_profiles=100):
    """
    Search hashtag and collect EXACT number of unique profile usernames
    (keeps scrolling until max_profiles is reached or content ends)
    """

    print(f"\n🔍 Opening hashtag #{hashtag}")
    driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
    human_delay(4, 6)

    collected_usernames = set()
    collected_posts = set()
    last_height = 0
    attempts_without_new = 0
    MAX_NO_NEW_ATTEMPTS = 5  # safety stop

    wait = WebDriverWait(driver, 10)

    while len(collected_usernames) < max_profiles and attempts_without_new < MAX_NO_NEW_ATTEMPTS:

        # Collect post links
        posts = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
        new_posts_found = False

        for post in posts:
            if len(collected_usernames) >= max_profiles:
                break

            post_link = post.get_attribute("href")
            if not post_link or post_link in collected_posts:
                continue

            collected_posts.add(post_link)
            new_posts_found = True

            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", post)
                human_delay(1, 2)
                post.click()
                human_delay(3, 4)

                username = extract_username_from_post(driver)
                if username:
                    if username not in collected_usernames:
                        collected_usernames.add(username)
                        print(f"  ➕ {len(collected_usernames)}/{max_profiles} → @{username}")

                close_post_modal(driver)

            except Exception:
                close_post_modal(driver)
                continue

        # Scroll more
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        human_delay(3, 5)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height and not new_posts_found:
            attempts_without_new += 1
        else:
            attempts_without_new = 0

        last_height = new_height

    print(f"\n✅ Collected {len(collected_usernames)} unique profiles for #{hashtag}")
    return list(collected_usernames)[:max_profiles]


# ============================================================================
# DATA EXPORT FUNCTIONS
# ============================================================================

def calculate_summary_stats(data):
    """Calculate summary statistics from scraped data"""
    with_email = sum(1 for d in data if d.get('email'))
    with_phone = sum(1 for d in data if d.get('phone'))
    with_whatsapp = sum(1 for d in data if d.get('whatsapp'))
    
    return {
        'total': len(data),
        'with_email': with_email,
        'with_phone': with_phone,
        'with_whatsapp': with_whatsapp
    }


def save_results(data, filename_prefix):
    """Save scraped data to CSV and JSON files"""
    
    # Save JSON
    json_filename = f"{filename_prefix}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved JSON: {json_filename}")
    
    # Print summary
    stats = calculate_summary_stats(data)
    print(f"\n📊 Summary:")
    print(f"   Total profiles: {stats['total']}")
    print(f"   With email: {stats['with_email']}")
    print(f"   With phone: {stats['with_phone']}")
    print(f"   With WhatsApp: {stats['with_whatsapp']}")


# ============================================================================
# CONFIGURATION FUNCTIONS
# ============================================================================

def load_configuration():
    """Load configuration from .env file at project root"""
    load_dotenv()  # auto-loads .env from project root

    config = {
        'ollama_model': os.getenv('OLLAMA_MODEL', 'qwen2.5:3b'),
        'instagram_username': os.getenv('INSTAGRAM_USERNAME'),
        'instagram_password': os.getenv('INSTAGRAM_PASSWORD'),
        'max_profiles': int(os.getenv('MAX_PROFILES', '20')),
        'headless': os.getenv('HEADLESS', 'false').lower() == 'true'
    }

    return config

def print_configuration(config):
    """Print loaded configuration"""
    print(f"📋 Configuration loaded from .env:")
    print(f"   Instagram User: {config['instagram_username']}")
    print(f"   Ollama model:   {config['ollama_model']}")
    print(f"   Max Profiles:    {config['max_profiles']}")
    print(f"   Headless:        {config['headless']}")
    print()


def validate_configuration(config):
    """Validate required configuration values"""
    if not config['instagram_username'] or not config['instagram_password']:
        print("❌ Instagram credentials not found in .env file")
        return False
    return True


# ============================================================================
# MAIN WORKFLOW FUNCTIONS
# ============================================================================

def process_single_hashtag(driver, hashtag, max_profiles, model, ollama_model):
    """Process a single hashtag: search and scrape profiles"""
    usernames = search_hashtag(driver, hashtag, max_profiles)
    print(f"\n✅ Found {len(usernames)} profiles under #{hashtag}")
    
    if not usernames:
        return None
    
    results = scrape_multiple_profiles(driver, usernames,model, ollama_model)
    
    if results:
        return results
    
    return None

def process_all_hashtags(driver, hashtags, max_profiles, model, ollama_model):
    """Process all hashtags sequentially and aggregate results"""
    
    all_results = []
    hashtag_summary = {}
    
    for idx, hashtag in enumerate(hashtags, 1):
        print(f"\n{'='*60}")
        print(f"🏷️  Processing Hashtag {idx}/{len(hashtags)}: #{hashtag}")
        print(f"{'='*60}")
        
        result = process_single_hashtag(driver, hashtag, max_profiles, model, ollama_model)
        
        if result:
            # Add hashtag field to each profile
            for profile in result:
                profile['source_hashtag'] = hashtag
            
            all_results.extend(result)
            hashtag_summary[hashtag] = len(result)
            print(f"✅ Collected {len(result)} profiles from #{hashtag}")
        else:
            print(f"⚠️ No results from #{hashtag}")
            hashtag_summary[hashtag] = 0
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"📊 PROCESSING COMPLETE")
    print(f"{'='*60}")
    for tag, count in hashtag_summary.items():
        print(f"  #{tag}: {count} profiles")
    print(f"\n  Total profiles: {len(all_results)}")
    
    return all_results if all_results else None


def print_final_summary(hashtags, total_profiles, results):
    """Print final summary of all operations"""
    print(f"\n{'='*60}")
    print(f"🎉 ALL HASHTAGS COMPLETED!")
    print(f"{'='*60}")
    print(f"\n📊 Final Summary:")
    print(f"   Total hashtags processed: {len(hashtags)}")
    print(f"   Total profiles scraped: {total_profiles}")
    print(f"\n📁 Files created:")
    for hashtag, info in results.items():
        print(f"   #{hashtag}: {info['count']} profiles → {info['filename']}")

def is_logged_in(driver, timeout=10) -> bool:
    driver.get("https://www.instagram.com/")
    human_delay(3, 5)

    wait = WebDriverWait(driver, timeout)

    # 1️⃣ Hard fail: login form exists
    try:
        driver.find_element(By.NAME, "username")
        print("🔐 Login form detected → NOT logged in")
        return False
    except NoSuchElementException:
        pass

    # 2️⃣ Logged-in indicators (ANY one is enough)
    logged_in_indicators = [
        (By.XPATH, "//a[contains(@href,'/direct')]"),      # DM icon
        (By.XPATH, "//svg[@aria-label='New post']"),       # + create
        (By.XPATH, "//input[@placeholder='Search']"),     # search bar
        (By.XPATH, "//img[contains(@alt,'profile')]"),    # avatar
    ]

    for by, xpath in logged_in_indicators:
        try:
            wait.until(EC.presence_of_element_located((by, xpath)))
            print("✅ Logged-in UI detected")
            return True
        except TimeoutException:
            continue

    # 3️⃣ Challenge / verification
    if "challenge" in driver.current_url:
        print("⚠️ Instagram challenge page detected")
        return False

    print("❌ Unable to confirm login → treating as logged out")
    return False

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def scrape(hashtags: list,max_profiles: int =10):
    config = load_configuration()

    if not validate_configuration(config):
        return

    print_configuration(config)

    model = init_cerebras()
    
    ollama_available = check_ollama_connection(config['ollama_model'])
    ollama_model = config['ollama_model'] if ollama_available else None

    driver = initialize_driver(config['headless'])

    try:
        if not is_logged_in(driver):
            login_to_instagram(
                driver,
                username=config['instagram_username'],
                password=config['instagram_password']
            )

        results = process_all_hashtags(
            driver,
            hashtags,
            max_profiles or config['max_profiles'],
            model,
            ollama_model
        )

        return results

    finally:
        print("\n🔴 Closing browser...")
        driver.quit()


def run_scrape_job(hashtags: List[str], max_profiles: int):
    print("🟢 Background scraping started")

    try:
        results = scrape(hashtags, max_profiles)

        if results:
            print(f"✅ Scraping completed. Total leads: {len(results)}")
            save_leads(results)
            print("💾 Leads saved successfully")
        else:
            print("⚠️ No leads found")

    except Exception as e:
        print(f"❌ Background scrape failed: {e}")