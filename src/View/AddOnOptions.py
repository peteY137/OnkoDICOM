import platform

from PySide6 import QtCore, QtGui, QtWidgets
from src.Controller.PathHandler import resource_path
from src.Model.Configuration import Configuration, SqlError


class UIAddOnOptions(object):
    """
    Create all UI components for the Add-On options window.
    """

    def __init__(self):
        self.table_view = None
        self.table_organ = None
        self.table_volume = None
        self.table_ids = None
        self.add_new_window = None
        self.delete_window = None
        self.add_standard_organ_name = None
        self.import_organ_csv = None
        self.add_standard_volume_name = None
        self.note = None
        self.fill_options = None
        self.change_default_directory_frame = None
        self.table_roi = None
        self.add_new_roi = None
        self.delete_roi = None

    def setup_ui(self, add_on_options, roi_line, roi_opacity, iso_line,
                 iso_opacity, line_width):
        """
        Create the window and the components for each option view.
        """
        self.stylesheet_path = ""

        if platform.system() == 'Darwin':
            self.stylesheet_path = "res/stylesheet.qss"
        else:
            self.stylesheet_path = "res/stylesheet-win-linux.qss"
        stylesheet = open(resource_path(self.stylesheet_path)).read()
        add_on_options.setObjectName("Add_On_Options")
        add_on_options.setMinimumSize(766, 600)
        add_on_options.setStyleSheet(stylesheet)
        add_on_options.setWindowIcon(QtGui.QIcon(
            resource_path("res/images/btn-icons/onkodicom_icon.png")))

        _translate = QtCore.QCoreApplication.translate
        add_on_options.setWindowTitle(
            _translate("Add_On_Options", "Add-On Options"))

        self.widget = QtWidgets.QWidget(add_on_options)

        self.init_user_options_header()

        self.windowing_options = WindowingOptions(self)
        self.standard_organ_options = StandardOrganOptions(self)
        self.standard_volume_options = StandardVolumeOptions(self)
        self.patient_hash_options = PatientHashId(self)
        self.line_fill_options = LineFillOptions(
            self, roi_line, roi_opacity, iso_line, iso_opacity, line_width)
        self.iso2roi_options = RoiFromIsodoseOptions(self)
        self.change_default_directory = ChangeDefaultDirectory(self)

        self.create_cancel_button()
        self.create_apply_button()
        self.init_tree_list()
        self.set_layout()

        add_on_options.setCentralWidget(self.widget)
        QtCore.QMetaObject.connectSlotsByName(add_on_options)

    def set_layout(self):
        # Layout for the whole window
        self.layout = QtWidgets.QGridLayout(self.widget)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.addWidget(self.treeList, 0, 0)

        # Container including the table view and the option buttons
        # for each options
        self.option_widget = QtWidgets.QWidget(self.widget)
        self.option_layout = QtWidgets.QGridLayout(self.option_widget)
        self.option_layout.setContentsMargins(5, 5, 5, 5)
        self.option_layout.setHorizontalSpacing(10)
        fixed_spacer = QtWidgets.QSpacerItem(
            70, 70, hData=QtWidgets.QSizePolicy.Expanding,
            vData=QtWidgets.QSizePolicy.Fixed)
        self.option_layout.addItem(fixed_spacer, 0, 0, 1, 3)

        # Add Table Widgets
        self.option_layout.addWidget(self.table_modules, 1, 0, 1, 3)
        self.option_layout.addWidget(self.table_view, 1, 0, 1, 3)
        self.option_layout.addWidget(self.table_organ, 1, 0, 1, 3)
        self.option_layout.addWidget(self.table_volume, 1, 0, 1, 3)
        self.option_layout.addWidget(self.table_roi, 1, 0, 1, 3)
        self.option_layout.addWidget(self.table_ids, 1, 0, 1, 3)
        self.option_layout.addWidget(self.fill_options, 1, 0, 1, 3)
        self.option_layout.addWidget(
            self.change_default_directory_frame, 1, 0, 1, 3)

        # Add Button Widgets
        self.option_layout.addWidget(self.add_new_window, 2, 2)
        self.option_layout.addWidget(self.delete_window, 2, 1)
        self.option_layout.addWidget(self.delete_roi, 2, 0)
        self.option_layout.addWidget(self.add_new_roi, 2, 2)
        self.option_layout.addWidget(self.import_organ_csv, 2, 1)
        self.option_layout.addWidget(self.add_standard_organ_name, 2, 2)
        self.option_layout.addWidget(self.add_standard_volume_name, 2, 2)
        self.option_layout.addWidget(self.note, 2, 0, 1, 3)

        self.layout.addWidget(self.option_widget, 0, 1, 1, 3)
        hspacer = QtWidgets.QSpacerItem(QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Minimum)
        self.layout.addItem(hspacer, 1, 1)
        self.layout.addWidget(self.apply_button, 1, 2)
        self.layout.addWidget(self.cancel_button, 1, 3)

    def create_cancel_button(self):
        """
        Create CANCEL button for the whole window.
        """
        self.cancel_button = QtWidgets.QPushButton(self.widget)
        self.cancel_button.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        _translate = QtCore.QCoreApplication.translate
        self.cancel_button.setText(_translate("Add_On_Options", "Cancel"))

    def create_apply_button(self):
        """
        Create APPLY button to save all changes made.
        """
        self.apply_button = QtWidgets.QPushButton(self.widget)
        self.apply_button.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        _translate = QtCore.QCoreApplication.translate
        self.apply_button.setText(_translate("Add_On_Options", "Apply"))

    def init_user_options_header(self):
        """
        Create title that holds the chosen option from the tree and its
        description.
        """
        # label that holds the chosen option from the tree
        self.optionTitle = QtWidgets.QLabel(self.widget)
        self.optionTitle.setGeometry(QtCore.QRect(290, 50, 281, 31))
        _translate = QtCore.QCoreApplication.translate
        self.optionTitle.setText(_translate("Add_On_Options", "User Options"))

        # Description holder widget
        self.table_modules = QtWidgets.QLabel(self.widget)
        self.table_modules.setGeometry(QtCore.QRect(290, 90, 451, 70))
        self.table_modules.setText(
            " Here are listed all the user options used in Onko. By using \n "
            "Add-On Options you will be able to Add/Modify/Delete the \n"
            "settings for the displayed options on the left. ")

    def init_tree_list(self):
        """
        Create a tree view that holds the different options.
        """
        self.treeList = QtWidgets.QTreeView(self.widget)
        self.treeList.setHeaderHidden(True)

        # Triggering the view change according to the row selected in the tree
        self.treeList.clicked.connect(self.display)
        self.treeList.setMaximumWidth(250)

    def display(self, index):
        """
        Function triggered when an item from the tree view on the left
        column is clicked.
        Change the display of the right view of the window in regards
        to the option chosen from the tree.
        """
        item = self.treeList.selectedIndexes()[0]
        # Changes the title
        self.optionTitle.setText(item.model().itemFromIndex(index).text())
        # Changes the display
        self.change_display(item.model().itemFromIndex(index).text())

    def change_display(self, type):
        """
        Update the right view display of the window.
        """
        # Check which option is chosen and update the views.
        # Commented out lines are for the extra option (ROI by Isodose)

        if type == "Image Windowing":
            self.table_modules.setVisible(False)
            self.table_view.setVisible(True)
            self.table_organ.setVisible(False)
            self.table_volume.setVisible(False)
            self.table_roi.setVisible(False)
            self.table_ids.setVisible(False)
            self.add_new_window.setVisible(True)
            self.delete_window.setVisible(True)
            self.add_new_roi.setVisible(False)
            self.delete_roi.setVisible(False)
            self.add_standard_volume_name.setVisible(False)
            self.add_standard_organ_name.setVisible(False)
            self.import_organ_csv.setVisible(False)
            self.note.setVisible(False)
            self.fill_options.setVisible(False)
            self.change_default_directory_frame.setVisible(False)
        elif type == "Standard Organ Names":
            self.table_modules.setVisible(False)
            self.table_view.setVisible(False)
            self.table_organ.setVisible(True)
            self.table_volume.setVisible(False)
            self.table_roi.setVisible(False)
            self.table_ids.setVisible(False)
            self.add_new_window.setVisible(False)
            self.delete_window.setVisible(False)
            self.add_new_roi.setVisible(False)
            self.delete_roi.setVisible(False)
            self.add_standard_volume_name.setVisible(False)
            self.add_standard_organ_name.setVisible(True)
            self.import_organ_csv.setVisible(True)
            self.note.setVisible(False)
            self.fill_options.setVisible(False)
            self.change_default_directory_frame.setVisible(False)
        elif type == "Standard Volume Names":
            self.table_modules.setVisible(False)
            self.table_view.setVisible(False)
            self.table_organ.setVisible(False)
            self.table_volume.setVisible(True)
            self.table_roi.setVisible(False)
            self.table_ids.setVisible(False)
            self.add_new_window.setVisible(False)
            self.delete_window.setVisible(False)
            self.add_new_roi.setVisible(False)
            self.delete_roi.setVisible(False)
            self.add_standard_volume_name.setVisible(True)
            self.add_standard_organ_name.setVisible(False)
            self.import_organ_csv.setVisible(False)
            self.note.setVisible(False)
            self.fill_options.setVisible(False)
            self.change_default_directory_frame.setVisible(False)

        elif type == "Create ROIs from Isodoses":
            self.table_modules.setVisible(False)
            self.table_view.setVisible(False)
            self.table_organ.setVisible(False)
            self.table_volume.setVisible(False)
            self.table_roi.setVisible(True)
            self.table_ids.setVisible(False)
            self.add_new_window.setVisible(False)
            self.delete_window.setVisible(False)
            self.add_new_roi.setVisible(True)
            self.delete_roi.setVisible(True)
            self.add_standard_volume_name.setVisible(False)
            self.add_standard_organ_name.setVisible(False)
            self.import_organ_csv.setVisible(False)
            self.note.setVisible(False)
            self.fill_options.setVisible(False)
            self.change_default_directory_frame.setVisible(False)

        elif type == "Patient ID - Hash ID":
            self.table_modules.setVisible(False)
            self.table_view.setVisible(False)
            self.table_organ.setVisible(False)
            self.table_volume.setVisible(False)
            self.table_roi.setVisible(False)
            self.table_ids.setVisible(True)
            self.add_new_window.setVisible(False)
            self.delete_window.setVisible(False)
            self.add_new_roi.setVisible(False)
            self.delete_roi.setVisible(False)
            self.add_standard_volume_name.setVisible(False)
            self.add_standard_organ_name.setVisible(False)
            self.import_organ_csv.setVisible(False)
            self.note.setVisible(True)
            self.fill_options.setVisible(False)
            self.change_default_directory_frame.setVisible(False)
        elif type == "User Options" or type == "Configuration":
            self.add_new_window.setVisible(False)
            self.delete_window.setVisible(False)
            self.add_new_roi.setVisible(False)
            self.delete_roi.setVisible(False)
            self.add_standard_volume_name.setVisible(False)
            self.add_standard_organ_name.setVisible(False)
            self.import_organ_csv.setVisible(False)
            self.table_modules.setVisible(True)
            self.table_view.setVisible(False)
            self.table_organ.setVisible(False)
            self.table_volume.setVisible(False)
            self.table_roi.setVisible(False)
            self.table_ids.setVisible(False)
            self.note.setVisible(False)
            self.fill_options.setVisible(False)
            self.change_default_directory_frame.setVisible(False)
        elif type == "Line & Fill configuration":
            self.add_new_window.setVisible(False)
            self.delete_window.setVisible(False)
            self.add_new_roi.setVisible(False)
            self.delete_roi.setVisible(False)
            self.add_standard_volume_name.setVisible(False)
            self.add_standard_organ_name.setVisible(False)
            self.import_organ_csv.setVisible(False)
            self.table_modules.setVisible(False)
            self.table_view.setVisible(False)
            self.table_organ.setVisible(False)
            self.table_volume.setVisible(False)
            self.table_roi.setVisible(False)
            self.table_ids.setVisible(False)
            self.note.setVisible(False)
            self.fill_options.setVisible(True)
            self.change_default_directory_frame.setVisible(False)
        elif type == "Default directory":
            self.add_new_window.setVisible(False)
            self.delete_window.setVisible(False)
            self.add_new_roi.setVisible(False)
            self.delete_roi.setVisible(False)
            self.add_standard_volume_name.setVisible(False)
            self.add_standard_organ_name.setVisible(False)
            self.import_organ_csv.setVisible(False)
            self.table_modules.setVisible(False)
            self.table_view.setVisible(False)
            self.table_organ.setVisible(False)
            self.table_volume.setVisible(False)
            self.table_roi.setVisible(False)
            self.table_ids.setVisible(False)
            self.note.setVisible(False)
            self.fill_options.setVisible(False)
            self.change_default_directory_frame.setVisible(True)


