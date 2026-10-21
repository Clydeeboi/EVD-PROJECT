import json
import re
from uuid import uuid4

from pyscript import document, window, when, ffi


foods = {
    "fries": {
        "name": "Fries",
        "category": "Crispy, savory goodness",
        "description": "Golden, crispy fries tossed in your favorite seasoning. Choose a size for a quick bite or a bigger snack break.",
        "size_label": "Choose your size",
        "sizes": [
            {"label": "Small", "detail": "Solo snack", "price": 20},
            {"label": "Medium", "detail": "Bigger bite", "price": 40},
            {"label": "Large", "detail": "More to share", "price": 60},
        ],
        "flavors": ["Cheese", "BBQ", "Sour cream"],
        "image": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=700&q=80",
    },
    "drinks": {
        "name": "Flavored drinks",
        "category": "Sip something refreshing",
        "description": "A chilled drink to pair with your favorite snack. Choose your cup size and a refreshing flavor.",
        "size_label": "Choose your cup size",
        "sizes": [
            {"label": "Small", "detail": "12 oz", "price": 20},
            {"label": "Medium", "detail": "16 oz", "price": 30},
            {"label": "Large", "detail": "22 oz", "price": 40},
        ],
        "flavors": ["Lemonade", "Cucumber lemon", "Iced tea"],
        "image": "assets/menu/flavored-drinks.jpg",
    },
    "munchkins": {
        "name": "Munchkins",
        "category": "Little bites of happiness",
        "description": "Soft, bite-size doughnut treats for your sweet cravings. Pick a pack and your favorite coating.",
        "size_label": "Choose your pack",
        "sizes": [
            {"label": "3 pieces", "detail": "Mini pack", "price": 15},
            {"label": "5 pieces", "detail": "Snack pack", "price": 25},
            {"label": "10 pieces", "detail": "Sharing pack", "price": 50},
        ],
        "flavors": ["Choco glazed", "Choco butternut", "Powdered sugar"],
        "image": "assets/menu/munchkins.jpg",
    },
    "sandwiches": {
        "name": "Sandwiches",
        "category": "Something filling",
        "description": "Toasted sandwiches for study days and in-between-class cravings. Choose your filling and serving.",
        "image": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=700&q=80",
        "size_label": "Choose your serving",
        "sizes": [
            {"label": "Single", "detail": "1 sandwich", "price": 20},
            {"label": "Double", "detail": "2 sandwiches", "price": 40},
        ],
        "flavors": ["Cheese", "Ham & cheese", "Chicken"],
        "flavor_label": "Choose your filling",
        "option_note": "All fillings are the same price for your selected serving.",
    },
    "cookies": {
        "name": "Cookies",
        "category": "A sweet little treat",
        "description": "A little chocolate, a little crunch, and a well-deserved sweet break. Choose a piece or a pack.",
        "image": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?auto=format&fit=crop&w=700&q=80",
        "size_label": "Choose your pack",
        "sizes": [
            {"label": "1 piece", "detail": "Solo treat", "price": 10},
            {"label": "3 pieces", "detail": "Snack pack", "price": 30},
        ],
        "flavors": ["Chocolate chip", "Double chocolate"],
    },
    "nachos": {
        "name": "Nachos",
        "category": "Crunch time",
        "description": "Crunchy tortilla chips with a cheesy topping. Pick a portion for a quick bite or a snack to share.",
        "image": "assets/menu/nachos.jpg",
        "size_label": "Choose your size",
        "sizes": [
            {"label": "Small", "detail": "Solo snack", "price": 25},
            {"label": "Medium", "detail": "Bigger bite", "price": 35},
            {"label": "Large", "detail": "Sharing portion", "price": 50},
        ],
        "flavors": ["Classic cheese", "BBQ cheese"],
    },
    "siomai": {
        "name": "Siomai",
        "category": "Steamed and savory",
        "description": "Soft, savory steamed pork dumplings. Choose your pack and a dipping sauce for a satisfying snack break.",
        "image": "assets/menu/siomai.jpg",
        "size_label": "Choose your pack",
        "sizes": [
            {"label": "4 pieces", "detail": "Solo pack", "price": 20},
            {"label": "8 pieces", "detail": "Sharing pack", "price": 40},
        ],
        "flavors": ["Soy calamansi", "Chili garlic"],
        "flavor_label": "Choose your sauce",
        "option_note": "Your choice of sauce is included in the pack price.",
    },
    "fried-siomai": {
        "name": "Fried siomai",
        "category": "Golden and crispy",
        "description": "A crispy twist on pork siomai, fried until golden. Pick your pack and your favorite dipping sauce.",
        "image": "assets/menu/fried-siomai.jpg",
        "size_label": "Choose your pack",
        "sizes": [
            {"label": "4 pieces", "detail": "Solo pack", "price": 25},
            {"label": "8 pieces", "detail": "Sharing pack", "price": 50},
        ],
        "flavors": ["Soy calamansi", "Chili garlic"],
        "flavor_label": "Choose your sauce",
        "option_note": "Your choice of sauce is included in the pack price.",
    },
    "custard-cake": {
        "name": "Custard cake",
        "category": "Soft and sweet",
        "description": "Soft cake with a smooth custard layer. Enjoy a slice for yourself or pick two to share.",
        "image": "assets/menu/cuscard-cake.jpg",
        "size_label": "Choose your serving",
        "sizes": [
            {"label": "1 slice", "detail": "Solo treat", "price": 35},
            {"label": "2 slices", "detail": "To share", "price": 70},
        ],
        "flavors": ["Classic custard"],
        "flavor_label": "Cake flavor",
        "option_note": "Classic custard is included in every slice.",
    },
    "custard": {
        "name": "Custard tarts",
        "category": "A creamy little bite",
        "description": "Buttery pastry filled with smooth custard. Choose a single tart or a pair for your snack break.",
        "image": "assets/menu/cuscard.jpg",
        "size_label": "Choose your serving",
        "sizes": [
            {"label": "1 piece", "detail": "Solo treat", "price": 30},
            {"label": "2 pieces", "detail": "To share", "price": 60},
        ],
        "flavors": ["Classic custard"],
        "flavor_label": "Tart flavor",
        "option_note": "Every tart comes with our classic custard filling.",
    },
    "pudding": {
        "name": "Pudding",
        "category": "A smooth sweet finish",
        "description": "Smooth caramel pudding for a sweet finish to your snack break. Choose one serving or two.",
        "image": "assets/menu/pudding.jpg",
        "size_label": "Choose your serving",
        "sizes": [
            {"label": "Single", "detail": "1 serving", "price": 50},
            {"label": "Double", "detail": "2 servings", "price": 100},
        ],
        "flavors": ["Caramel"],
        "flavor_label": "Pudding flavor",
        "option_note": "Caramel is included in every serving.",
    },
}

