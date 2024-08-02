import flet as ft
import sqlite3
from flet import View
from deep_translator import GoogleTranslator
import time
from gtts import gTTS
from playsound import playsound
import os
from docx import Document



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
                ft.dropdown.Option("chinese (traditional)")
            ],
            width=150,
            text_size=12,
            border_color="white",
            text_style=ft.TextStyle(color="white"),
            color=ft.TextStyle(color="black"),
            bgcolor="grey"
        )
        languages = ''' SELECT * FROM langs'''
        cursor.execute(languages)
        for obj in cursor.fetchall():
            self.Translator.options.append(
                ft.dropdown.Option(f"{obj[1]}")
            )
        
        
        self.Progress = ft.Column(
            [
                ft.Text("Translating...",size=10,color="white"),
                ft.ProgressBar(width=200,color="white"),
            ],
            visible=False
        )

        self.Translated = ft.Column(
            width=500,
            scroll=ft.ScrollMode.HIDDEN,
            visible=False
        )

    

        self.Doc_title = ft.TextField(hint_text="Name")
    
        self.Saved_announcement = ft.SnackBar(
            content= ft.Text(f"File {self.Doc_title.value} have saved")
        )

        self.Save_docx_dialog  =ft.AlertDialog(
            modal=True,
            title=ft.Text("Save Document"),
            content=self.Doc_title,
            actions=[
                ft.TextButton("Save",on_click=self.Save_to_Docx),
                ft.TextButton("Close",on_click=self.Close_save_docx)
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )

        self.Display_title = ft.Text(value=self.title, color="white", size=20,weight="bold")
        self.Display_text = ft.Text(value=self.Text,color="white",size=15)
        self.Edit_text = ft.TextField(value=self.Display_text.value,border_color="grey",
                                      color="white",text_size=15,multiline=True)
        
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
            width=400,
            bgcolor="Grey",
            padding=20,
            border_radius=15
            
            
        )
        self.Edit_Textline = ft.Container(
            ft.Column(
                [
                    self.Edit_text
                ],
                width=400,
                height=300,
                scroll=ft.ScrollMode.HIDDEN,
            ),
            
            height=300,
            width=400,
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
                width=400,
                height=300,
                scroll=ft.ScrollMode.HIDDEN,
            ),
            
            height=300,
            width=400,
            bgcolor="Grey",
            padding=15,
            border = ft.border.BorderSide(1,"grey"),
            border_radius=15
            
        )

        self.Save_docx = ft.ElevatedButton('Save docx',color="white",bgcolor="blue",on_click=self.Open_save_docx,visible=False)

        

        self.Display_Note = ft.Container(
            ft.Column(
                [
                    self.Display_title,
                    self.Textline,
                    ft.Row(
                        [
                            ft.ElevatedButton("Delete",bgcolor="grey",color="white",on_click=self.Delete_note),
                            ft.ElevatedButton("Edit",bgcolor="Grey",color="white",on_click=self.Edit_Note),
                            ft.ElevatedButton("Translate",bgcolor="grey",color="white",on_click=self.keyword_Note)
                        ]
                    )
                ]
            ),
            
            width=450,
            bgcolor="black",
            padding=20,
            height=430,
            border = ft.border.BorderSide(1,"grey"),
            border_radius=15
            
        )

        self.Edit_Note_text = ft.Container(
            ft.Column(
                [
                    self.Display_title,
                    self.Edit_Textline,
                    ft.Row(
                        [
                            ft.ElevatedButton("Delete",bgcolor="grey",color="white",on_click=self.Delete_note),
                            ft.ElevatedButton("Save",bgcolor="grey",color="white",on_click=self.Save_Note)
                        ]
                    )
                ]
            ),
            
            width=450,
            bgcolor="black",
            padding=20,
            height=430,
            visible=False,
            border = ft.border.BorderSide(1,"grey"),
            border_radius=15
        )
        self.Keyword_Search = ft.Container(
            ft.Column(
                [
                    self.Display_title,
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

                                        self.Save_docx,
                                        ft.ElevatedButton('Back',color="white",bgcolor="grey",on_click=self.Back_event_keyword),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
                                margin=ft.margin.only(top=5)
                            )

                        ],
                        width=520,
                        scroll=ft.ScrollMode.HIDDEN
                        
                    )
                    
                ],
                scroll=ft.ScrollMode.HIDDEN
                
               
            ),
            
            width=450,
            bgcolor="black",
            padding=20,
            height=600,
            visible=False,
            border = ft.border.BorderSide(1,"grey"),
            border_radius=15,
        )
        

        self.controls = [self.Display_Note, self.Edit_Note_text, self.Keyword_Search,self.Save_docx_dialog, self.Saved_announcement]
    def Open_save_docx(self, e):
        self.Save_docx_dialog.open = True
        self.update()

    def Close_save_docx(self, e):
        self.Save_docx_dialog.open = False
        self.update()

    def Open_Saved_announ(self, e):
        self.Saved_announcement.open = True
        self.update()

    def Delete_note(self, e):
        
        Remove_Note = f''' DELETE FROM note WHERE title = '{self.Display_title.value}' '''
        try:
            cursor.execute(Remove_Note)
            print("Note Removed")
            db.commit()
        except sqlite3.Error as error:
            print(error)
        self.Delete(self)

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

    def Save_to_Docx(self, e):
        try:
            
            doc = Document()
            doc.add_paragraph(f'{self.trans_text.value}\n{self.translated_text.value}')
            doc.save(f"{self.Doc_title.value}.docx")
            self.Close_save_docx(e)
            self.Open_Saved_announ(e)
            print("docx saved")
        except Exception as error:
            print(error)
        self.update()


    def Keyword_trans(self, e):
        try:
            self.loading(e)
            self.Save_docx.visible = True
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
                        ft.Text(value=self.Translator.value,color="white",size=20,weight="bold"),
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
        

        self.Note_title = ft.TextField(width=400,border_color="white",hint_text="Tittle...",
                                       color="white",hint_style=ft.TextStyle(color="white"))
        self.Note_textField = ft.TextField(value="\n\n",width=400,border_color="white",hint_text="TextLine...",
                                           multiline=True,hint_style=ft.TextStyle(color="white"),
                                           min_lines=1,max_lines=4,color="white")
        self.banner = ft.Row(
            [
                ft.Text("copyright by Tran Quoc Minh - Aigus Group Ⓒ",size=10,color="grey")
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        self.Note_list = ft.Column(
            [
                self.banner
            ],
            height=630,
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

        


        self.NoteBar = ft.Container(
                ft.Column(
                    [
                        
                        ft.Row(
                            [
                                ft.Icon(name=ft.icons.BOOK,color="white"),
                                ft.Text("TransGram",color="white",size=25,weight="bold"),
                                ft.Icon(name=ft.icons.TRANSLATE,color="white")
                                
                            ],
                            alignment="spaceBetween",
                        ),
                        
                        self.Note_title,
                        self.Note_textField,
                        ft.Row(
                            [
                                ft.FloatingActionButton(
                                    icon=ft.icons.ADD, on_click=self.Add_note
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
            width=400,
            height=55,
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
            ft.Row(
                [
                    self.OpenNoteBar,
                    self.CloseNoteBar
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            self.Note_list,
            
            
        ]

    def Add_note(self, e):
        note = Note(self.Note_title.value,self.Note_textField.value, self.Delete_note)
        
        index_tub = [self.Note_title.value, self.Note_textField.value]
        Query_index = '''INSERT INTO note (title, textiled) VALUES (?,?)'''
        try:
            cursor.execute(Query_index,index_tub)
            print("New Note Added")
            db.commit()
        except sqlite3.Error as error:
            print(error)
        
        self.Note_list.controls.append(note)
        self.Note_textField.value = "\n\n\n"
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
        self.NoteBar.height = 350 if self.NoteBar.height == 55 else 55
        self.update()

    def Note_TopBar_close(self, e):
        self.OpenNoteBar.visible = True
        self.CloseNoteBar.visible = False
        self.NoteBar.height = 55 if self.NoteBar.height == 350 else 350
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
        print("clicked")
        Wordlist.controls.clear()
        page.clean()  # Clear the page
        main(page)
        page.window_close()
        page.update()

    #Annoucement
    def Open_langs_annoucement(e):
        new_lans_anounce.open = True
        page.update()
    def Open_deleted_lans_announcement(e):
        deleted_langs_anounce.open = True
        page.update()
    def Open_deleted_text_announcement(e):
        deleted_text_anounce.open = True
        page.update()

    def Open_deleted_word_announcement(e):
        deleted_word_anounce.open = True
        page.update()
    #Interacting functions 
    def Open_language_setting_layout(e):
        open_language_button.visible = False
        close_language_button.visible = True
        Language_field.visible = True
        Submit_Result.visible = True
        Language_layout.height = 200
        page.update()
    
    def close_language_setting_layout(e):
        open_language_button.visible = True
        close_language_button.visible = False
        Language_field.visible = False
        Submit_Result.visible = False
        Language_layout.height = 80
        page.update()
    def Upload_language(e):
        try:
            new_lans = [Language_field.value.lower()]
            cursor.execute('INSERT INTO langs (lans) VALUES (?)',new_lans)
            print("new language upload")
            
            Open_langs_annoucement(e)
            
            db.commit()
        except sqlite3.Error as error:
            print(error)
        page.update()

    def Deleted_language(e):
        try:
            cursor.execute('DELETE FROM langs')
            db.commit()
            
            Open_deleted_lans_announcement(e)
            
        except sqlite3.Error as error:
            print(error)
        page.update()

    def Deleted_Text(e):
        try:
            cursor.execute('DELETE FROM note')
            db.commit()
           
            Open_deleted_text_announcement(e)
            
        except sqlite3.Error as error:
            print(error)
        page.update()
    def Deleted_Word(e):
        try:
            cursor.execute('DELETE FROM word')
            db.commit()
           
            Open_deleted_word_announcement(e)
            
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
        Storage_layout.height = 250
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
    Language_field = ft.TextField(hint_text="New Language",hint_style=ft.TextStyle(color="white"),
                                  color="white",
                                  border_color="white",visible=False)
    Submit_Result = ft.ElevatedButton("Update",color="white",bgcolor="grey",
                                      width=100,visible=False,on_click=Upload_language)
    #Update Storage - button - controls
    Delete_language = ft.IconButton(ft.icons.DELETE,icon_color="red",on_click=Deleted_language)
    Delete_Context = ft.IconButton(ft.icons.DELETE,icon_color="red",on_click=Deleted_Text)
    Delete_dictionary = ft.IconButton(ft.icons.DELETE,icon_color="red",on_click=Deleted_Word)



    #User's interact with button - select options - controls
    #button - language's Selection
    open_language_button = ft. IconButton(ft.icons.ARROW_RIGHT,visible=True,
                                          icon_color="white",icon_size=30,
                                          on_click=Open_language_setting_layout)
    
    close_language_button = ft. IconButton(ft.icons.ARROW_LEFT,visible=False,
                                           icon_color="white",icon_size=30,
                                           on_click=close_language_setting_layout)
    

    #button - theme's Selection
    open_theme_button = ft. IconButton(ft.icons.ARROW_RIGHT,visible=True,
                                          icon_color="white",icon_size=30,
                                          on_click=Open_theme_setting_layout)
    close_theme_button = ft. IconButton(ft.icons.ARROW_LEFT,visible=False,
                                           icon_color="white",icon_size=30,
                                           on_click=close_theme_setting_layout)
    


    #button - Storage's Selection
    open_storage_button = ft. IconButton(ft.icons.ARROW_RIGHT,visible=True,
                                          icon_color="white",icon_size=30,
                                          on_click=Open_storage_setting_layout)
    close_storage_button = ft. IconButton(ft.icons.ARROW_LEFT,visible=False,
                                           icon_color="white",icon_size=30,
                                           on_click=close_storage_setting_layout)

    
    new_lans_anounce = ft.SnackBar(
        content=ft.Text("New language uploaded, press 'Update' to restart your app")
    )

    deleted_langs_anounce = ft.SnackBar(
        content=ft.Text("all uploaded languages deleted, press 'Update' to restart your app")
    )
    deleted_text_anounce = ft.SnackBar(
        content=ft.Text("all text deleted, press 'Update' to restart your app")
    )
    deleted_word_anounce = ft.SnackBar(
        content=ft.Text("Dictionary deleted, press 'Update' to restart your app")
    )
    
    
    #container - language's Selection
    Language_layout = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Language's update", weight="bold",color="white"),
                        open_language_button,
                        close_language_button,
                        
                        
                    ],
                    alignment="spacebetween"
                ),
                Language_field,
                Submit_Result
            ]
        ),
        height=80,
        width=450,
        bgcolor="black",
        border_radius=20,
        padding=15,
        animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT), 
    )
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
        width=450,
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
                        ft.Text("Delete all languages",color="white"),
                        Delete_language
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
        width=450,
        bgcolor="black",
        border_radius=20,
        padding=15,
        animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT), 
    )
    Reboot_layout = ft.Container(
        ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Update",color="white",weight="bold"),
                        ft.Text("Shut down and start updating, then open App again",
                                color="white",size=10),
                    ]
                ),
                ft.IconButton(ft.icons.RESTART_ALT,icon_color="white",on_click=Reload_app)
            ],
            alignment="spacebetween"
        ),
        height=80,
        width=450,
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
                print("2")
                db.commit()
            except sqlite3.Error as error:
                print(error)
        page.update()

    Word_field = ft.TextField(width=300,hint_text="New Word")
    Converted_line = ft.Text(visible=False)
    Translated_line = ft.Text(visible=False)
    Language_convert = ft.Dropdown(
            options=[
                ft.dropdown.Option("vietnamese"),
                ft.dropdown.Option("english"),
                ft.dropdown.Option("russian"),
                ft.dropdown.Option("chinese (traditional)")
            ],
            width=180,
            text_size=12
        )
    languages = ''' SELECT * FROM langs'''
    cursor.execute(languages)
    for obj in cursor.fetchall():
        Language_convert.options.append(
            ft.dropdown.Option(f"{obj[1]}")
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
    
    # Language_Speech = ft.Dropdown(
    #         options=[
    #             ft.dropdown.Option("Vietnamese"),
    #             ft.dropdown.Option("English"),
    #             ft.dropdown.Option("Russian"),
    #             ft.dropdown.Option("Chinese"),
    #             ft.dropdown.Option("French"),
    #             ft.dropdown.Option("Spanish")
    #         ],
    #         width=180,
    #         text_size=12
    #     )
    # def Speech_1(e):
    #     language_code_map = {
    #         'English': 'en',
    #         'Spanish': 'es',
    #         'French': 'fr',
    #         'German': 'de',
    #         'Chinese': 'zh',
    #         'Russian':'ru'
    #     }
    #     langs_code = language_code_map.get(Language_Speech.value,'en')
    #     speech = gTTS(text=Translated_line.value, lang=langs_code)
    #     file_path = 'GetProjects.mp3'
    #     speech.save(file_path)
    #     playsound(file_path)
    #     time.sleep(1)
    #     os.remove(file_path)
    #     page.update()

    

    
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
                        ft.Text("Saved - Noted",size=20),
                        
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(color="grey"),
                ft.Column(
                    [
                        ft.Row(
                            [
                                Wordlist
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                # Language_Speech,
                                Floatbutton
                            ],
                            alignment=ft.MainAxisAlignment.END
                            
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
                        ft.Text("Settings ",size=20),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(color="grey"),
                
                Language_layout,
                Theme_layout,
                Storage_layout,
                Reboot_layout
                
            ],
            scroll=ft.ScrollMode.ALWAYS
        ),
        visible=False
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
                Display_wordlist_item(e)
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
    page.window_width = 380
    page.window_resizable = False
    page.on_resize = False
    page.update()
    page.theme_mode = ft.ThemeMode.LIGHT

    page.window_width = 380
    page.window_height = 830
    page.on_resize = False
    page.window_resizable = False
    page.window_resizable = False
    page.update()

if __name__ == "__main__":
    ft.app(target=main)