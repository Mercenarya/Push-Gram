# -*- coding: utf-8 -*-

import flet as ft
import sys
import os
import time


def restart_program():
    '''
    Restarts the current program.
    Note: this function does not return. Any cleanup action (like saving data) 
    must be done before calling this function.
    '''

    python = sys.executable
    os.execl(python, python, *sys.argv)


def handle_restart(e):
    e.page.window_destroy()

    # todo How to confirm that the application has exited?

    time.sleep(3)
    restart_program()


def main(page: ft.Page):
    btn = ft.ElevatedButton('restart', on_click=handle_restart)
    page.add(btn)


ft.app(target=main)