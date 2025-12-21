import tkinter as tk
from constants import COLORS, FONT_FAMILY

class StyledButton(tk.Frame):

    def __init__(self, parent, text, command, bg_color, fg_color='#ffffff',
                 font_size=11, bold=True, padx=20, pady=10, state='normal', **kwargs):
        super().__init__(parent, bg=parent.cget('bg') if hasattr(parent, 'cget') else COLORS['bg_primary'])

        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.disabled_bg = '#555555'
        self.disabled_fg = '#888888'
        self._state = state

        font_weight = "bold" if bold else "normal"
        self.label = tk.Label(
            self, text=text,
            font=(FONT_FAMILY, font_size, font_weight),
            bg=bg_color, fg=fg_color,
            padx=padx, pady=pady, cursor='hand2'
        )
        self.label.pack(fill=tk.BOTH, expand=True)

        self.label.bind('<Button-1>', self._on_click)
        self.label.bind('<Enter>', self._on_enter)
        self.label.bind('<Leave>', self._on_leave)

        if state == 'disabled':
            self.disable()

    def _on_click(self, event):
        if self._state == 'normal' and self.command:
            self.command()

    def _on_enter(self, event):
        if self._state == 'normal':
            # Rengi biraz açıklaştır
            self.label.config(bg=self._lighten_color(self.bg_color))

    def _on_leave(self, event):
        if self._state == 'normal':
            self.label.config(bg=self.bg_color)
        else:
            self.label.config(bg=self.disabled_bg)

    def _lighten_color(self, color):
        """Rengi biraz açıklaştır."""
        try:
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            r = min(255, r + 30)
            g = min(255, g + 30)
            b = min(255, b + 30)
            return f'#{r:02x}{g:02x}{b:02x}'
        except:
            return color

    def enable(self):
        self._state = 'normal'
        self.label.config(bg=self.bg_color, fg=self.fg_color, cursor='hand2')

    def disable(self):
        self._state = 'disabled'
        self.label.config(bg=self.disabled_bg, fg=self.disabled_fg, cursor='arrow')

    def config(self, **kwargs):
        if 'state' in kwargs:
            if kwargs['state'] == tk.NORMAL or kwargs['state'] == 'normal':
                self.enable()
            else:
                self.disable()

