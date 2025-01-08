"""
Reusable UI Components
Custom widget library for the encryption utility dashboard.

Author: Sahil Wade
"""

import customtkinter as ctk
from typing import Optional, Callable
from app.theme import *


class GlowCard(ctk.CTkFrame):
    """
    Premium card component with subtle glow border effect.
    Used for dashboard statistics and content sections.
    """

    def __init__(
        self,
        master,
        title: str = "",
        subtitle: str = "",
        value: str = "",
        accent_color: str = ACCENT_PRIMARY,
        **kwargs
    ):
        super().__init__(
            master,
            fg_color=BG_CARD,
            corner_radius=RADIUS_LG,
            border_width=1,
            border_color=BORDER_SUBTLE,
            **kwargs
        )

        self.accent_color = accent_color
        self._hover_active = False

        # Bind hover events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

        # Layout
        if title:
            self.title_label = ctk.CTkLabel(
                self,
                text=title,
                font=FONT_CAPTION,
                text_color=TEXT_TERTIARY,
                anchor="w"
            )
            self.title_label.pack(
                anchor="w", padx=PAD_CARD, pady=(PAD_CARD, 0)
            )

        if value:
            self.value_label = ctk.CTkLabel(
                self,
                text=value,
                font=(FONT_FAMILY, FONT_SIZE_2XL, "bold"),
                text_color=TEXT_PRIMARY,
                anchor="w"
            )
            self.value_label.pack(
                anchor="w", padx=PAD_CARD, pady=(SPACING_XS, 0)
            )

        if subtitle:
            self.subtitle_label = ctk.CTkLabel(
                self,
                text=subtitle,
                font=(FONT_FAMILY, FONT_SIZE_SM),
                text_color=TEXT_SECONDARY,
                anchor="w"
            )
            self.subtitle_label.pack(
                anchor="w", padx=PAD_CARD, pady=(SPACING_XS, PAD_CARD)
            )

    def _on_enter(self, event):
        """Elevate card on hover with accent border glow."""
        self._hover_active = True
        self.configure(
            border_color=self.accent_color,
            fg_color=BG_CARD_HOVER
        )

    def _on_leave(self, event):
        """Reset card to default resting state."""
        self._hover_active = False
        self.configure(
            border_color=BORDER_SUBTLE,
            fg_color=BG_CARD
        )

    def update_value(self, value: str):
        """Update the displayed value."""
        if hasattr(self, "value_label"):
            self.value_label.configure(text=value)


class StatusBadge(ctk.CTkFrame):
    """Small status indicator badge."""

    def __init__(self, master, status: str = "success", text: str = "", **kwargs):
        colors = {
            "success": STATUS_SUCCESS,
            "warning": STATUS_WARNING,
            "error": STATUS_ERROR,
            "info": STATUS_INFO,
        }
        color = colors.get(status, STATUS_INFO)

        super().__init__(
            master,
            fg_color=color + "20",
            corner_radius=RADIUS_SM,
            **kwargs
        )

        label = ctk.CTkLabel(
            self,
            text=text or status.capitalize(),
            font=(FONT_FAMILY, FONT_SIZE_XS, "bold"),
            text_color=color
        )
        label.pack(padx=SPACING_SM, pady=SPACING_XS)