class WindowingOptions(object):
    """
    Manage the UI of Windowing option.
    """

    def __init__(self, window_options):
        """
        Create the components for the UI of Windowing view.
        """
        self.window = window_options
        self.create_buttons()
        self.create_table_view()

    def create_buttons(self):
        """
        Create a button to add a new window view and delete a window view
        """
        self.window.add_new_window = QtWidgets.QPushButton(self.window.widget)
        self.window.delete_window = QtWidgets.QPushButton(self.window.widget)

        self.window.add_new_window.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.window.add_new_window.setVisible(False)
        self.window.delete_window.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.window.delete_window.setVisible(False)

        _translate = QtCore.QCoreApplication.translate
        self.window.add_new_window.setText(
            _translate("Add_On_Options", "Add New Window"))
        self.window.delete_window.setText(
            _translate("Add_On_Options", "Delete Window"))

    def create_table_view(self):
        """
        Create a table to hold all the windowing options.
        """
        self.window.table_view = QtWidgets.QTableWidget(self.window.widget)
        self.window.table_view.setStyleSheet(
            "background-color: rgb(255, 255, 255);")
        self.window.table_view.setColumnCount(4)
        self.window.table_view.setHorizontalHeaderLabels(
            [" Window Name ", " Scan ", " Window ", " Level "])
        self.window.table_view.horizontalHeaderItem(0).setTextAlignment(
            QtCore.Qt.AlignLeft)
        self.window.table_view.horizontalHeaderItem(1).setTextAlignment(
            QtCore.Qt.AlignLeft)
        self.window.table_view.horizontalHeaderItem(2).setTextAlignment(
            QtCore.Qt.AlignLeft)
        self.window.table_view.horizontalHeaderItem(3).setTextAlignment(
            QtCore.Qt.AlignLeft)
        self.window.table_view.verticalHeader().hide()
        image_windowing_header = self.window.table_view.horizontalHeader()
        image_windowing_header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        image_windowing_header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        image_windowing_header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.Stretch)
        image_windowing_header.setSectionResizeMode(
            3, QtWidgets.QHeaderView.Stretch)
        self.window.table_view.setVisible(False)

        # removing the ability to edit tables with immediate click
        self.window.table_view.setEditTriggers(
            QtWidgets.QTreeView.NoEditTriggers
            | QtWidgets.QTreeView.NoEditTriggers)


