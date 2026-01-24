import re
from pathlib import Path

# Known brands and branded terms to filter out
BRAND_KEYWORDS = {
    # Social Networks
    'instagram', 'snapchat', 'facebook', 'x', 'reddit', 'tiktok', 'tik tok', 'whatsapp', 'youtube', 
    'telegram', 'grindr', 'discord', 'tinder', 'messenger', 'hinge', 'pinterest', 'threads', 'signal',
    'twitter', 'viber', 'line', 'wechat', 'imo', 'bigo', 'badoo', 'match', 'bumble', 'tea app',
    
    # AI/Productivity
    'chatgpt', 'gemini', 'copilot', 'chat gpt', 'grok', 'perplexity', 'claude', 'deepseek',
    'openai', 'sora', 'sora ai', 'character ai', 'chai', 'bard',
    
    # Browsers
    'chrome', 'firefox', 'safari', 'edge', 'opera', 'brave', 'google chrome',
    
    # Email/Communication
    'gmail', 'outlook', 'yahoo mail', 'aol', 'hotmail', 'protonmail',
    
    # Navigation
    'google maps', 'waze', 'apple maps', 'maps', 'google earth',
    
    # Payments/Finance (Company specific)
    'venmo', 'paypal', 'cash app', 'stripe', 'square', 'zelle', 'wise', 'revolut',
    'chase', 'capital one', 'bank of america', 'wells fargo', 'ally', 'citi', 'amex',
    
    # Shopping
    'amazon', 'ebay', 'etsy', 'walmart', 'target', 'shein', 'temu', 'alibaba', 'aliexpress',
    'shopee', 'lazada', 'mercado libre', 'aliexpress', 'wish', 'newegg', 'costco',
    
    # Food Delivery/Restaurants
    'doordash', 'uber eats', 'grubhub', 'deliveroo', 'instacart', 'mcdonalds', 'starbucks',
    'chipotle', 'chick fil a', 'kfc', 'pizza hut', 'dominos', 'subway', 'taco bell',
    
    # Entertainment/Streaming
    'netflix', 'spotify', 'hulu', 'disney+', 'apple tv', 'hbo max', 'prime video', 'youtube tv',
    'twitch', 'crunchyroll', 'disney plus', 'paramount', 'peacock', 'tubi',
    
    # Travel/Ride Sharing
    'uber', 'lyft', 'airbnb', 'booking', 'expedia', 'hotels.com', 'trivago', 'kayak',
    'delta', 'united', 'southwest', 'american airlines',
    
    # Office/Business
    'microsoft', 'excel', 'word', 'powerpoint', 'google docs', 'sheets', 'slack', 'teams',
    'zoom', 'google meet', 'dropbox', 'one drive', 'onedrive',
    
    # Other Company Specific
    'google', 'apple', 'samsung', 'microsoft', 'meta', 'ibm', 'cisco', 'intel',
    'paylocity', 'workday', 'salesforce', 'oracle', 'hubspot', 'stripe', 'twilio',
    'roblox', 'epic games', 'steam', 'playstation', 'xbox', 'nintendo', 'riot games',
    'activision', 'ubisoft', 'ea', 'call of duty', 'fortnite', 'minecraft', 'gta', 'pubg',
}

def load_keywords(filepath):
    """Parse the markdown keyword file."""
    keywords = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip header and empty lines
        if not line or line.startswith('Keyword') or line.startswith('```'):
            i += 1
            continue
        
        # Keyword is on its own line
        keyword = line.lower()
        
        # Next line should have the metadata
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            parts = next_line.split('\t')
            
            # Should have: Genre, Store, Popularity
            if len(parts) >= 3:
                try:
                    genre = parts[0].strip()
                    store = parts[1].strip()
                    popularity = int(parts[2].strip())
                    
                    if keyword and store == "United States":
                        keywords.append({
                            'keyword': keyword,
                            'genre': genre,
                            'popularity': popularity
                        })
                except (ValueError, IndexError):
                    pass
        
        i += 2  # Skip both keyword and metadata lines
    
    return keywords

def is_branded(keyword):
    """Check if keyword is branded."""
    keyword_lower = keyword.lower().strip()
    
    # Exact matches
    if keyword_lower in BRAND_KEYWORDS:
        return True
    
    # Check for brand names as substrings
    for brand in BRAND_KEYWORDS:
        if brand in keyword_lower:
            return True
    
    # Check for app-specific terms
    if any(x in keyword_lower for x in [' app', 'app ', 'driver', 'driver app']):
        # These are often company-specific
        company_terms = ['uber', 'lyft', 'doordash', 'grubhub', 'instacart', 'amazon',
                         'google', 'microsoft', 'apple', 'meta', 'snapchat', 'tiktok',
                         'spotify', 'netflix', 'adobe', 'salesforce']
        if any(term in keyword_lower for term in company_terms):
            return True
    
    # Obvious brand patterns
    if any(keyword_lower.startswith(brand) for brand in ['google', 'microsoft', 'apple', 'meta', 'amazon']):
        return True
    
    return False

def categorize_keywords(keywords):
    """Separate branded and non-branded keywords."""
    branded = []
    non_branded = []
    
    for kw in keywords:
        if is_branded(kw['keyword']):
            branded.append(kw)
        else:
            non_branded.append(kw)
    
    return branded, non_branded

