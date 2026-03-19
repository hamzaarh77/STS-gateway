from app.entities import Order
import logging

logger = logging.getLogger(__name__)

DRUG_DB = {
    "aspirine": {
        "name": "Acide acétylsalicylique",
        "price": 5.99,
        "description": "Anti-inflammatoire non stéroïdien pour le soulagement de la douleur et la réduction de la fièvre",
        "quantity": 30
    },
    "ibuprofene": {
        "name": "Ibuprofène",
        "price": 7.99,
        "description": "Médicament anti-inflammatoire pour la gestion de la douleur et de l'inflammation",
        "quantity": 20
    },
    "paracétamol": {
        "name": "Paracétamol",
        "price": 6.99,
        "description": "Médicament analgésique et antipyrétique pour le contrôle de la douleur et de la fièvre",
        "quantity": 25
    },
    "metformine": {
        "name": "Chlorhydrate de metformine",
        "price": 12.50,
        "description": "Médicament antidiabétique biguanide pour la gestion du diabète de type 2",
        "quantity": 60
    },
    "lisinopril": {
        "name": "Lisinopril",
        "price": 8.75,
        "description": "Inhibiteur de l'ECA pour le traitement de l'hypertension et de l'insuffisance cardiaque",
        "quantity": 30
    },
    "atorvastatine": {
        "name": "Atorvastatine calcique",
        "price": 15.25,
        "description": "Inhibiteur de l'HMG-CoA réductase pour la gestion du cholestérol",
        "quantity": 30
    },
    "omeprazole": {
        "name": "Oméprazole",
        "price": 11.99,
        "description": "Inhibiteur de la pompe à protons pour le traitement du reflux gastrique et des ulcères",
        "quantity": 28
    },
    "amlodipine": {
        "name": "Bésilate d'amlodipine",
        "price": 9.50,
        "description": "Inhibiteur calcique pour l'hypertension et l'angine de poitrine",
        "quantity": 30
    },
    "metoprolol": {
        "name": "Tartrate de métoprolol",
        "price": 7.25,
        "description": "Bêta-bloquant pour l'hypertension et les troubles du rythme cardiaque",
        "quantity": 30
    },
    "sertraline": {
        "name": "Chlorhydrate de sertraline",
        "price": 13.75,
        "description": "Inhibiteur sélectif de la recapture de la sérotonine pour la dépression et l'anxiété",
        "quantity": 30
    }
}


def get_drug_info(drug_name):
    """Get drug information."""
    drug = DRUG_DB.get(drug_name.lower())
    if drug:
        return {
            "name": drug["name"],
            "description": drug["description"],
            "price": drug["price"],
            "quantity": drug["quantity"]
        }
    return {"error": f"Drug '{drug_name}' not found"}


def place_order(customer_name, drug_name):
    """Place a simple order with predefined quantity."""
    drug = DRUG_DB.get(drug_name.lower())
    if not drug:
        return {"error": f"Drug '{drug_name}' not found"}

    order = Order(
        id=1,
        customer=customer_name,
        drug=drug["name"],
        quantity=drug["quantity"],
        total=drug["price"]
    )

    order_id = order.id
    logger.info(
        f"$$$$ place order appelé, order id: {order_id} pour le client {customer_name}, il veux => {drug_name}")

    return {
        "order_id": order_id,
        "message": f"Order {order_id} placed: {drug['quantity']} {drug['name']} for ${drug['price']:.2f}",
        "total": drug["price"],
        "quantity": drug["quantity"]
    }


def lookup_order(order_id):
    """Look up an order."""

    order = DRUG_DB.filter(Order.id == int(order_id)).first()

    if order:
        logger.info(
            f"$$$$ GET - chercher un order -> trouvé order d'id => {order.id} pour le client {order.customer} il veux -> {order.drug}")
        return {
            "order_id": order.id,
            "customer": order.customer,
            "drug": order.drug,
            "quantity": order.quantity,
            "total": order.total,
            "status": order.status
        }
    return {"error": f"Order {order_id} not found"}


# Function mapping dictionary
FUNCTION_MAP = {
    'get_drug_info': get_drug_info,
    'place_order': place_order,
    'lookup_order': lookup_order
}
