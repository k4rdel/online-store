import requests
from app import app, db, Product, Category

API_KEY = 'C7FE564950F84CA2A64CE37CBF608D2D'
CATEGORY_MAP = {
    "Motherboards": 1,
    "GPU": 2,
    "Hard disks": 3,
    "Computer cases": 4
}

def seed_products_from_rainforest():
    for label, cat_id in CATEGORY_MAP.items():
        print(f"Pobieranie produktów dla kategorii: {label}...")
        
        params = {
            'api_key': API_KEY,
            'type': 'search',
            'amazon_domain': 'amazon.com',
            'search_term': label # Możesz tu dopisać np. label + " gaming"
        }

        response = requests.get('https://api.rainforestapi.com/request', params=params)
        
        if response.status_code == 200:
            results = response.json().get('search_results', [])[:5] # Bierzemy 5 sztuk
            
            for item in results:
                # Wyciąganie ceny (Rainforest podaje 'value' jako float w pod-słowniku price)
                raw_price = item.get('price', {}).get('value', 0.0)
                
                # Skracamy opis/nazwę, żeby pasowała do Twojego db.String(100/200)
                name = item.get('title', 'No Name')[:100]
                # Rainforest w 'search' nie daje pełnego opisu, użyjemy ASIN lub krótkiej notki
                desc = f"Amazon ASIN: {item.get('asin')} - High quality {label}"[:200]
                
                new_product = Product(
                    name=name,
                    description=desc,
                    price=float(raw_price),
                    image_url=item.get('image', ''),
                    category_id=cat_id
                )
                
                db.session.add(new_product)
            
            db.session.commit()
            print(f"Dodano 5 produktów do kategorii {label}.")
        else:
            print(f"Błąd API dla {label}: {response.status_code}")

with app.app_context():
    seed_products_from_rainforest() 