import flet as ft

async def main(page: ft.Page):
    # Function to add a new option to the dropdown
    async def add_option(e):
        new_value = txt_field.value
        if new_value:
            dropdown.options.append(ft.dropdown.Option(new_value))
            txt_field.value = ""  # Clear the text field after adding the new option
            page.update()

    # Define the dropdown with initial options
    dropdown = ft.Dropdown(
        width=200,
        options=[
            ft.dropdown.Option("a"),
            ft.dropdown.Option("b"),
            ft.dropdown.Option("c"),
        ],
    )

    # Define the text field for inputting a new option
    txt_field = ft.TextField(label="Add new option")

    # Define the button to trigger the addition of a new option
    add_button = ft.ElevatedButton("Add Option", on_click=add_option)

    # Add all controls to the page
    page.add(
        dropdown,
        txt_field,
        add_button,
    )

# Run the application
ft.app(target=main)