class AnimatedProgressBar(ctk.CTkFrame):
    """Custom progress bar with gradient styling."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=BG_INPUT,
            corner_radius=RADIUS_SM,
            height=PROGRESS_HEIGHT,
            **kwargs
        )

        self.progress_fill = ctk.CTkFrame(
            self,
            fg_color=ACCENT_PRIMARY,
            corner_radius=RADIUS_SM,
            height=PROGRESS_HEIGHT
        )
        self._progress = 0.0

    def set_progress(self, value: float):
        """Set progress value (0.0 to 1.0)."""
        self._progress = max(0.0, min(1.0, value))
        self.update_idletasks()
        width = int(self.winfo_width() * self._progress)
        if width > 0:
            self.progress_fill.place(x=0, y=0, width=width, relheight=1.0)
        else:
            self.progress_fill.place_forget()

    def reset(self):
        """Reset progress to zero."""
        self._progress = 0.0
        self.progress_fill.place_forget()


class SidebarButton(ctk.CTkButton):
    """Navigation sidebar button with active state indicator."""

    def __init__(
        self,
        master,
        text: str,
        icon: str = "",
        command: Optional[Callable] = None,
        is_active: bool = False,
        **kwargs
    ):
        display_text = f"  {icon}   {text}" if icon else f"  {text}"

        super().__init__(
            master,
            text=display_text,
            command=command,
            font=(FONT_FAMILY, FONT_SIZE_SM),
            text_color=TEXT_SECONDARY,
            fg_color="transparent",
            hover_color=BG_CARD,
            anchor="w",
            height=BUTTON_HEIGHT,
            corner_radius=RADIUS_MD,
            **kwargs
        )

        if is_active:
            self.set_active()

    def set_active(self):
        """Set button to active state."""
        self.configure(
            fg_color=ACCENT_PRIMARY + "15",
            text_color=ACCENT_BLUE_SOFT,
            border_width=0
        )

    def set_inactive(self):
        """Set button to inactive state."""
        self.configure(
            fg_color="transparent",
            text_color=TEXT_SECONDARY
        )


class FileDropZone(ctk.CTkFrame):
    """Drag-and-drop file area with visual feedback."""

    def __init__(self, master, on_file_selected: Optional[Callable] = None, **kwargs):
        super().__init__(
            master,
            fg_color=BG_INPUT,
            corner_radius=RADIUS_LG,
            border_width=2,
            border_color=BORDER_DEFAULT,
            **kwargs
        )

        self.on_file_selected = on_file_selected

        # Icon
        self.icon_label = ctk.CTkLabel(
            self,
            text="📂",
            font=(FONT_FAMILY, 32)
        )
        self.icon_label.pack(pady=(SPACING_2XL, SPACING_SM))

        # Primary text
        self.primary_label = ctk.CTkLabel(
            self,
            text="Drop file here or click to browse",
            font=(FONT_FAMILY, FONT_SIZE_MD),
            text_color=TEXT_SECONDARY
        )
        self.primary_label.pack(pady=(0, SPACING_XS))

        # Secondary text
        self.secondary_label = ctk.CTkLabel(
            self,
            text="Supports all file types",
            font=FONT_CAPTION,
            text_color=TEXT_TERTIARY
        )
        self.secondary_label.pack(pady=(0, SPACING_2XL))

        # Make clickable
        self.bind("<Button-1>", self._on_click)
        self.icon_label.bind("<Button-1>", self._on_click)
        self.primary_label.bind("<Button-1>", self._on_click)
        self.secondary_label.bind("<Button-1>", self._on_click)

        # Hover effects
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_click(self, event):
        from tkinter import filedialog
        filepath = filedialog.askopenfilename()
        if filepath and self.on_file_selected:
            self.on_file_selected(filepath)

    def _on_enter(self, event):
        self.configure(border_color=ACCENT_PRIMARY)

    def _on_leave(self, event):
        self.configure(border_color=BORDER_DEFAULT)

    def set_file(self, filename: str, size: str = ""):
        """Update display with selected file info."""
        self.icon_label.configure(text="📄")
        self.primary_label.configure(
            text=filename, text_color=TEXT_PRIMARY
        )
        if size:
            self.secondary_label.configure(text=size)

    def reset(self):
        """Reset to default state."""
        self.icon_label.configure(text="📂")
        self.primary_label.configure(
            text="Drop file here or click to browse",
            text_color=TEXT_SECONDARY
        )
        self.secondary_label.configure(text="Supports all file types")


class ActivityItem(ctk.CTkFrame):
    """Single activity/history item in the timeline."""

    def __init__(
        self,
        master,
        operation: str,
        filename: str,
        timestamp: str,
        status: str = "success",
        **kwargs
    ):
        super().__init__(
            master,
            fg_color="transparent",
            **kwargs
        )

        # Status dot
        status_colors = {
            "success": STATUS_SUCCESS,
            "failed": STATUS_ERROR,
            "warning": STATUS_WARNING
        }
        dot_color = status_colors.get(status, STATUS_INFO)

        # Left column: dot + line
        dot = ctk.CTkFrame(
            self, width=8, height=8,
            fg_color=dot_color,
            corner_radius=4
        )
        dot.place(x=0, y=6)

        # Content
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="x", padx=(20, 0))

        # Operation + filename
        op_icon = "🔒" if operation == "encrypt" else "🔓"
        ctk.CTkLabel(
            content_frame,
            text=f"{op_icon}  {filename}",
            font=(FONT_FAMILY, FONT_SIZE_SM),
            text_color=TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w")

        # Timestamp
        ctk.CTkLabel(
            content_frame,
            text=timestamp,
            font=FONT_CAPTION,
            text_color=TEXT_TERTIARY,
            anchor="w"
        ).pack(anchor="w", pady=(2, SPACING_SM))


class MetricWidget(ctk.CTkFrame):
    """Small inline metric display widget."""

    def __init__(
        self,
        master,
        label: str,
        value: str,
        trend: str = "",
        color: str = ACCENT_PRIMARY,
        **kwargs
    ):
        super().__init__(master, fg_color="transparent", **kwargs)

        ctk.CTkLabel(
            self,
            text=label,
            font=FONT_CAPTION,
            text_color=TEXT_TERTIARY,
            anchor="w"
        ).pack(anchor="w")

        value_frame = ctk.CTkFrame(self, fg_color="transparent")
        value_frame.pack(anchor="w", fill="x")

        ctk.CTkLabel(
            value_frame,
            text=value,
            font=(FONT_FAMILY, FONT_SIZE_LG, "bold"),
            text_color=color,
            anchor="w"
        ).pack(side="left")

        if trend:
            ctk.CTkLabel(
                value_frame,
                text=trend,
                font=FONT_CAPTION,
                text_color=STATUS_SUCCESS if "+" in trend else TEXT_TERTIARY,
                anchor="w"
            ).pack(side="left", padx=(SPACING_SM, 0))
