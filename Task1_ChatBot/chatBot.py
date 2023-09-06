import re

end = False
order = ""
menu_price = {
    "Margherita Pizza": 12.99,
    "Pepperoni Passion": 14.99,
    "Veggie Supreme": 15.99,
    "Hawaiian Delight": 13.99,
    "Four Cheese Special": 16.99,
    "BBQ Chicken Bliss": 17.99,
    "Mediterranean Marvel": 18.99,
    "Spicy Meat Feast": 19.99,
    "Truffle Elegance": 21.99,
    "Seafood Sensation": 22.99,
    "Garlic Knots (6 pieces)": 4.99,
    "Caprese Salad": 6.99,
    "Seasoned Fries": 3.99,
    "Soft Drinks": 2.49,
    "Bottled Water": 1.49,
    "Iced Tea": 2.99,
    "Fresh Lemonade": 3.49,
}
menu_ingredients = {
    "Margherita Pizza": ["Tomato sauce", "Mozzarella cheese", "Fresh basil"],
    "Pepperoni Passion": ["Tomato sauce", "Mozzarella cheese", "Pepperoni"],
    "Veggie Supreme": ["Tomato sauce", "Mozzarella cheese", "Bell peppers", "Red onions", "Mushrooms", "Olives"],
    "Hawaiian Delight": ["Tomato sauce", "Mozzarella cheese", "Ham", "Pineapple"],
    "Four Cheese Special": ["Tomato sauce", "Mozzarella cheese", "Cheddar cheese", "Parmesan cheese", "Feta cheese"],
    "BBQ Chicken Bliss": ["BBQ sauce", "Mozzarella cheese", "Grilled chicken", "Red onions", "Cilantro"],
    "Mediterranean Marvel": ["Pesto sauce", "Mozzarella cheese", "Cherry tomatoes", "Black olives", "Feta cheese",
                             "Spinach"],
    "Spicy Meat Feast": ["Spicy marinara", "Mozzarella cheese", "Italian sausage", "Salami", "Jalapenos"],
    "Truffle Elegance": ["White sauce", "Mozzarella cheese", "Truffle oil", "Mushrooms", "Arugula", "Shaved parmesan"],
    "Seafood Sensation": ["Alfredo sauce", "Mozzarella cheese", "Shrimp", "Crab", "Clams", "Garlic"],
    "Garlic Knots (6 pieces)": ["Dough", "Garlic", "Butter", "Parsley"],
    "Caprese Salad": ["Fresh mozzarella", "Tomatoes", "Fresh basil", "Balsamic glaze"],
    "Seasoned Fries": ["Potato fries", "Seasoning"],
    "Soft Drinks": ["Assorted soft drinks"],
    "Bottled Water": ["Bottled water"],
    "Iced Tea": ["Iced tea"],
    "Fresh Lemonade": ["Lemon juice", "Water", "Sugar"],
}

intents = {
    "greeting": ["welcome", "hello", "al-salam alykom", "hi"],
    "order_pizza": ["want to make an order", "want to order", "get a pizza"],
    "confirm_inquiry": ["confirm the order", "assure", "approve", "prove", "affirm", "assert", "get my order"],
    "menu_inquiry": ["menu", "show me the options", "what's on the menu", "what do you do"],
    "specials_inquiry": ["specials", "discount", "what's on offer"],
    "location_ inquiry": ["location", "branches", "place", "how can i go to the restaurant", "near", "close"],
    "recommendation_inquiry": ["best", "I am confused", "I am lost", "best seller", "good pizza", "recommendations"],
    "delivery_inquiry": ["delivery", "deliver", "shipping", "home"],
    "beverages_inquiry": ["drinks", "syrup", "juice", "soda"],
    "gift_inquiry": ["grant", "present", "gifts", "give", "children"],
    "extra_inquiry": ["more", "too", "want", "extra"],
    "price_inquiry": ["price", "money", "pay"],
    "time_inquiry": ["time", "long time", "when i will get the order"],
    "end_inquiry": ["end", "goodbye", "bye", "thanks I am done", "I am finished", "thanks", "thank you"],
    "ingredients_inquiry": ["ingredients of", "made from"]
}

