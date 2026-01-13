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
from app.utils.gemini import init_gemini , process_with_gemini

# ============================================================================
# BROWSER SETUP FUNCTIONS
# ============================================================================

def create_chrome_options(headless=False):
    """Create and configure Chrome options for anti-detection"""
    options = Options()
    
    # Anti-detection settings
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    
    if headless:
        options.add_argument('--headless')
    
    return options


def initialize_driver(headless=False):
    """Initialize Selenium WebDriver with anti-detection measures"""
    print("🚀 Starting browser...")
    options = create_chrome_options(headless)
    driver = webdriver.Chrome(options=options)
    
    # Remove webdriver property
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

def login_to_instagram(driver, username, password):
    """Login to Instagram with given credentials"""
    try:
        print("📱 Opening Instagram...")
        driver.get("https://www.instagram.com/")
        human_delay(3, 5)
        
        # Handle cookie consent if present
        try:
            driver.find_element(
                By.XPATH, "//button[contains(text(), 'Allow') or contains(text(), 'Accept')]"
            ).click()
        except:
            pass
        
        print("🔐 Logging in...")
        wait = WebDriverWait(driver, 10)
        
        # Enter username
        username_input = wait.until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        slow_type(username_input, username)
        human_delay(1, 2)
        
        # Enter password
        password_input = driver.find_element(By.NAME, "password")
        slow_type(password_input, password)
        human_delay(1, 2)
        
        # Submit login
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        human_delay(5, 8)
        
        print("✅ Login successful!")
        return True
        
    except Exception as e:
        print(f"❌ Login failed: {e}")
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


def scrape_profile(driver, username, gemini_model, ollama_model):
    """Scrape a single Instagram profile"""
    try:
        print(f"\n📊 Scraping @{username}...")
        
        # Extract HTML
        html_content = extract_profile_html(driver, username)
        if not html_content:
            return None
        
        # Clean HTML
        cleaned_content = clean_html_keep_links(html_content)
        
        if gemini_model:
            # Process with Gemini
            ai_data = process_with_gemini(cleaned_content, username, gemini_model)
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


def scrape_multiple_profiles(driver, usernames, gemini_model, ollama_model, delay_range=(5, 10)):
    """Scrape multiple Instagram profiles with delays"""
    results = []
    for username in usernames:
        data = scrape_profile(driver, username, gemini_model, ollama_model)
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
            "/html/body/div[6]/div[1]/div/div[3]/div/div/div/div/"
            "div[2]/div/article/div/div[2]/div/div/div[1]/"
            "div/header/div[2]/div[1]/div[1]/div/div[1]/span/span/span/div/div/a"
        )
        
        profile_elem = wait.until(
            EC.presence_of_element_located((By.XPATH, profile_xpath))
        )
        
        profile_url = profile_elem.get_attribute("href")
        username = profile_url.rstrip('/').split('/')[-1]
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