class StandardOrganOptions(object):
    """
    Manage the UI of Standard Organ option.
    """

    def __init__(self, window_options):
        """
        Create the components for the UI of Standard Organ view.
        """
        self.window = window_options
        self.create_add_button()
        self.create_import_csv_button()
        self.create_table_view()

    def create_add_button(self):
        """
        Create a button to add a new standard organ name.
        """
        self.window.add_standard_organ_name = QtWidgets.QPushButton(
            self.window.widget)
        self.window.add_standard_organ_name.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.window.add_standard_organ_name.setVisible(False)
        _translate = QtCore.QCoreApplication.translate
        self.window.add_standard_organ_name.setText(
            _translate("Add_On_Options", "Add Standard Name"))

    def create_import_csv_button(self):
        """
        Create a button to import a csv of standard organs.
        """
        self.window.import_organ_csv = QtWidgets.QPushButton(
            self.window.widget)
        self.window.import_organ_csv.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.window.import_organ_csv.setVisible(False)
        _translate = QtCore.QCoreApplication.translate
        self.window.import_organ_csv.setText(
            _translate("Add_On_Options", "Import Spreadsheet"))

    def create_table_view(self):
        """
        Create a table to hold all the standard organ entries.
        """
        self.window.table_organ = QtWidgets.QTableWidget(self.window.widget)
        self.window.table_organ.setStyleSheet(
            "background-color: rgb(255, 255, 255);")
        self.window.table_organ.setColumnCount(4)
        self.window.table_organ.setHorizontalHeaderLabels(
            [" Standard Name ", " FMA ID ", " Organ ", " Url "])
        self.window.table_organ.horizontalHeaderItem(0).setTextAlignment(
            QtCore.Qt.AlignLeft)
        self.window.table_organ.horizontalHeaderItem(1).setTextAlignment(
            QtCore.Qt.AlignLeft)
        self.window.table_organ.horizontalHeaderItem(2).setTextAlignment(
            QtCore.Qt.AlignLeft)
        self.window.table_organ.horizontalHeaderItem(3).setTextAlignment(
            QtCore.Qt.AlignLeft)

        standard_organ_names_header = \
            self.window.table_organ.horizontalHeader()
        standard_organ_names_header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        standard_organ_names_header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        standard_organ_names_header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.Stretch)
        standard_organ_names_header.setSectionResizeMode(
            3, QtWidgets.QHeaderView.Stretch)
        self.window.table_organ.setVisible(False)
        self.window.table_organ.verticalHeader().hide()

        # Removing the ability to edit tables with immediate click
        self.window.table_organ.setEditTriggers(
            QtWidgets.QTreeView.NoEditTriggers
            | QtWidgets.QTreeView.NoEditTriggers)