def main():
    # File paths
    script_dir = Path(__file__).parent
    input_file = script_dir.parent / 'public' / 'data' / 'most_searched_keywords_astro.md'
    output_file = script_dir.parent / 'public' / 'data' / 'non_branded_keywords_opportunities.md'
    
    print(f"Loading keywords from {input_file}...")
    keywords = load_keywords(input_file)
    print(f"Total keywords loaded: {len(keywords)}")
    
    print("Categorizing keywords...")
    branded, non_branded = categorize_keywords(keywords)
    
    # Sort by popularity
    non_branded_sorted = sorted(non_branded, key=lambda x: x['popularity'], reverse=True)
    branded_sorted = sorted(branded, key=lambda x: x['popularity'], reverse=True)
    
    print(f"\nBranded keywords: {len(branded)}")
    print(f"Non-branded keywords: {len(non_branded)}")
    
    # Group non-branded by genre
    genre_groups = {}
    for kw in non_branded_sorted:
        genre = kw['genre']
        if genre not in genre_groups:
            genre_groups[genre] = []
        genre_groups[genre].append(kw)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Non-Branded Keywords - iOS App Store Search Opportunities\n\n")
        f.write(f"Generated from Astro Keywords Tool data\n")
        f.write(f"Total non-branded keywords identified: {len(non_branded)}\n")
        f.write(f"Total branded keywords: {len(branded)}\n\n")
        
        f.write("## Summary\n\n")
        f.write("This document isolates **non-branded keywords** from iOS App Store searches, ")
        f.write("representing generic terms users search for without a specific app/company in mind. ")
        f.write("These are high-opportunity keywords for ASO and app discovery.\n\n")
        
        f.write("---\n\n")
        
        # Top 20 overall
        f.write("## Top 20 Non-Branded Keywords (All Genres)\n\n")
        f.write("| Keyword | Genre | Popularity |\n")
        f.write("|---------|-------|------------|\n")
        for kw in non_branded_sorted[:20]:
            f.write(f"| {kw['keyword']} | {kw['genre']} | {kw['popularity']} |\n")
        
        f.write("\n---\n\n")
        
        # By genre
        f.write("## Non-Branded Keywords by Genre\n\n")
        
        # Sort genres by keyword count
        sorted_genres = sorted(genre_groups.items(), key=lambda x: len(x[1]), reverse=True)
        
        for genre, keywords_in_genre in sorted_genres:
            sorted_kw = sorted(keywords_in_genre, key=lambda x: x['popularity'], reverse=True)
            f.write(f"### {genre} ({len(keywords_in_genre)} keywords)\n\n")
            
            # Top 10 for this genre
            f.write(f"**Top 10:**\n\n")
            f.write("| Keyword | Popularity |\n")
            f.write("|---------|------------|\n")
            for kw in sorted_kw[:10]:
                f.write(f"| {kw['keyword']} | {kw['popularity']} |\n")
            
            # All keywords for this genre
            if len(sorted_kw) > 10:
                f.write(f"\n**All {len(sorted_kw)} keywords:**\n\n")
                keywords_text = ", ".join([f"{kw['keyword']} ({kw['popularity']})" for kw in sorted_kw])
                f.write(keywords_text + "\n")
            
            f.write("\n")
        
        # High-opportunity keywords (popularity >= 70)
        f.write("\n---\n\n")
        f.write("## High-Opportunity Keywords (Popularity ≥ 70)\n\n")
        high_opp = [kw for kw in non_branded_sorted if kw['popularity'] >= 70]
        f.write(f"Found {len(high_opp)} keywords with popularity ≥ 70\n\n")
        f.write("| Keyword | Genre | Popularity |\n")
        f.write("|---------|-------|------------|\n")
        for kw in high_opp:
            f.write(f"| {kw['keyword']} | {kw['genre']} | {kw['popularity']} |\n")
        
        # Medium-high opportunities
        f.write("\n---\n\n")
        f.write("## Medium-High Opportunities (Popularity 60-69)\n\n")
        med_high = [kw for kw in non_branded_sorted if 60 <= kw['popularity'] < 70]
        f.write(f"Found {len(med_high)} keywords\n\n")
        f.write("| Keyword | Genre | Popularity |\n")
        f.write("|---------|-------|------------|\n")
        for kw in med_high[:50]:  # Show first 50
            f.write(f"| {kw['keyword']} | {kw['genre']} | {kw['popularity']} |\n")
    
    print(f"\nOutput written to {output_file}")
    
    # Also print some highlights
    print("\n" + "="*60)
    print("TOP 15 NON-BRANDED KEYWORDS BY POPULARITY")
    print("="*60)
    for i, kw in enumerate(non_branded_sorted[:15], 1):
        print(f"{i:2}. {kw['keyword']:30} | {kw['genre']:20} | {kw['popularity']}")
    
    print("\n" + "="*60)
    print("OPPORTUNITIES BY GENRE (Top 5 per genre)")
    print("="*60)
    for genre, keywords_in_genre in sorted_genres[:10]:
        sorted_kw = sorted(keywords_in_genre, key=lambda x: x['popularity'], reverse=True)
        print(f"\n{genre}:")
        for kw in sorted_kw[:5]:
            print(f"  - {kw['keyword']:30} ({kw['popularity']})")

if __name__ == "__main__":
    main()