saved_choices = {}
current_food = ""
last_food_button = None
press_started_outside = False

popup = document.getElementById("product-dialog")
size_container = document.getElementById("product-sizes")
flavor_container = document.getElementById("product-flavors")


def show_pesos(price):
    return "₱" + str(price)


def create_choice(group_name, number, title, extra_lines, is_selected):
    choice = document.createElement("label")
    choice.className = "variant-option"

    radio_button = document.createElement("input")
    radio_button.type = "radio"
    radio_button.name = group_name
    radio_button.value = str(number)
    radio_button.checked = is_selected

    choice_box = document.createElement("span")
    choice_box.className = "variant-choice"

    choice_title = document.createElement("strong")
    choice_title.textContent = title
    choice_box.appendChild(choice_title)

    for line in extra_lines:
        small_text = document.createElement("small")
        small_text.textContent = line
        choice_box.appendChild(small_text)

    choice.appendChild(radio_button)
    choice.appendChild(choice_box)
    return choice


def show_size_choices(food, saved_size):
    size_container.innerHTML = ""
    sizes = food["sizes"]

    for number in range(len(sizes)):
        size = sizes[number]
        extra_lines = [size["detail"], show_pesos(size["price"])]
        is_selected = False

        if number == saved_size:
            is_selected = True

        choice = create_choice(
            "product-size", number, size["label"], extra_lines, is_selected
        )
        size_container.appendChild(choice)


def show_flavor_choices(food, saved_flavor):
    flavor_container.innerHTML = ""
    flavors = food["flavors"]

    for number in range(len(flavors)):
        is_selected = False

        if number == saved_flavor:
            is_selected = True

        choice = create_choice(
            "product-flavor", number, flavors[number], [], is_selected
        )
        flavor_container.appendChild(choice)


def read_product_quantity():
    quantity_box = document.getElementById("product-quantity")
    if not quantity_box.validity.valid:
        return 0
    try:
        quantity = int(quantity_box.value)
    except ValueError:
        return 0
    if quantity < 1 or quantity > 99:
        return 0
    return quantity