class StandardVolumeOptions(object):
    """
    Manage the UI of Standard Volume option.
    """

    def __init__(self, window_options):
        """
        Create the components for the UI of Standard Volume view.
        """
        self.window = window_options
        self.create_add_button()
        self.create_table_view()

    def create_add_button(self):
        """
        Create a button to add a new standard volume name.
        """
        self.window.add_standard_volume_name = QtWidgets.QPushButton(
            self.window.widget)
        self.window.add_standard_volume_name.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.window.add_standard_volume_name.setVisible(False)
        _translate = QtCore.QCoreApplication.translate
        self.window.add_standard_volume_name.setText(
            _translate("Add_On_Options", "Add Standard Name"))

    def create_table_view(self):
        """
        Create a table to hold the volume entries.
        """
        self.window.table_volume = QtWidgets.QTableWidget(self.window.widget)
        self.window.table_volume.setStyleSheet(
            "background-color: rgb(255, 255, 255);")
        self.window.table_volume.setColumnCount(2)
        self.window.table_volume.setHorizontalHeaderLabels(
            [" Standard Name ", " Volume Name"])
        self.window.table_volume.horizontalHeaderItem(0).setTextAlignment(
            QtCore.Qt.AlignLeft)
        self.window.table_volume.horizontalHeaderItem(1).setTextAlignment(
            QtCore.Qt.AlignLeft)
        standard_volume_names_header = \
            self.window.table_volume.horizontalHeader()
        self.window.table_volume.verticalHeader().hide()
        standard_volume_names_header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        standard_volume_names_header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)
        self.window.table_volume.setVisible(False)

        # Removing the ability to edit tables with immediate click
        self.window.table_volume.setEditTriggers(
            QtWidgets.QTreeView.NoEditTriggers
            | QtWidgets.QTreeView.NoEditTriggers)


