import requests
import mysql.connector
from datetime import datetime


def getToday():
    today = datetime.now()
    return today


def lambda_handler(event, context):
    # Fetching data from the API
    api_url = "https://apis.zigbang.com/apt/locals/prices/on-danjis?minPynArea=10%ED%8F%89%EC%9D%B4%ED%95%98&maxPynArea=60%ED%8F%89%EB%8C%80%EC%9D%B4%EC%83%81&geohash=0nYddK2EzyUOdQr3kMLaOiWukIIB71ZDHJxXU%2BntxMA%3D"

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        print(data)
        apartments = data.get('filtered', [])

        # Connecting to MariaDB
        conn = mysql.connector.connect(
            host="YOUR_RDS_ENDPOINT",
            user="YOUR_RDS_USERNAME",
            port="3306",
            password="YOUR_USER_PASSWORD",
            database="pipelinedb"
        )

        # Creating a cursor object
        cursor = conn.cursor()

        # Inserting data into MariaDB
        for json_data in apartments:
            try:
                # Print the entire data
                print(json_data)

                sales_data = json_data.get('price', {}).get('sales', {})

                insert_data = {
                    'id': json_data['id'],
                    'name': json_data['name'],
                    'lat': json_data['lat'],
                    'lng': json_data['lng'],
                    'total_units': json_data.get('총세대수'),
                    'approval_date': json_data.get('사용승인일'),
                    'service_type': json_data.get('서비스구분'),
                    'real_type': json_data.get('real_type'),
                    'sido': json_data.get('sido'),
                    'gugun': json_data.get('gugun'),
                    'dong': json_data.get('dong'),
                    'image_url': json_data.get('image'),
                    'is_after_prefunding': json_data.get('is후분양'),
                    'min_sales_price': sales_data.get('min'),
                    'max_sales_price': sales_data.get('max'),
                    'avg_sales_price': sales_data.get('avg'),
                    'price_per_area': sales_data.get('perArea')
                }

                # SQL query
                sql = """
                    INSERT INTO apart_sales_info (
                        id, name, lat, lng, total_units, approval_date, service_type,
                        real_type, sido, gugun, dong, image_url, is_after_prefunding,
                        min_sales_price, max_sales_price, avg_sales_price, price_per_area
                    ) VALUES (
                        %(id)s, %(name)s, %(lat)s, %(lng)s, %(total_units)s, %(approval_date)s,
                        %(service_type)s, %(real_type)s, %(sido)s, %(gugun)s, %(dong)s,
                        %(image_url)s, %(is_after_prefunding)s, %(min_sales_price)s,
                        %(max_sales_price)s, %(avg_sales_price)s, %(price_per_area)s
                    )
                """

                # Execute SQL
                cursor.execute(sql, insert_data)
                conn.commit()

            except Exception as e:
                print(f"Error processing data: {e}")
                continue

        # Close database connection
        cursor.close()
        conn.close()

    else:
        print("Failed to fetch data from the API")