def update_price():
    if current_food == "":
        return

    food = foods[current_food]
    selected_size = document.querySelector("#product-sizes input:checked")
    selected_flavor = document.querySelector("#product-flavors input:checked")

    size_number = int(selected_size.value)
    flavor_number = int(selected_flavor.value)

    size = food["sizes"][size_number]
    flavor = food["flavors"][flavor_number]
    price = size["price"]

    price_label = document.getElementById("product-price")
    quantity = read_product_quantity()
    add_button = document.getElementById("product-add")
    add_button.disabled = quantity == 0
    if quantity == 0:
        price_label.value = "—"
        document.getElementById("product-feedback").textContent = "Enter a whole number from 1 to 99."
    else:
        price_label.value = show_pesos(price * quantity)
        document.getElementById("product-feedback").textContent = ""

    summary = size["label"] + " · " + flavor
    if current_food == "drinks":
        summary = summary + " · " + size["detail"]

    summary = summary + " · " + show_pesos(price) + " each"
    document.getElementById("product-selection").textContent = summary

    saved_choices[current_food] = {
        "size": size_number,
        "flavor": flavor_number,
    }


def show_food_information(food_button, food):
    popup_picture = document.getElementById("product-image")
    popup_picture.src = food["image"]
    popup_picture.alt = food["name"]

    document.getElementById("product-title").textContent = food["name"]
    document.getElementById("product-category").textContent = food["category"]
    document.getElementById("product-description").textContent = food["description"]
    document.getElementById("product-size-label").textContent = food["size_label"]
    document.getElementById("product-flavor-label").textContent = food.get("flavor_label", "Choose your flavor")
    document.getElementById("product-option-note").textContent = food.get(
        "option_note", "All flavors are the same price for your selected size."
    )


def press_is_outside_popup(event):
    popup_edges = popup.getBoundingClientRect()

    if event.clientX < popup_edges.left:
        return True
    if event.clientX > popup_edges.right:
        return True
    if event.clientY < popup_edges.top:
        return True
    if event.clientY > popup_edges.bottom:
        return True

    return False


if not ffi.is_none(popup):

    @when("click", ".product-open")
    def open_food_popup(event):
        global current_food, last_food_button

        food_button = event.currentTarget
        current_food = food_button.dataset.product
        last_food_button = food_button
        food = foods[current_food]

        saved_size = 0
        saved_flavor = 0

        if current_food in saved_choices:
            saved_size = saved_choices[current_food]["size"]
            saved_flavor = saved_choices[current_food]["flavor"]

        document.getElementById("product-quantity").value = "1"
        show_food_information(food_button, food)
        show_size_choices(food, saved_size)
        show_flavor_choices(food, saved_flavor)
        update_price()

        document.body.classList.add("product-dialog-open")
        popup.showModal()

        close_button = document.getElementById("product-close")
        focus_settings = ffi.to_js({"preventScroll": True})
        close_button.focus(focus_settings)

    @when("input", "#product-quantity")
    @when("change", "#product-dialog")
    def change_food_option(event):
        update_price()

    @when("click", "#product-close")
    def close_food_popup(event):
        popup.close()

    @when("keydown", "#product-dialog")
    def keep_keyboard_inside_popup(event):
        if event.key != "Tab":
            return

        controls = popup.querySelectorAll(
            'button:not([disabled]), input[type="radio"]:checked, input[type="number"]'
        )
        first_control = controls[0]
        last_control = controls[len(controls) - 1]
        current_control = document.activeElement

        if event.shiftKey:
            if current_control.isSameNode(first_control):
                event.preventDefault()
                last_control.focus()
        else:
            if current_control.isSameNode(last_control):
                event.preventDefault()
                first_control.focus()

    @when("pointerdown", "#product-dialog")
    def remember_where_press_started(event):
        global press_started_outside
        press_started_outside = False

        if event.target.isSameNode(popup):
            if press_is_outside_popup(event):
                press_started_outside = True

    @when("click", "#product-dialog")
    def close_when_background_clicked(event):
        global press_started_outside

        if press_started_outside:
            if event.target.isSameNode(popup):
                if press_is_outside_popup(event):
                    popup.close()

        press_started_outside = False

    @when("close", "#product-dialog")
    def return_to_page(event):
        document.body.classList.remove("product-dialog-open")

        if last_food_button is not None:
            focus_settings = ffi.to_js({"preventScroll": True})
            last_food_button.focus(focus_settings)


cart = []
cart_storage_key = "snackspot-cart-v1"
cart_popup = document.getElementById("cart-dialog")
checkout_popup = document.getElementById("checkout-dialog")
last_cart_button = None
cart_press_started_outside = False


def cart_item_key(item):
    return item["food"] + "-" + str(item["size"]) + "-" + str(item["flavor"])


