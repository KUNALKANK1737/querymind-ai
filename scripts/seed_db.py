import random
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from sqlalchemy import text

from app.db.session import get_database_engine

random.seed(42)

CUSTOMER_COUNT = 100
PRODUCT_COUNT = 50
ORDER_COUNT = 500

STATES_AND_CITIES = {
    "Maharashtra": ["Pune", "Mumbai", "Nashik", "Nagpur"],
    "Karnataka": ["Bengaluru", "Mysuru", "Mangaluru"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai"],
    "Telangana": ["Hyderabad", "Warangal"],
    "Delhi": ["New Delhi"],
}

CATEGORY_NAMES = [
    "Electronics",
    "Home Appliances",
    "Clothing",
    "Footwear",
    "Books",
    "Sports",
    "Beauty",
    "Furniture",
    "Groceries",
    "Accessories",
]

ORDER_STATUSES = [
    "completed",
    "completed",
    "completed",
    "completed",
    "shipped",
    "processing",
    "cancelled",
]

PAYMENT_METHODS = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Cash on Delivery",
]


def random_date(start: datetime, end: datetime) -> datetime:
    delta = end - start
    return start + timedelta(
        seconds=random.randint(0, int(delta.total_seconds()))
    )


def seed_database() -> None:
    engine = get_database_engine()

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                TRUNCATE TABLE
                    payments,
                    order_items,
                    orders,
                    addresses,
                    products,
                    categories,
                    customers
                RESTART IDENTITY CASCADE
                """
            )
        )

        # Categories
        for category_name in CATEGORY_NAMES:
            connection.execute(
                text(
                    """
                    INSERT INTO categories (category_name)
                    VALUES (:category_name)
                    """
                ),
                {"category_name": category_name},
            )

        # Products
        for product_number in range(1, PRODUCT_COUNT + 1):
            price = Decimal(random.randint(500, 50000))
            cost = price * Decimal("0.65")

            connection.execute(
                text(
                    """
                    INSERT INTO products (
                        product_name,
                        category_id,
                        price,
                        cost,
                        stock_quantity
                    )
                    VALUES (
                        :product_name,
                        :category_id,
                        :price,
                        :cost,
                        :stock_quantity
                    )
                    """
                ),
                {
                    "product_name": f"Product {product_number}",
                    "category_id": random.randint(1, len(CATEGORY_NAMES)),
                    "price": price,
                    "cost": cost,
                    "stock_quantity": random.randint(10, 500),
                },
            )

        # Customers and addresses
        for customer_number in range(1, CUSTOMER_COUNT + 1):
            state = random.choice(list(STATES_AND_CITIES))
            city = random.choice(STATES_AND_CITIES[state])

            customer_id = connection.execute(
                text(
                    """
                    INSERT INTO customers (
                        name,
                        email,
                        phone,
                        city,
                        state,
                        country,
                        created_at
                    )
                    VALUES (
                        :name,
                        :email,
                        :phone,
                        :city,
                        :state,
                        'India',
                        :created_at
                    )
                    RETURNING customer_id
                    """
                ),
                {
                    "name": f"Customer {customer_number}",
                    "email": f"customer{customer_number}@example.com",
                    "phone": f"9{random.randint(100000000, 999999999)}",
                    "city": city,
                    "state": state,
                    "created_at": random_date(
                        datetime(2024, 1, 1, tzinfo=UTC),
                        datetime(2026, 8, 31, tzinfo=UTC),
                    ),
                },
            ).scalar_one()

            connection.execute(
                text(
                    """
                    INSERT INTO addresses (
                        customer_id,
                        address_line,
                        city,
                        state,
                        country,
                        postal_code
                    )
                    VALUES (
                        :customer_id,
                        :address_line,
                        :city,
                        :state,
                        'India',
                        :postal_code
                    )
                    """
                ),
                {
                    "customer_id": customer_id,
                    "address_line": f"{random.randint(1, 500)} Main Road",
                    "city": city,
                    "state": state,
                    "postal_code": str(random.randint(100000, 999999)),
                },
            )

        # Orders, order items and payments
        for _ in range(ORDER_COUNT):
            customer_id = random.randint(1, CUSTOMER_COUNT)
            order_date = random_date(
                datetime(2025, 1, 1, tzinfo=UTC),
                datetime(2026, 8, 31, tzinfo=UTC),
            )
            status = random.choice(ORDER_STATUSES)

            item_count = random.randint(1, 4)
            order_items = []
            total_amount = Decimal(0)

            for _ in range(item_count):
                product_id = random.randint(1, PRODUCT_COUNT)
                quantity = random.randint(1, 5)

                unit_price = connection.execute(
                    text(
                        """
                        SELECT price
                        FROM products
                        WHERE product_id = :product_id
                        """
                    ),
                    {"product_id": product_id},
                ).scalar_one()

                total_amount += unit_price * quantity

                order_items.append(
                    {
                        "product_id": product_id,
                        "quantity": quantity,
                        "unit_price": unit_price,
                    }
                )

            order_id = connection.execute(
                text(
                    """
                    INSERT INTO orders (
                        customer_id,
                        order_date,
                        status,
                        total_amount
                    )
                    VALUES (
                        :customer_id,
                        :order_date,
                        :status,
                        :total_amount
                    )
                    RETURNING order_id
                    """
                ),
                {
                    "customer_id": customer_id,
                    "order_date": order_date,
                    "status": status,
                    "total_amount": total_amount,
                },
            ).scalar_one()

            for item in order_items:
                connection.execute(
                    text(
                        """
                        INSERT INTO order_items (
                            order_id,
                            product_id,
                            quantity,
                            unit_price
                        )
                        VALUES (
                            :order_id,
                            :product_id,
                            :quantity,
                            :unit_price
                        )
                        """
                    ),
                    {
                        "order_id": order_id,
                        **item,
                    },
                )

            payment_status = (
                "refunded"
                if status == "cancelled"
                else "completed"
            )

            connection.execute(
                text(
                    """
                    INSERT INTO payments (
                        order_id,
                        payment_method,
                        payment_status,
                        payment_date,
                        amount
                    )
                    VALUES (
                        :order_id,
                        :payment_method,
                        :payment_status,
                        :payment_date,
                        :amount
                    )
                    """
                ),
                {
                    "order_id": order_id,
                    "payment_method": random.choice(PAYMENT_METHODS),
                    "payment_status": payment_status,
                    "payment_date": order_date
                    + timedelta(minutes=random.randint(1, 120)),
                    "amount": total_amount,
                },
            )

    print("Database seeded successfully.")
    print(f"Customers: {CUSTOMER_COUNT}")
    print(f"Products: {PRODUCT_COUNT}")
    print(f"Orders: {ORDER_COUNT}")


if __name__ == "__main__":
    seed_database()