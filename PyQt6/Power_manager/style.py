VIEW_STYLE = ""

STYLE = """
                
QWidget#screen_widget {
    background-color: rgba(30, 32, 36, 220);
    border: 1px solid rgba(255, 255, 255, 15);
    border-radius: 12px;
}

QWidget#scan_panel {
    background-color: rgba(20, 22, 26, 180);
    border: 2px solid rgba(55, 58, 65, 255);
    border-radius: 4px;
    padding: 12px;
}
/* <--------Buttons----------> */
        
QPushButton {
    font-family: "Segoe UI", "Comic Sans MS";
    background-color: rgba(255, 255, 255, 10);
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 30);
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: rgba(255, 255, 255, 20);
    border-color: rgba(255, 255, 255, 100);
}

QPushButton:pressed {
    background-color: rgba(255, 255, 255, 5);
    transform: translateY(1px);
}

QPushButton#browse_btn {
    background-color: #3b82f6; /* Accent color to stand out */
    border: none;
}

QPushButton#browse_btn:hover {
    background-color: #2563eb;
}

/* Disabled State - General Buttons */
QPushButton:disabled {
    background-color: rgba(255, 255, 255, 5); /* Fainter surface */
    color: rgba(255, 255, 255, 40);           /* Ghosted text */
    border: 1px solid rgba(255, 255, 255, 15); /* Faded border */
}
/* <---------------- BUTTONS MODES -------------->*/

QToolButton {
    background-color: rgba(255, 255, 255, 10);
    color: #a0aec0;
    border: 1px solid rgba(255, 255, 255, 20);
    padding: 10px 22px;
    font-weight: bold;

    min-width: 120px;

    transition: all 150ms ease;
}

QToolButton:hover {
    background-color: rgba(120, 35, 40, 220);
    border-color: rgba(255, 120, 120, 220);

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,80),
        0 0 14px rgba(255, 80, 80, 180);
}

QToolButton:pressed {
    background-color: rgba(170, 40, 45, 240);
    border-bottom: 2px solid rgba(120, 20, 25, 255);

    box-shadow:
        inset 0 4px 8px rgba(0,0,0,200),
        0 0 10px rgba(255, 60, 60, 200);
}

/* CHECKED – red = active mode */
QToolButton:checked {
    background-color: rgba(180, 55, 55, 235);
    color: #ffffff;

    border-color: rgba(255, 200, 200, 220);
    font-weight: 600;
}

QToolButton:disabled {
    background-color: rgba(28, 30, 36, 120);
    color: rgba(200,200,200,90);
    border: 1px solid rgba(255,255,255,25);
}

QToolButton:first-child {
    border-top-left-radius: 14px;
    border-bottom-left-radius: 14px;
}

QToolButton:last-child {
    border-top-right-radius: 14px;
    border-bottom-right-radius: 14px;
}


/* <---------------- PATH INPUT -------------->*/

QLineEdit#path_input {

    font-family: Comic Sans MS;
    background-color: rgba(24, 26, 30, 230);
    color: #e6e8ec;
    
    border: 1.5px solid rgba(255, 255, 255, 55);
    border-radius: 8px;
    padding: 6px 10px;
}

/* hover → clean edge, no glow yet */
QLineEdit#path_input:hover {
    border-color: rgba(255, 255, 255, 110);
}

/* focus → white glow (soft, professional) */
QLineEdit#path_input:focus {
    background-color: rgba(28, 30, 34, 240);

    border: 2px solid rgba(255, 255, 255, 200);

    /* fake glow via inset + outer highlight */
    box-shadow:
        inset 0 0 0 1px rgba(255, 255, 255, 60),
        0 0 6px rgba(255, 255, 255, 80);
}

/* placeholder text */
QLineEdit#path_input::placeholder {
    color: rgba(200, 200, 200, 120);
    font-style: italic;
}

/* Read-Only - Differentiates from active inputs */
QLineEdit#path_input:read-only {
    background-color: rgba(15, 17, 20, 150);
    color: rgba(200, 200, 200, 150);
    border-style: dashed;
}

/* disabled → visually clear */
QLineEdit#path_input:disabled {
    background-color: rgba(20, 22, 26, 160);
    color: rgba(180, 180, 180, 120);
    border-color: rgba(255, 255, 255, 25);
}

/* <---------------- LINE EDITS -------------->*/
QLineEdit {
    font-family: "Segoe UI";
    /* Deep dark base to make text pop against the glass */
    background-color: rgba(10, 12, 16, 230);
    color: #f1f3f5;
    
    /* Thin, sharp "glass edge" */
    border: 1.5px solid rgba(255, 255, 255, 45);
    border-radius: 8px;
    padding: 7px 12px;
    
    /* High-contrast selection */
    selection-background-color: rgba(255, 255, 255, 60);
    selection-color: #ffffff;
}

/* Hover - Subtle brightening of the edge */
QLineEdit:hover {
    background-color: rgba(15, 18, 24, 250);
    border-color: rgba(255, 255, 255, 90);
}

/* Focus - The "Clickable" Highlight */
QLineEdit:focus {
    background-color: rgba(5, 5, 8, 255);
    /* Pure white sharp edge */
    border: 1.5px solid rgba(255, 255, 255, 200);
    
    /* Moody Shadow Effect: 
       Inner shadow makes it look deep, 
       Outer glow makes it stand out */
    box-shadow: 
        inset 0 2px 4px rgba(0, 0, 0, 150),
        0 0 8px rgba(255, 255, 255, 40);
}

/* Placeholder - Moody ghost text */
QLineEdit::placeholder {
    color: rgba(200, 200, 200, 80);
    font-style: italic;
}

/* Disabled - Clearly dead but still glass-themed */
QLineEdit:disabled {
    background-color: rgba(20, 22, 26, 120);
    color: rgba(255, 255, 255, 30);
    border-color: rgba(255, 255, 255, 15);
}

/* Read-Only - Differentiates from active inputs */
QLineEdit:read-only {
    background-color: rgba(15, 17, 20, 150);
    color: rgba(200, 200, 200, 150);
    border-style: dashed;
}

/* <---------------- LABELS -------------->*/

QLabel {
    font-family: Comic Sans MS;
    color: #cfd2da;
    padding: 1px 6px;
}

QLabel:hover {
    color: #ffffff;
    background-color: #2a2c31;
    border-radius: 4px;
    border: 1px solid #cfd2da;
}

QLabel#label{
    color: #ffffff;
    background-color: #2a2c31;
    border-radius: 4px;
    border: 0.8px solid #cfd2da;
}
QLabel {
    font-family: "Comic Sans MS", "Segoe UI";
    color: rgba(224, 230, 240, 200); /* Moody off-white */
    background: transparent;
    padding: 2px 5px;
    font-weight: 600;
}

QLabel#label {
    color: #ffffff;
    font-weight: 600;
    
    /* Layered Glass Effect */
    background-color: rgba(42, 44, 49, 230);
    border: 1px solid rgba(207, 210, 218, 120);
    border-radius: 5px;
    
    /* Subtle Depth Shadow */
    padding: 4px 10px;
}

QLabel#label:hover {
    background-color: rgba(55, 58, 65, 255);
    border-color: #ffffff;
    
    /* Moody white glow shadow */
    box-shadow: 0 0 10px rgba(255, 255, 255, 30);
}


/* <---------------- TABLE VIEW ----------------> */
QTableView {
    background-color: rgba(15, 17, 20, 150);
    border: 2px solid rgba(255, 255, 255, 20);
    border-radius: 3px;
    gridline-color: rgba(255, 255, 255, 10);
    color: #e2e8f0;
    /* This ensures the selection background covers the whole row nicely */
    selection-background-color: rgba(70, 75, 85, 180); 
    selection-color: #ffffff;
    outline: none;
}

QTableView::item:hover {
    background-color: rgba(255, 255, 255, 10);
}

/* Moody grayish selection */
QTableView::item:selected {
    background-color: rgba(80, 85, 95, 200); /* Deep moody slate gray */
    color: #ffffff;
    border-top: 2px solid rgba(255, 255, 255, 20); /* Subtle definition */
    border-bottom: 2px solid rgba(255, 255, 255, 20);
}

/* Focused selection (slightly brighter moody gray) */
QTableView::item:selected:active {
    background-color: rgba(105, 110, 115, 220);
}

QHeaderView::section {
    /* Adjusted to a darker, more matte gray */
    background-color: rgba(35, 38, 45, 230); 
    color: #cbd5e0;
    padding: 8px;
    font-weight: 600;
    border: none;
    border-bottom: 2px solid rgba(255, 255, 255, 15);
}

/* Hover effect for the headers themselves */
QHeaderView::section:hover {
    background-color: rgba(50, 55, 65, 240);
    color: #ffffff;

}
/* ================== SPIN BOX ================== */

QSpinBox {
    /* Base appearance */
    background-color: rgba(28, 30, 34, 230);
    color: #e6e8ec;

    border: 1px solid rgba(255, 255, 255, 55);
    border-radius: 5px;

    /* Space for text so it doesn't touch borders */
    padding: 3px 3x 3px 3px;

    font-family: Comic Sans MS;
    selection-background-color: rgba(120, 170, 255, 180);
    selection-color: #ffffff;
}

/* Hover → clearer edge */
QSpinBox:hover {
    border-color: rgba(255, 255, 255, 110);
}

/* Focus → subtle glow */
QSpinBox:focus {
    border: 2px solid rgba(120, 170, 255, 220);
    background-color: rgba(32, 34, 40, 240);
}

/* ================== BUTTON CONTAINER ================== */

/* Common styling for both buttons */
QSpinBox::up-button,
QSpinBox::down-button {
    subcontrol-origin: border;
    width: 20px;

    background-color: rgba(255, 255, 255, 10);
    border-left: 1px solid rgba(255, 255, 255, 40);
}

/* Up button positioning */
QSpinBox::up-button {
    subcontrol-position: top right;
    border-top-right-radius: 8px;
}

/* Down button positioning */
QSpinBox::down-button {
    subcontrol-position: bottom right;
    border-bottom-right-radius: 8px;
}

/* Hover feedback on buttons */
QSpinBox::up-button:hover,
QSpinBox::down-button:hover {
    background-color: rgba(120, 170, 255, 60);
}

/* Pressed → darker, tactile */
QSpinBox::up-button:pressed,
QSpinBox::down-button:pressed {
    background-color: rgba(120, 170, 255, 120);
}
/*<--------------------RADIO BUTTON---------------->*/

 /*<-------------GROUP BOX----------------->
QGroupBox {
    border: 1px solid rgba(255, 255, 255, 25);
    border-radius: 12px;
    margin-top: 25px;
    background-color: rgba(255, 255, 255, 5); /* Barely there frost */
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 20px;
    padding: 0 10px;
    color: rgba(255, 255, 255, 220); /* Stale white */
    font-weight: 600;
}
"""