responses = {
    "greeting": "Hello Dear, How can I help you?",
    "order_pizza": "Sure, happy that you are here. \nwhat do u want to order? ",
    "menu_inquiry": "Here is the menu, \n 🍕 Pizzeria Bella Menu 🍕\n",
    "specials_inquiry": "Today's specials include our Seafood Sensation and Mediterranean Marvel!",
    "location_ inquiry": "Sure, Branches Locations: \n 1. Pizzeria Bella 🍕 \n - Address: 123 Broadway Street, "
                         "New York, NY. \n"
                         " - Phone: (212) 555-1234 \n - Hours: Mon-Sat 11:00 AM - 10:00 PM, Sun 12:00 PM - 9:00 PM\n"
                         "2. Pizzeria Bella 🍕 \n - Address: 456 Oak Lane, Los Angeles, CA. \n - Phone: (323) "
                         "555-5678. \n"
                         " - Hours: Mon-Sat 10:30 AM - 9:30 PM, Sun 11:00 AM - 8:00 PM. \n",
    "recommendation_inquiry": "Our Best Sellers Pizza are Pepperoni Passion and BBQ Chicken Bliss,\n You can order your"
                              "favourite drink too. 😉\n",
    "delivery_inquiry": "Delivery is available in New York and Los Angeles only for $10.\n",
    "beverages_inquiry": "Sure, our beverages are: \n"
                         "- Soft Drinks - $2.49\n"
                         "- Bottled Water - $1.49\n"
                         "- Iced Tea - $2.99\n"
                         "- Fresh Lemonade -  $3.49\n",
    "gift_inquiry": "Ofc, you can choose one with each pizza:\n"
                    "- Tom statue.\n"
                    "- Jerry statue.\n"
                    "- Pen.\n"
                    "- Notebook.\n"
                    "- Tote bag.\n"
                    "- Mug.\n",
    "extra_inquiry": "Sure, anything else?",
    "price_inquiry": "Here is the menu, you can check all prices\n",
    "confirm_inquiry": "Sure, we confirmed your order and it will take maximum 30 mins. \n",
    "time_inquiry": "The order takes maximum 30 mins to be done.\n",
    "end_inquiry": "** Thanks for your time, see you soon. ** \n",
    "ingredients_inquiry": "Here is teh menu, you can check the ingredients of each item.\n"
}


def display_menu():
    file = open("menu.txt", 'r')
    menu_text = file.read()
    return menu_text


def get_intent(message):
    message = message.lower()

    for intent, keywords in intents.items():
        for keyword in keywords:
            if re.search(r'\b' + keyword + r'\b', message):
                return intent
    return None


def generate_response(intent):
    if intent in responses:
        return responses[intent]
    else:
        return "I'm sorry, I didn't understand that."


def chatbot_response(message):
    global end, order
    user_intent = get_intent(message)
    if user_intent:
        response = generate_response(user_intent)
        if user_intent == "menu_inquiry" or user_intent == "price_inquiry" or user_intent == "ingredients_inquiry":
            menu_text = display_menu()
            response += menu_text + "\n"

        if user_intent == "order_inquiry":
            response += " " + generate_response("confirm_inquiry")

        if user_intent == "confirm_inquiry":
            response += " " + order

        if user_intent == "end_inquiry":
            end = True

    else:
        response = "I'm not sure how to respond to that, can you make your message more clear?"

    return response


def user_input():
    message = str(input("You: ")).strip().lower()
    return message


def chatbot():
    print(f"=========== Hello, =============")
    print("Welcome to our Pizza Restaurant")

    while not end:
        message = user_input()
        response = chatbot_response(message)
        print(response)


chatbot()
