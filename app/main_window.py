"""
Main Application Window
Primary UI controller for the AES File Encryption Utility.

Author: Sahil Wade
"""

import os
import time
import threading
import logging
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from app.theme import *
from app.components import (
    GlowCard, StatusBadge, AnimatedProgressBar,
    SidebarButton, FileDropZone, ActivityItem, MetricWidget
)
from core.encryption import encrypt_file, decrypt_file, EncryptionError, DecryptionError
from core.password_generator import generate_password, generate_passphrase
from database.history import HistoryDB
from modules.file_utils import (
    format_file_size, get_file_info, validate_file_for_encryption,
    validate_file_for_decryption, generate_output_path
)

logger = logging.getLogger(__name__)



class MainWindow(ctk.CTk):
    """Main application window with sidebar navigation and content panels."""

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("AES File Encryption Utility")
        self.geometry("1280x780")
        self.minsize(1000, 650)
        self.configure(fg_color=BG_PRIMARY)

        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # State
        self.current_page = "dashboard"
        self.selected_file = None
        self.db = HistoryDB()
        self.nav_buttons = {}

        # Build UI
        self._build_sidebar()
        self._build_content_area()
        self._show_page("dashboard")

    # ─── Sidebar ──────────────────────────────────────────────────────────

    def _build_sidebar(self):
        """Build the navigation sidebar."""
        self.sidebar = ctk.CTkFrame(
            self,
            fg_color=BG_SIDEBAR,
            width=SIDEBAR_WIDTH,
            corner_radius=0,
            border_width=1,
            border_color=BORDER_SUBTLE
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # App branding
        brand_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand_frame.pack(fill="x", padx=PAD_SIDEBAR, pady=(SPACING_XL, SPACING_LG))

        ctk.CTkLabel(
            brand_frame,
            text="🛡️  AES Utility",
            font=(FONT_FAMILY, FONT_SIZE_LG, "bold"),
            text_color=TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            brand_frame,
            text="File Encryption Tool",
            font=FONT_CAPTION,
            text_color=TEXT_TERTIARY,
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))


        # Separator
        ctk.CTkFrame(
            self.sidebar, fg_color=BORDER_SUBTLE, height=1
        ).pack(fill="x", padx=PAD_SIDEBAR, pady=SPACING_MD)

        # Navigation buttons
        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.pack(fill="x", padx=SPACING_SM, pady=SPACING_SM)

        for item in NAV_ITEMS:
            btn = SidebarButton(
                nav_frame,
                text=item["label"],
                icon=item["icon"],
                command=lambda page=item["id"]: self._show_page(page),
                is_active=(item["id"] == "dashboard")
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons[item["id"]] = btn

        # Bottom section - version info
        bottom_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom_frame.pack(side="bottom", fill="x", padx=PAD_SIDEBAR, pady=PAD_SIDEBAR)

        ctk.CTkLabel(
            bottom_frame,
            text="v1.2.0",
            font=FONT_CAPTION,
            text_color=TEXT_TERTIARY,
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            bottom_frame,
            text="by Sahil Wade",
            font=FONT_CAPTION,
            text_color=TEXT_TERTIARY,
            anchor="w"
        ).pack(anchor="w")

    # ─── Content Area ─────────────────────────────────────────────────────

    def _build_content_area(self):
        """Build the main content area container."""
        self.content_frame = ctk.CTkFrame(
            self, fg_color=BG_PRIMARY, corner_radius=0
        )
        self.content_frame.pack(side="left", fill="both", expand=True)

    def _clear_content(self):
        """Clear current content page."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def _show_page(self, page_id: str):
        """Switch to a different page."""
        # Update nav state
        for nav_id, btn in self.nav_buttons.items():
            if nav_id == page_id:
                btn.set_active()
            else:
                btn.set_inactive()

        self.current_page = page_id
        self._clear_content()

        pages = {
            "dashboard": self._build_dashboard_page,
            "encrypt": self._build_encrypt_page,
            "decrypt": self._build_decrypt_page,
            "password": self._build_password_page,
            "history": self._build_history_page,
            "settings": self._build_settings_page,
        }

        builder = pages.get(page_id)
        if builder:
            builder()


    # ─── Dashboard Page ───────────────────────────────────────────────────

    def _build_dashboard_page(self):
        """Build the main dashboard overview page."""
        # Scrollable container
        scroll = ctk.CTkScrollableFrame(
            self.content_frame, fg_color="transparent"
        )
        scroll.pack(fill="both", expand=True, padx=SPACING_2XL, pady=SPACING_XL)

        # Page header
        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, SPACING_XL))

        ctk.CTkLabel(
            header,
            text="Dashboard",
            font=FONT_TITLE,
            text_color=TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Overview of your encryption activity and security status",
            font=(FONT_FAMILY, FONT_SIZE_SM),
            text_color=TEXT_SECONDARY,
            anchor="w"
        ).pack(anchor="w", pady=(SPACING_XS, 0))

        # Statistics cards row
        stats = self.db.get_statistics()

        cards_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, SPACING_XL))
        cards_frame.columnconfigure((0, 1, 2, 3), weight=1)

        card_data = [
            ("Total Operations", str(stats["total_operations"]), "All time", ACCENT_PRIMARY),
            ("Encryptions", str(stats["total_encryptions"]), "Files secured", STATUS_SUCCESS),
            ("Decryptions", str(stats["total_decryptions"]), "Files restored", ACCENT_CYAN),
            ("Success Rate", f"{stats['success_rate']}%", "Reliability", ACCENT_SECONDARY),
        ]

        for i, (title, value, subtitle, color) in enumerate(card_data):
            card = GlowCard(
                cards_frame,
                title=title,
                value=value,
                subtitle=subtitle,
                accent_color=color
            )
            card.grid(row=0, column=i, padx=SPACING_SM, sticky="nsew")


        # Quick actions + Recent activity row
        bottom_row = ctk.CTkFrame(scroll, fg_color="transparent")
        bottom_row.pack(fill="x", pady=(0, SPACING_XL))
        bottom_row.columnconfigure(0, weight=2)
        bottom_row.columnconfigure(1, weight=1)

        # Quick Actions panel
        actions_panel = ctk.CTkFrame(
            bottom_row, fg_color=BG_CARD, corner_radius=RADIUS_LG,
            border_width=1, border_color=BORDER_SUBTLE
        )
        actions_panel.grid(row=0, column=0, sticky="nsew", padx=(0, SPACING_MD))

        ctk.CTkLabel(
            actions_panel, text="Quick Actions",
            font=FONT_SUBHEADING, text_color=TEXT_PRIMARY, anchor="w"
        ).pack(anchor="w", padx=PAD_CARD, pady=(PAD_CARD, SPACING_MD))

        actions_grid = ctk.CTkFrame(actions_panel, fg_color="transparent")
        actions_grid.pack(fill="x", padx=PAD_CARD, pady=(0, PAD_CARD))

        ctk.CTkButton(
            actions_grid, text="🔒  Encrypt File",
            font=(FONT_FAMILY, FONT_SIZE_SM, "bold"),
            fg_color=ACCENT_PRIMARY, hover_color=ACCENT_SECONDARY,
            height=36, corner_radius=RADIUS_MD,
            command=lambda: self._show_page("encrypt")
        ).pack(side="left", padx=(0, SPACING_SM))

        ctk.CTkButton(
            actions_grid, text="🔓  Decrypt File",
            font=(FONT_FAMILY, FONT_SIZE_SM, "bold"),
            fg_color=BG_SURFACE, hover_color=BG_CARD_HOVER,
            height=36, corner_radius=RADIUS_MD,
            command=lambda: self._show_page("decrypt")
        ).pack(side="left", padx=(0, SPACING_SM))

        ctk.CTkButton(
            actions_grid, text="🔑  Generate Password",
            font=(FONT_FAMILY, FONT_SIZE_SM, "bold"),
            fg_color=BG_SURFACE, hover_color=BG_CARD_HOVER,
            height=36, corner_radius=RADIUS_MD,
            command=lambda: self._show_page("password")
        ).pack(side="left")

        # Recent Activity panel
        activity_panel = ctk.CTkFrame(
            bottom_row, fg_color=BG_CARD, corner_radius=RADIUS_LG,
            border_width=1, border_color=BORDER_SUBTLE
        )
        activity_panel.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(
            activity_panel, text="Recent Activity",
            font=FONT_SUBHEADING, text_color=TEXT_PRIMARY, anchor="w"
        ).pack(anchor="w", padx=PAD_CARD, pady=(PAD_CARD, SPACING_MD))

        recent = self.db.get_recent_operations(limit=5)
        if recent:
            for op in recent:
                ts = op["timestamp"][:16].replace("T", "  ")
                ActivityItem(
                    activity_panel,
                    operation=op["operation_type"],
                    filename=op["filename"],
                    timestamp=ts,
                    status=op["status"]
                ).pack(fill="x", padx=PAD_CARD, pady=2)
        else:
            ctk.CTkLabel(
                activity_panel,
                text="No recent activity",
                font=(FONT_FAMILY, FONT_SIZE_SM),
                text_color=TEXT_TERTIARY
            ).pack(padx=PAD_CARD, pady=SPACING_XL)

        # Security status card
        security_frame = ctk.CTkFrame(
            scroll, fg_color=BG_CARD, corner_radius=RADIUS_LG,
            border_width=1, border_color=BORDER_SUBTLE
        )
        security_frame.pack(fill="x", pady=(0, SPACING_XL))

        sec_inner = ctk.CTkFrame(security_frame, fg_color="transparent")
        sec_inner.pack(fill="x", padx=PAD_CARD, pady=PAD_CARD)

        ctk.CTkLabel(
            sec_inner, text="🛡️  Security Status",
            font=FONT_SUBHEADING, text_color=TEXT_PRIMARY, anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            sec_inner,
            text="AES-256-GCM  •  PBKDF2-SHA256 (600K iterations)  •  Local processing only",
            font=(FONT_FAMILY, FONT_SIZE_SM),
            text_color=STATUS_SUCCESS, anchor="w"
        ).pack(anchor="w", pady=(SPACING_XS, 0))


    # ─── Encrypt Page ─────────────────────────────────────────────────────

    def _build_encrypt_page(self):
        """Build the file encryption page."""
        scroll = ctk.CTkScrollableFrame(
            self.content_frame, fg_color="transparent"
        )
        scroll.pack(fill="both", expand=True, padx=SPACING_2XL, pady=SPACING_XL)

        # Header
        ctk.CTkLabel(
            scroll, text="Encrypt File",
            font=FONT_TITLE, text_color=TEXT_PRIMARY, anchor="w"
        ).pack(anchor="w")
        ctk.CTkLabel(
            scroll, text="Secure your files with AES-256-GCM encryption",
            font=(FONT_FAMILY, FONT_SIZE_SM), text_color=TEXT_SECONDARY, anchor="w"
        ).pack(anchor="w", pady=(SPACING_XS, SPACING_XL))

        # File selection
        self.encrypt_drop = FileDropZone(
            scroll, on_file_selected=self._on_encrypt_file_selected,
            height=160
        )
        self.encrypt_drop.pack(fill="x", pady=(0, SPACING_XL))

        # Password input section
        pass_frame = ctk.CTkFrame(
            scroll, fg_color=BG_CARD, corner_radius=RADIUS_LG,
            border_width=1, border_color=BORDER_SUBTLE
        )
        pass_frame.pack(fill="x", pady=(0, SPACING_XL))

        pass_inner = ctk.CTkFrame(pass_frame, fg_color="transparent")
        pass_inner.pack(fill="x", padx=PAD_CARD, pady=PAD_CARD)

        ctk.CTkLabel(
            pass_inner, text="Encryption Password",
            font=FONT_BOLD, text_color=TEXT_PRIMARY, anchor="w"
        ).pack(anchor="w")
        ctk.CTkLabel(
            pass_inner, text="Choose a strong password — you'll need it to decrypt",
            font=FONT_CAPTION, text_color=TEXT_TERTIARY, anchor="w"
        ).pack(anchor="w", pady=(2, SPACING_MD))

        self.encrypt_password = ctk.CTkEntry(
            pass_inner, placeholder_text="Enter encryption password",
            show="•", height=INPUT_HEIGHT, font=FONT_REGULAR,
            fg_color=BG_INPUT, border_color=BORDER_DEFAULT,
            corner_radius=RADIUS_MD
        )
        self.encrypt_password.pack(fill="x", pady=(0, SPACING_SM))

        self.encrypt_confirm = ctk.CTkEntry(
            pass_inner, placeholder_text="Confirm password",
            show="•", height=INPUT_HEIGHT, font=FONT_REGULAR,
            fg_color=BG_INPUT, border_color=BORDER_DEFAULT,
            corner_radius=RADIUS_MD
        )
        self.encrypt_confirm.pack(fill="x")

        # Progress area
        self.encrypt_progress_frame = ctk.CTkFrame(
            scroll, fg_color=BG_CARD, corner_radius=RADIUS_LG,
            border_width=1, border_color=BORDER_SUBTLE
        )

        self.encrypt_status_label = ctk.CTkLabel(
            self.encrypt_progress_frame, text="Ready",
            font=(FONT_FAMILY, FONT_SIZE_SM), text_color=TEXT_SECONDARY
        )

        self.encrypt_progress = ctk.CTkProgressBar(
            self.encrypt_progress_frame,
            fg_color=BG_INPUT, progress_color=ACCENT_PRIMARY,
            height=6, corner_radius=3
        )

        # Encrypt button
        self.encrypt_btn = ctk.CTkButton(
            scroll, text="🔒  Encrypt File",
            font=(FONT_FAMILY, FONT_SIZE_MD, "bold"),
            fg_color=ACCENT_PRIMARY, hover_color=ACCENT_SECONDARY,
            height=44, corner_radius=RADIUS_MD,
            command=self._do_encrypt
        )
        self.encrypt_btn.pack(fill="x")

    def _on_encrypt_file_selected(self, filepath: str):
        """Handle file selection for encryption."""
        self.selected_file = filepath
        info = get_file_info(filepath)
        if info:
            self.encrypt_drop.set_file(
                info["name"], info["size_formatted"]
            )


    def _do_encrypt(self):
        """Execute file encryption in background thread."""
        if not self.selected_file:
            messagebox.showwarning("No File", "Please select a file to encrypt.")
            return

        password = self.encrypt_password.get()
        confirm = self.encrypt_confirm.get()

        if not password:
            messagebox.showwarning("Password Required", "Please enter an encryption password.")
            return

        if password != confirm:
            messagebox.showerror("Mismatch", "Passwords do not match.")
            return

        if len(password) < 6:
            messagebox.showwarning("Weak Password", "Password should be at least 6 characters.")
            return

        valid, msg = validate_file_for_encryption(self.selected_file)
        if not valid:
            messagebox.showerror("Invalid File", msg)
            return

        # Show progress
        self.encrypt_progress_frame.pack(fill="x", pady=(0, SPACING_MD))
        self.encrypt_status_label.pack(padx=PAD_CARD, pady=(PAD_CARD, SPACING_SM), anchor="w")
        self.encrypt_progress.pack(fill="x", padx=PAD_CARD, pady=(0, PAD_CARD))
        self.encrypt_progress.set(0)
        self.encrypt_status_label.configure(text="Encrypting...", text_color=ACCENT_CYAN)
        self.encrypt_btn.configure(state="disabled")

        def run_encryption():
            start = time.time()
            try:
                output_path = generate_output_path(self.selected_file, "encrypt")

                def progress_cb(val):
                    self.after(0, lambda: self.encrypt_progress.set(val))

                result = encrypt_file(
                    self.selected_file, output_path, password,
                    progress_callback=progress_cb
                )

                duration_ms = int((time.time() - start) * 1000)
                info = get_file_info(self.selected_file)

                self.db.record_operation(
                    operation_type="encrypt",
                    filename=info["name"] if info else Path(self.selected_file).name,
                    filepath=self.selected_file,
                    file_size=result["original_size"],
                    status="success",
                    duration_ms=duration_ms,
                    file_hash=result["original_hash"]
                )

                self.after(0, lambda: self._encryption_complete(True, output_path))

            except EncryptionError as e:
                duration_ms = int((time.time() - start) * 1000)
                self.db.record_operation(
                    operation_type="encrypt",
                    filename=Path(self.selected_file).name,
                    filepath=self.selected_file,
                    status="failed",
                    duration_ms=duration_ms,
                    notes=str(e)
                )
                self.after(0, lambda: self._encryption_complete(False, str(e)))

        thread = threading.Thread(target=run_encryption, daemon=True)
        thread.start()

    def _encryption_complete(self, success: bool, message: str):
        """Handle encryption completion."""
        self.encrypt_btn.configure(state="normal")
        if success:
            self.encrypt_status_label.configure(
                text="✓ Encryption complete", text_color=STATUS_SUCCESS
            )
            self.encrypt_progress.set(1.0)
            messagebox.showinfo(
                "Success", f"File encrypted successfully.\n\nSaved to:\n{message}"
            )
        else:
            self.encrypt_status_label.configure(
                text="✗ Encryption failed", text_color=STATUS_ERROR
            )
            messagebox.showerror("Error", f"Encryption failed:\n{message}")


    # ─── Decrypt Page ─────────────────────────────────────────────────────

    def _build_decrypt_page(self):
        """Build the file decryption page."""
        scroll = ctk.CTkScrollableFrame(
            self.content_frame, fg_color="transparent"
        )
        scroll.pack(fill="both", expand=True, padx=SPACING_2XL, pady=SPACING_XL)

        # Header
        ctk.CTkLabel(
            scroll, text="Decrypt File",
            font=FONT_TITLE, text_color=TEXT_PRIMARY, anchor="w"
        ).pack(anchor="w")
        ctk.CTkLabel(
            scroll, text="Restore files encrypted with this utility",
            font=(FONT_FAMILY, FONT_SIZE_SM), text_color=TEXT_SECONDARY, anchor="w"
        ).pack(anchor="w", pady=(SPACING_XS, SPACING_XL))

        # File selection
        self.decrypt_drop = FileDropZone(
            scroll, on_file_selected=self._on_decrypt_file_selected,
            height=160
        )
        self.decrypt_drop.pack(fill="x", pady=(0, SPACING_XL))

        # Password input
        pass_frame = ctk.CTkFrame(
            scroll, fg_color=BG_CARD, corner_radius=RADIUS_LG,
            border_width=1, border_color=BORDER_SUBTLE
        )
        pass_frame.pack(fill="x", pady=(0, SPACING_XL))

        pass_inner = ctk.CTkFrame(pass_frame, fg_color="transparent")
        pass_inner.pack(fill="x", padx=PAD_CARD, pady=PAD_CARD)

        ctk.CTkLabel(
            pass_inner, text="Decryption Password",
            font=FONT_BOLD, text_color=TEXT_PRIMARY, anchor="w"
        ).pack(anchor="w")
        ctk.CTkLabel(
            pass_inner, text="Enter the password used during encryption",
            font=FONT_CAPTION, text_color=TEXT_TERTIARY, anchor="w"
        ).pack(anchor="w", pady=(2, SPACING_MD))

        self.decrypt_password = ctk.CTkEntry(
            pass_inner, placeholder_text="Enter decryption password",
            show="•", height=INPUT_HEIGHT, font=FONT_REGULAR,
            fg_color=BG_INPUT, border_color=BORDER_DEFAULT,
            corner_radius=RADIUS_MD
        )
        self.decrypt_password.pack(fill="x")

        # Output directory
        dir_frame = ctk.CTkFrame(
            scroll, fg_color=BG_CARD, corner_radius=RADIUS_LG,
            border_width=1, border_color=BORDER_SUBTLE
        )
        dir_frame.pack(fill="x", pady=(0, SPACING_XL))

        dir_inner = ctk.CTkFrame(dir_frame, fg_color="transparent")
        dir_inner.pack(fill="x", padx=PAD_CARD, pady=PAD_CARD)

        ctk.CTkLabel(
            dir_inner, text="Output Directory",
            font=FONT_BOLD, text_color=TEXT_PRIMARY, anchor="w"
        ).pack(anchor="w", pady=(0, SPACING_SM))

        dir_row = ctk.CTkFrame(dir_inner, fg_color="transparent")
        dir_row.pack(fill="x")

        self.decrypt_output_dir = ctk.CTkEntry(
            dir_row, placeholder_text="Select output directory...",
            height=INPUT_HEIGHT, font=FONT_REGULAR,
            fg_color=BG_INPUT, border_color=BORDER_DEFAULT,
            corner_radius=RADIUS_MD
        )
        self.decrypt_output_dir.pack(side="left", fill="x", expand=True, padx=(0, SPACING_SM))

        ctk.CTkButton(
            dir_row, text="Browse", width=80,
            fg_color=BG_SURFACE, hover_color=BG_CARD_HOVER,
            font=(FONT_FAMILY, FONT_SIZE_SM),
            corner_radius=RADIUS_MD,
            command=self._browse_output_dir
        ).pack(side="right")

        # Progress
        self.decrypt_progress_frame = ctk.CTkFrame(
            scroll, fg_color=BG_CARD, corner_radius=RADIUS_LG,
            border_width=1, border_color=BORDER_SUBTLE
        )
        self.decrypt_status_label = ctk.CTkLabel(
            self.decrypt_progress_frame, text="Ready",
            font=(FONT_FAMILY, FONT_SIZE_SM), text_color=TEXT_SECONDARY
        )
        self.decrypt_progress = ctk.CTkProgressBar(
            self.decrypt_progress_frame,
            fg_color=BG_INPUT, progress_color=ACCENT_CYAN,
            height=6, corner_radius=3
        )

        # Decrypt button
        self.decrypt_btn = ctk.CTkButton(
            scroll, text="🔓  Decrypt File",
            font=(FONT_FAMILY, FONT_SIZE_MD, "bold"),
            fg_color=ACCENT_CYAN, hover_color=ACCENT_PRIMARY,
            text_color=BG_PRIMARY,
            height=44, corner_radius=RADIUS_MD,
            command=self._do_decrypt
        )
        self.decrypt_btn.pack(fill="x")


    def _on_decrypt_file_selected(self, filepath: str):
        """Handle file selection for decryption."""
        self.selected_file = filepath
        info = get_file_info(filepath)
        if info:
            self.decrypt_drop.set_file(info["name"], info["size_formatted"])
            # Auto-fill output dir
            self.decrypt_output_dir.delete(0, "end")
            self.decrypt_output_dir.insert(0, info["parent"])

    def _browse_output_dir(self):
        """Browse for output directory."""
        dirpath = filedialog.askdirectory()
        if dirpath:
            self.decrypt_output_dir.delete(0, "end")
            self.decrypt_output_dir.insert(0, dirpath)

    def _do_decrypt(self):
        """Execute file decryption in background thread."""
        if not self.selected_file:
            messagebox.showwarning("No File", "Please select a file to decrypt.")
            return

        password = self.decrypt_password.get()
        if not password:
            messagebox.showwarning("Password Required", "Please enter the decryption password.")
            return

        output_dir = self.decrypt_output_dir.get()
        if not output_dir:
            output_dir = str(Path(self.selected_file).parent)

        valid, msg = validate_file_for_decryption(self.selected_file)
        if not valid:
            messagebox.showerror("Invalid File", msg)
            return

        # Show progress
        self.decrypt_progress_frame.pack(fill="x", pady=(0, SPACING_MD))
        self.decrypt_status_label.pack(padx=PAD_CARD, pady=(PAD_CARD, SPACING_SM), anchor="w")
        self.decrypt_progress.pack(fill="x", padx=PAD_CARD, pady=(0, PAD_CARD))
        self.decrypt_progress.set(0)
        self.decrypt_status_label.configure(text="Decrypting...", text_color=ACCENT_CYAN)
        self.decrypt_btn.configure(state="disabled")

        def run_decryption():
            start = time.time()
            try:
                def progress_cb(val):
                    self.after(0, lambda: self.decrypt_progress.set(val))

                result = decrypt_file(
                    self.selected_file, output_dir, password,
                    progress_callback=progress_cb
                )

                duration_ms = int((time.time() - start) * 1000)

                self.db.record_operation(
                    operation_type="decrypt",
                    filename=result["original_name"],
                    filepath=result["output_path"],
                    file_size=result["file_size"],
                    status="success",
                    duration_ms=duration_ms,
                    file_hash=result["file_hash"]
                )

                self.after(0, lambda: self._decryption_complete(True, result["output_path"]))

            except DecryptionError as e:
                duration_ms = int((time.time() - start) * 1000)
                self.db.record_operation(
                    operation_type="decrypt",
                    filename=Path(self.selected_file).name,
                    filepath=self.selected_file,
                    status="failed",
                    duration_ms=duration_ms,
                    notes=str(e)
                )
                self.after(0, lambda: self._decryption_complete(False, str(e)))

        thread = threading.Thread(target=run_decryption, daemon=True)
        thread.start()

    def _decryption_complete(self, success: bool, message: str):
        """Handle decryption completion."""
        self.decrypt_btn.configure(state="normal")
        if success:
            self.decrypt_status_label.configure(
                text="✓ Decryption complete", text_color=STATUS_SUCCESS
            )
            self.decrypt_progress.set(1.0)
            messagebox.showinfo(
                "Success", f"File decrypted successfully.\n\nSaved to:\n{message}"
            )
        else:
            self.decrypt_status_label.configure(
                text="✗ Decryption failed", text_color=STATUS_ERROR
            )
            messagebox.showerror("Error", f"Decryption failed:\n{message}")


    # ─── Password Generator Page ──────────────────────────────────────────

    def _build_password_page(self):
        """Build the password generator page."""
        scroll = ctk.CTkScrollableFrame(
            self.content_frame, fg_color="transparent"
        )
        scroll.pack(fill="both", expand=True, padx=SPACING_2XL, pady=SPACING_XL)

        # Header
        ctk.CTkLabel(
            scroll, text="Password Generator",
            font=FONT_TITLE, text_color=TEXT_PRIMARY, anchor="w"
        ).pack(anchor="w")
        ctk.CTkLabel(
            scroll,
            text="Generate cryptographically secure passwords for encryption",
            font=(FONT_FAMILY, FONT_SIZE_SM), text_color=TEXT_SECONDARY, anchor="w"
        ).pack(anchor="w", pady=(SPACING_XS, SPACING_XL))

        # Generated password display
        result_frame = ctk.CTkFrame(
            scroll, fg_color=BG_CARD, corner_radius=RADIUS_LG,
            border_width=1, border_color=BORDER_SUBTLE
        )
        result_frame.pack(fill="x", pady=(0, SPACING_XL))

        result_inner = ctk.CTkFrame(result_frame, fg_color="transparent")
        result_inner.pack(fill="x", padx=PAD_CARD, pady=PAD_CARD)

        self.password_display = ctk.CTkEntry(
            result_inner, font=(FONT_FAMILY_MONO, FONT_SIZE_LG),
            fg_color=BG_INPUT, border_color=BORDER_DEFAULT,
            height=50, corner_radius=RADIUS_MD,
            text_color=ACCENT_BLUE_SOFT
        )
        self.password_display.pack(fill="x", pady=(0, SPACING_MD))

        # Action buttons row
        btn_row = ctk.CTkFrame(result_inner, fg_color="transparent")
        btn_row.pack(fill="x")

        ctk.CTkButton(
            btn_row, text="⟳  Generate",
            font=(FONT_FAMILY, FONT_SIZE_SM, "bold"),
            fg_color=ACCENT_PRIMARY, hover_color=ACCENT_SECONDARY,
            height=36, corner_radius=RADIUS_MD, width=130,
            command=self._generate_new_password
        ).pack(side="left", padx=(0, SPACING_SM))

        ctk.CTkButton(
            btn_row, text="📋  Copy",
            font=(FONT_FAMILY, FONT_SIZE_SM, "bold"),
            fg_color=BG_SURFACE, hover_color=BG_CARD_HOVER,
            height=36, corner_radius=RADIUS_MD, width=100,
            command=self._copy_password
        ).pack(side="left")

        # Strength display
        self.strength_frame = ctk.CTkFrame(result_inner, fg_color="transparent")
        self.strength_frame.pack(fill="x", pady=(SPACING_MD, 0))

        self.strength_label = ctk.CTkLabel(
            self.strength_frame, text="Strength: —",
            font=(FONT_FAMILY, FONT_SIZE_SM, "bold"),
            text_color=TEXT_SECONDARY, anchor="w"
        )
        self.strength_label.pack(side="left")

        self.entropy_label = ctk.CTkLabel(
            self.strength_frame, text="Entropy: — bits",
            font=(FONT_FAMILY, FONT_SIZE_SM),
            text_color=TEXT_TERTIARY, anchor="e"
        )
        self.entropy_label.pack(side="right")

        # Options panel
        options_frame = ctk.CTkFrame(
            scroll, fg_color=BG_CARD, corner_radius=RADIUS_LG,
            border_width=1, border_color=BORDER_SUBTLE
        )
        options_frame.pack(fill="x", pady=(0, SPACING_XL))

        options_inner = ctk.CTkFrame(options_frame, fg_color="transparent")
        options_inner.pack(fill="x", padx=PAD_CARD, pady=PAD_CARD)

        ctk.CTkLabel(
            options_inner, text="Options",
            font=FONT_SUBHEADING, text_color=TEXT_PRIMARY, anchor="w"
        ).pack(anchor="w", pady=(0, SPACING_MD))

        # Length slider
        len_row = ctk.CTkFrame(options_inner, fg_color="transparent")
        len_row.pack(fill="x", pady=(0, SPACING_MD))

        ctk.CTkLabel(
            len_row, text="Length:",
            font=(FONT_FAMILY, FONT_SIZE_SM), text_color=TEXT_SECONDARY
        ).pack(side="left")

        self.length_value_label = ctk.CTkLabel(
            len_row, text="20",
            font=(FONT_FAMILY, FONT_SIZE_SM, "bold"), text_color=TEXT_PRIMARY
        )
        self.length_value_label.pack(side="right")

        self.length_slider = ctk.CTkSlider(
            options_inner, from_=8, to=64, number_of_steps=56,
            fg_color=BG_INPUT, progress_color=ACCENT_PRIMARY,
            button_color=ACCENT_PRIMARY, button_hover_color=ACCENT_SECONDARY,
            command=self._on_length_change
        )
        self.length_slider.set(20)
        self.length_slider.pack(fill="x", pady=(0, SPACING_MD))

        # Character options
        self.use_upper = ctk.CTkCheckBox(
            options_inner, text="Uppercase (A-Z)",
            font=(FONT_FAMILY, FONT_SIZE_SM), text_color=TEXT_SECONDARY,
            fg_color=ACCENT_PRIMARY, hover_color=ACCENT_SECONDARY,
            corner_radius=RADIUS_SM
        )
        self.use_upper.select()
        self.use_upper.pack(anchor="w", pady=3)

        self.use_lower = ctk.CTkCheckBox(
            options_inner, text="Lowercase (a-z)",
            font=(FONT_FAMILY, FONT_SIZE_SM), text_color=TEXT_SECONDARY,
            fg_color=ACCENT_PRIMARY, hover_color=ACCENT_SECONDARY,
            corner_radius=RADIUS_SM
        )
        self.use_lower.select()
        self.use_lower.pack(anchor="w", pady=3)

        self.use_digits = ctk.CTkCheckBox(
            options_inner, text="Digits (0-9)",
            font=(FONT_FAMILY, FONT_SIZE_SM), text_color=TEXT_SECONDARY,
            fg_color=ACCENT_PRIMARY, hover_color=ACCENT_SECONDARY,
            corner_radius=RADIUS_SM
        )
        self.use_digits.select()
        self.use_digits.pack(anchor="w", pady=3)

        self.use_symbols = ctk.CTkCheckBox(
            options_inner, text="Symbols (!@#$%...)",
            font=(FONT_FAMILY, FONT_SIZE_SM), text_color=TEXT_SECONDARY,
            fg_color=ACCENT_PRIMARY, hover_color=ACCENT_SECONDARY,
            corner_radius=RADIUS_SM
        )
        self.use_symbols.select()
        self.use_symbols.pack(anchor="w", pady=3)

        # Generate initial password
        self._generate_new_password()


    def _on_length_change(self, value):
        """Handle password length slider change."""
        self.length_value_label.configure(text=str(int(value)))

    def _generate_new_password(self):
        """Generate and display a new password."""
        length = int(self.length_slider.get()) if hasattr(self, "length_slider") else 20
        use_upper = self.use_upper.get() if hasattr(self, "use_upper") else True
        use_lower = self.use_lower.get() if hasattr(self, "use_lower") else True
        use_digits = self.use_digits.get() if hasattr(self, "use_digits") else True
        use_symbols = self.use_symbols.get() if hasattr(self, "use_symbols") else True

        result = generate_password(
            length=length,
            use_uppercase=bool(use_upper),
            use_lowercase=bool(use_lower),
            use_digits=bool(use_digits),
            use_symbols=bool(use_symbols)
        )

        # Update display
        self.password_display.delete(0, "end")
        self.password_display.insert(0, result.password)

        # Update strength
        strength_colors = {
            "Excellent": STATUS_SUCCESS,
            "Strong": STATUS_SUCCESS,
            "Good": ACCENT_PRIMARY,
            "Fair": STATUS_WARNING,
            "Weak": STATUS_ERROR
        }
        color = strength_colors.get(result.strength, TEXT_SECONDARY)

        self.strength_label.configure(
            text=f"Strength: {result.strength}", text_color=color
        )
        self.entropy_label.configure(
            text=f"Entropy: {result.entropy} bits"
        )

    def _copy_password(self):
        """Copy generated password to clipboard."""
        password = self.password_display.get()
        if password:
            self.clipboard_clear()
            self.clipboard_append(password)
            # Brief visual feedback
            self.strength_label.configure(
                text="✓ Copied to clipboard!", text_color=STATUS_SUCCESS
            )
            self.after(2000, self._generate_new_password)


    # ─── History Page ─────────────────────────────────────────────────────

    def _build_history_page(self):
        """Build the encryption history page."""
        scroll = ctk.CTkScrollableFrame(
            self.content_frame, fg_color="transparent"
        )
        scroll.pack(fill="both", expand=True, padx=SPACING_2XL, pady=SPACING_XL)

        # Header
        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, SPACING_XL))

        ctk.CTkLabel(
            header, text="Encryption History",
            font=FONT_TITLE, text_color=TEXT_PRIMARY, anchor="w"
        ).pack(side="left", anchor="w")

        ctk.CTkButton(
            header, text="Clear History", width=110,
            font=(FONT_FAMILY, FONT_SIZE_SM),
            fg_color=BG_SURFACE, hover_color=STATUS_ERROR + "30",
            text_color=STATUS_ERROR, corner_radius=RADIUS_MD,
            height=32, command=self._clear_history
        ).pack(side="right")

        # Operations list
        operations = self.db.get_recent_operations(limit=50)

        if not operations:
            empty_frame = ctk.CTkFrame(
                scroll, fg_color=BG_CARD, corner_radius=RADIUS_LG,
                border_width=1, border_color=BORDER_SUBTLE
            )
            empty_frame.pack(fill="x", pady=SPACING_XL)
            ctk.CTkLabel(
                empty_frame, text="No operations recorded yet",
                font=(FONT_FAMILY, FONT_SIZE_MD), text_color=TEXT_TERTIARY
            ).pack(pady=SPACING_3XL)
            ctk.CTkLabel(
                empty_frame,
                text="Encrypt or decrypt a file to see history here",
                font=(FONT_FAMILY, FONT_SIZE_SM), text_color=TEXT_TERTIARY
            ).pack(pady=(0, SPACING_3XL))
            return

        # Table header
        table_header = ctk.CTkFrame(
            scroll, fg_color=BG_TERTIARY, corner_radius=RADIUS_MD, height=36
        )
        table_header.pack(fill="x", pady=(0, 2))
        table_header.pack_propagate(False)

        cols = ["Time", "Operation", "File", "Size", "Status"]
        widths = [140, 80, 250, 80, 80]

        header_inner = ctk.CTkFrame(table_header, fg_color="transparent")
        header_inner.pack(fill="x", padx=SPACING_MD, pady=SPACING_SM)

        for col, w in zip(cols, widths):
            ctk.CTkLabel(
                header_inner, text=col, width=w,
                font=(FONT_FAMILY, FONT_SIZE_XS, "bold"),
                text_color=TEXT_TERTIARY, anchor="w"
            ).pack(side="left")

        # Table rows
        for op in operations:
            row = ctk.CTkFrame(
                scroll, fg_color=BG_CARD, corner_radius=RADIUS_SM,
                height=38, border_width=1, border_color=BORDER_SUBTLE
            )
            row.pack(fill="x", pady=1)
            row.pack_propagate(False)

            row_inner = ctk.CTkFrame(row, fg_color="transparent")
            row_inner.pack(fill="x", padx=SPACING_MD, pady=SPACING_SM)

            # Timestamp
            ts = op["timestamp"][:16].replace("T", " ")
            ctk.CTkLabel(
                row_inner, text=ts, width=140,
                font=FONT_MONO_SM, text_color=TEXT_SECONDARY, anchor="w"
            ).pack(side="left")

            # Operation type
            op_text = op["operation_type"].capitalize()
            ctk.CTkLabel(
                row_inner, text=op_text, width=80,
                font=(FONT_FAMILY, FONT_SIZE_SM),
                text_color=ACCENT_PRIMARY if op["operation_type"] == "encrypt" else ACCENT_CYAN,
                anchor="w"
            ).pack(side="left")

            # Filename
            fname = op["filename"][:30] + "..." if len(op["filename"]) > 30 else op["filename"]
            ctk.CTkLabel(
                row_inner, text=fname, width=250,
                font=(FONT_FAMILY, FONT_SIZE_SM), text_color=TEXT_PRIMARY, anchor="w"
            ).pack(side="left")

            # Size
            size_text = format_file_size(op["file_size"]) if op["file_size"] else "—"
            ctk.CTkLabel(
                row_inner, text=size_text, width=80,
                font=(FONT_FAMILY, FONT_SIZE_SM), text_color=TEXT_SECONDARY, anchor="w"
            ).pack(side="left")

            # Status
            status_color = STATUS_SUCCESS if op["status"] == "success" else STATUS_ERROR
            ctk.CTkLabel(
                row_inner, text=op["status"].capitalize(), width=80,
                font=(FONT_FAMILY, FONT_SIZE_SM, "bold"),
                text_color=status_color, anchor="w"
            ).pack(side="left")

    def _clear_history(self):
        """Clear all history with confirmation."""
        confirm = messagebox.askyesno(
            "Clear History",
            "Are you sure you want to clear all encryption history?\n\nThis cannot be undone."
        )
        if confirm:
            self.db.clear_history()
            self._show_page("history")


    # ─── Settings Page ────────────────────────────────────────────────────

    def _build_settings_page(self):
        """Build the settings page."""
        scroll = ctk.CTkScrollableFrame(
            self.content_frame, fg_color="transparent"
        )
        scroll.pack(fill="both", expand=True, padx=SPACING_2XL, pady=SPACING_XL)

        # Header
        ctk.CTkLabel(
            scroll, text="Settings",
            font=FONT_TITLE, text_color=TEXT_PRIMARY, anchor="w"
        ).pack(anchor="w")
        ctk.CTkLabel(
            scroll, text="Configure application preferences",
            font=(FONT_FAMILY, FONT_SIZE_SM), text_color=TEXT_SECONDARY, anchor="w"
        ).pack(anchor="w", pady=(SPACING_XS, SPACING_XL))

        # Encryption settings
        enc_frame = ctk.CTkFrame(
            scroll, fg_color=BG_CARD, corner_radius=RADIUS_LG,
            border_width=1, border_color=BORDER_SUBTLE
        )
        enc_frame.pack(fill="x", pady=(0, SPACING_XL))

        enc_inner = ctk.CTkFrame(enc_frame, fg_color="transparent")
        enc_inner.pack(fill="x", padx=PAD_CARD, pady=PAD_CARD)

        ctk.CTkLabel(
            enc_inner, text="Encryption",
            font=FONT_SUBHEADING, text_color=TEXT_PRIMARY, anchor="w"
        ).pack(anchor="w", pady=(0, SPACING_MD))

        # Algorithm info
        info_items = [
            ("Algorithm", "AES-256-GCM (Galois/Counter Mode)"),
            ("Key Derivation", "PBKDF2-HMAC-SHA256"),
            ("Iterations", "600,000"),
            ("Salt Size", "256 bits"),
            ("Nonce Size", "96 bits"),
        ]

        for label, value in info_items:
            row = ctk.CTkFrame(enc_inner, fg_color="transparent")
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(
                row, text=label, font=(FONT_FAMILY, FONT_SIZE_SM),
                text_color=TEXT_TERTIARY, anchor="w", width=150
            ).pack(side="left")
            ctk.CTkLabel(
                row, text=value, font=(FONT_FAMILY, FONT_SIZE_SM),
                text_color=TEXT_PRIMARY, anchor="w"
            ).pack(side="left")

        # About section
        about_frame = ctk.CTkFrame(
            scroll, fg_color=BG_CARD, corner_radius=RADIUS_LG,
            border_width=1, border_color=BORDER_SUBTLE
        )
        about_frame.pack(fill="x", pady=(0, SPACING_XL))

        about_inner = ctk.CTkFrame(about_frame, fg_color="transparent")
        about_inner.pack(fill="x", padx=PAD_CARD, pady=PAD_CARD)

        ctk.CTkLabel(
            about_inner, text="About",
            font=FONT_SUBHEADING, text_color=TEXT_PRIMARY, anchor="w"
        ).pack(anchor="w", pady=(0, SPACING_MD))

        about_items = [
            ("Application", "AES File Encryption Utility"),
            ("Version", "1.2.0"),
            ("Developer", "Sahil Wade"),
            ("License", "MIT"),
            ("Python", f"3.11+"),
            ("Purpose", "Educational & secure file protection"),
        ]

        for label, value in about_items:
            row = ctk.CTkFrame(about_inner, fg_color="transparent")
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(
                row, text=label, font=(FONT_FAMILY, FONT_SIZE_SM),
                text_color=TEXT_TERTIARY, anchor="w", width=150
            ).pack(side="left")
            ctk.CTkLabel(
                row, text=value, font=(FONT_FAMILY, FONT_SIZE_SM),
                text_color=TEXT_PRIMARY, anchor="w"
            ).pack(side="left")

        # Disclaimer
        disclaimer_frame = ctk.CTkFrame(
            scroll, fg_color=STATUS_WARNING + "10", corner_radius=RADIUS_LG,
            border_width=1, border_color=STATUS_WARNING + "30"
        )
        disclaimer_frame.pack(fill="x")

        ctk.CTkLabel(
            disclaimer_frame,
            text="⚠️  This tool is intended for educational purposes and secure local "
                 "file protection only. Do not use for illegal activity.",
            font=(FONT_FAMILY, FONT_SIZE_SM),
            text_color=STATUS_WARNING,
            wraplength=600, justify="left"
        ).pack(padx=PAD_CARD, pady=PAD_CARD, anchor="w")