def load_cart():
    global cart
    try:
        stored_text = window.localStorage.getItem(cart_storage_key)
        if ffi.is_none(stored_text):
            return
        stored_items = json.loads(stored_text)
        if not isinstance(stored_items, list):
            return
        maximum_entries = 0
        for food in foods.values():
            maximum_entries = maximum_entries + len(food["sizes"]) * len(food["flavors"])
        if len(stored_items) > maximum_entries:
            return
        for item in stored_items:
            if not isinstance(item, dict):
                continue
            food_key = item.get("food")
            if not isinstance(food_key, str) or food_key not in foods:
                continue
            size_number = item.get("size")
            flavor_number = item.get("flavor")
            quantity = item.get("quantity")
            if type(size_number) is not int or type(flavor_number) is not int:
                continue
            if type(quantity) is not int:
                continue
            if not 0 <= size_number < len(foods[food_key]["sizes"]):
                continue
            if not 0 <= flavor_number < len(foods[food_key]["flavors"]):
                continue
            if not 1 <= quantity <= 99:
                continue
            matching_item = None
            for existing_item in cart:
                if cart_item_key(existing_item) == cart_item_key(item):
                    matching_item = existing_item
            if matching_item is None:
                cart.append({"food": food_key, "size": size_number,
                             "flavor": flavor_number, "quantity": quantity})
            else:
                matching_item["quantity"] = min(99, matching_item["quantity"] + quantity)
    except Exception:
        cart = []


def save_cart():
    try:
        window.localStorage.setItem(cart_storage_key, json.dumps(cart))
    except Exception:
        document.getElementById("cart-note-storage").textContent = "Your browser could not save this cart. Keep this page open to keep your items."


def make_cart_text(tag, text, class_name=""):
    element = document.createElement(tag)
    element.textContent = text
    element.className = class_name
    return element


def make_cart_button(text, action, item_number, description):
    button = make_cart_text("button", text)
    button.type = "button"
    button.dataset.cartAction = action
    button.dataset.cartIndex = str(item_number)
    button.setAttribute("aria-label", description)
    return button


def render_cart(focus_key="", focus_action=""):
    cart_list = document.getElementById("cart-items")
    cart_list.innerHTML = ""
    total_price = 0
    total_quantity = 0
    next_focus = None

    for number in range(len(cart)):
        item = cart[number]
        food = foods[item["food"]]
        size = food["sizes"][item["size"]]
        flavor = food["flavors"][item["flavor"]]
        quantity = item["quantity"]
        line_price = size["price"] * quantity
        total_price = total_price + line_price
        total_quantity = total_quantity + quantity
        details = size["label"] + " · " + flavor
        if item["food"] == "drinks":
            details = details + " · " + size["detail"]
        description = food["name"] + ", " + details

        row = document.createElement("li")
        row.className = "cart-item"
        picture = document.createElement("img")
        picture.src = food["image"]
        picture.alt = ""
        row.appendChild(picture)

        information = document.createElement("div")
        information.className = "cart-item-info"
        information.appendChild(make_cart_text("h3", food["name"]))
        information.appendChild(make_cart_text("p", details, "cart-item-details"))
        information.appendChild(make_cart_text("p", show_pesos(size["price"]) + " each", "cart-unit-price"))

        controls = document.createElement("div")
        controls.className = "cart-item-controls"
        quantity_group = document.createElement("div")
        quantity_group.className = "cart-quantity"
        quantity_group.setAttribute("role", "group")
        quantity_group.setAttribute("aria-label", "Quantity for " + description)
        minus = make_cart_button("−", "decrease", number, "Decrease quantity for " + description)
        minus.disabled = quantity == 1
        plus = make_cart_button("+", "increase", number, "Increase quantity for " + description)
        plus.disabled = quantity == 99
        quantity_group.appendChild(minus)
        quantity_group.appendChild(make_cart_text("span", str(quantity), "cart-quantity-value"))
        quantity_group.appendChild(plus)
        remove = make_cart_button("Remove", "remove", number, "Remove " + description)
        remove.className = "cart-remove"
        controls.appendChild(quantity_group)
        controls.appendChild(remove)
        information.appendChild(controls)
        row.appendChild(information)
        row.appendChild(make_cart_text("strong", show_pesos(line_price), "cart-line-total"))
        cart_list.appendChild(row)

        if cart_item_key(item) == focus_key:
            if focus_action == "increase" and not plus.disabled:
                next_focus = plus
            elif focus_action == "decrease" and not minus.disabled:
                next_focus = minus
            else:
                next_focus = remove

    count_label = str(total_quantity) + " items"
    if total_quantity == 1:
        count_label = "1 item"
    for badge in document.querySelectorAll(".cart-count"):
        badge.textContent = str(total_quantity)
        badge.setAttribute("aria-label", count_label)
    document.getElementById("cart-item-count").textContent = count_label
    document.getElementById("cart-total").value = show_pesos(total_price)
    document.getElementById("cart-empty").hidden = len(cart) > 0
    cart_list.hidden = len(cart) == 0
    checkout_button = document.getElementById("cart-checkout")
    if not ffi.is_none(checkout_button):
        checkout_button.disabled = len(cart) == 0

    if focus_key != "":
        if next_focus is None:
            next_focus = cart_list.querySelector("button:not([disabled])")
        if ffi.is_none(next_focus) or next_focus is None:
            next_focus = document.getElementById("cart-close")
        next_focus.focus(ffi.to_js({"preventScroll": True}))