class RoiFromIsodoseOptions(object):
    """
    Manage the UI of ROI from isodose option.
    """

    def __init__(self, window_options):
        """
        Create the components for the UI of ROI from Isodose view.
        """
        self.window = window_options
        self.create_buttons()
        self.create_table_view()

    def create_buttons(self):
        """
        Create buttons to create and delete ROIs from isodose.
        """
        # Buttons
        self.window.add_new_roi = QtWidgets.QPushButton(self.window.widget)
        self.window.delete_roi = QtWidgets.QPushButton(self.window.widget)

        # Set cursor
        self.window.add_new_roi.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.window.delete_roi.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # Set visibility
        self.window.add_new_roi.setVisible(False)
        self.window.delete_roi.setVisible(False)

        # Set style
        self.window.add_new_roi.setProperty("QPushButtonClass",
                                            "success-button")
        self.window.delete_roi.setProperty("QPushButtonClass", "fail-button")

        # Set text
        _translate = QtCore.QCoreApplication.translate
        self.window.add_new_roi.setText(_translate("Add_On_Options",
                                                   "Add new Isodose"))
        self.window.delete_roi.setText(_translate("Add_On_Options",
                                                  "Remove Isodose"))

    def create_table_view(self):
        """
        Create a table to hold all the ROI creation by isodose entries.
        """
        self.window.table_roi = QtWidgets.QTableWidget(self.window.widget)
        self.window.table_roi.setStyleSheet(
            "background-color: rgb(255, 255, 255);")
        self.window.table_roi.setColumnCount(4)
        self.window.table_roi.verticalHeader().hide()
        self.window.table_roi.setHorizontalHeaderLabels(
            [" Isodose Level ", " Unit ", " ROI Name ", " Notes "])

        self.window.table_roi.horizontalHeaderItem(0).setTextAlignment(
            QtCore.Qt.AlignLeft)
        self.window.table_roi.horizontalHeaderItem(1).setTextAlignment(
            QtCore.Qt.AlignLeft)
        self.window.table_roi.horizontalHeaderItem(2).setTextAlignment(
            QtCore.Qt.AlignLeft)
        self.window.table_roi.horizontalHeaderItem(3).setTextAlignment(
            QtCore.Qt.AlignLeft)

        roi_from_isodose_header = self.window.table_roi.horizontalHeader()
        roi_from_isodose_header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        roi_from_isodose_header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)
        roi_from_isodose_header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.Stretch)
        roi_from_isodose_header.setSectionResizeMode(
            3, QtWidgets.QHeaderView.Stretch)

        self.window.table_roi.setVisible(False)

        # Removing the ability to edit tables with immediate click
        self.window.table_roi.setEditTriggers(
            QtWidgets.QTreeView.NoEditTriggers |
            QtWidgets.QTreeView.NoEditTriggers)


