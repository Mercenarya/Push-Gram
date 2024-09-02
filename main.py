import flet as ft
import sqlite3
from flet import View
from deep_translator import GoogleTranslator
import time
import random



#Database Connection

db = sqlite3.connect('telegram-trans.db',check_same_thread=False)
cursor = db.cursor()

#Test connection


class Note(ft.Column):
    def __init__(self,Title,Text,Delete):
        super().__init__()
        self.title = Title
        self.Text = Text
        self.Delete = Delete
        self.Language = ft.TextField(width=100,border_color="white",color="white",text_size=15,height=50,border_radius=20)
        
        self.Translator = ft.Dropdown(
            options=[
                ft.dropdown.Option("vietnamese"),
                ft.dropdown.Option("english"),
                ft.dropdown.Option("russian"),
                ft.dropdown.Option("chinese (traditional)"),
                ft.dropdown.Option("french"),
            ],
            width=150,
            text_size=12,
            border_color="white",
            text_style=ft.TextStyle(color="white"),
            color=ft.TextStyle(color="black"),
            bgcolor="grey"
        )

        self.lans_dict = GoogleTranslator().get_supported_languages(as_dict=False)

        for lang in self.lans_dict:
            self.Translator.options.append(
                ft.dropdown.Option(f"{lang}")
            )
        
        
        self.Progress = ft.Column(
            [
                ft.Text("Translating...",size=10,color="white"),
                ft.ProgressBar(width=200,color="white"),
            ],
            visible=False
        )

        self.Translated = ft.Column(
            scroll=ft.ScrollMode.HIDDEN,
            visible=False
        )


        self.Display_title = ft.Text(value=self.title, color="white", size=13,weight="bold",width=200)
        self.Display_text = ft.Text(value=self.Text,color="white",size=15)
        self.Edit_text = ft.TextField(value=self.Display_text.value,border_color="grey",
                                      color="white",text_size=15,multiline=True)
        

        self.Copy_clipboard = ft.IconButton(ft.icons.CONTENT_COPY,on_click=self.Copy_to_clipboard,
                                            icon_color="lightblue",)

        self.Copied_Annoucement = ft.SnackBar(
            content=ft.Text("Copied !!!")
        )

        self.Deleted_Annoucement = ft.SnackBar(
            content=ft.Text("Post Deleted !!!")
        )
        
        #this mode will activate if title have filled with a link code
        #Allow user store and access the original link to find the pure-prototype (post)

        self.Open_link = ft.Text(
            spans=[
                ft.TextSpan(
                    "open link",
                    ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE,color="white"),
                    url=f"{self.Display_title.value}",
                )
            ]
        )
        self.BoxText = ft.Container(
            ft.Row(
                [
                    ft.Text(
                        f"{self.Display_title.value}",
                        weight="bold",
                        color="white",
                        size=15,
                        width=150
                    ),
                    ft.TextButton("Open",on_click=self.Open_Note_Box,style=ft.ButtonStyle(color="white"))
                ],
                alignment='spacebetween'
            ),
            padding=20,
            height=60,
            bgcolor="black",
            border_radius=20,
            margin=ft.margin.only(bottom=-20)
        )

        self.trans_text = ft.Text(color="white",size=15)

        self.Textline = ft.Container(
            ft.Column(
                [
                    self.Display_text,
                
                ],
                height=400,
                scroll=ft.ScrollMode.HIDDEN,
            ),
            
            height=300,
            width=2000,
            bgcolor="Grey",
            padding=20,
            border_radius=15
            
            
        )
        self.Edit_Textline = ft.Container(
            ft.Column(
                [
                    self.Edit_text
                ],
                width=2000,
                height=300,
                scroll=ft.ScrollMode.HIDDEN,
            ),
            
            height=300,
            width=2000,
            bgcolor="Grey",
            padding=15,
            border = ft.border.BorderSide(1,"grey"),
            border_radius=15
            
        )

        self.Trans_Textline = ft.Container(
            ft.Column(
                [
                    self.trans_text
                ],
                # width=400,
                height=300,
                scroll=ft.ScrollMode.HIDDEN,
            ),
            
            height=300,
            width=2000,
            bgcolor="Grey",
            padding=15,
            border = ft.border.BorderSide(1,"grey"),
            border_radius=15
            
        )

        self.Back_to_box_btn = ft.TextButton("Close", on_click=self.Back_to_box,style=ft.ButtonStyle(color="white"))

        self.Display_Note = ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            self.Back_to_box_btn,
                            self.Open_link,
                        ],
                        alignment="spacebetween"
                    ),
                    
                    self.Textline,
                    ft.Row(
                        [
                            ft.ElevatedButton("Delete",bgcolor="grey",color="white",on_click=self.Delete_note),
                            ft.ElevatedButton("Edit",bgcolor="Grey",color="white",on_click=self.Edit_Note),
                            ft.ElevatedButton("Translate",bgcolor="grey",color="white",on_click=self.keyword_Note)
                        ],
                        alignment = ft.MainAxisAlignment.CENTER
                    )
                ]
            ),
            # width=450,
            bgcolor="black",
            padding=20,
            height=450,
            border = ft.border.BorderSide(1,"grey"),
            border_radius=15,
            visible=False
            
        )

        self.Edit_Note_text = ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            self.Back_to_box_btn,
                            self.Open_link,
                        ],
                        alignment="spacebetween"
                    ),
                    self.Edit_Textline,
                    ft.Row(
                        [
                            ft.ElevatedButton("Delete",bgcolor="grey",color="white",on_click=self.Delete_note),
                            ft.ElevatedButton("Save",bgcolor="grey",color="white",on_click=self.Save_Note)
                        ],
                        alignment = ft.MainAxisAlignment.CENTER
                    )
                ]
            ),
            
            # width=450,
            bgcolor="black",
            padding=20,
            height=450,
            visible=False,
            border = ft.border.BorderSide(1,"grey"),
            border_radius=15
        )
        self.Keyword_Search = ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            self.Back_to_box_btn,
                            self.Open_link,
                        ],
                        alignment="spacebetween"
                    ),
                    self.Trans_Textline,
                    ft.Column(
                        [  
                            ft.Row(
                                [   
                                    ft.ElevatedButton("Trans",color="white",bgcolor="grey",on_click=self.Keyword_trans,
                                                      icon=ft.icons.TRANSLATE,icon_color="white"),
                                    ft.Text("To: ",size=15,color="white"),
                                    self.Translator
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.Row(
                                [
                                    self.Progress
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            self.Translated,
                            ft.Container(
                                ft.Row(
                                    [
                                        ft.ElevatedButton('Back',color="white",bgcolor="grey",on_click=self.Back_event_keyword),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
                                margin=ft.margin.only(top=5)
                            )

                        ],
                        # width=520,
                        scroll=ft.ScrollMode.HIDDEN
                        
                    )
                    
                ],
                scroll=ft.ScrollMode.HIDDEN
                
               
            ),
            # width=450,
            bgcolor="black",
            padding=20,
            height=600,
            visible=False,
            border = ft.border.BorderSide(1,"grey"),
            border_radius=15,
        )
        self.controls = [self.Display_Note,self.BoxText, self.Edit_Note_text,self.Keyword_Search,self.Copied_Annoucement,self.Deleted_Annoucement]


    def Open_copied_announcement(self, e):
        self.Copied_Annoucement.open = True
        self.update()

    def Open_deleted_announcement(self, e):
        self.Deleted_Annoucement.open = True
        self.update()
    
        
    def Copy_to_clipboard(self, e):
        self.page.set_clipboard(self.translated_text.value)
        self.Open_copied_announcement(e)
        self.update()

    def Delete_note(self, e):
        Remove_Note = f''' DELETE FROM note WHERE title = '{self.Display_title.value}' '''
        self.Open_deleted_announcement(e)
        try:
            cursor.execute(Remove_Note)
            db.commit()
        except sqlite3.Error as error:
            print(error)
        self.Delete(self)
    
    #Throw result when user assign a new title
    def Check_open_link(self, e):
        if "https://" in self.Display_title.value:
            print("true")
        if "https://" not in self.Display_title.value:
            print("false")
        self.update()
        
    def Open_Note_Box(self, e):
        self.BoxText.visible = False
        self.Display_Note.visible = True
        self.update()
    
    def Back_to_box(self,e):
        self.BoxText.visible = True
        self.Display_Note.visible = False
        self.Edit_Note_text.visible = False
        self.Keyword_Search.visible = False
        self.update()

    def Edit_Note(self, e):
        self.Display_Note.visible = False
        self.Edit_Note_text.visible = True
        self.update()

    def Save_Note(self,e):
        Edit_Query = f'''UPDATE note SET textiled = '{self.Edit_text.value}' WHERE title = '{self.Display_title.value}' '''
        try:
            cursor.execute(Edit_Query)
            print("Note Updated")
            db.commit()
        except sqlite3.Error as error:
            print(error)
        self.Display_text.value = self.Edit_text.value
        self.trans_text.value = self.Edit_text.value
        self.Display_Note.visible = True
        self.Edit_Note_text.visible = False
        self.update()

    def keyword_Note(self,e):
        self.Display_Note.visible = False
        self.trans_text.value = self.Edit_text.value
        self.Keyword_Search.visible = True
        self.update()


    def Keyword_trans(self, e):
        try:
            self.loading(e)
            self.Progress.visible=False
            translation = GoogleTranslator(target=f"{self.Translator.value}")
            reavel = translation.translate(self.Edit_text.value)
            self.translated_text = ft.TextField(value=reavel,color="white",read_only=True,border_color="black",multiline=True) 
            self.Keyword_Search.height=600
            self.Translated.visible = True
            self.Translated.controls.clear()
            self.Translated.controls.append(
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(value=self.Translator.value,color="white",size=20,weight="bold"),
                                self.Copy_clipboard,
                            ],
                            alignment="spacebetween"
                        ),
                        self.translated_text
                    ]
                )
            )
        except:
            self.translated_text.value = f"{self.Translator.value} cannot be a language,\nPlease check your corrected target language"
        self.update()

    def loading(self,e):
        self.Progress.visible=True
        self.Keyword_Search.height=600
        time.sleep(3)
        self.update()

    def Back_event_keyword(self, e):
        self.Keyword_Search.visible = False
        self.Display_Note.visible = True
        self.Display_text.color = "white"
        self.update()

    def Back_event_Edit(self, e):
        self.Edit_Note_text.visible = False
        self.Display_Note.visible = True
        self.Display_text.color = "white"
        self.update()
    
    
        