if not ffi.is_none(cart_popup):
    load_cart()
    render_cart()

    if not ffi.is_none(popup):

        @when("click", "#product-add")
        def add_food_to_cart(event):
            quantity = read_product_quantity()
            if quantity == 0:
                document.getElementById("product-quantity").reportValidity()
                return
            choice = saved_choices[current_food]
            new_item = {"food": current_food, "size": choice["size"],
                        "flavor": choice["flavor"], "quantity": quantity}
            matching_item = None
            for item in cart:
                if cart_item_key(item) == cart_item_key(new_item):
                    matching_item = item
            if matching_item is not None:
                if matching_item["quantity"] + quantity > 99:
                    document.getElementById("product-feedback").textContent = "You can add up to 99 of the same size and flavor. Adjust the quantity in your cart."
                    return
                matching_item["quantity"] = matching_item["quantity"] + quantity
            else:
                cart.append(new_item)
            save_cart()
            render_cart()
            document.getElementById("cart-notice").hidden = False
            document.getElementById("cart-notice-message").textContent = str(quantity) + " × " + foods[current_food]["name"] + " added to your cart."
            popup.close()

    @when("click", ".cart-open")
    def open_cart(event):
        global last_cart_button
        last_cart_button = event.currentTarget
        document.getElementById("cart-update").textContent = ""
        render_cart()
        cart_popup.showModal()
        document.body.classList.add("product-dialog-open")
        document.getElementById("cart-close").focus(ffi.to_js({"preventScroll": True}))

    notice_button = document.getElementById("notice-dismiss")
    if not ffi.is_none(notice_button):

        @when("click", "#notice-dismiss")
        def dismiss_cart_notice(event):
            document.getElementById("cart-notice").hidden = True
            document.querySelector(".cart-open").focus(ffi.to_js({"preventScroll": True}))

    @when("click", "#cart-close, #cart-continue")
    def close_cart(event):
        cart_popup.close()

    @when("close", "#cart-dialog")
    def return_from_cart(event):
        if not ffi.is_none(checkout_popup) and checkout_popup.open:
            return
        document.body.classList.remove("product-dialog-open")
        if last_cart_button is not None:
            last_cart_button.focus(ffi.to_js({"preventScroll": True}))

    @when("click", "#cart-items")
    def change_cart(event):
        button = event.target.closest("button[data-cart-action]")
        if ffi.is_none(button):
            return
        number = int(button.dataset.cartIndex)
        item = cart[number]
        key = cart_item_key(item)
        action = button.dataset.cartAction
        name = foods[item["food"]]["name"]
        if action == "remove":
            cart.pop(number)
            message = name + " removed from your cart."
        else:
            if action == "increase" and item["quantity"] < 99:
                item["quantity"] = item["quantity"] + 1
            elif action == "decrease" and item["quantity"] > 1:
                item["quantity"] = item["quantity"] - 1
            message = name + " quantity: " + str(item["quantity"]) + "."
        save_cart()
        render_cart(key, action)
        document.getElementById("cart-update").textContent = message
        cart_notice = document.getElementById("cart-notice")
        if not ffi.is_none(cart_notice):
            cart_notice.hidden = True

    @when("keydown", "#cart-dialog")
    def keep_keyboard_inside_cart(event):
        if event.key != "Tab":
            return
        buttons = cart_popup.querySelectorAll("button:not([disabled])")
        first_button = buttons[0]
        last_button = buttons[len(buttons) - 1]
        if event.shiftKey and document.activeElement.isSameNode(first_button):
            event.preventDefault()
            last_button.focus()
        elif not event.shiftKey and document.activeElement.isSameNode(last_button):
            event.preventDefault()
            first_button.focus()

    @when("pointerdown", "#cart-dialog")
    def remember_cart_press(event):
        global cart_press_started_outside
        cart_press_started_outside = False
        if event.target.isSameNode(cart_popup):
            edges = cart_popup.getBoundingClientRect()
            if event.clientX < edges.left or event.clientX > edges.right or event.clientY < edges.top or event.clientY > edges.bottom:
                cart_press_started_outside = True

    @when("click", "#cart-dialog")
    def close_cart_from_background(event):
        global cart_press_started_outside
        if cart_press_started_outside and event.target.isSameNode(cart_popup):
            edges = cart_popup.getBoundingClientRect()
            if event.clientX < edges.left or event.clientX > edges.right or event.clientY < edges.top or event.clientY > edges.bottom:
                cart_popup.close()
        cart_press_started_outside = False