class PatientHashId(object):
    """
    Manage the UI of Patient ID - Hash ID option.
    """

    def __init__(self, window_options):
        """
        Create the components for the UI of Patient ID - Hash ID view.
        """
        self.window = window_options
        self.create_table_view()
        self.create_note()

    def create_table_view(self):
        """
        Create a table to hold all the patients and their hash that the
        software has anonymised.
        """
        self.window.table_ids = QtWidgets.QTableWidget(self.window.widget)
        self.window.table_ids.setStyleSheet(
            "background-color: rgb(255, 255, 255);")
        self.window.table_ids.setColumnCount(2)
        self.window.table_ids.setHorizontalHeaderLabels(
            [" Patient ID ", " Hash ID "])
        self.window.table_ids.horizontalHeaderItem(0).setTextAlignment(
            QtCore.Qt.AlignLeft)
        self.window.table_ids.horizontalHeaderItem(1).setTextAlignment(
            QtCore.Qt.AlignLeft)
        patient_hash_id_header = self.window.table_ids.horizontalHeader()
        self.window.table_ids.verticalHeader().hide()
        patient_hash_id_header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        patient_hash_id_header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)
        self.window.table_ids.setVisible(False)
        # removing the ability to edit tables with immediate click
        self.window.table_ids.setEditTriggers(
            QtWidgets.QTreeView.NoEditTriggers
            | QtWidgets.QTreeView.NoEditTriggers)

    def create_note(self):
        """
        Create a note for the user about data privacy.
        """
        self.window.note = QtWidgets.QLabel(self.window.widget)
        self.window.note.setVisible(False)
        _translate = QtCore.QCoreApplication.translate
        self.window.note.setText(
            _translate(
                "Add_On_Options",
                "Note: This is a list of all the patients anonymized "
                "using Onko.\nIt is your responsability to ensure "
                "their privacy."))