class NotedApp(ft.Column):
    def __init__(self):
        super().__init__()
        

        self.Note_title = ft.TextField(border_color="white",hint_text="Title",
                                       color="white",hint_style=ft.TextStyle(color="white"))
        self.Note_textField = ft.TextField(value="",border_color="black",hint_text="Textline...",
                                           multiline=True,hint_style=ft.TextStyle(color="white"),
                                           min_lines=1,max_lines=4,color="white")
        

        self.Field_Pad = ft.Container(
            self.Note_textField,
            height=140,
            border=ft.border.all(1,"white")
        )
        self.Note_list = ft.Column(
            [
                
            ],
            height=710,
            scroll=ft.ScrollMode.HIDDEN
        )

        self.OpenNoteBar = ft.Container(width=100,height=10,bgcolor="grey",on_click=self.Note_TopBar_Open,visible=True)
        self.CloseNoteBar = ft.Container(width=100,height=10,bgcolor="grey",on_click=self.Note_TopBar_close,visible=False)

    
        cursor.execute("SELECT * FROM note")
        for objn in cursor.fetchall():
            self.Note_list.controls.append(
                Note(objn[0],objn[1],self.Delete_note)
            )
        db.commit()

        self.Search_button = ft.IconButton(ft.icons.SEARCH,icon_color="white",)
        
        self.Search_field = ft.TextField(bgcolor=None,width=300,border_color="white",border_radius=30,prefix_icon=ft.icons.SEARCH,
                                         color="white",on_change=self.Search_Result)
        self.Dialog_post = ft.AlertDialog(
            modal=True,
            title=ft.Text("Warning"),
            content=ft.Text("Cannot append this form to stack"),
            actions=[
                ft.TextButton("Got it", on_click=self.Close_Dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )

        self.Dialog_post_2 = ft.AlertDialog(
            modal=True,
            title=ft.Text("Warning"),
            content=ft.Text("The text titles already exist."),
            actions=[
                ft.TextButton("Got it", on_click=self.Close_Dialog_2),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        self.New_Post_annoucement = ft.SnackBar(
            content=ft.Text("new post released !!!")
        )

        self.NoteSearchBar = ft.Container(
                ft.Column(
                    [
                        
                        ft.Row(
                            [
                                ft.IconButton(ft.icons.TELEGRAM,icon_color="white",on_click= None),
                                ft.Text("PushGram",color="white",size=25,weight="bold"),
                                ft.IconButton(ft.icons.POST_ADD,icon_color="white",on_click=self.Add_post)
                                
                            ],
                            alignment="spaceBetween",
                        ),
                        ft.Row(
                            [
                                self.Search_field
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ]
                ),
                border_radius=ft.border_radius.vertical(
                bottom=25
            ),
            bgcolor="black",
            height=59,
            padding=10,
            shadow= ft.BoxShadow(
                blur_radius=3,
                color="black",
                blur_style=ft.ShadowBlurStyle.OUTER
            ),
            animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT),
            visible=False
        )

        self.NoteBar = ft.Container(
                ft.Column(
                    [
                        
                        ft.Row(
                            [
                                ft.IconButton(ft.icons.TELEGRAM,icon_color="white",on_click=None ),
                                ft.Text("PushGram",color="white",size=25,weight="bold"),
                                ft.IconButton(ft.icons.SEARCH,icon_color="white",on_click=self.Search_post)
                                
                            ],
                            alignment="spaceBetween",
                        ),
                        
                        self.Note_title,
                        self.Field_Pad,
                        
                        ft.Row(
                            [
                                ft.FloatingActionButton(
                                    icon=ft.icons.ADD, on_click=self.Add_note,
                                ),
                                ft.FloatingActionButton(
                                    icon=ft.icons.DELETE, on_click=self.Clear_Field
                                ),
                                
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        
                    ]
                ),
                border_radius=ft.border_radius.vertical(
                bottom=25
            ),
            bgcolor="black",
            # width=400,
            height=59,
            padding=10,
            shadow= ft.BoxShadow(
                blur_radius=3,
                color="black",
                blur_style=ft.ShadowBlurStyle.OUTER
            ),
            animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT),
        )

        self.controls = [
            self.NoteBar,
            self.NoteSearchBar,
            
            ft.Row(
                [
                    self.OpenNoteBar,
                    self.CloseNoteBar
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            self.Note_list,
            self.Dialog_post,
            self.Dialog_post_2,
            self.New_Post_annoucement
            
        ]
        
        self.Search_List = []
        try:
            cursor.execute("SELECT * FROM note")
            for obj in cursor.fetchall():
                self.Search_List.append(
                    {"title":obj[0],"content":obj[1]}
                )
            print(self.Search_List)
            db.commit()
        except Exception as error:
            print(error)

    def Link_random(self, e):
        self.page.launch_url("https://shopee.vn/")
        self.update()

    def Search_Result(self, e):
        self.Note_list.controls.clear()
        for part in self.Search_List:
            if self.Search_field.value in part["title"] or self.Search_field.value in part["content"]:
                self.Note_list.controls.append(
                    Note(part['title'],part['content'], self.Delete_note)
                )
        self.update()
    def Close_Dialog(self,e):
        self.Dialog_post.open = False
        self.update()
    def Close_Dialog_2(self,e):
        self.Dialog_post_2.open = False
        self.update()

    def Add_note(self, e):
        
        note = Note(self.Note_title.value,self.Note_textField.value, self.Delete_note)
        self.Search_List.append( {"title":self.Note_title.value,"content":self.Note_textField.value})
        index_tub = [self.Note_title.value, self.Note_textField.value]
        Query_index = '''INSERT INTO note (title, textiled) VALUES (?,?)'''
        try:
            if self.Note_title.value == "" or self.Note_textField.value == "":
                self.Dialog_post.open = True
            elif self.Note_title.value == "" and self.Note_textField.value == "":
                self.Dialog_post.open = True
            else:
                cursor.execute(Query_index,index_tub)
                
                self.Note_title.value = ""
                self.Note_textField.value = ""
                self.Note_list.controls.append(note)
                self.New_Post_annoucement.open = True
            db.commit()
        except sqlite3.Error as error:
            self.Dialog_post_2.open = True

        time.sleep(2)
        self.Link_random(e)
        self.update()

    def Search_post(self,e):
        self.NoteBar.visible = False
        self.NoteSearchBar.visible = True
        self.update()

    def Add_post(self,e):
        self.NoteBar.visible = True
        self.NoteSearchBar.visible = False
        self.Note_list.controls.clear()
        cursor.execute("SELECT * FROM note")

        for objn in cursor.fetchall():
            self.Note_list.controls.append(
                Note(objn[0],objn[1],self.Delete_note)
            )
        db.commit()
        self.update()


    def Delete_note(self, note):
        self.Note_list.controls.remove(note)
        self.update()

    def Clear_Field(self, e):
        self.Note_title.value = ""
        self.Note_textField.value = "\n\n\n"
        self.update()

    def Note_TopBar_Open(self, e):
        self.OpenNoteBar.visible = False
        self.CloseNoteBar.visible = True
        self.NoteSearchBar.height = 150 if self.NoteSearchBar.height == 59 else 59
        self.NoteBar.height = 360 if self.NoteBar.height == 59 else 59
        self.update()

    def Note_TopBar_close(self, e):
        self.OpenNoteBar.visible = True
        self.CloseNoteBar.visible = False
        self.NoteSearchBar.height = 59 if self.NoteSearchBar.height == 150 else 150
        self.NoteBar.height = 59 if self.NoteBar.height == 360 else 360
        self.update()




def main(page:ft.Page):
    def Selected_page(e):
        for index, page_nav in enumerate(page_stack):
            page_nav.visible = True if index == NavBar.selected_index else False
        page.update()

    NavBar = ft.CupertinoNavigationBar(
        selected_index=0,
        on_change=Selected_page,
        bgcolor=ft.colors.BLACK,
        inactive_color=ft.colors.WHITE54,
        active_color=ft.colors.WHITE,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.HOME, label="Home"),
            ft.NavigationDestination(icon=ft.icons.LIST, label="Dictionary"),
            ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Settings"),
        ],
    )


    
    #SETTINGS CUSTOMIZE AND ELEMENTS
    def Reload_app(e):
        # Clear the page
        Syncho(e)
        page.update()
    def Syncho(e):
        print("Update")
        page.clean()
        # asyncio.run(Upload_language(e))
        page.go("/Home")
        print("Complete")
        page.update()
    #Annoucement
    def Open_deleted_text_announcement(e):
        deleted_text_anounce.open = True
        page.update()

    def Open_deleted_word_announcement(e):
        deleted_word_anounce.open = True
        page.update()
    #Interacting functions 
    def Deleted_Text(e):
        Open_deleted_text_announcement(e)
        try:
            cursor.execute('DELETE FROM note')
            db.commit()
            
            
        except sqlite3.Error as error:
            print(error)
        page.update()
    def Deleted_Word(e):
        Open_deleted_word_announcement(e)
        try:
            cursor.execute('DELETE FROM word')
            db.commit()
            
            
        except sqlite3.Error as error:
            print(error)
        page.update()

    def Theme_selection(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        Theme_switch.label =(
            "Light" if page.theme_mode == ft.ThemeMode.LIGHT else "Dark"
        )
        
        page.update()

    def Open_theme_setting_layout(e):
        open_theme_button.visible = False
        close_theme_button.visible = True
        Theme_switch.visible = True
        Theme_layout.height = 150
        page.update()
    
    def close_theme_setting_layout(e):
        open_theme_button.visible = True
        close_theme_button.visible = False
        Theme_switch.visible = False
        Theme_layout.height = 80
        page.update()


    def Open_storage_setting_layout(e):
        open_storage_button.visible = False
        close_storage_button.visible = True
        Storage_layout.height = 200
        page.update()
    
    def close_storage_setting_layout(e):
        open_storage_button.visible = True
        close_storage_button.visible = False
        Storage_layout.height = 80
        page.update()

    #Update Theme Elements - controls - Switch
    Theme_switch = ft.Switch(label="Dark", on_change=Theme_selection,visible=False,
                             active_color="white",label_style=ft.TextStyle(color="white"))


    #Update Language Elements - controls - selection - input
    
    #Update Storage - button - controls
    
    Delete_Context = ft.IconButton(ft.icons.DELETE,icon_color="red",on_click=Deleted_Text)
    Delete_dictionary = ft.IconButton(ft.icons.DELETE,icon_color="red",on_click=Deleted_Word)



    #User's interact with button - select options - controls
    #button - language's Selection
    

    #button - theme's Selection
    open_theme_button = ft. IconButton(ft.icons.ARROW_RIGHT,visible=True,
                                          icon_color="white",icon_size=30,
                                          on_click=Open_theme_setting_layout)
    close_theme_button = ft. IconButton(ft.icons.ARROW_DROP_DOWN,visible=False,
                                           icon_color="white",icon_size=30,
                                           on_click=close_theme_setting_layout)
    


    #button - Storage's Selection
    open_storage_button = ft. IconButton(ft.icons.ARROW_RIGHT,visible=True,
                                          icon_color="white",icon_size=30,
                                          on_click=Open_storage_setting_layout)
    close_storage_button = ft. IconButton(ft.icons.ARROW_DROP_DOWN,visible=False,
                                           icon_color="white",icon_size=30,
                                           on_click=close_storage_setting_layout)

    
    new_lans_anounce = ft.SnackBar(
        content=ft.Text("New language uploaded, press 'Refresh'")
    )

    deleted_langs_anounce = ft.SnackBar(
        content=ft.Text("all uploaded languages deleted, press 'Refresh'")
    )
    deleted_text_anounce = ft.SnackBar(
        content=ft.Text("all text deleted, press 'Refresh'")
    )
    deleted_word_anounce = ft.SnackBar(
        content=ft.Text("Dictionary deleted, press 'Refresh'")
    )
    
    
    #container - language's Selection
    
    #container - Theme's Selection
    Theme_layout = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Theme mode", weight="bold", color="white"),
                        open_theme_button,
                        close_theme_button,
                        
                        
                    ],
                    alignment="spacebetween"
                ),
                Theme_switch
            ]
        ),
        height=80,
        # width=450,
        bgcolor="black",
        border_radius=20,
        padding=15,
        animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT), 
    )

    Storage_layout = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Storage", weight="bold", color="white"),
                        open_storage_button,
                        close_storage_button,
                        
                        
                    ],
                    alignment="spacebetween"
                ),
                ft.Row(
                    [
                        ft.Text("Delete all text",color="white"),
                        Delete_Context
                    ],
                    alignment="spacebetween"
                ),
                ft.Row(
                    [
                        ft.Text("Delete dictionary",color="white"),
                        Delete_dictionary
                    ],
                    alignment="spacebetween"
                )
                
            ]
        ),
        height=80,
        # width=450,
        bgcolor="black",
        border_radius=20,
        padding=15,
        animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT), 
    )
    Reboot_layout = ft.Container(
        ft.Row(
            [
                ft.Row(
                    [
                        ft.Text("Refresh",color="white",weight="bold"),
                        
                    ]
                ),
                ft.IconButton(ft.icons.RESTART_ALT,icon_color="white",on_click=Reload_app)
            ],
            alignment="spacebetween"
        ),
        height=80,
        # width=450,
        bgcolor="black",
        border_radius=20,
        padding=15,
    )

    

    ''' 
    SECOND PAGE HAVE STORED AND NOTED ANY WORDS OR CAPTION FROM
    TEXTLINE, ESPECIALLY, IT'S CAN HEP USER NOTED ALL TRANSLATED WORD - FORMAL WORD
    AS A LANGUAGE DICTIONARY
    '''

    #Second page
    def Open_Warning(e):
        Warning.open = True
        page.update()
    def Close_Warning(e):
        Warning.open = False
        page.update()
    Warning = ft.AlertDialog(
        modal=True,
        title=ft.Text("Warning"),
        content=ft.Text(value="Something went wrong with your selection, try again"),
        actions=[
            ft.TextButton("Got it",on_click=Close_Warning)
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER
    )
    # -- Noted word List --
    def Open_AddForm(e):
        Add_Form.open = True
        page.update()
    def Close_AddForm(e):
        Add_Form.open = False
        page.update()
    def New_word_translated(e):
        try:
            if Language_convert.value == "":
                Open_Warning(e)
            else:
                translation_target = GoogleTranslator(target=f"{Language_convert.value}")
                converted = translation_target.translate(Word_field.value)
                Converted_line.visible = True
                Converted_line.value = f"{Word_field.value}"
                Translated_line.visible = True
                Translated_line.value = f"{converted}"
                Translated_text_line.visible = True
                Translated_text_line.value = f"{Converted_line.value} : {Translated_line.value}"
        except Exception:
            Wordlist.controls.pop()
            Open_Warning(e)
        

        page.update()
   
    def Add_Wordlist_item(e):
        
        Wordlist_Announcement.visible = False
        Add_Form.open = False
        AddButton.visible = False
        Floatbutton.visible = True
        if Word_field.value == "" or Word_field.value.isnumeric() or Language_convert.value == "" :
            print("no field value")
            Open_Warning(e)
        else:
            try:
                New_word_translated(e)
                item2 = [Converted_line.value,Translated_line.value]
                cursor.execute("INSERT INTO word (items,trans) VALUES (?, ?)",item2)
                Wordlist.controls.append(
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text(value=Converted_line.value+" : "+Translated_line.value,color="white",width=250),
                                # ft.IconButton(ft.icons.VOLUME_DOWN,icon_color="blue",on_click=Speech_1)
                            ],
                            
                        ),
                        height=60,
                        width=340,
                        bgcolor="black",
                        padding=15,
                        border_radius=15
                    )
                )
                Keyword_list.append(
                    {"word":Converted_line.value,"trans":Translated_line.value}
                )
                print("2")
                db.commit()
            except sqlite3.Error as error:
                print(error)
        page.update()

    Word_field = ft.TextField(width=300,hint_text="New Word")
    Converted_line = ft.Text(visible=False)
    Translated_line = ft.Text(visible=False)
    lang_list = GoogleTranslator().get_supported_languages(as_dict=False)
    Language_convert = ft.Dropdown(
            options=[
                ft.dropdown.Option("vietnamese"),
                ft.dropdown.Option("english"),
                ft.dropdown.Option("russian"),
                ft.dropdown.Option("chinese (traditional)"),
                ft.dropdown.Option("french"),
            ],
            width=180,
            text_size=12
        )
    for lang in lang_list:
        Language_convert.options.append(
            ft.dropdown.Option(f"{lang}")
        )
    
    Submit_word = ft.IconButton(ft.icons.TRANSLATE,icon_color="white",bgcolor="grey",
                                icon_size=30,on_click=New_word_translated)
    Translated_text_line = ft.Text(visible=False)
    Add_Form = ft.AlertDialog(
        modal=True,
        content=ft.Column(
            [
                Word_field,
                ft.Row(
                    [
                        Language_convert,
                        Submit_word
                    ]
                ),
                Translated_text_line
                
            ],
            height=200
        ),
        actions=[
            ft.TextButton("Add",on_click=Add_Wordlist_item),
            ft.TextButton("Dismiss",on_click=Close_AddForm)
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER
        

    )


    


    Wordlist_Announcement = ft.Text("Add your\nnew note",color="grey",size=30,visible=True)
    AddButton = ft.IconButton(ft.icons.ADD,icon_color="white",
                            icon_size=50,bgcolor="grey",on_click=Open_AddForm,visible=True)

    Floatbutton = ft.FloatingActionButton(icon=ft.icons.ADD,
                            bgcolor="grey",on_click=Open_AddForm,visible=False)
    Wordlist = ft.Column(
        [
            Wordlist_Announcement,
            ft.Row(
                [
                    AddButton,
                    
                ],
                width=120,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            
        ],
        height=595,
        scroll=ft.ScrollMode.ALWAYS
    )
    def Display_wordlist_item(e):
        if len(Wordlist.controls[:]) == 0:
            Wordlist_Announcement.visible = True
            Add_Form.open = True
            AddButton.visible = True
            Floatbutton.visible = False
        else:
            Wordlist_Announcement.visible = False
            Add_Form.open = False
            AddButton.visible = False
            Floatbutton.visible = True
            try:
                cursor.execute("SELECT * FROM word")
                for objw in cursor.fetchall():
                    Wordlist.controls.append(
                            ft.Container(
                                ft.Row(
                                    [
                                        ft.Text(value=f"{objw[1]} : {objw[2]}",color="white",width=250),
                                        # ft.IconButton(ft.icons.VOLUME_DOWN,icon_color="blue",on_click=Speech_1)
                                    ],
                                    
                                ),
                                height=60,
                                width=340,
                                bgcolor="black",
                                padding=15,
                                border_radius=15
                            )
                        )
                db.commit()
            except sqlite3.Error as error:
                print(error)
        page.update()
    


    Keyword_list = []
    
    cursor.execute("SELECT * FROM word")
    try:
        for kw in cursor.fetchall():
            Keyword_list.append(
                {"word":kw[1],"trans":kw[2]}
            )
        db.commit()
    except Exception as error:
        print(error)

    def Search_keyword_result(e):
        
        Wordlist.controls.clear()
        for result in Keyword_list:
            if Search_keyword.value in result['word'] or Search_keyword.value in result['trans']:
                Wordlist.controls.append(
                    ft.Container(
                            ft.Row(
                                [
                                    ft.Text(value=f"{result['word']} : {result['trans']}",color="white",width=250),
                                    # ft.IconButton(ft.icons.VOLUME_DOWN,icon_color="blue",on_click=Speech_1)
                                ],
                                
                            ),
                            height=60,
                            width=340,
                            bgcolor="black",
                            padding=15,
                            border_radius=15
                        )
                )
            elif Search_keyword.value == "":
                Display_wordlist_item(e)

        page.update()
    Search_keyword = ft.Container(
        ft.TextField(width=350,border_radius=30,border_color="grey",on_change=Search_keyword_result,
                                prefix_icon=ft.icons.SEARCH,hint_text="Search..."),
        margin=ft.margin.only(top=15)
    )
            
    page_1 = ft.Container(
        ft.Column(
            [
                NotedApp()
            ]
        ),
        visible=True
    )
    page_2 = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        Search_keyword
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),                
                ft.Column(
                    [
                        ft.Row(
                            [
                                Wordlist
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Container(
                            ft.Row(
                            [
                                # Language_Speech,
                                    Floatbutton
                                ],
                                alignment=ft.MainAxisAlignment.END
                                
                            ),
                            padding=ft.padding.only(top=40)
                        )
                    ]
                )
                
            ]
        ),
        visible=False
    )

    


    page_3 = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Settings ",size=30),
                    ],
                    
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(color="grey"),
                Theme_layout,
                Storage_layout,
                Reboot_layout,
                ft.Divider(),
                ft.Container(
                    ft.Column(
                        [
                            ft.Text("Application details",size=20,weight="bold"),
                        ]
                    ),
                    padding=ft.padding.only(left=10)
                ),
                ft.Container(
                    ft.Column(
                        [
                            ft.Text("Version: 0.7.12",size=20),
                            ft.Text("SDK version: 0.4.10",size=20),
                            ft.Text("IPA version: 0.2.2",size=20),

                        ]
                    ),
                    padding=ft.padding.only(top=15,left=10)
                ),
                ft.Divider(),
                ft.Container(
                    ft.Column(
                        [
                            ft.Text("Developer details",size=20,weight="bold"),
                        ]
                    ),
                    padding=ft.padding.only(left=10)
                ),
                ft.Container(
                    ft.Column(
                        [
                            ft.Container(
                                ft.Row(
                                    [
                                        ft.Icon(name=ft.icons.TELEGRAM, color="lightblue"),
                                        ft.Text(
                                            spans=[
                                                ft.TextSpan(
                                                    "russianb_0",
                                                    ft.TextStyle(color="white"),
                                                    url= random.choice(['https://t.me/russianb_0'])
                                                    
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                padding=10,
                                border_radius=30,
                                bgcolor="black"
                            ),
                            ft.Container(
                                ft.Row(
                                    [
                                        ft.Icon(name=ft.icons.EMAIL, color="red"),
                                        ft.Text(
                                            spans=[
                                                ft.TextSpan(
                                                    "mtranquoc77@gmail.com",
                                                    ft.TextStyle(color="white"),
                                                    url="https://www.mtranquoc77@gmail.com",
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                padding=10,
                                border_radius=30,
                                bgcolor="black"
                                
                            )
                        ]
                    ),
                    padding=ft.padding.only(top=15,left=5)
                ),
                ft.Divider(),
                ft.Container(
                    ft.Column(
                        [
                            ft.Text("Come join us",size=20,weight="bold"),
                        ]
                    ),
                    padding=ft.padding.only(left=10)
                ),
                ft.Container(
                    ft.Row(
                        [
                            ft.Icon(name=ft.icons.TELEGRAM, color="lightblue",size=40),
                            ft.Text(
                                spans=[
                                    ft.TextSpan(
                                        "t.me/puzlevn",
                                        ft.TextStyle(color="white"),
                                        url="https://t.me/puzlevn",
                                    )
                                ]
                            )
                        ]
                    ),
                    padding=10,
                    border_radius=30,
                    bgcolor="black",
                    height=60
                    
                ),
                ft.Container(
                    ft.Row(
                        [
                            ft.Icon(name=ft.icons.TIKTOK_OUTLINED, color="white",size=40),
                            ft.Text(
                                spans=[
                                    ft.TextSpan(
                                        "www.tiktok.com/@puzlevn",
                                        ft.TextStyle(color="white"),
                                        url="https://www.tiktok.com/@puzlevn",
                                    )
                                ]
                            )
                        ]
                    ),
                    padding=10,
                    border_radius=30,
                    bgcolor="black",
                    height=60,
                    margin=ft.margin.only(bottom=10)
                    
                )
                
            ],
            height=810,
            scroll=ft.ScrollMode.HIDDEN,
            
        ),
        visible=False,
        
    )


    page_stack = [
        page_1,
        page_2,
        page_3    
    ]


    #Telegram Login



    def route_change(e):
        page.views.clear
        page.views.append(
            View(
                "/Home",
                [
                    NavBar,
                    ft.Column(page_stack,expand=True),
                    Add_Form,
                    Warning,
                ],
                Display_wordlist_item(e),
                
            )
        )
        
            
        
        '''
            USE THIS TO UPDATE AND CREATE 
            YOUR OWN ROUTE WHEN YOU HAVE TO
            OPEN A NEW FUNCTION (OR NON-FUNCTION) FOR YOUR APP

            TRY IF PAGE.ROUTE AND THEN 
        '''
        
        page.update()
    def view_pop(View):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route, skip_route_change_event=True)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    page.add(new_lans_anounce,deleted_langs_anounce,deleted_text_anounce,deleted_word_anounce)
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 380
    page.window.height = 830
    page.update()
   
  
    page.update()

if __name__ == "__main__":
    ft.app(target=main,assets_dir='assets')
   
