from flet import *
import flet_easy as fs
import sqlite3



app = fs.FletEasy(route_init='/')



class PageStandart():
    def __init__(self, page, title:str, padding:int=0, spacing:int=0):
        self.page = page
        self.title = title
        self.padding = padding
        self.spacing = spacing
    
    
    def return_page(self):
        self.page.title = self.title
        self.page.padding = self.padding
        self.page.spacing = self.spacing
        
        return self.page
    

class ColorPage():
    purple = colors.DEEP_PURPLE_600
    card_color = colors.BACKGROUND
    bgcolor = colors.BLACK
    text = colors.WHITE


class CardTemplate():
    def __init__(self, page, id:int, number:str, date:str, cvv:str, owner:str, bank_name:str):
        self.id = id
        self.number = number
        self.date = date
        self.cvv = cvv
        self.owner = owner
        self.bank = bank_name
        
        self.page = page
        


    def page_reload_exstra(self):
        self.page.go('/add')
        self.page.go('/')
    
    
    def page_go_edit(self):
        self.page.client_storage.set("card_id", self.id)
        self.page.go('/edit')
        

    def delete_btn(self):
        conn = sqlite3.connect('baza.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cards WHERE id = ?", (str(self.id)))
        conn.commit()
        self.page.update()
        self.page_reload_exstra()

        
        
    def build(self):
        return CupertinoContextMenu(
            enable_haptic_feedback=True,
            content=Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Container(
                                # height=170,
                                width=320,
                                bgcolor=ColorPage.card_color,
                                adaptive=True,
                                border_radius=8,
                                # alignment=alignment.center,
                                padding=padding.only(top=10),
                                content=Column(
                                    controls=[
                                        Container(
                                            alignment=alignment.center,
                                            padding=padding.only(top=10),
                                            content=Text(self.number, selectable=True),
                                        ),
                                        Container(
                                            alignment=alignment.center,
                                            padding=padding.only(top=5),
                                            content=Text(self.date, selectable=True)
                                        ),
                                        
                                        Container(
                                            content=Row(
                                                controls=[
                                                    Container(
                                                        padding=padding.only(top=25),
                                                        content=Text(self.owner, selectable=True)
                                                    ),
                                                    Container(
                                                        padding=padding.only(top=25),
                                                        content=Text(self.bank, selectable=True)
                                                    ),
                                                ],
                                                alignment=MainAxisAlignment.SPACE_AROUND
                                            ),
                                                padding=padding.only(bottom=20)
                                        ),
                                        
                                    ],
                                    ),
                            ),
                            Text(value=self.id, visible=False),
                        ],
                    ),
            actions=[
                CupertinoContextMenuAction(
                    text="Edit card",
                    is_default_action=False,
                    is_destructive_action=False,
                    trailing_icon=icons.EDIT,
                    on_click=lambda _: self.page_go_edit(),
                    
                    # on_click=lambda _: self.page.go('/edit'),
                ),
                CupertinoContextMenuAction(
                    text="Delete card",
                    is_default_action=False,
                    is_destructive_action=False,
                    trailing_icon=icons.DELETE_FOREVER,
                    on_click=lambda _: self.delete_btn(),

                    
                    # on_click=lambda _: self.page.go('/edit'),
                ),
            ],
        )
        
        
class TextInput():
    def __init__(self, lable:str):
        self.lable = lable
    
    def build(self):
        return TextField(
            label=self.lable,
            adaptive=True,
            cursor_color=ColorPage.purple,
            cursor_width=3,
            border_color=ColorPage.purple,
            selection_color=ColorPage.purple,
            bgcolor=ColorPage.card_color,
            focused_border_color=ColorPage.purple,
            )



def create_conn_db():
    conn = sqlite3.connect('baza.db')    
    return conn


