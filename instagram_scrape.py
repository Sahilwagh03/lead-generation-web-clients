"""
Instagram Selenium Scraper - Multi-Hashtag Version (Ollama/Qwen version)
Scrapes multiple hashtags and creates separate CSV files for each
Credentials loaded from .env file

Fixed: NoneType formatting error when followers/following/posts are null
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
import ollama           # pip install ollama
from bs4 import BeautifulSoup

class InstagramSeleniumScraper:
    def __init__(self, headless=False, ollama_model="qwen2.5:14b"):
        """
        Initialize Selenium WebDriver and Ollama (local Qwen)
        """
        self.options = Options()
        
        # Anti-detection settings
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--window-size=1920,1080')
        self.options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        if headless:
            self.options.add_argument('--headless')
        
        print("🚀 Starting browser...")
        self.driver = webdriver.Chrome(options=self.options)
        
        self.driver.execute_cdp_cmd(
            'Page.addScriptToEvaluateOnNewDocument',
            {'source': "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"}
        )
        
        self.wait = WebDriverWait(self.driver, 10)
        self.logged_in = False
        
        # Initialize Ollama
        print(f"🤖 Initializing Ollama with model: {ollama_model}")
        try:
            ollama.list()  # simple check if ollama is running
            self.ollama_model = ollama_model
        except Exception as e:
            print("⚠️  Cannot connect to Ollama! Make sure Ollama is running.")
            print("   Command:  ollama serve")
            print("   And pull model:  ollama pull qwen2.5:14b  (or your preferred size)")
            self.ollama_model = None
    
    
    def human_delay(self, min_sec=2, max_sec=5):
        time.sleep(random.uniform(min_sec, max_sec))
    
    
    def slow_type(self, element, text):
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
    
    
    def login(self, username, password):
        try:
            print("📱 Opening Instagram...")
            self.driver.get("https://www.instagram.com/")
            self.human_delay(3, 5)
            
            try:
                self.driver.find_element(
                    By.XPATH, "//button[contains(text(), 'Allow') or contains(text(), 'Accept')]"
                ).click()
            except:
                pass
            
            print("🔐 Logging in...")
            
            username_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            self.slow_type(username_input, username)
            self.human_delay(1, 2)
            
            password_input = self.driver.find_element(By.NAME, "password")
            self.slow_type(password_input, password)
            self.human_delay(1, 2)
            
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
            self.human_delay(5, 8)
            
            self.logged_in = True
            print("✅ Login successful!")
            return True
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
    
    
    def extract_profile_html(self, username):
        try:
            url = f"https://www.instagram.com/{username}/"
            self.driver.get(url)
            self.human_delay(3, 5)
            
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "header")))
            
            try:
                section_xpath = "/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div[2]/section/main/div/div/header"
                section_element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, section_xpath))
                )
                html_content = section_element.get_attribute('innerHTML')
                print(f"  ✓ Extracted HTML for @{username} ({len(html_content)} chars)")
                return html_content
            except:
                header_element = self.driver.find_element(By.TAG_NAME, "header")
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
                tag.attrs = {}              # remove all attributes
                if href:
                    tag["href"] = href
            else:
                tag.unwrap()  # remove tag, keep text

        cleaned_html = " ".join(str(soup).split())
        return cleaned_html

    def process_with_ollama(self, html_content, username):
        print(f"  🤖 Sending htmlcontent to Ollama for {html_content}")
        if not self.ollama_model:
            print("  ⚠️  Ollama not available, skipping AI processing")
            return None
        
        time.sleep(2)
        
        try:
            prompt = f"""
Analyze this Instagram profile HTML and extract the following information in JSON format.
Be precise and extract ONLY what you can find in the HTML. If something is not found, use null.

IMPORTANT RULES FOR WEBSITE EXTRACTION:
- ONLY extract actual business websites (company websites, e-commerce stores, landing pages, portfolios)
- EXCLUDE all social media links like: Facebook, Twitter/X, LinkedIn, TikTok, YouTube, Pinterest, Snapchat, Telegram, etc.
- INCLUDE WhatsApp links/numbers separately in the "whatsapp" field, NOT in website
- If multiple URLs exist, prioritize the main business website
- Common website patterns: company.com, mybrand.com, shop.example.com, www.business.co

Extract:
1. followers_count: Number of followers (convert K→1000, M→1000000, B→1000000000)
2. following_count: Number of accounts following
3. posts_count: Number of posts
4. bio: Profile biography text (full text, not truncated)
5. website: ONLY actual business website URLs (NO social media)
6. email: Any email address found in bio or profile
7. phone: Any phone number found (include country code if visible)
8. whatsapp: ONLY WhatsApp links or numbers (wa.me links, WhatsApp Business numbers)
9. is_verified: true/false if verified badge/checkmark is present
10. is_business: true/false if business/professional/creator account
11. category: Business category if present (e.g., "Digital Marketing Agency", "Fashion Brand")
12. full_name: Display name/full name shown on profile