checkout_form = document.getElementById("checkout-form")
checkout_complete = False
checkout_press_started_outside = False


def fill_checkout_items(list_id):
    item_list = document.getElementById(list_id)
    item_list.innerHTML = ""
    total = 0
    for item in cart:
        food = foods[item["food"]]
        size = food["sizes"][item["size"]]
        flavor = food["flavors"][item["flavor"]]
        line_price = size["price"] * item["quantity"]
        total = total + line_price
        details = str(item["quantity"]) + " × " + size["label"] + " · " + flavor
        if item["food"] == "drinks":
            details = details + " · " + size["detail"]
        row = document.createElement("li")
        information = document.createElement("div")
        information.className = "checkout-line-info"
        information.appendChild(make_cart_text("strong", food["name"]))
        information.appendChild(make_cart_text("p", details))
        row.appendChild(information)
        row.appendChild(make_cart_text("strong", show_pesos(line_price), "checkout-line-price"))
        item_list.appendChild(row)
    return total


def validate_checkout_phone():
    phone_box = document.getElementById("checkout-phone")
    error_label = document.getElementById("checkout-phone-error")
    phone = phone_box.value
    message = ""
    if phone == "":
        message = "Enter your mobile number."
    elif re.fullmatch(r"(09[0-9]{9}|[+]639[0-9]{9})", phone) is None:
        message = "Enter a valid mobile number: 09XXXXXXXXX or +639XXXXXXXXX."
    phone_box.setCustomValidity(message)
    if error_label.textContent != message:
        error_label.textContent = message
    if message != "":
        phone_box.setAttribute("aria-invalid", "true")
        return False
    phone_box.removeAttribute("aria-invalid")
    return True


def press_is_outside_checkout(event):
    edges = checkout_popup.getBoundingClientRect()
    if event.clientX < edges.left or event.clientX > edges.right:
        return True
    if event.clientY < edges.top or event.clientY > edges.bottom:
        return True
    return False


gcash_confirmed = False
gcash_cart_signature = ""
gcash_reference = ""


def current_cart_signature():
    return json.dumps(cart, sort_keys=True)


def reset_gcash_payment():
    global gcash_confirmed, gcash_cart_signature, gcash_reference
    gcash_confirmed = False
    gcash_cart_signature = ""
    gcash_reference = ""


def gcash_payment_matches_cart():
    if not gcash_confirmed:
        return False
    return gcash_cart_signature == current_cart_signature()


def update_payment_details():
    is_paid = gcash_payment_matches_cart()
    total = fill_checkout_items("checkout-items")
    document.getElementById("checkout-total").value = show_pesos(total)
    document.getElementById("gcash-amount").value = show_pesos(total)
    document.getElementById("gcash-payment").hidden = False
    document.getElementById("checkout-submit").disabled = not is_paid
    document.getElementById("checkout-pickup-payment").textContent = "Payment: GCash"
    simulate_button = document.getElementById("gcash-simulate")
    simulate_button.disabled = is_paid
    document.getElementById("gcash-reference-row").hidden = not is_paid
    document.getElementById("gcash-reference").textContent = gcash_reference
    status = document.getElementById("gcash-status")
    if is_paid:
        document.getElementById("checkout-payment-note").textContent = "GCash · Payment simulated"
        simulate_button.textContent = "Payment simulated ✓"
        status.textContent = "Payment simulated. You can now place your order."
    else:
        document.getElementById("checkout-payment-note").textContent = "GCash · Complete the showcase payment below"
        simulate_button.textContent = "Simulate payment →"
        status.textContent = ""


if not ffi.is_none(checkout_popup):

    @when("click", "#gcash-simulate")
    def simulate_gcash_payment(event):
        global gcash_confirmed, gcash_cart_signature, gcash_reference
        if len(cart) == 0:
            return
        if gcash_payment_matches_cart():
            return
        gcash_cart_signature = current_cart_signature()
        gcash_reference = "GC-" + str(uuid4())[:8].upper()
        gcash_confirmed = True
        document.getElementById("checkout-feedback").textContent = ""
        update_payment_details()
        document.getElementById("checkout-submit").focus(ffi.to_js({"preventScroll": True}))