def search_hashtag(driver, hashtag, max_profiles=20):
    """Search hashtag and collect profile usernames"""
    try:
        print(f"\n🔍 Opening hashtag #{hashtag}")
        driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
        human_delay(4, 6)
        
        scrolls_needed = max(2, (max_profiles // 9) + 1)
        print(f"📊 Need to collect {max_profiles} profiles, performing {scrolls_needed} scrolls...")
        
        scroll_page(driver, scrolls_needed)
        
        profile_links = []
        attempted_posts = 0
        max_attempts = max_profiles * 3
        wait = WebDriverWait(driver, 10)

        for row in range(1, 20):
            if len(profile_links) >= max_profiles:
                break
                
            for col in range(1, 4):
                if len(profile_links) >= max_profiles or attempted_posts >= max_attempts:
                    break
                
                attempted_posts += 1
                
                try:
                    post_xpath = (
                        f"/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/"
                        f"section/main/div/div[2]/div[1]/div/div[{row}]/div[{col}]"
                    )
                    
                    # Scroll to post
                    try:
                        post = driver.find_element(By.XPATH, post_xpath)
                        driver.execute_script("arguments[0].scrollIntoView(true);", post)
                        human_delay(1, 2)
                    except:
                        continue
                    
                    # Click post
                    post = wait.until(EC.element_to_be_clickable((By.XPATH, post_xpath)))
                    post.click()
                    human_delay(3, 4)

                    # Extract username
                    username = extract_username_from_post(driver)
                    
                    if username and username not in profile_links:
                        profile_links.append(username)
                        print(f"  ➕ Found profile #{len(profile_links)}: @{username}")
                    
                    # Close modal
                    close_post_modal(driver)

                except Exception as e:
                    close_post_modal(driver)
                    continue

        print(f"✅ Collected {len(profile_links)} unique profiles (attempted {attempted_posts} posts)")
        return profile_links[:max_profiles]

    except Exception as e:
        print(f"❌ Error in hashtag processing: {e}")
        return []


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
    # Get project root reliably (two levels up from this file)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))

    env_path = os.path.join(project_root, '.env')
    print(f"📄 Loading .env from: {env_path}")  # debug

    if not os.path.exists(env_path):
        print("❌ .env file not found at project root!")
    
    load_dotenv(dotenv_path=env_path)

    config = {
        'ollama_model': os.getenv('OLLAMA_MODEL', 'qwen2.5:14b'),
        'instagram_username': os.getenv('INSTAGRAM_USERNAME'),
        'instagram_password': os.getenv('INSTAGRAM_PASSWORD'),
        'max_profiles': int(os.getenv('MAX_PROFILES', '20')),
        'headless': os.getenv('HEADLESS', 'false').lower() == 'true'
    }

    # Debug: print what was loaded
    print(f"🔑 Instagram username: {config['instagram_username']}")
    print(f"🤖 Ollama model: {config['ollama_model']}")
    print(f"🖥️ Headless: {config['headless']}")
    print(f"📄 Max profiles: {config['max_profiles']}")
    
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

def process_single_hashtag(driver, hashtag, max_profiles, gemini_model, ollama_model):
    """Process a single hashtag: search and scrape profiles"""
    usernames = search_hashtag(driver, hashtag, max_profiles)
    print(f"\n✅ Found {len(usernames)} profiles under #{hashtag}")
    
    if not usernames:
        return None
    
    results = scrape_multiple_profiles(driver, usernames,gemini_model, ollama_model)
    
    if results:
        return results
    
    return None


def process_all_hashtags(driver, hashtags, max_profiles, gemini_model, ollama_model):
    """Process all hashtags sequentially"""
    
    for idx, hashtag in enumerate(hashtags, 1):
        print(f"\n{'='*60}")
        print(f"🏷️  Processing Hashtag {idx}/{len(hashtags)}: #{hashtag}")
        print(f"{'='*60}")
        
        result = process_single_hashtag(driver, hashtag, max_profiles,gemini_model, ollama_model)
        
        if result:
            return result
    
    return None


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


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def scrape(hashtags: list):
    """Main execution function"""
    # Load and validate configuration
    config = load_configuration()
    
    if not validate_configuration(config):
        return
    
    print_configuration(config)

    gemini_model = init_gemini()
    
    # Check Ollama connection
    ollama_available = check_ollama_connection(config['ollama_model'])
    ollama_model = config['ollama_model'] if ollama_available else None
    
    # Initialize browser
    driver = initialize_driver(config['headless'])
    
    try:
        # Login to Instagram
        if not login_to_instagram(driver, config['instagram_username'], config['instagram_password']):
            return
        
        # Process all hashtags
        results = process_all_hashtags(
            driver,
            hashtags,
            config['max_profiles'],
            gemini_model,
            ollama_model
        )
        
        return results
        
    finally:
        # Clean up
        print("\n🔴 Closing browser...")
        driver.quit()


if __name__ == "__main__":
    scrape(hashtags=["nature", "travel", "food"])