HTML Content (truncated if too long):
{html_content}

Return ONLY valid JSON, no other text, no explanation, no markdown.
Use this exact structure:

{{
  "followers_count": number or null,
  "following_count": number or null,
  "posts_count": number or null,
  "bio": "text" or null,
  "website": "url" or null,
  "email": "email" or null,
  "phone": "number" or null,
  "whatsapp": "number/link" or null,
  "is_verified": boolean,
  "is_business": boolean,
  "category": "text" or null,
  "full_name": "text" or null
}}
""".strip()

            print(f"  🤖 Processing @{username} with Ollama ({self.ollama_model})...")
            
            response = ollama.generate(
                model=self.ollama_model,
                prompt=prompt,
                options={
                    "temperature": 0.0,
                    "num_predict": 800,
                }
            )
            
            response_text = response['response'].strip()
            
            # Clean possible markdown / code fences
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
    
    
    def scrape_profile(self, username):
        try:
            print(f"\n📊 Scraping @{username}...")
            
            html_content = self.extract_profile_html(username)
            content = self.clean_html_keep_links(html_content)
            if not html_content:
                return None
            
            ai_data = self.process_with_ollama(content, username)
            
            profile_data = {
                'username': username,
                'profile_url': f"https://www.instagram.com/{username}/",
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            if ai_data:
                # Safe defaults for all fields
                followers = ai_data.get('followers_count') or 0
                following = ai_data.get('following_count') or 0
                posts     = ai_data.get('posts_count')     or 0
                
                profile_data.update({
                    'followers':   followers,
                    'following':   following,
                    'posts':       posts,
                    'bio':         ai_data.get('bio')          or '',
                    'website':     ai_data.get('website')      or '',
                    'email':       ai_data.get('email')        or '',
                    'phone':       ai_data.get('phone')        or '',
                    'whatsapp':    ai_data.get('whatsapp')     or '',
                    'is_verified': ai_data.get('is_verified')  is True,
                    'is_business': ai_data.get('is_business')  is True,
                    'category':    ai_data.get('category')     or '',
                    'full_name':   ai_data.get('full_name')    or ''
                })
                
                # Now safe to format with thousands separator
                print(f"  ✅ @{username}: {followers:,} followers")
                if profile_data['email']:
                    print(f"     📧 Email: {profile_data['email']}")
                if profile_data['phone']:
                    print(f"     📱 Phone: {profile_data['phone']}")
                if profile_data['whatsapp']:
                    print(f"     💬 WhatsApp: {profile_data['whatsapp']}")
            else:
                # Fallback when AI completely failed
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
                print(f"  ⚠️ @{username}: No AI data → using defaults")
            
            return profile_data
            
        except Exception as e:
            print(f"  ✗ Error scraping {username}: {e}")
            return None
    
    
    def scroll_page(self, scrolls=3):
        for i in range(scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"  📜 Scrolling... ({i+1}/{scrolls})")
            self.human_delay(2, 3)
    
    
    def search_hashtag(self, hashtag, max_profiles=20):
        try:
            print(f"\n🔍 Opening hashtag #{hashtag}")
            self.driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
            self.human_delay(4, 6)
            
            scrolls_needed = max(2, (max_profiles // 9) + 1)
            print(f"📊 Need to collect {max_profiles} profiles, performing {scrolls_needed} scrolls...")
            
            self.scroll_page(scrolls_needed)
            
            profile_links = []
            attempted_posts = 0
            max_attempts = max_profiles * 3

            for j in range(1, 20):
                if len(profile_links) >= max_profiles:
                    break
                    
                for i in range(1, 4):
                    if len(profile_links) >= max_profiles or attempted_posts >= max_attempts:
                        break
                    
                    attempted_posts += 1
                    
                    try:
                        post_xpath = (
                            f"/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/"
                            f"section/main/div/div[2]/div[1]/div/div[{j}]/div[{i}]"
                        )
                        
                        try:
                            post = self.driver.find_element(By.XPATH, post_xpath)
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", post)
                            self.human_delay(1, 2)
                        except:
                            continue
                        
                        post = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, post_xpath))
                        )
                        post.click()
                        self.human_delay(3, 4)

                        profile_xpath = (
                            "/html/body/div[6]/div[1]/div/div[3]/div/div/div/div/"
                            "div[2]/div/article/div/div[2]/div/div/div[1]/"
                            "div/header/div[2]/div[1]/div[1]/div/div[1]/span/span/span/div/div/a"
                        )

                        profile_elem = self.wait.until(
                            EC.presence_of_element_located((By.XPATH, profile_xpath))
                        )

                        profile_url = profile_elem.get_attribute("href")
                        username = profile_url.rstrip('/').split('/')[-1]
                        
                        if username not in profile_links:
                            profile_links.append(username)
                            print(f"  ➕ Found profile #{len(profile_links)}: @{username}")
                        
                        self.wait.until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "/html/body/div[6]/div[1]/div/div[2]/div")
                            )
                        ).click()
                        self.human_delay(2, 3)

                    except Exception as e:
                        try:
                            self.driver.find_element(
                                By.CSS_SELECTOR, "svg[aria-label='Close']"
                            ).click()
                            self.human_delay(1, 2)
                        except:
                            pass
                        continue

            print(f"✅ Collected {len(profile_links)} unique profiles (attempted {attempted_posts} posts)")
            return profile_links[:max_profiles]

        except Exception as e:
            print(f"❌ Error in hashtag processing: {e}")
            return []
    
    
    def scrape_multiple(self, usernames, delay_range=(5, 10)):
        results = []
        for username in usernames:
            data = self.scrape_profile(username)
            if data:
                results.append(data)
            time.sleep(random.randint(*delay_range))
        return results
    
    
    def save_results(self, data, filename_prefix):
        csv_filename = f"{filename_prefix}.csv"
        df = pd.DataFrame(data)
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        print(f"\n✅ Saved CSV: {csv_filename}")
        
        json_filename = f"{filename_prefix}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved JSON: {json_filename}")
        
        with_email = sum(1 for d in data if d.get('email'))
        with_phone = sum(1 for d in data if d.get('phone'))
        with_whatsapp = sum(1 for d in data if d.get('whatsapp'))
        
        print(f"\n📊 Summary:")
        print(f"   Total profiles: {len(data)}")
        print(f"   With email: {with_email}")
        print(f"   With phone: {with_phone}")
        print(f"   With WhatsApp: {with_whatsapp}")
    
    
    def close(self):
        print("\n🔴 Closing browser...")
        self.driver.quit()


def main():
    load_dotenv()
    
    ollama_model = os.getenv('OLLAMA_MODEL', 'qwen2.5:14b')
    instagram_username = os.getenv('INSTAGRAM_USERNAME')
    instagram_password = os.getenv('INSTAGRAM_PASSWORD')
    
    hashtags_str = os.getenv('HASHTAGS', 'marketing,business,startup')
    hashtags = [tag.strip() for tag in hashtags_str.split(',')]
    
    max_profiles = int(os.getenv('MAX_PROFILES', '20'))
    headless_mode = os.getenv('HEADLESS', 'false').lower() == 'true'
    
    if not instagram_username or not instagram_password:
        print("❌ Instagram credentials not found in .env file")
        return
    
    print(f"📋 Configuration loaded from .env:")
    print(f"   Instagram User: {instagram_username}")
    print(f"   Ollama model:   {ollama_model}")
    print(f"   Hashtags:        {', '.join(['#' + tag for tag in hashtags])}")
    print(f"   Max Profiles:    {max_profiles}")
    print(f"   Headless:        {headless_mode}")
    print()
    
    scraper = InstagramSeleniumScraper(
        headless=headless_mode,
        ollama_model=ollama_model
    )

    if not scraper.login(instagram_username, instagram_password):
        scraper.close()
        return
    
    total_profiles_scraped = 0
    all_hashtag_results = {}
    
    for idx, hashtag in enumerate(hashtags, 1):
        print(f"\n{'='*60}")
        print(f"🏷️  Processing Hashtag {idx}/{len(hashtags)}: #{hashtag}")
        print(f"{'='*60}")
        
        usernames = scraper.search_hashtag(hashtag, max_profiles)
        print(f"\n✅ Found {len(usernames)} profiles under #{hashtag}")
        
        if usernames:
            results = scraper.scrape_multiple(usernames)

            if results:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename_prefix = f"instagram_leads_{hashtag}_{timestamp}"
                
                scraper.save_results(results, filename_prefix)
                
                total_profiles_scraped += len(results)
                all_hashtag_results[hashtag] = {
                    'count': len(results),
                    'filename': f"{filename_prefix}.csv"
                }
        
        if idx < len(hashtags):
            wait_time = random.randint(10, 20)
            print(f"\n⏳ Waiting {wait_time} seconds before next hashtag...")
            time.sleep(wait_time)
    
    print(f"\n{'='*60}")
    print(f"🎉 ALL HASHTAGS COMPLETED!")
    print(f"{'='*60}")
    print(f"\n📊 Final Summary:")
    print(f"   Total hashtags processed: {len(hashtags)}")
    print(f"   Total profiles scraped: {total_profiles_scraped}")
    print(f"\n📁 Files created:")
    for hashtag, info in all_hashtag_results.items():
        print(f"   #{hashtag}: {info['count']} profiles → {info['filename']}")

    scraper.close()


if __name__ == "__main__":
    main()