if not ffi.is_none(checkout_popup):

    @when("click", "#cart-checkout")
    def open_checkout(event):
        global checkout_complete
        if len(cart) == 0:
            return
        checkout_complete = False
        total = fill_checkout_items("checkout-items")
        quantity = 0
        for item in cart:
            quantity = quantity + item["quantity"]
        count = str(quantity) + " items"
        if quantity == 1:
            count = "1 item"
        document.getElementById("checkout-count").textContent = count
        document.getElementById("checkout-total").value = show_pesos(total)
        document.getElementById("checkout-entry").hidden = False
        document.getElementById("checkout-success").hidden = True
        document.getElementById("checkout-feedback").textContent = ""
        document.getElementById("checkout-submit").disabled = False
        document.getElementById("checkout-title").textContent = "Checkout"
        if not gcash_payment_matches_cart():
            reset_gcash_payment()
        update_payment_details()
        cart_popup.close()
        checkout_popup.showModal()
        checkout_popup.scrollTop = 0
        document.body.classList.add("product-dialog-open")
        document.getElementById("checkout-name").focus(ffi.to_js({"preventScroll": True}))

    @when("click", "#checkout-back")
    def go_back_to_cart(event):
        checkout_popup.close()
        cart_popup.showModal()
        document.body.classList.add("product-dialog-open")
        document.getElementById("cart-checkout").focus(ffi.to_js({"preventScroll": True}))

    @when("click", "#checkout-close, #checkout-done")
    def close_checkout(event):
        checkout_popup.close()

    @when("close", "#checkout-dialog")
    def return_from_checkout(event):
        if cart_popup.open:
            return
        document.body.classList.remove("product-dialog-open")
        if last_cart_button is not None:
            last_cart_button.focus(ffi.to_js({"preventScroll": True}))

    @when("input", "#checkout-name")
    def clear_name_error(event):
        event.currentTarget.setCustomValidity("")
        document.getElementById("checkout-feedback").textContent = ""

    @when("blur", "#checkout-phone")
    @when("invalid", "#checkout-phone")
    def show_phone_error(event):
        validate_checkout_phone()

    @when("input", "#checkout-phone")
    def update_phone_error(event):
        error_label = document.getElementById("checkout-phone-error")
        if error_label.textContent != "":
            validate_checkout_phone()

    @when("submit", "#checkout-form")
    def place_order(event):
        global checkout_complete
        event.preventDefault()
        if checkout_complete:
            return
        if len(cart) == 0:
            document.getElementById("checkout-feedback").textContent = "Your cart is empty. Add a snack before checking out."
            return
        name_box = document.getElementById("checkout-name")
        name = name_box.value.strip()
        name_box.setCustomValidity("")
        if name == "":
            name_box.setCustomValidity("Enter a name for pickup.")
            document.getElementById("checkout-feedback").textContent = "Please enter your name for pickup."
        validate_checkout_phone()
        if not checkout_form.checkValidity():
            checkout_form.reportValidity()
            return
        if not gcash_payment_matches_cart():
            reset_gcash_payment()
            update_payment_details()
            document.getElementById("checkout-feedback").textContent = "Complete the GCash showcase payment before placing your order."
            return
        phone = document.getElementById("checkout-phone").value.strip()
        notes = document.getElementById("checkout-notes").value.strip()
        document.getElementById("checkout-submit").disabled = True
        total = fill_checkout_items("receipt-items")
        order_number = "SS-" + str(uuid4())[:8].upper()
        document.getElementById("receipt-number").textContent = order_number
        document.getElementById("receipt-date").textContent = window.Date.new().toLocaleString()
        document.getElementById("receipt-name").textContent = name
        document.getElementById("receipt-phone").textContent = phone
        document.getElementById("receipt-phone-row").hidden = False
        document.getElementById("receipt-notes").textContent = notes
        document.getElementById("receipt-notes-row").hidden = notes == ""
        document.getElementById("receipt-total").value = show_pesos(total)
        payment_status = document.getElementById("receipt-payment-status")
        document.getElementById("receipt-payment").textContent = "GCash · Showcase payment"
        payment_status.textContent = "Paid (simulated)"
        payment_status.classList.add("checkout-gcash-paid")
        document.getElementById("receipt-payment-reference-row").hidden = False
        document.getElementById("receipt-payment-reference").textContent = gcash_reference
        checkout_complete = True
        cart.clear()
        save_cart()
        render_cart()
        cart_notice = document.getElementById("cart-notice")
        if not ffi.is_none(cart_notice):
            cart_notice.hidden = True
        checkout_form.reset()
        reset_gcash_payment()
        document.getElementById("checkout-entry").hidden = True
        document.getElementById("checkout-success").hidden = False
        document.getElementById("checkout-title").textContent = "Your order"
        checkout_popup.scrollTop = 0
        document.getElementById("checkout-success-title").focus(ffi.to_js({"preventScroll": True}))

    @when("keydown", "#checkout-dialog")
    def keep_keyboard_inside_checkout(event):
        if event.key != "Tab":
            return
        controls = []
        for control in checkout_popup.querySelectorAll("button:not([disabled]), input, textarea, a[href]"):
            if len(control.getClientRects()) > 0:
                controls.append(control)
        first_control = controls[0]
        last_control = controls[len(controls) - 1]
        active = document.activeElement
        heading = document.getElementById("checkout-success-title")
        if active.isSameNode(heading):
            event.preventDefault()
            if event.shiftKey:
                last_control.focus()
            else:
                first_control.focus()
        elif event.shiftKey and active.isSameNode(first_control):
            event.preventDefault()
            last_control.focus()
        elif not event.shiftKey and active.isSameNode(last_control):
            event.preventDefault()
            first_control.focus()

    @when("pointerdown", "#checkout-dialog")
    def remember_checkout_press(event):
        global checkout_press_started_outside
        checkout_press_started_outside = False
        if event.target.isSameNode(checkout_popup):
            checkout_press_started_outside = press_is_outside_checkout(event)

    @when("click", "#checkout-dialog")
    def close_checkout_from_background(event):
        global checkout_press_started_outside
        if checkout_press_started_outside and event.target.isSameNode(checkout_popup):
            if press_is_outside_checkout(event):
                checkout_popup.close()
        checkout_press_started_outside = False


