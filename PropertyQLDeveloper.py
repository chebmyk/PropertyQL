import re
import tkinter as tk
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator

import yaml

import service.propertyQL
import service.xmlQL
import utils.file_utils as file_utils
import utils.xml_utils as xml_utils


class PropertyQLDeveloper:

    def __init__(self):
        self.root = tk.Tk()

        self.root.geometry("1200x1000")
        self.root.title("PropertyQL Developer")

        # ==========  MENU =========================
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.rowconfigure(0, weight=1)
        self.menu_frame.pack(padx=10, pady=1, fill=tk.BOTH)
        btn_icon = tk.PhotoImage(file='icons/play.png')
        self.run_button = tk.Button(self.menu_frame, image=btn_icon, relief=tk.FLAT, command=self.execute)
        self.run_button.grid(row=0, column=0, sticky=tk.E)

        # ==========  Layout =========================
        self.layout_frame = tk.Frame(self.root)

        self.layout_frame.rowconfigure(0, weight=1)
        self.layout_frame.rowconfigure(1, weight=4)
        self.layout_frame.rowconfigure(2, weight=1)
        self.layout_frame.rowconfigure(3, weight=4)

        self.layout_frame.columnconfigure(0, weight=1)
        self.layout_frame.columnconfigure(1, weight=1)

        self.layout_frame.pack(padx=10, pady=10, fill=tk.BOTH)

#=============================================================================
        self.input_labels_frame = tk.Frame(self.layout_frame)
        self.input_labels_frame.rowconfigure(0, weight=1)
        self.input_labels_frame.columnconfigure(0, weight=8)
        self.input_labels_frame.columnconfigure(1, weight=1)
        self.input_labels_frame.columnconfigure(2, weight=1)

#=========================================================================
        self.input_field_label = tk.Label(self.input_labels_frame, text="Input")
        self.input_field_label.grid(row=0, column=0, sticky=tk.W)

        self.selected_file_type = tk.StringVar(self.root, "xml")
        tk.Radiobutton(self.input_labels_frame, text = ".xml", variable = self.selected_file_type, value = "xml").grid(row=0, column=1, sticky=tk.W)
        tk.Radiobutton(self.input_labels_frame, text = ".properties", variable = self.selected_file_type, value = "properties").grid(row=0, column=2, sticky=tk.W)
        self.input_labels_frame.grid(row=0, column=0, sticky=tk.W)

        self.query_field_label = tk.Label(self.layout_frame, text="Query")
        self.query_field_label.grid(row=0, column=1, sticky=tk.W)

#=======================================================================


        self.input_field = tk.Text(self.layout_frame, undo=True)

        self.cdg = ColorDelegator()
       # self.cdg.prog = re.compile(r"\b(?P<tags>property\b|" + make_pat(), re.S)
       # self.cdg.prog = re.compile(r"\b(?P<MYGROUP>tkinter)\b|" + ic.make_pat(), re.S)
        self.cdg.idprog = re.compile(r"\s+(\w+)", re.S)
        self.cdg.tagdefs["MYGROUP"] = {"foreground": "blue", "background": "#FFFFFF"}
        self.cdg.tagdefs["COMMENT"] = {"foreground": "red", "background": "#FFFFFF"}
        self.cdg.tagdefs["KEYWORD"] = {"foreground": "yellow", "background": "#FFFFFF"}
        self.cdg.tagdefs["BUILTIN"] = {"foreground": "green", "background": "#FFFFFF"}
        self.cdg.tagdefs["STRING"] = {"foreground": "orange", "background": "#FFFFFF"}
        self.cdg.tagdefs["DEFINITION"] = {"foreground": "purple", "background": "#FFFFFF"}
        self.cdg.tagdefs["CLASS"] = {"foreground": "black", "background": "#FFFFFF"}


        Percolator(self.input_field).insertfilter(self.cdg)


        self.input_field.bind("<<Modified>>", self.text_onchange)
        self.input_field.bind("<Control-v>", self.on_paste)
        self.input_field.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        self.query_field = tk.Text(self.layout_frame, undo=True)
        Percolator(self.query_field).insertfilter(ColorDelegator())
        self.query_field.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

#=======================================================================

        self.result_field_label = tk.Label(self.layout_frame, text="Result")
        self.result_field_label.grid(row=2, column=0, sticky=tk.W)

        clr_btn_icon = tk.PhotoImage(file='icons/clear.png')
        self.clear_result = tk.Button(self.layout_frame, image=clr_btn_icon, relief=tk.FLAT, command=self.clear_result)
        self.clear_result.grid(row=2, column=1, sticky=tk.E)

        self.result_field = tk.Text(self.layout_frame)
        Percolator(self.result_field).insertfilter(ColorDelegator())
        self.result_field.grid(row=3, columnspan=2, sticky=tk.N + tk.W + tk.E + tk.S, padx=5, pady=5)

        self.root.mainloop()


    def clear_result(self):
        self.result_field.delete("1.0", tk.END)


    def execute(self):

        self.result_field.delete("1.0", tk.END)

        input_type=self.selected_file_type.get()

        input_str = self.input_field.get("1.0", tk.END)
        query_str = self.query_field.get("1.0", tk.END)

        if input_type in ["xml"]:
            xml_tree = xml_utils.parse_xml(input_str)
            query = yaml.safe_load(query_str)
            xml_tree = service.xmlQL.apply_config(xml_tree, query)
            self.result_field.insert("1.0", xml_tree)

        elif input_type in ["properties"]:

            input_file_path = "input.tmp"
            output_file_path = "output.tmp"

            input_file = file_utils.write_file(input_file_path)
            input_file.write(input_str)
            input_file.close()

            input_file = file_utils.read_file(input_file_path)
            query = yaml.safe_load(query_str)

            output_file = service.propertyQL.apply_config(input_file, query, file_utils.write_file(output_file_path))
            output_file.close()

            output = file_utils.read_file(output_file_path).read()
            self.result_field.insert("1.0", output)
            input_file.close()


    def text_onchange(self, event):
        print(f"Onchange text event {event}" )
        input_str = self.input_field.get("1.0", tk.END)

        xml_match = re.findall(r'<\w+[^>]*>', input_str)
        prop_match = re.findall(r'^[^#]\s*(\w+(\.\w+)+|\w+)\s*=\s*', input_str)
        if len(xml_match) > len(prop_match):
            print("Text detected as XML")
            self.selected_file_type.set("xml")
        else:
            print("Text detected as Property")
            self.selected_file_type.set("properties")
        self.input_field.edit_modified(False)

    def on_paste(self, event):
        print(f"On Paste event {event}")
        self.input_field.insert(tk.END, "")
        self.input_field.edit_modified(True)


PropertyQLDeveloper()