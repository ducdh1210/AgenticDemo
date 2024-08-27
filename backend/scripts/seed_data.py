from datetime import datetime, timedelta

from sqlmodel import Session, create_engine

from backend.config import CONNECTION_STRING
from backend.schema.recommendation import Item, PurchaseHistory, User

engine = create_engine(CONNECTION_STRING)


def seed_data():
    with Session(engine) as session:
        # Create Users
        john = User(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone_number="1234567890",
            address="123 Main St",
        )
        mary = User(
            first_name="Mary",
            last_name="Smith",
            email="mary@example.com",
            phone_number="0987654321",
            address="456 Elm St",
        )
        session.add_all([john, mary])
        session.commit()

        # Create Items
        items = [
            Item(
                item_name="Running Shoe",
                category="Footwear",
                price=89.99,
                brand="Nike",
                color="Blue",
                size="10",
                image_url="https://example.com/nike_shoe.jpg",
                description="Comfortable running shoe",
            ),
            Item(
                item_name="Casual Sneaker",
                category="Footwear",
                price=59.99,
                brand="Adidas",
                color="White",
                size="9",
                image_url="https://example.com/adidas_sneaker.jpg",
                description="Stylish casual sneaker",
            ),
            Item(
                item_name="Hiking Boot",
                category="Footwear",
                price=129.99,
                brand="Merrell",
                color="Brown",
                size="11",
                image_url="https://example.com/merrell_boot.jpg",
                description="Durable hiking boot",
            ),
            Item(
                item_name="Day Backpack",
                category="Bags",
                price=49.99,
                brand="JanSport",
                color="Red",
                size="20L",
                image_url="https://example.com/jansport_backpack.jpg",
                description="Everyday backpack for school or work",
            ),
            Item(
                item_name="Hiking Backpack",
                category="Outdoor Gear",
                price=129.99,
                brand="North Face",
                color="Green",
                size="40L",
                image_url="https://example.com/northface_backpack.jpg",
                description="Durable hiking backpack",
            ),
            Item(
                item_name="Travel Backpack",
                category="Bags",
                price=89.99,
                brand="Osprey",
                color="Black",
                size="30L",
                image_url="https://example.com/osprey_backpack.jpg",
                description="Versatile travel backpack",
            ),
            Item(
                item_name="Mechanical Pencil",
                category="Stationery",
                price=5.99,
                brand="Pentel",
                color="Black",
                size="0.5mm",
                image_url="https://example.com/pencil.jpg",
                description="Reliable mechanical pencil",
            ),
        ]
        session.add_all(items)
        session.commit()

        # Create Purchase History
        purchases = [
            PurchaseHistory(
                user_id=john.user_id,
                item_id=items[0].item_id,  # Running Shoe
                quantity=1,
                purchase_date=datetime.utcnow() - timedelta(days=5),
                total_price=89.99,
            ),
            PurchaseHistory(
                user_id=mary.user_id,
                item_id=items[4].item_id,  # Hiking Backpack
                quantity=1,
                purchase_date=datetime.utcnow() - timedelta(days=3),
                total_price=129.99,
            ),
            PurchaseHistory(
                user_id=john.user_id,
                item_id=items[6].item_id,  # Mechanical Pencil
                quantity=2,
                purchase_date=datetime.utcnow() - timedelta(days=1),
                total_price=11.98,
            ),
            PurchaseHistory(
                user_id=mary.user_id,
                item_id=items[2].item_id,  # Hiking Boot
                quantity=1,
                purchase_date=datetime.utcnow() - timedelta(days=7),
                total_price=129.99,
            ),
            PurchaseHistory(
                user_id=john.user_id,
                item_id=items[5].item_id,  # Travel Backpack
                quantity=1,
                purchase_date=datetime.utcnow() - timedelta(days=2),
                total_price=89.99,
            ),
        ]
        session.add_all(purchases)
        session.commit()

        print("Seed data has been added successfully!")


if __name__ == "__main__":
    seed_data()