def create_db():
    conn = create_conn_db()
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS cards (
                    id INTEGER PRIMARY KEY,
                    number TEXT,
                    data TEXT,
                    cvv TEXT,
                    owner TEXT,
                    bank TEXT
                  )''')
    conn.commit()
    conn.close()
    

create_db()


@app.page(route='/')
def home(data:fs.Datasy):
    page = data.page
    PageStandart(page, 'HOME').return_page()

    def appbar_page(title:str, color):
        return AppBar(
                title = Text(title),
                center_title = True,
                bgcolor = color,
                adaptive = True,
            )
    
    
    
    card_list = Column(
        alignment=MainAxisAlignment.CENTER,
        controls=[],
        )
    
    
    conn = create_conn_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM cards")
    rows = cursor.fetchall()
    cards = []
    for row in rows:
        cards.append(row)
        

    
    conn.close()

    
    for row in cards:
        card_list.controls.append(CardTemplate(page, row[0], row[1], row[2], row[3], row[4], row[5]).build())
    

    page.update()
    #                          \\id
    # print(card_list.controls[1].controls[-1].value)
    
    
    
    def bottom_appbar_page():
        return BottomAppBar(
            bgcolor=ColorPage.purple,
            shape=NotchShape.CIRCULAR,
            content=Row(
                controls=[
                    IconButton(icon=icons.MENU, icon_color=ColorPage.text),
                    Container(expand=True),
                    IconButton(icon=icons.ADD, icon_color=ColorPage.text, on_click=lambda _: page.go('/add')),
                    Container(expand=True),
                    IconButton(icon=icons.FAVORITE, icon_color=ColorPage.text),
                ]
            ),
        )
    
    
    interface = View(
        route='/',
        appbar=appbar_page('Choose your Card', color=ColorPage.purple),
        bottom_appbar=bottom_appbar_page(),
        scroll=True,
        adaptive=True,
        bgcolor=ColorPage.bgcolor,
        controls=[
                Column(
                    horizontal_alignment=MainAxisAlignment.CENTER,
                    controls=[
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            card_list
                        ],
                        
                ),
                ],
            ),
        ],
    )
    
    return interface




@app.page(route='/add')
def add(data:fs.Datasy):
    page = data.page
    PageStandart(page, 'ADD').return_page()
    
        
    def add_card(e):
        conn = create_conn_db()
        
        conn.cursor().execute("INSERT INTO cards (number, data, cvv, owner, bank) VALUES (?, ?, ?, ?, ?)", (pay_info.value, pay_data.value, pay_cvv.value, pay_owner.value, pay_bank.value))
        conn.commit()
        
        pay_info.value = ''
        pay_data.value = ''
        pay_cvv.value = ''
        pay_owner.value = ''
        pay_bank.value = ''
        
        conn.close()
        page.update()
        
        
        
    def appbar_page(title:str, color):
        return AppBar(
                title = Text(title),
                center_title = True,
                bgcolor = color,
                adaptive = True,
                leading=Container(
                    IconButton(icon=icons.ARROW_BACK_IOS_NEW_OUTLINED,
                                icon_color=ColorPage.text,
                                on_click=lambda _: page.go('/')
                                            ),
                                )
            )

    
    pay_info = TextInput('pay info').build()
    pay_data = TextInput('pay data').build()
    pay_cvv = TextInput('pay cvv').build()
    pay_owner = TextInput('pay owner').build()
    pay_bank = TextInput('bank').build()
    

    
    interface = View(
        route='/add',
        appbar=appbar_page('Add pay Informayion', color=ColorPage.purple),
        adaptive=True,
            
        controls=[
            Column(
                horizontal_alignment=MainAxisAlignment.CENTER,
                controls=[
                    Container(
                            alignment=alignment.center,
                            padding=padding.only(top=20),
                            content=Column(
                                alignment=MainAxisAlignment.CENTER,
                                controls=[
                                    Container(
                                        alignment=alignment.center,
                                        padding=padding.only(top=10),
                                        content=pay_info
                                    ),
                                    Container(
                                        alignment=alignment.center,
                                        padding=padding.only(top=20),
                                        content=pay_data
                                    ),
                                    Container(
                                        alignment=alignment.center,
                                        padding=padding.only(top=20),
                                        content=pay_cvv
                                    ),
                                    Container(
                                        alignment=alignment.center,
                                        padding=padding.only(top=20),
                                        content=pay_owner
                                    ),
                                    Container(
                                        alignment=alignment.center,
                                        padding=padding.only(top=20),
                                        content=pay_bank
                                    ),
                                    ],

                            ),
                            ),
                ]
            ),
        ],
        floating_action_button = FloatingActionButton(
            alignment=MainAxisAlignment.CENTER, spacing=5,
            bgcolor=ColorPage.purple,
            on_click=add_card,
            width=300,
            shape=RoundedRectangleBorder(radius=10),
            content=Row(
            [
                Icon(icons.ADD_CARD_ROUNDED, color=ColorPage.text),
                Text("Add", color=ColorPage.text)
                ],
        ),
            ),
            
        floating_action_button_location= FloatingActionButtonLocation.MINI_CENTER_FLOAT
        
    )
    
    return interface





@app.page(route='/edit')
def add(data:fs.Datasy):
    page = data.page
    PageStandart(page, 'EDIT').return_page()
       
        
    def appbar_page(title:str, color):
        return AppBar(
                title = Text(title),
                center_title = True,
                bgcolor = color,
                adaptive = True,
                leading=Container(IconButton(icon=icons.ARROW_BACK_IOS_NEW_OUTLINED,
                                icon_color=ColorPage.text,
                                on_click=lambda _: page.go('/')
                                            ),
                                )
            )


    def save_card_changes(e):
        conn = create_conn_db()
        cursor = conn.cursor()
    
        cursor.execute(f"UPDATE cards SET number = ?,  data = ?,  cvv = ?, owner = ?,  bank = ? WHERE id = {str(page.client_storage.get('card_id'))}", (pay_info.value, pay_data.value, pay_cvv.value, pay_owner.value, pay_bank.value))
        
        conn.commit()
        conn.close()

        page.go('/')

    

    conn = create_conn_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM cards WHERE id = ?", str(page.client_storage.get('card_id')))
    card_id = cursor.fetchone()
    
    print(card_id)
    
    conn.close()

    
    pay_info = TextInput('pay info').build()
    pay_data = TextInput('pay data').build()
    pay_cvv = TextInput('pay cvv').build()
    pay_owner = TextInput('pay owner').build()
    pay_bank = TextInput('bank').build()
    
    pay_info.value = card_id[1]
    pay_data.value = card_id[2]
    pay_cvv.value = card_id[3]
    pay_owner.value = card_id[4]
    pay_bank.value = card_id[5]

    
    
    interface = View(
        route='/edit',
        appbar=appbar_page('Edit pay Informayion', color=ColorPage.purple),
        adaptive=True,
            
        controls=[
            Column(
                horizontal_alignment=MainAxisAlignment.CENTER,
                controls=[
                    Container(
                            alignment=alignment.center,
                            padding=padding.only(top=20),
                            content=Column(
                                alignment=MainAxisAlignment.CENTER,
                                controls=[
                                    Container(
                                        alignment=alignment.center,
                                        padding=padding.only(top=10),
                                        content=pay_info
                                    ),
                                    Container(
                                        alignment=alignment.center,
                                        padding=padding.only(top=20),
                                        content=pay_data
                                    ),
                                    Container(
                                        alignment=alignment.center,
                                        padding=padding.only(top=20),
                                        content=pay_cvv
                                    ),
                                    Container(
                                        alignment=alignment.center,
                                        padding=padding.only(top=20),
                                        content=pay_owner
                                    ),
                                    Container(
                                        alignment=alignment.center,
                                        padding=padding.only(top=20),
                                        content=pay_bank
                                    ),
                                    ],

                            ),
                            ),
                ]
            ),
        ],
        floating_action_button = FloatingActionButton(
            bgcolor=ColorPage.purple,
            on_click=save_card_changes,
            width=300,
            shape=RoundedRectangleBorder(radius=10),
            content=Row(
            alignment=MainAxisAlignment.CENTER,
            spacing=5,
            content = [
                Icon(icons.SAVE, color=ColorPage.text),
                Text("Save", color=ColorPage.text)
                ],
        ),
            ),
            
        floating_action_button_location= FloatingActionButtonLocation.MINI_CENTER_FLOAT
        
    )
    
    return interface






app.run()



