import tkinter as tk
from tkinter import ttk

class FilterMenu:
    def __init__(self):
        self.make = 'Any'
        self.model = 'Any'
        self.year_start = 'Any'
        self.year_end = 'Any'
        self.location = 'Any'

    def __submit(self):
        self.make = self.__make_dropdown.get()
        self.model = self.__model_dropdown.get()
        self.year_start = self.__year_start_entry.get()
        self.year_end = self.__year_end_entry.get()
        self.location = self.__location_dropdown.get()

        self.__filter_window.destroy()
        self.__filter_window.quit()

    def create_menu(self, makes, models):
        self.__filter_window = tk.Toplevel()

        filter_window = self.__filter_window
        filter_window.title('Filters')

        # Make dropdown stuff
        make_label = tk.Label(filter_window, text='Make: ')
        make_label.grid(column=0, row=0, sticky='w')

        self.__make_dropdown = ttk.Combobox(filter_window)
        self.__make_dropdown['values'] = ['Any'] + makes
        self.__make_dropdown.set('Any')
        self.__make_dropdown.grid(column=1, row=0)

        # Model dropdown stuff
        model_label = tk.Label(filter_window, text='Model: ')
        model_label.grid(column=0, row=1, sticky='w')

        self.__model_dropdown = ttk.Combobox(filter_window)
        self.__model_dropdown['values'] = ['Any'] + models
        self.__model_dropdown.set('Any')
        self.__model_dropdown.grid(column=1, row=1)

        # Year range stuff
        year_start_label = tk.Label(filter_window, text='Year Start: ')
        year_start_label.grid(column=0, row=3, sticky='w')

        self.__year_start_entry = tk.Entry(filter_window)
        self.__year_start_entry.insert(0, 'Any')
        self.__year_start_entry.grid(column=1, row=3)

        year_end_label = tk.Label(filter_window, text='Year End: ')
        year_end_label.grid(column=0, row=4)

        self.__year_end_entry = tk.Entry(filter_window)
        self.__year_end_entry.insert(0, 'Any')
        self.__year_end_entry.grid(column=1, row=4, sticky='w')

        # Location stuff
        location_label = tk.Label(filter_window, text='Location: ')
        location_label.grid(column=0, row=5, sticky='w')

        self.__location_dropdown = ttk.Combobox(filter_window)
        self.__location_dropdown['values'] = ['Any', 'Bath', 'Rochester', 'Buffalo']
        self.__location_dropdown.set('Any')
        self.__location_dropdown.grid(column=1, row=5, sticky='w')

        # Submit button stuff
        submit_button = tk.Button(filter_window, text='Done', command=self.__submit)
        submit_button.grid(column=1, row=6, sticky='nsew')

        filter_window.mainloop()