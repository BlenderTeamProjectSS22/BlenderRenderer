from tkinter import Frame, Label, Checkbutton, Scale, Entry, OptionMenu, StringVar, BooleanVar, DoubleVar, IntVar
import tkinter as tk
from tkinter.ttk import Separator
import enum
import utils
from gui.gui_utils import frame_set_enabled, widget_set_enabled

class MaterialWidgets(Frame):
    def __init__(self, master, control):
        Frame.__init__(self, master, borderwidth=2, relief="groove")
        self.control = control
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        mat_selected = StringVar(self)
        mat_selected.set("default")
        
        lbl_materials = Label(master=self, text="Material selection", font="Arial 10 bold")
        lbl_metallic  = Label(master=self, text="Metallic")
        lbl_roughness = Label(master=self, text="Roughness")
        lbl_transmiss = Label(master=self, text="Transmission")
        
        self.frm_emissive = Frame(master=self)
        lbl_emissive  = Label(master=self.frm_emissive, text="Emissive Strength")
        self.emissive = BooleanVar(self)
        self.glow     = BooleanVar(self)
        check_emiss   = Checkbutton(master=self, text="Emissive", variable=self.emissive, anchor="w", command=lambda: self.toggle_emissive(rerender=True))
        check_glow    = Checkbutton(master=self, text="Glow", variable=self.glow, command=self.toggle_glow)
        
        validate_int = self.register(self.validate_integer)
        self.ent_metallic  = Entry(master=self, validate="key", validatecommand=(validate_int, '%P'), width=10)
        self.ent_roughness = Entry(master=self, validate="key", validatecommand=(validate_int, '%P'), width=10)
        self.ent_transmiss = Entry(master=self, validate="key", validatecommand=(validate_int, '%P'), width=10)
        self.ent_emissive  = Entry(master=self.frm_emissive, validate="key", validatecommand=(validate_int, '%P'), width=10)
        self.ent_metallic.bind("<Return>",  self.set_metallic_input)
        self.ent_roughness.bind("<Return>", self.set_roughness_input)
        self.ent_transmiss.bind("<Return>", self.set_transmiss_input)
        self.ent_emissive.bind("<Return>", self.set_emissive_input)
        
        self.slider_metallic  = Scale(master=self, orient="horizontal", showvalue=False, command=lambda val: self.set_metallic(val, False))
        self.slider_roughness = Scale(master=self, orient="horizontal", showvalue=False, command=lambda val: self.set_roughness(val, False))
        self.slider_transmiss = Scale(master=self, orient="horizontal", showvalue=False, command=lambda val: self.set_transmission(val, False))
        self.emissive_strength = IntVar()
        self.slider_emissive  = Scale(master=self.frm_emissive, orient="horizontal", variable=self.emissive_strength, showvalue=False, command=lambda val: self.set_emissive(False))
        self.slider_metallic.bind("<ButtonRelease-1>",  lambda event: self.set_metallic(self.slider_metallic.get(), True))
        self.slider_roughness.bind("<ButtonRelease-1>", lambda event: self.set_roughness(self.slider_roughness.get(), True))
        self.slider_transmiss.bind("<ButtonRelease-1>", lambda event: self.set_transmission(self.slider_transmiss.get(), True)) 
        self.slider_emissive.bind("<ButtonRelease-1>", lambda event: self.set_emissive(True)) 
        
        lbl_sel_mat   = Label(master=self, text="Select:")
        materials = ("default", Materials.GOLD.value, Materials.GLASS.value, Materials.WATER.value, Materials.STONE.value, Materials.EMISSIVE.value, Materials.THICK_GLASS.value)
        dropdown_materials = OptionMenu(self, mat_selected, *materials, command=self.set_material)
        
        self.frm_bump   = Frame(master=self, borderwidth=3)
        lbl_scale      = Label(master=self.frm_bump, text="Noise scale")
        lbl_detail     = Label(master=self.frm_bump, text="Noise detail")
        lbl_distortion = Label(master=self.frm_bump, text="Distortion")
        
        lbl_scale.grid(row=0, column=0)
        lbl_detail.grid(row=0, column=1)
        lbl_distortion.grid(row=0, column=2)
        self.noise_scale = DoubleVar()
        self.noise_detail = DoubleVar()
        self.noise_distortion = DoubleVar()
        self.slider_scale      = Scale(master=self.frm_bump, from_=1, to=10, resolution=0.1, variable=self.noise_scale, command=lambda val: self.set_noise_scale(False), relief=tk.SOLID)
        self.slider_detail     = Scale(master=self.frm_bump, from_=1, to=10, resolution=0.1, variable=self.noise_detail, command=lambda val: self.set_noise_detail(False), relief=tk.SOLID)
        self.slider_distortion = Scale(master=self.frm_bump, from_=0, to=5,  resolution=0.1, variable=self.noise_distortion, command=lambda val: self.set_noise_distortion(False), relief=tk.SOLID)
        self.slider_scale.grid(row=1, column=0)
        self.slider_detail.grid(row=1, column=1)
        self.slider_distortion.grid(row=1, column=2)
        
        self.bump = BooleanVar()
        check_bump = Checkbutton(master=self, text="Enable bumpiness", variable=self.bump, command=lambda: self.toogle_bumpiness(rerender=True))
        
        lbl_materials.grid(row=0, column=0, columnspan=2, sticky="we")
        lbl_metallic.grid(row=1, column=0, sticky="we")
        self.ent_metallic.grid(row=1, column=1, sticky="w")
        self.slider_metallic.grid(row=2, column=0, sticky="we", columnspan=2)
        
        lbl_roughness.grid(row=3, column=0, sticky="we")
        self.ent_roughness.grid(row=3, column=1, sticky="w")
        self.slider_roughness.grid(row=4, column=0, sticky="we", columnspan=2)
        
        lbl_transmiss.grid(row=5, column=0, sticky="we")
        self.ent_transmiss.grid(row=5, column=1, sticky="we")
        self.slider_transmiss.grid(row=6, column=0, sticky="we", columnspan=2)
        
        check_emiss.grid(row=7, column=0, sticky="w")
        check_glow.grid(row=7, column=1, sticky="w")
        
        self.frm_emissive.columnconfigure(0, weight=1)
        self.frm_emissive.columnconfigure(1, weight=1)
        lbl_emissive.grid(row=1, column=0, sticky="we")
        self.ent_emissive.grid(row=1, column=1)
        self.slider_emissive.grid(row=2, column=0, sticky="we", columnspan=2)
        
        self.frm_emissive.grid(row=8, column=0, columnspan=4, sticky="we")
        
        lbl_sel_mat.grid(row=10, column=0, sticky="w")
        dropdown_materials.grid(row=10, column=1, sticky="w")
        
        sep = Separator(self,orient="horizontal")
        sep.grid(row=11, column=0, columnspan=2, sticky="nesw", pady=5, padx=5)
        check_bump.grid(row=12, column=0, columnspan=2)
        self.frm_bump.grid(row=13, column=0, columnspan=2)
        
        self.default_values()
        
        
    def default_values(self):
        self.control.material.default_material()
        if self.control.model is not None:
            self.control.material.set_solidified(self.control.model, False)
        self.adjust_sliders()
        
    def validate_integer(self, P):
        # TODO This prevents deleting e.g. '5', because field can't be empty
        # Implement that it sets it to 0 automatically if last digit is deleted
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
    
    def set_material(self, *args):
        if self.control.model is not None:
            self.control.material.set_solidified(self.control.model, False)
        
        match Materials(args[0]):
            case Materials.GLASS:
                self.control.material.glass_material()
            case Materials.STONE:
                self.control.material.stone_material()
            case Materials.EMISSIVE:
                self.control.material.emissive_material()
            case Materials.WATER:
                self.control.material.water_material()
            case Materials.THICK_GLASS:
                if self.control.model is not None:
                    self.control.material.thick_glass(self.control.model)
            case Materials.GOLD:
                self.control.material.gold_material()
                
            case _:
                self.default_values()
        self.adjust_sliders()
        self.control.re_render()
    
    # Readjust sliders to fit the active material
    def adjust_sliders(self):
        self.set_metallic(int(self.control.material.metallic*100), False)
        self.set_roughness(int(self.control.material.roughness*100), False)
        self.set_transmission(int(self.control.material.transmission*100), False)
        self.glow.set(int(self.control.material.compositing.glow))
        self.emissive.set(int(self.control.material.emissive))
        self.bump.set(self.control.material.noise.is_enabled)
        self.noise_scale.set(self.control.material.noise.scale)
        self.noise_detail.set(self.control.material.noise.detail)
        self.noise_distortion.set(self.control.material.noise.distortion)
        self.toogle_bumpiness(rerender=False)
        self.emissive_strength.set(int(self.control.material.strength*100))
        self.ent_emissive.delete(0, tk.END)
        self.ent_emissive.insert(tk.END, self.emissive_strength.get())
        self.toggle_emissive(rerender=False)
        if self.emissive.get():
            self.set_emissive(isReleased=False)
    
    def set_metallic_input(self, event):
        x = 0
        if self.ent_metallic.get() != "":
            x = utils.clamp(int(self.ent_metallic.get()), 0, 100)
        self.set_metallic(x, True)
        
    def set_roughness_input(self, event):
        x = 0
        if self.ent_roughness.get() != "":
            x = utils.clamp(int(self.ent_roughness.get()), 0, 100)
        self.set_roughness(x, True)
        
    def set_transmiss_input(self, event):
        x = 0
        if self.ent_transmiss.get() != "":
            x = utils.clamp(int(self.ent_transmiss.get()), 0, 100)
        self.set_transmission(x, True)
    
    def set_emissive_input(self, event):
        x = 0
        if self.ent_emissive.get() != "":
            x = utils.clamp(int(self.ent_emissive.get()), 0, 100)
            self.emissive_strength.set(x)
        self.set_emissive(True)
        
    def set_metallic(self, value: int, isReleased: bool):
        self.ent_metallic.delete(0, tk.END)
        self.ent_metallic.insert(tk.END, value)
        self.slider_metallic.set(value)
        self.control.material.set_metallic(utils.percent(int(value)))
        
        if isReleased:
            print("Setting metallic to " + str(value))
            self.control.re_render()
    
    def set_roughness(self, value, isReleased: bool):
        self.ent_roughness.delete(0, tk.END)
        self.ent_roughness.insert(tk.END, value)
        self.slider_roughness.set(value)
        self.control.material.set_roughness(utils.percent(int(value)))
        
        if isReleased:
            print("Setting roughness to " + str(value))
            self.control.re_render()
    
    def set_transmission(self, value, isReleased: bool):
        self.ent_transmiss.delete(0, tk.END)
        self.ent_transmiss.insert(tk.END, value)
        self.slider_transmiss.set(value)
        self.control.material.set_transmission(utils.percent(int(value)))
        
        if isReleased:
            print("Setting transmission to " + str(value))
            self.control.re_render()
    
    def set_emissive(self, isReleased: bool):
        self.ent_emissive.delete(0, tk.END)
        self.ent_emissive.insert(tk.END, self.emissive_strength.get())
        self.slider_emissive.set(self.emissive_strength.get())
        
        self.control.material.set_emissive_strength(utils.percent(self.emissive_strength.get()))
        
        if isReleased:
                print("Setting emissive strength to " + str(self.emissive_strength.get()))
                self.control.re_render()
        
    def toggle_emissive(self, rerender: bool):
        is_emissive = self.emissive.get()
        
        frame_set_enabled(self.frm_emissive, is_emissive)
        
        if is_emissive:
            self.slider_emissive.bind("<ButtonRelease-1>",  lambda event: self.set_emissive(True))
        else:
            self.slider_emissive.unbind("<ButtonRelease-1>")
            
        self.control.material.set_emissive(is_emissive)
        
        if rerender:
            print("Setting emissive to " + str(is_emissive))
            self.control.re_render()
    
    def toggle_glow(self):
        frame_set_enabled(self.slider_emissive, self.glow.get())
        self.control.material.compositing.set_glow(self.glow.get())
        print("Setting glow to " + str(self.glow.get()))
        self.control.re_render()
        
    def toogle_bumpiness(self, rerender: bool):
        if self.bump.get():
            frame_set_enabled(self.frm_bump, True)
            self.slider_scale.bind("<ButtonRelease-1>",  lambda event: self.set_noise_scale(True))
            self.slider_detail.bind("<ButtonRelease-1>",  lambda event: self.set_noise_detail(True))
            self.slider_distortion.bind("<ButtonRelease-1>",  lambda event: self.set_noise_distortion(True))
            self.control.material.bump_material(
                self.noise_scale.get(),
                self.noise_detail.get(),
                self.noise_distortion.get())
        else:
            frame_set_enabled(self.frm_bump, False)
            self.slider_scale.unbind("<ButtonRelease-1>")
            self.slider_detail.unbind("<ButtonRelease-1>")
            self.slider_distortion.unbind("<ButtonRelease-1>")
            self.control.material.noise.disable()
        if rerender:
            print("Setting bumpiness to " + str(self.bump.get()))
            self.control.re_render()
    
    def set_noise_scale(self, isReleased: bool):
        self.control.material.noise.set_scale(self.noise_scale.get())
        if isReleased:
            print("Setting noise scale to " + str(self.noise_scale.get()))
            self.control.re_render()
    
    def set_noise_detail(self, isReleased: bool):
        self.control.material.noise.set_detail(self.noise_detail.get())
        if isReleased:
            print("Setting noise detail to " + str(self.noise_detail.get()))
            self.control.re_render()
    
    def set_noise_distortion(self, isReleased: bool):
        self.control.material.noise.set_distortion(self.noise_distortion.get())
        if isReleased:
            print("Setting noise distortion to " + str(self.noise_distortion.get()))
            self.control.re_render()

# Enum containing all possible materials
class Materials(enum.Enum):
    DEFAULT = "default"
    GLASS = "glass"
    STONE = "stone"
    EMISSIVE = "emissive"
    WATER = "water"
    THICK_GLASS = "thick glass"
    GOLD = "gold"

