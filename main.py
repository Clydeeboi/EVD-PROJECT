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
    price_label.value = show_pesos(price)

    summary = size["label"] + " · " + flavor
    if current_food == "drinks":
        summary = summary + " · " + size["detail"]

    document.getElementById("product-selection").textContent = summary

    saved_choices[current_food] = {
        "size": size_number,
        "flavor": flavor_number,
    }


def show_food_information(food_button, food):
    food_card = food_button.closest(".product-card")
    card_picture = food_card.querySelector("img")
    popup_picture = document.getElementById("product-image")

    popup_picture.src = card_picture.getAttribute("src")
    popup_picture.alt = card_picture.alt

    document.getElementById("product-title").textContent = food["name"]
    document.getElementById("product-category").textContent = food["category"]
    document.getElementById("product-description").textContent = food["description"]
    document.getElementById("product-size-label").textContent = food["size_label"]


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

        show_food_information(food_button, food)
        show_size_choices(food, saved_size)
        show_flavor_choices(food, saved_flavor)
        update_price()

        document.body.classList.add("product-dialog-open")
        popup.showModal()

        close_button = document.getElementById("product-close")
        focus_settings = ffi.to_js({"preventScroll": True})
        close_button.focus(focus_settings)

    @when("change", "#product-dialog")
    def change_food_option(event):
        update_price()

    @when("click", "#product-close, #product-done")
    def close_food_popup(event):
        popup.close()

    @when("keydown", "#product-dialog")
    def keep_keyboard_inside_popup(event):
        if event.key != "Tab":
            return

        controls = popup.querySelectorAll(
            'button:not([disabled]), input[type="radio"]:checked'
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
                "Thank you! This is a demo confirmation; your message has not been sent."
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
    food_buttons = document.querySelectorAll(".product-open")
    for button in food_buttons:
        button.disabled = False

    if not ffi.is_none(contact_form):
        send_button = contact_form.querySelector('button[type="submit"]')
        send_button.disabled = False

    loading_message = document.getElementById("menu-status")
    if not ffi.is_none(loading_message):
        loading_message.hidden = True

    document.documentElement.dataset.snackspotReady = "true"


finish_loading()