contact_form = document.getElementById("concernForm")

if not ffi.is_none(contact_form):

    @when("submit", "#concernForm")
    def check_contact_message(event):
        event.preventDefault()

        message_box = document.getElementById("concern-message")
        response_label = document.getElementById("responseMessage")
        message = message_box.value.strip()

        if message == "":
            response_label.textContent = "Please enter a message before submitting."
            message_box.focus()
        else:
            response_label.textContent = (
                "Your message has been checked. It has not been sent."
            )
            contact_form.reset()


scroll_selector = (
    ".hero-copy,.hero-image,.section-head,.product-card,.more-snacks,"
    ".visit-grid > div,.concern-section,.footer-top,.footer-bottom,"
    "main > .hero:not(#home),.menu-heading,.food-grid > .food-card,"
    ".order-note,footer:not(.site-footer)"
)
scroll_items = document.querySelectorAll(scroll_selector)
motion_setting = window.matchMedia("(prefers-reduced-motion: reduce)")
scroll_observer = None


def show_or_hide_scroll_items(entries, observer):
    for entry in entries:
        if entry.isIntersecting and entry.intersectionRatio >= 0.08:
            entry.target.classList.add("is-visible")
        else:
            entry.target.classList.remove("is-visible")


def set_up_scroll_animation(event=None):
    global scroll_observer

    if scroll_observer is not None:
        scroll_observer.disconnect()
        scroll_observer = None

    if motion_setting.matches or not hasattr(window, "IntersectionObserver"):
        for item in scroll_items:
            item.classList.remove("scroll-reveal", "is-visible")
        return

    observer_settings = {
        "threshold": [0, 0.08],
        "rootMargin": "0px 0px -24px 0px",
    }
    browser_settings = ffi.to_js(observer_settings)
    scroll_observer = window.IntersectionObserver.new(
        scroll_callback, browser_settings
    )

    for item in scroll_items:
        item.classList.add("scroll-reveal")
        scroll_observer.observe(item)


scroll_callback = ffi.create_proxy(show_or_hide_scroll_items)
motion_callback = ffi.create_proxy(set_up_scroll_animation)
motion_setting.addEventListener("change", motion_callback)
set_up_scroll_animation()


def finish_loading():
    food_buttons = document.querySelectorAll(".product-open, .cart-open")
    for button in food_buttons:
        button.disabled = False

    if not ffi.is_none(contact_form):
        send_button = contact_form.querySelector('button[type="submit"]')
        send_button.disabled = False

    for message_id in ["menu-status", "contact-status"]:
        loading_message = document.getElementById(message_id)
        if not ffi.is_none(loading_message):
            loading_message.hidden = True

    document.documentElement.dataset.snackspotReady = "true"


finish_loading()