class LineFillOptions(object):
    """
    Manage the UI of Line and Fill Configuration options for ROIs and
    Isodoses display.
    """

    def __init__(self, window_options, roi_line, roi_opacity, iso_line,
                 iso_opacity, line_width):
        """
        Create the components for the UI of Line and Fill options and
        set the layout.
        """
        self.window = window_options
        self.roi_line = roi_line
        self.roi_opacity = roi_opacity
        self.iso_line = iso_line
        self.iso_opacity = iso_opacity
        self.line_width = line_width

        window_options.fill_layout = QtWidgets.QFormLayout(
            window_options.widget)
        window_options.fill_options = QtWidgets.QWidget(window_options.widget)
        self.create_combobox_line_style_roi()
        self.create_slider_opacity_roi()
        self.create_combobox_line_style_isodoses()
        self.create_slider_opacity_isodose()
        self.create_combobox_line_width()
        self.set_layout()

    def set_layout(self):
        """
        Add the components into a layout and initialize the values
        according to the last configuration settings.
        """
        # Adding the components into a layout
        self.window.fill_layout.addRow(QtWidgets.QLabel("ROI Line Style: "),
                                       self.window.line_style_ROI)
        self.window.fill_layout.addRow(QtWidgets.QLabel(""))
        self.window.fill_layout.addRow(self.window.opacityLabel_ROI,
                                       self.window.opacity_ROI)
        self.window.fill_layout.addRow(QtWidgets.QLabel(""))
        self.window.fill_layout.addRow(QtWidgets.QLabel("ISO Line Style: "),
                                       self.window.line_style_ISO)
        self.window.fill_layout.addRow(QtWidgets.QLabel(""))
        self.window.fill_layout.addRow(self.window.opacityLabel_ISO,
                                       self.window.opacity_ISO)
        self.window.fill_layout.addRow(QtWidgets.QLabel(""))
        self.window.fill_layout.addRow(QtWidgets.QLabel("Line Width: "),
                                       self.window.line_width)

        # Inserting the last configuration settings on initialisation
        self.window.line_style_ROI.setCurrentIndex(self.roi_line)
        self.window.line_style_ISO.setCurrentIndex(self.iso_line)
        self.window.line_width.setCurrentText(str(self.line_width))

        self.window.fill_options.setLayout(self.window.fill_layout)
        # self.window.fill_options.setGeometry(QtCore.QRect(290, 90, 451, 370))
        self.window.fill_options.setVisible(False)

    def create_combobox_line_style_roi(self):
        """
        Create combobox with the available lines for ROIs.
        """
        self.window.line_style_ROI = QtWidgets.QComboBox(
            self.window.fill_options)
        self.window.line_style_ROI.addItem("No Pen")
        self.window.line_style_ROI.addItem("Solid Line")
        self.window.line_style_ROI.addItem("Dash Line")
        self.window.line_style_ROI.addItem("Dot Line")
        self.window.line_style_ROI.addItem("Dash-Dot Line")
        self.window.line_style_ROI.addItem("Dash-Dot-Dot Line")
        self.window.line_style_ROI.setSizeAdjustPolicy(
            QtWidgets.QComboBox.AdjustToContents)

    def create_slider_opacity_roi(self):
        """
        Create slider to determine the opacity of the fill for ROIs
        """
        self.window.opacity_ROI = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.window.opacity_ROI.setMinimum(0)
        self.window.opacity_ROI.setMaximum(100)
        self.window.opacity_ROI.setTickPosition(QtWidgets.QSlider.TicksLeft)
        self.window.opacity_ROI.setTickInterval(10)
        self.window.opacity_ROI.setValue(self.roi_opacity)
        self.window.opacity_ROI.valueChanged.connect(self.update_roi_opacity)
        self.window.opacityLabel_ROI = QtWidgets.QLabel(
            "ROI Fill Opacity: \t {}%".format(
                int(self.window.opacity_ROI.value())))

    def create_combobox_line_style_isodoses(self):
        """
        Create combobox with the available lines for isodoses
        """
        self.window.line_style_ISO = QtWidgets.QComboBox(
            self.window.fill_options)
        self.window.line_style_ISO.addItem("No Pen")
        self.window.line_style_ISO.addItem("Solid Line")
        self.window.line_style_ISO.addItem("Dash Line")
        self.window.line_style_ISO.addItem("Dot Line")
        self.window.line_style_ISO.addItem("Dash-Dot Line")
        self.window.line_style_ISO.addItem("Dash-Dot-Dot Line")
        self.window.line_style_ISO.setSizeAdjustPolicy(
            QtWidgets.QComboBox.AdjustToContents)

    def create_slider_opacity_isodose(self):
        """
        Create slider to determine opacity of the fill for isodoses
        """
        self.window.opacity_ISO = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.window.opacity_ISO.setMinimum(0)
        self.window.opacity_ISO.setMaximum(100)
        self.window.opacity_ISO.setTickPosition(QtWidgets.QSlider.TicksLeft)
        self.window.opacity_ISO.setTickInterval(10)
        self.window.opacity_ISO.setValue(self.iso_opacity)
        self.window.opacity_ISO.valueChanged.connect(self.update_iso_opacity)
        self.window.opacityLabel_ISO = QtWidgets.QLabel(
            "ISO Fill Opacity: \t {}%".format(
                int(self.window.opacity_ISO.value())))

    def create_combobox_line_width(self):
        """
        Create combobox to hold the line width options
        """
        self.window.line_width = QtWidgets.QComboBox(self.window.fill_options)
        self.window.line_width.addItem("0.5")
        self.window.line_width.addItem("1")
        self.window.line_width.addItem("1.5")
        self.window.line_width.addItem("2")
        self.window.line_width.addItem("2.5")
        self.window.line_width.setSizeAdjustPolicy(
            QtWidgets.QComboBox.AdjustToContents)

    def update_roi_opacity(self):
        """
        Update the percentage on slider change for ROIs.
        """
        self.window.opacityLabel_ROI.setText("ROI Fill Opacity: \t {}%".format(
            int(self.window.opacity_ROI.value())))

    def update_iso_opacity(self):
        """
        Update the percentage on slider change for isodoses.
        """
        self.window.opacityLabel_ISO.setText("ISO Fill Opacity: \t {}%".format(
            int(self.window.opacity_ISO.value())))


class ChangeDefaultDirectory(object):
    """
    Manage the UI of Change Default Directory option.
    """

    def __init__(self, window_options):
        """
        Create the components for the UI of Change Default Directory view.
        """
        self.window = window_options
        self.create_change_default_directory_frame()

    def create_change_default_directory_frame(self):
        config = Configuration()
        default_directory = None
        try:
            default_directory = config.get_default_directory()
        except SqlError:
            config.set_up_config_db()
            QtWidgets.QMessageBox.critical(
                self.window, "Config file error",
                """Failed to access configuration file.
                \nConfiguration file recreated with no default directory.
                \nPlease update your default directory.""")

        self.window.change_default_directory_frame = QtWidgets.QFrame()
        self.window.change_default_directory_frame.setVisible(False)
        self.change_default_directory_vertical_layout = QtWidgets.QVBoxLayout()
        self.change_default_directory_prompt = QtWidgets.QLabel()
        self.change_default_directory_prompt.setAlignment(QtCore.Qt.AlignLeft)
        self.change_default_directory_prompt.setVisible(True)
        self.change_default_directory_prompt.setText(
            "Default directory's path:")
        self.change_default_directory_vertical_layout.addWidget(
            self.change_default_directory_prompt)
        # Create a horizontal box to hold the input box for the
        # directory and the choose button
        self.change_default_directory_input_horizontal_box = \
            QtWidgets.QHBoxLayout()

        # Create a textbox to contain the path to the directory that
        # contains the DICOM files
        self.change_default_directory_input_box = \
            UIChangeDefaultDirDragAndDropEvent(self)
        self.change_default_directory_input_box.setCursorPosition(0)
        self.change_default_directory_input_box.setText(default_directory)
        self.change_default_directory_input_horizontal_box.addWidget(
            self.change_default_directory_input_box)

        # Create a choose button to open the file dialog
        self.change_default_directory_button = QtWidgets.QPushButton()
        self.change_default_directory_button.setText("Change")
        self.change_default_directory_button.resize(
            self.change_default_directory_button.sizeHint().width(),
            self.change_default_directory_input_box.height())
        self.change_default_directory_button.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.change_default_directory_input_horizontal_box.addWidget(
            self.change_default_directory_button)
        self.change_default_directory_button.clicked.connect(
            self.change_button_clicked)

        # Create a widget to hold the input fields
        self.change_default_directory_input_widget = QtWidgets.QWidget()
        self.change_default_directory_input_horizontal_box.setStretch(0, 4)
        self.change_default_directory_input_widget.setLayout(
            self.change_default_directory_input_horizontal_box)
        self.change_default_directory_vertical_layout.addWidget(
            self.change_default_directory_input_widget, 1,
            QtCore.Qt.AlignTop)

        self.window.change_default_directory_frame.setLayout(
            self.change_default_directory_vertical_layout)

    def change_button_clicked(self):
        """
            Executes when the choose button is clicked.
            Gets filepath from the user and loads all files and subdirectories.
        """
        # Get folder path from pop up dialog box

        self.default_directory = QtWidgets.QFileDialog.getExistingDirectory(
            None, 'Select patient folder...', '')
        if len(self.default_directory) > 0:
            self.change_default_directory_input_box.setText(
                self.default_directory)


class UIChangeDefaultDirDragAndDropEvent(QtWidgets.QLineEdit):
    parent_window = None

    def __init__(self, UIOpenPatientWindowInstance):
        super(UIChangeDefaultDirDragAndDropEvent, self).__init__()
        self.parent_window = UIOpenPatientWindowInstance
        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            # Removes the doubled intro slash
            directory_path = str(urls[0].path())[1:]
            # add / for not Windows machines
            if platform.system() != 'Windows':
                directory_path = "/" + directory_path
            # Pastes the directory into the text field
            self.setText(directory_path)
